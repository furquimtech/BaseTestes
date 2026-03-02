"""
base_testes_replicar_dados_parquet.py
-------------------------------------
Exporta tabelas de PROD para arquivos parquet/<DEV_DB>/<tabela>.parquet,
deduplica por PK e tambem suporta importar esses parquets para o banco DEV.
"""

import argparse
import datetime as dt
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extras import RealDictCursor, execute_values
from tqdm import tqdm


# =============================================================
# CARREGA CREDENCIAIS DO .env / .env.scripts
# =============================================================
def _encontrar_env() -> Path:
    candidatos = [
        Path(__file__).parent / ".env",
        Path(__file__).parent.parent / ".env",
        Path(__file__).parent / ".env.scripts",
        Path(__file__).parent.parent / ".env.scripts",
    ]
    for p in candidatos:
        if p.exists():
            return p
    raise FileNotFoundError(
        "Arquivo .env nao encontrado. Crie-o a partir do .env.example:\n"
        "  cp .env.example .env"
    )


load_dotenv(_encontrar_env())

# =============================================================
# CONEXOES
# =============================================================
PROD = dict(
    host=os.environ["PROD_HOST"],
    port=int(os.environ.get("PROD_PORT", 5432)),
    dbname=os.environ["PROD_DB"],
    user=os.environ["PROD_USER"],
    password=os.environ["PROD_PASS"],
)

DEV = dict(
    host=os.environ.get("DEV_HOST", "localhost"),
    port=int(os.environ.get("DEV_PORT", 5432)),
    dbname=os.environ["DEV_DB"],
    user=os.environ["DEV_USER"],
    password=os.environ["DEV_PASS"],
)

SCHEMA = "public"
MAX_WORKERS = 5
BATCH_SIZE = 100

_print_lock = threading.Lock()


def tprint(msg: str) -> None:
    with _print_lock:
        tqdm.write(msg)


# =============================================================
# UTILITARIOS
# =============================================================
def diretorio_base_parquet() -> Path:
    base_dir = Path(__file__).parent / "parquet" / DEV["dbname"]
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def caminho_parquet_tabela(base_dir: Path, tabela: str) -> Path:
    return base_dir / f"{tabela}.parquet"


def qname(tabela: str) -> str:
    return f"{SCHEMA}.{tabela}"


def pk_de(tabela: str) -> str:
    return f"id_{tabela}_int"


def int_positivo(valor: str) -> int:
    try:
        inteiro = int(valor)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Valor invalido: {valor}") from exc
    if inteiro <= 0:
        raise argparse.ArgumentTypeError(f"Valor deve ser > 0: {valor}")
    return inteiro


def adaptar_valor_pg(valor):
    if pd.isna(valor):
        return None
    if hasattr(valor, "to_pydatetime"):
        return valor.to_pydatetime()
    if hasattr(valor, "item"):
        try:
            return valor.item()
        except Exception:
            return valor
    return valor


