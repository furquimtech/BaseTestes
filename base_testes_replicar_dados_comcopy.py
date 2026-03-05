"""
base_testes_replicar_dados_comcopy.py
-------------------------------------
Fase 1 - GERAR: coleta dados de PROD e gera um .sql com blocos COPY.
Fase 2 - APLICAR: executa o .sql no banco DEV via psql.
"""

import argparse
import datetime as dt
import os
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from tqdm import tqdm

from util import (
    buscar_por_pk,
    buscar_registros,
    conexoes_env,
    dependencias_de,
    encontrar_env,
    int_positivo,
    ler_config_tabelas_e_workers,
    pk_de,
    qname,
    tabela_existe,
)


load_dotenv(encontrar_env())

PROD, DEV = conexoes_env()
SCHEMA_DEFAULT = os.environ.get("DB_SCHEMA", "public")
PG_BIN_DEFAULT = os.environ.get("PG_BIN", r"C:\Program Files\PostgreSQL\15\bin")
PSQL_DEFAULT = str(Path(PG_BIN_DEFAULT) / "psql.exe")
OUT_DIR_DEFAULT = Path(os.environ.get("OUT_DIR", str(Path(__file__).parent / "out")))
MAX_WORKERS = 5

# Tabelas que nao devem ser resolvidas como dependencia (env: "t1,t2,t3")
DEPENDENCIA_IGNORAR_DEFAULT = {
    t.strip().lower()
    for t in os.environ.get("DEPENDENCIA_IGNORAR", "").split(",")
    if t.strip()
}

_print_lock = threading.Lock()


def tprint(msg: str) -> None:
    with _print_lock:
        tqdm.write(msg)


def valor_para_copy(v) -> str:
    if v is None:
        return r"\N"
    if isinstance(v, bool):
        return "t" if v else "f"
    if isinstance(v, (dt.date, dt.datetime)):
        return v.isoformat()
    return str(v).replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")


def gerar_bloco_copy(schema: str, tabela: str, colunas: list[str], registros: list[dict]) -> str:
    cols_sql = ", ".join(colunas)
    linhas = ["\t".join(valor_para_copy(reg.get(c)) for c in colunas) for reg in registros]
    return (
        f"-- {tabela}: {len(registros)} registro(s)\n"
        f"COPY {qname(schema, tabela)} ({cols_sql}) FROM stdin;\n"
        + "\n".join(linhas)
        + "\n\\.\n"
    )


def coletar_com_deps(
    cur_prod,
    schema: str,
    tabela: str,
    registro: dict,
    ja_coletados: set,
    cache_colunas: dict,
    buffer: dict,
    dependencia_ignorar: set[str],
) -> None:
    pk_val = registro.get(pk_de(tabela))
    if pk_val is None:
        return

    chave = (tabela, int(pk_val))
    if chave in ja_coletados:
        return

    ja_coletados.add(chave)

    for coluna_fk, tabela_dep in dependencias_de(
        cur_prod,
        schema=schema,
        tabela=tabela,
        cache_colunas=cache_colunas,
        dependencia_ignorar=dependencia_ignorar,
    ):
        id_dep = registro.get(coluna_fk)
        if id_dep is None:
            continue

        registro_dep = buscar_por_pk(cur_prod, schema=schema, tabela=tabela_dep, pk_valor=id_dep)
        if registro_dep is None:
            tprint(f"   [AVISO] {tabela}.{coluna_fk}={id_dep} -> {tabela_dep} nao encontrado, ignorando.")
            continue

        coletar_com_deps(
            cur_prod=cur_prod,
            schema=schema,
            tabela=tabela_dep,
            registro=registro_dep,
            ja_coletados=ja_coletados,
            cache_colunas=cache_colunas,
            buffer=buffer,
            dependencia_ignorar=dependencia_ignorar,
        )

    buffer.setdefault(tabela, {})[int(pk_val)] = registro


def processar_tabela(item: dict, schema: str, dependencia_ignorar: set[str]) -> dict:
    tabela = item["tabela"]
    coluna_data = item["coluna_data"]
    dias = item["dias"]
    limit = item["limit"]

    resultado = {
        "tabela": tabela,
        "lidos": 0,
        "coletados": 0,
        "erro": None,
        "buffer": {},
    }

    try:
        with psycopg2.connect(**PROD) as conn_prod:
            conn_prod.autocommit = True
            with conn_prod.cursor(cursor_factory=RealDictCursor) as cur_prod:
                if not tabela_existe(cur_prod, schema=schema, tabela=tabela):
                    tprint(f"[{tabela}] [AVISO] Tabela nao existe em producao, pulando.")
                    return resultado

                registros = buscar_registros(
                    cur_prod,
                    schema=schema,
                    tabela=tabela,
                    coluna_data=coluna_data,
                    dias=dias,
                    limit=limit,
                )
                resultado["lidos"] = len(registros)

                local_buffer: dict[str, dict[int, dict]] = {}
                local_ja_coletados: set[tuple[str, int]] = set()
                cache_colunas: dict[str, list[str]] = {}

                for reg in registros:
                    coletar_com_deps(
                        cur_prod=cur_prod,
                        schema=schema,
                        tabela=tabela,
                        registro=reg,
                        ja_coletados=local_ja_coletados,
                        cache_colunas=cache_colunas,
                        buffer=local_buffer,
                        dependencia_ignorar=dependencia_ignorar,
                    )

                resultado["coletados"] = sum(len(v) for v in local_buffer.values())
                resultado["buffer"] = local_buffer
                tprint(f"[{tabela}] lidos={resultado['lidos']} | coletados={resultado['coletados']}")
    except Exception as e:
        resultado["erro"] = str(e)
        tprint(f"[{tabela}] [ERRO] {e}")

    return resultado