# =============================================================
# LEITURA DE CONFIG
# =============================================================
def ler_config(path: Path) -> tuple[list[dict], dict, int | None]:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuracao nao encontrado: {path}")

    items = []
    mapa = {}
    workers = None

    for numero, linha in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue

        partes = [p.strip() for p in linha.split("|")]

        if partes[0] == "@workers":
            if len(partes) != 2:
                raise ValueError(f"Linha {numero}: use '@workers | N'")
            try:
                workers = int(partes[1])
            except ValueError as exc:
                raise ValueError(f"Linha {numero}: '@workers' deve ser inteiro") from exc
            if workers <= 0:
                raise ValueError(f"Linha {numero}: '@workers' deve ser > 0")
            continue

        if partes[0] == "@mapa":
            if len(partes) < 3 or len(partes) > 4:
                raise ValueError(
                    f"Linha {numero}: '@mapa | origem | destino' ou '@mapa | origem | destino | pk'"
                )
            origem = partes[1]
            destino = partes[2]
            pk = partes[3] if len(partes) == 4 and partes[3] else None
            mapa[origem] = {"destino": destino, "pk": pk}
            continue

        if len(partes) > 4:
            raise ValueError(f"Linha {numero} invalida: '{linha}'")

        while len(partes) < 4:
            partes.append("")

        tabela, coluna_data, dias, limit = partes

        if bool(coluna_data) != bool(dias):
            raise ValueError(f"Linha {numero}: 'coluna_data' e 'dias' devem vir juntos")

        try:
            dias_int = int(dias) if dias else None
        except ValueError as exc:
            raise ValueError(f"Linha {numero}: 'dias' deve ser inteiro") from exc
        if dias_int is not None and dias_int < 0:
            raise ValueError(f"Linha {numero}: 'dias' deve ser >= 0")

        try:
            limit_int = int(limit) if limit else None
        except ValueError as exc:
            raise ValueError(f"Linha {numero}: 'limit' deve ser inteiro") from exc
        if limit_int is not None and limit_int <= 0:
            raise ValueError(f"Linha {numero}: 'limit' deve ser > 0")

        items.append(
            {
                "tabela": tabela,
                "coluna_data": coluna_data or None,
                "dias": dias_int,
                "limit": limit_int,
            }
        )

    if not items:
        raise ValueError(f"Nenhuma tabela configurada em {path}")

    return items, mapa, workers


# =============================================================
# EXPORTACAO PARA PARQUET
# =============================================================
def tabela_existe(cur, tabela: str) -> bool:
    cur.execute("SELECT to_regclass(%s) AS oid", (qname(tabela),))
    row = cur.fetchone()
    return row is not None and row["oid"] is not None


def buscar_registros(cur, tabela: str, coluna_data: str | None, dias: int | None, limit: int | None) -> list[dict]:
    query = sql.SQL("SELECT * FROM {}") .format(sql.Identifier(SCHEMA, tabela))
    params = []

    if coluna_data and dias is not None:
        cutoff = dt.date.today() - dt.timedelta(days=dias)
        query += sql.SQL(" WHERE {} >= %s").format(sql.Identifier(coluna_data))
        params.append(cutoff)

    query += sql.SQL(" ORDER BY {} DESC").format(sql.Identifier(pk_de(tabela)))

    if limit is not None:
        query += sql.SQL(" LIMIT %s")
        params.append(limit)

    cur.execute(query, params)
    return cur.fetchall()


def salvar_em_parquet(path_arquivo: Path, registros: list[dict]) -> int:
    if not registros:
        if path_arquivo.exists():
            path_arquivo.unlink()
        return 0

    df = pd.DataFrame(registros)
    df.to_parquet(path_arquivo, index=False)
    return len(df)


def deduplicar_arquivo_parquet(path_arquivo: Path, tabela: str) -> tuple[int, int]:
    if not path_arquivo.exists():
        return 0, 0

    df = pd.read_parquet(path_arquivo)
    if df.empty:
        return 0, 0

    coluna_pk = pk_de(tabela)
    if coluna_pk not in df.columns:
        return len(df), 0

    total_antes = len(df)
    df = df.drop_duplicates(subset=[coluna_pk], keep="first")
    removidos = total_antes - len(df)
    if removidos > 0:
        df.to_parquet(path_arquivo, index=False)
    return len(df), removidos


def processar_tabela_export(item: dict, dry_run: bool, pbar_total: tqdm, parquet_dir: Path) -> dict:
    tabela = item["tabela"]
    coluna_data = item["coluna_data"]
    dias = item["dias"]
    limit = item["limit"]

    resultado = {
        "tabela": tabela,
        "gravados": 0,
        "apos_dedup": 0,
        "deduplicados": 0,
        "erro": None,
    }

    try:
        with psycopg2.connect(**PROD) as conn_prod:
            conn_prod.autocommit = True
            with conn_prod.cursor(cursor_factory=RealDictCursor) as cur_prod:
                if not tabela_existe(cur_prod, tabela):
                    tprint(f"[AVISO] {tabela}: nao existe em producao, pulando")
                    return resultado

                registros = buscar_registros(cur_prod, tabela, coluna_data, dias, limit)
                for _ in registros:
                    pbar_total.update(1)

                if dry_run:
                    tprint(f"[{tabela}] DRY-RUN export: {len(registros)} registro(s)")
                    return resultado

                caminho_saida = caminho_parquet_tabela(parquet_dir, tabela)
                gravados = salvar_em_parquet(caminho_saida, registros)
                apos_dedup, removidos = deduplicar_arquivo_parquet(caminho_saida, tabela)

                resultado["gravados"] = gravados
                resultado["apos_dedup"] = apos_dedup
                resultado["deduplicados"] = removidos
                tprint(
                    f"[{tabela}] parquet={caminho_saida.name} gravados={gravados} "
                    f"deduplicados={removidos} final={apos_dedup}"
                )
    except Exception as e:
        resultado["erro"] = str(e)
        tprint(f"[{tabela}] ERRO export: {e}")

    return resultado


def executar_exportacao(tabelas_conf: list[dict], workers: int, dry_run: bool, parquet_dir: Path) -> list[dict]:
    with tqdm(desc="Registros processados", unit="reg", position=0) as pbar_total:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(processar_tabela_export, item, dry_run, pbar_total, parquet_dir): item["tabela"]
                for item in tabelas_conf
            }
            return [future.result() for future in as_completed(futures)]