def gerar_sql(
    config_path: Path,
    sql_path: Path,
    schema: str,
    out_dir: Path,
    dependencia_ignorar: set[str],
    workers: int | None,
) -> int:
    tabelas_conf, workers_conf = ler_config_tabelas_e_workers(config_path)
    buffer: dict[str, dict[int, dict]] = {}
    workers_base = workers if workers is not None else (workers_conf or MAX_WORKERS)
    workers_exec = min(workers_base, len(tabelas_conf))
    tprint(f"Config: {len(tabelas_conf)} tabela(s) | workers={workers_exec}")
    if workers_conf:
        tprint("  (workers definido via @workers no conf)")

    resultados = []
    with ThreadPoolExecutor(max_workers=workers_exec) as executor:
        futures = {
            executor.submit(processar_tabela, item, schema, dependencia_ignorar): item["tabela"]
            for item in tabelas_conf
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processando tabelas", unit="tabela"):
            resultados.append(future.result())

    erros = [r for r in resultados if r["erro"]]
    if erros:
        tabelas_erro = ", ".join(sorted(r["tabela"] for r in erros))
        raise RuntimeError(f"Falha em {len(erros)} tabela(s): {tabelas_erro}")

    for r in resultados:
        for tabela, registros_dict in r["buffer"].items():
            destino = buffer.setdefault(tabela, {})
            destino.update(registros_dict)

    out_dir.mkdir(parents=True, exist_ok=True)
    total = sum(len(v) for v in buffer.values())

    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("-- =================================================\n")
        f.write(f"-- Gerado em : {dt.datetime.now().isoformat()}\n")
        f.write(f"-- Origem    : {PROD['host']} / {PROD['dbname']}\n")
        f.write(f"-- Destino   : {DEV['host']} / {DEV['dbname']}\n")
        f.write(f"-- Schema    : {schema}\n")
        f.write(f"-- Registros : {total}\n")
        f.write("-- =================================================\n\n")
        f.write("BEGIN;\n\n")
        f.write("SET LOCAL session_replication_role = replica;\n\n")

        for tabela, registros_dict in buffer.items():
            registros = list(registros_dict.values())
            if not registros:
                continue
            colunas = list(registros[0].keys())
            f.write(gerar_bloco_copy(schema, tabela, colunas, registros))
            f.write("\n")

        f.write("SET LOCAL session_replication_role = origin;\n")
        f.write("COMMIT;\n")

    tqdm.write(f"\n{'=' * 60}")
    tqdm.write(f"OK .sql gerado : {sql_path}")
    tqdm.write(f"  Tabelas      : {len(buffer)}")
    tqdm.write(f"  Registros    : {total}")
    return total


def aplicar_sql(sql_path: Path, psql_path: str) -> None:
    if not sql_path.exists():
        raise FileNotFoundError(f".sql nao encontrado: {sql_path}")

    if not Path(psql_path).exists():
        raise FileNotFoundError(f"psql nao encontrado: {psql_path}\nAjuste --psql ou PG_BIN.")

    env = os.environ.copy()
    env["PGPASSWORD"] = DEV["password"]

    cmd = [
        psql_path,
        "-h",
        DEV["host"],
        "-p",
        str(DEV["port"]),
        "-U",
        DEV["user"],
        "-d",
        DEV["dbname"],
        "-v",
        "ON_ERROR_STOP=1",
        "-f",
        str(sql_path),
    ]

    print(f"\nAplicando {sql_path.name} no banco dev...")
    p = subprocess.run(cmd, env=env, text=True, capture_output=True, encoding="utf-8", errors="replace")

    if p.returncode != 0:
        raise RuntimeError(f"Erro ao aplicar o .sql:\n\nSTDOUT:\n{p.stdout}\n\nSTDERR:\n{p.stderr}")

    print("OK Aplicado com sucesso!")


def main():
    parser = argparse.ArgumentParser(description="Replica dados de producao para dev via .sql COPY.")
    default_config = Path(__file__).parent / "tabelas.conf"
    parser.add_argument("--config", default=str(default_config))
    parser.add_argument("--schema", default=SCHEMA_DEFAULT, help=f"Schema de origem/destino (padrao: {SCHEMA_DEFAULT})")
    parser.add_argument("--out-dir", default=str(OUT_DIR_DEFAULT), help=f"Pasta dos .sql gerados (padrao: {OUT_DIR_DEFAULT})")
    parser.add_argument("--psql", default=PSQL_DEFAULT, help=f"Caminho completo do psql (padrao: {PSQL_DEFAULT})")
    parser.add_argument("--workers", type=int_positivo, default=None, help=f"Numero de tabelas em paralelo (padrao: {MAX_WORKERS})")
    parser.add_argument("--dry-run", action="store_true", help="Gera o .sql mas nao aplica")
    parser.add_argument("--apenas-gerar", action="store_true", help="So gera o .sql")
    parser.add_argument("--apenas-aplicar", action="store_true", help="Aplica o ultimo .sql gerado")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    sql_path = out_dir / f"dados_{ts}.sql"

    if args.apenas_aplicar:
        sqls = sorted(out_dir.glob("dados_*.sql"), reverse=True)
        if not sqls:
            raise FileNotFoundError(f"Nenhum .sql encontrado em {out_dir}")
        sql_path = sqls[0]
        print(f"Usando .sql mais recente: {sql_path}")
        aplicar_sql(sql_path, args.psql)
        return

    gerar_sql(
        config_path=Path(args.config),
        sql_path=sql_path,
        schema=args.schema,
        out_dir=out_dir,
        dependencia_ignorar=DEPENDENCIA_IGNORAR_DEFAULT,
        workers=args.workers,
    )

    if args.dry_run or args.apenas_gerar:
        print("\n.sql gerado mas nao aplicado (--dry-run / --apenas-gerar).")
        return

    aplicar_sql(sql_path, args.psql)
    print(f"\n{'=' * 60}")
    print("Concluido.")


if __name__ == "__main__":
    main()