# =============================================================
# IMPORTACAO DE PARQUET PARA DEV
# =============================================================
def colunas_de_tabela(cur, tabela: str) -> list[str]:
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
        """,
        (SCHEMA, tabela),
    )
    return [r[0] for r in cur.fetchall()]


def inserir_dataframe_em_tabela(cur_dev, tabela_destino: str, df: pd.DataFrame, batch_size: int) -> tuple[int, int]:
    if df.empty:
        return 0, 0

    colunas_tabela = colunas_de_tabela(cur_dev, tabela_destino)
    colunas_insert = [c for c in df.columns if c in colunas_tabela]
    if not colunas_insert:
        raise ValueError(f"{tabela_destino}: nenhuma coluna em comum entre parquet e tabela")

    dados = df[colunas_insert]
    total_lidos = len(dados)
    inseridos = 0

    cols_sql = sql.SQL(", ").join(sql.Identifier(c) for c in colunas_insert)
    stmt = sql.SQL("INSERT INTO {} ({}) VALUES %s ON CONFLICT DO NOTHING").format(
        sql.Identifier(SCHEMA, tabela_destino),
        cols_sql,
    )

    for inicio in range(0, total_lidos, batch_size):
        fim = min(inicio + batch_size, total_lidos)
        chunk = dados.iloc[inicio:fim]
        valores = [
            tuple(adaptar_valor_pg(v) for v in row)
            for row in chunk.itertuples(index=False, name=None)
        ]
        execute_values(cur_dev, stmt, valores, page_size=batch_size)
        inseridos += max(cur_dev.rowcount, 0)

    ignorados = total_lidos - inseridos
    return inseridos, ignorados


def importar_parquets_para_dev(
    tabelas_conf: list[dict],
    mapa_tabelas: dict,
    parquet_dir: Path,
    dry_run: bool,
    batch_size: int,
    disable_fks: bool,
) -> list[dict]:
    resultados = []
    conn_dev = psycopg2.connect(**DEV)
    conn_dev.autocommit = False

    try:
        with conn_dev.cursor() as cur_dev:
            if disable_fks and not dry_run:
                cur_dev.execute("SET session_replication_role = replica")
                tprint("[DEV] FKs/Triggers desativados temporariamente")

            for item in tabelas_conf:
                tabela_origem = item["tabela"]
                mapa_entry = mapa_tabelas.get(tabela_origem)
                tabela_destino = mapa_entry["destino"] if mapa_entry else tabela_origem
                arquivo_parquet = caminho_parquet_tabela(parquet_dir, tabela_origem)

                resultado = {
                    "tabela_origem": tabela_origem,
                    "tabela_destino": tabela_destino,
                    "lidos": 0,
                    "inseridos": 0,
                    "ignorados": 0,
                    "erro": None,
                }

                try:
                    if not arquivo_parquet.exists():
                        tprint(f"[{tabela_origem}] parquet nao encontrado: {arquivo_parquet.name}")
                        resultados.append(resultado)
                        continue

                    df = pd.read_parquet(arquivo_parquet)
                    resultado["lidos"] = len(df)

                    if dry_run:
                        tprint(
                            f"[{tabela_origem}] DRY-RUN import: {resultado['lidos']} registro(s) "
                            f"-> {tabela_destino}"
                        )
                        resultados.append(resultado)
                        continue

                    inseridos, ignorados = inserir_dataframe_em_tabela(
                        cur_dev=cur_dev,
                        tabela_destino=tabela_destino,
                        df=df,
                        batch_size=batch_size,
                    )
                    resultado["inseridos"] = inseridos
                    resultado["ignorados"] = ignorados
                    tprint(
                        f"[{tabela_origem} -> {tabela_destino}] "
                        f"lidos={resultado['lidos']} inseridos={inseridos} ignorados={ignorados}"
                    )
                except Exception as e:
                    resultado["erro"] = str(e)
                    tprint(f"[{tabela_origem}] ERRO import: {e}")

                resultados.append(resultado)

        if not dry_run:
            conn_dev.commit()
    except Exception:
        conn_dev.rollback()
        raise
    finally:
        if disable_fks and not dry_run and not conn_dev.closed:
            try:
                with conn_dev.cursor() as cur_dev:
                    cur_dev.execute("SET session_replication_role = origin")
                conn_dev.commit()
                tprint("[DEV] FKs/Triggers reativados")
            except Exception as e:
                tprint(f"[DEV] AVISO: falha ao reativar FKs/Triggers: {e}")
        conn_dev.close()

    return resultados


# =============================================================
# RESUMOS
# =============================================================
def imprimir_resumo_export(resultados: list[dict]) -> None:
    print(f"\n{'=' * 70}")
    print(f"{'Tabela':<30} {'Gravados':>10} {'Dedup':>10} {'Final':>10} {'Status':>8}")
    print(f"{'-' * 70}")

    total_gravados = 0
    total_final = 0
    total_dedup = 0
    total_erros = 0
    for r in sorted(resultados, key=lambda x: x["tabela"]):
        status = "ERRO" if r["erro"] else "OK"
        print(
            f"{r['tabela']:<30} {r['gravados']:>10} "
            f"{r['deduplicados']:>10} {r['apos_dedup']:>10} {status:>8}"
        )
        total_gravados += r["gravados"]
        total_dedup += r["deduplicados"]
        total_final += r["apos_dedup"]
        if r["erro"]:
            total_erros += 1
            print(f"  -> {r['erro']}")

    print(f"{'=' * 70}")
    print(f"Total gravado     : {total_gravados}")
    print(f"Total deduplicado : {total_dedup}")
    print(f"Total final       : {total_final}")
    print(f"Tabelas com erro  : {total_erros}")


def imprimir_resumo_import(resultados: list[dict]) -> None:
    print(f"\n{'=' * 90}")
    print(f"{'Tabela origem':<30} {'Destino':<25} {'Lidos':>10} {'Inseridos':>10} {'Ignorados':>10} {'Status':>8}")
    print(f"{'-' * 90}")

    total_lidos = 0
    total_inseridos = 0
    total_ignorados = 0
    total_erros = 0

    for r in resultados:
        status = "ERRO" if r["erro"] else "OK"
        print(
            f"{r['tabela_origem']:<30} {r['tabela_destino']:<25} {r['lidos']:>10} "
            f"{r['inseridos']:>10} {r['ignorados']:>10} {status:>8}"
        )
        total_lidos += r["lidos"]
        total_inseridos += r["inseridos"]
        total_ignorados += r["ignorados"]
        if r["erro"]:
            total_erros += 1
            print(f"  -> {r['erro']}")

    print(f"{'=' * 90}")
    print(f"Total lido       : {total_lidos}")
    print(f"Total inserido   : {total_inseridos}")
    print(f"Total ignorado   : {total_ignorados}")
    print(f"Tabelas com erro : {total_erros}")


# =============================================================
# MAIN
# =============================================================
def main() -> None:
    parser = argparse.ArgumentParser(description="Exporta/importa dados via Parquet")
    default_config = Path(__file__).parent / "tabelas.conf"
    parser.add_argument("--config", default=str(default_config))
    parser.add_argument("--dry-run", action="store_true", help="Simula sem gravar arquivo nem inserir no banco")
    parser.add_argument("--import-parquet", action="store_true", help="Compatibilidade: executa apenas importacao")
    parser.add_argument("--only-export", action="store_true", help="Executa somente a etapa de exportacao")
    parser.add_argument("--only-import", action="store_true", help="Executa somente a etapa de importacao")
    parser.add_argument(
        "--disable-fks",
        dest="disable_fks",
        action="store_true",
        default=True,
        help="Importacao: desativa FKs/Triggers temporariamente (padrao: ativo)",
    )
    parser.add_argument(
        "--enable-fks",
        dest="disable_fks",
        action="store_false",
        help="Importacao: mantem FKs/Triggers ativos durante a carga",
    )
    parser.add_argument("--workers", type=int_positivo, default=None, help=f"Numero de tabelas em paralelo (padrao: {MAX_WORKERS})")
    parser.add_argument("--batch-size", type=int_positivo, default=BATCH_SIZE, help=f"Tamanho do lote (padrao: {BATCH_SIZE})")
    args = parser.parse_args()

    tabelas_conf, mapa_tabelas, workers_conf = ler_config(Path(args.config))
    workers_base = args.workers if args.workers is not None else (workers_conf or MAX_WORKERS)
    workers = min(workers_base, len(tabelas_conf))

    parquet_dir = diretorio_base_parquet()
    print(f"Config: {len(tabelas_conf)} tabela(s) | workers={workers} | batch={args.batch_size}")
    print(f"Parquet dir: {parquet_dir}")
    if args.only_export and (args.only_import or args.import_parquet):
        raise ValueError("Use apenas um entre --only-export e --only-import/--import-parquet")
    if args.only_import and args.import_parquet:
        raise ValueError("Use apenas um entre --only-import e --import-parquet")

    # Padrao: sempre exporta e depois importa.
    run_export = True
    run_import = True
    if args.only_export:
        run_import = False
    if args.only_import or args.import_parquet:
        run_export = False

    if run_export:
        if args.dry_run:
            print("*** MODO DRY-RUN EXPORT ***")

        resultados_export = executar_exportacao(
            tabelas_conf=tabelas_conf,
            workers=workers,
            dry_run=args.dry_run,
            parquet_dir=parquet_dir,
        )
        imprimir_resumo_export(resultados_export)

    if run_import:
        if args.dry_run:
            print("*** MODO DRY-RUN IMPORT ***")
        if args.disable_fks:
            print("*** Import com FKs/Triggers temporariamente desativados ***")

        resultados_import = importar_parquets_para_dev(
            tabelas_conf=tabelas_conf,
            mapa_tabelas=mapa_tabelas,
            parquet_dir=parquet_dir,
            dry_run=args.dry_run,
            batch_size=args.batch_size,
            disable_fks=args.disable_fks,
        )
        imprimir_resumo_import(resultados_import)


if __name__ == "__main__":
    main()
