"""
replicar_dados_semcopy.py
-------------------------
Conecta em produção, busca os registros configurados em tabelas.conf,
resolve dependências e insere no banco dev usando INSERT ... ON CONFLICT
(pk) DO NOTHING.

Processa até MAX_WORKERS tabelas em paralelo — cada worker tem seu
próprio par de conexões (prod + dev), garantindo thread safety.

Uso:
    python replicar_dados_semcopy.py
    python replicar_dados_semcopy.py --config outro_arquivo.conf
    python replicar_dados_semcopy.py --dry-run
    python replicar_dados_semcopy.py --workers 3
"""

import re
import os
import argparse
import datetime as dt
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

import psycopg2
from psycopg2.extras import RealDictCursor
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
        "Arquivo .env não encontrado. Crie-o a partir do .env.example:\n"
        "  cp .env.example .env"
    )

load_dotenv(_encontrar_env())

# =============================================================
# CONEXÕES
# =============================================================
PROD = dict(
    host     = os.environ["PROD_HOST"],
    port     = int(os.environ.get("PROD_PORT", 5432)),
    dbname   = os.environ["PROD_DB"],
    user     = os.environ["PROD_USER"],
    password = os.environ["PROD_PASS"],
)

DEV = dict(
    host     = os.environ.get("DEV_HOST", "localhost"),
    port     = int(os.environ.get("DEV_PORT", 5432)),
    dbname   = os.environ["DEV_DB"],
    user     = os.environ["DEV_USER"],
    password = os.environ["DEV_PASS"],
)

SCHEMA      = "public"
MAX_WORKERS = 5
BATCH_SIZE  = 100

# Tabelas que NÃO devem ser resolvidas como dependência
DEPENDENCIA_IGNORAR: set[str] = set()

# Lock para o tqdm (saída no terminal compartilhada entre threads)
_print_lock = threading.Lock()

def tprint(msg: str) -> None:
    """tqdm.write thread-safe."""
    with _print_lock:
        tqdm.write(msg)

# =============================================================
# LEITURA DO ARQUIVO DE CONFIGURAÇÃO
# =============================================================
def ler_config(path: Path) -> tuple[list[dict], dict, int | None]:
    """
    Lê o tabelas.conf e retorna:
      - lista de itens de tabelas a replicar
      - dicionário de mapeamento de tabelas herdadas { origem: {destino, pk} }
      - número de workers definido via @workers (ou None se não configurado)

    Formatos aceitos por linha:
        @workers | N                              -> define max workers
        @mapa | origem | destino | pk (opcional) -> mapeamento de herança
        tabela
        tabela | coluna_data | dias
        tabela | coluna_data | dias | limit
        tabela | | | limit
    """
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {path}")

    items   = []
    mapa    = {}
    workers = None

    for numero, linha in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue

        partes = [p.strip() for p in linha.split("|")]

        # @workers | N
        if partes[0] == "@workers":
            if len(partes) != 2 or not partes[1].isdigit():
                raise ValueError(f"Linha {numero}: '@workers' requer '@workers | N' onde N é um número inteiro")
            workers = int(partes[1])
            continue

        # @mapa | origem | destino | pk (opcional)
        if partes[0] == "@mapa":
            if len(partes) < 3 or len(partes) > 4:
                raise ValueError(f"Linha {numero}: '@mapa' requer '@mapa | origem | destino' ou '@mapa | origem | destino | pk'")
            origem  = partes[1]
            destino = partes[2]
            pk      = partes[3] if len(partes) == 4 and partes[3] else None
            mapa[origem] = {"destino": destino, "pk": pk}
            pk_info = f" (pk: {pk})" if pk else ""
            tprint(f"[MAPA] {origem} → {destino}{pk_info}")
            continue

        if len(partes) > 4:
            raise ValueError(f"Linha {numero} inválida: '{linha}'")

        while len(partes) < 4:
            partes.append("")

        tabela, coluna_data, dias, limit = partes

        if bool(coluna_data) != bool(dias):
            raise ValueError(f"Linha {numero}: 'coluna_data' e 'dias' devem ser preenchidos juntos.")

        dias_int  = int(dias)  if dias  else None
        limit_int = int(limit) if limit else None

        items.append({
            "tabela":      tabela,
            "coluna_data": coluna_data or None,
            "dias":        dias_int,
            "limit":       limit_int,
        })

    if not items:
        raise ValueError(f"Nenhuma tabela configurada em {path}")

    return items, mapa, workers

# =============================================================
# HELPERS DE BANCO
# =============================================================
def qname(tabela: str) -> str:
    return f"{SCHEMA}.{tabela}"

def pk_de(tabela: str) -> str:
    return f"id_{tabela}_int"

def tabela_existe(cur, tabela: str) -> bool:
    cur.execute("SELECT to_regclass(%s) AS oid", (qname(tabela),))
    row = cur.fetchone()
    return row is not None and row["oid"] is not None

def colunas_de(cur, tabela: str) -> list[str]:
    cur.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
    """, (SCHEMA, tabela))
    return [r["column_name"] for r in cur.fetchall()]

def buscar_registros(cur, tabela: str, coluna_data: str | None,
                     dias: int | None, limit: int | None) -> list[dict]:
    sql    = f"SELECT * FROM {qname(tabela)}"
    params = []

    if coluna_data and dias is not None:
        cutoff = dt.date.today() - dt.timedelta(days=dias)
        sql   += f" WHERE {coluna_data} >= %s"
        params.append(cutoff)

    sql += f" ORDER BY {pk_de(tabela)} DESC"

    if limit is not None:
        sql += " LIMIT %s"
        params.append(limit)

    cur.execute(sql, params)
    return cur.fetchall()

def buscar_por_pk(cur, tabela: str, pk_valor) -> dict | None:
    pk = pk_de(tabela)
    cur.execute(f"SELECT * FROM {qname(tabela)} WHERE {pk} = %s", (pk_valor,))
    return cur.fetchone()

def inserir_registro(cur_dev, tabela: str, registro: dict,
                     dry_run: bool, mapa_tabelas: dict) -> bool:
    """
    INSERT com ON CONFLICT (pk) DO NOTHING.
    Se a tabela estiver no mapa_tabelas, redireciona o insert para a tabela destino
    (ex: cbcontrato → cbcontratoeleva), usando a PK configurada se informada.
    Usa SAVEPOINT para isolar erros sem derrubar a transação.
    """
    if dry_run:
        return True

    # Redireciona para tabela herdada se houver mapeamento
    mapa_entry     = mapa_tabelas.get(tabela)
    tabela_destino = mapa_entry["destino"] if mapa_entry else tabela
    pk             = mapa_entry["pk"] if mapa_entry and mapa_entry["pk"] else pk_de(tabela_destino)

    colunas  = list(registro.keys())
    cols_sql = ", ".join(colunas)
    vals_sql = ", ".join([f"%({c})s" for c in colunas])

    sql = f"""
        INSERT INTO {qname(tabela_destino)} ({cols_sql})
        VALUES ({vals_sql})
        ON CONFLICT ({pk}) DO NOTHING
    """

    cur_dev.execute("SAVEPOINT insert_row")
    try:
        cur_dev.execute(sql, registro)
        cur_dev.execute("RELEASE SAVEPOINT insert_row")
        return True
    except Exception as e:
        cur_dev.execute("ROLLBACK TO SAVEPOINT insert_row")
        cur_dev.execute("RELEASE SAVEPOINT insert_row")
        pk_val = registro.get(pk_de(tabela), "?")
        tprint(f"   [IGNORADO] {tabela} pk={pk_val}: {e}")
        return False

# =============================================================
# RESOLUÇÃO DE DEPENDÊNCIAS
# =============================================================
RE_COLUNA_DEP = re.compile(r"^id_([a-z0-9]+)_int$", re.IGNORECASE)

def dependencias_de(cur_prod, tabela: str, cache_colunas: dict) -> list[tuple[str, str]]:
    if tabela not in cache_colunas:
        cache_colunas[tabela] = colunas_de(cur_prod, tabela)

    deps = []
    for col in cache_colunas[tabela]:
        match = RE_COLUNA_DEP.match(col)
        if not match:
            continue

        tabela_ref = match.group(1).lower()

        if tabela_ref == tabela.lower():
            continue
        if tabela_ref in DEPENDENCIA_IGNORAR:
            continue
        if tabela_existe(cur_prod, tabela_ref):
            deps.append((col, tabela_ref))

    return deps

def inserir_com_deps(cur_prod, cur_dev, tabela: str, registro: dict,
                     ja_inseridos: set, cache_colunas: dict,
                     dry_run: bool, mapa_tabelas: dict) -> None:
    """
    Insere registro e suas dependências recursivamente.
    ja_inseridos é LOCAL a cada worker — não compartilhado entre threads.
    ON CONFLICT DO NOTHING resolve colisões entre workers no banco.
    """
    pk_val = registro.get(pk_de(tabela))
    if pk_val is None:
        return

    chave = (tabela, int(pk_val))
    if chave in ja_inseridos:
        return

    ja_inseridos.add(chave)

    # 1) Resolve dependências primeiro
    for coluna_fk, tabela_dep in dependencias_de(cur_prod, tabela, cache_colunas):
        id_dep = registro.get(coluna_fk)
        if id_dep is None:
            continue

        registro_dep = buscar_por_pk(cur_prod, tabela_dep, id_dep)
        if registro_dep is None:
            tprint(f"   [AVISO] {tabela}.{coluna_fk}={id_dep} → {tabela_dep} não encontrado, ignorando.")
            continue

        inserir_com_deps(cur_prod, cur_dev, tabela_dep, registro_dep,
                         ja_inseridos, cache_colunas, dry_run, mapa_tabelas)

    # 2) Insere o registro atual
    inserir_registro(cur_dev, tabela, registro, dry_run, mapa_tabelas)

# =============================================================
# WORKER — processa uma tabela por completo
# =============================================================
def processar_tabela(item: dict, dry_run: bool, pbar_total: tqdm,
                     mapa_tabelas: dict, batch_size: int = BATCH_SIZE) -> dict:
    """
    Executado em thread separada. Cria suas próprias conexões
    prod e dev — psycopg2 não é thread-safe entre conexões.
    Retorna dict com resultado: { tabela, inseridos, ignorados, erro }.
    """
    tabela      = item["tabela"]
    coluna_data = item["coluna_data"]
    dias        = item["dias"]
    limit       = item["limit"]

    filtro_desc = []
    if coluna_data and dias is not None:
        filtro_desc.append(f"{coluna_data} >= hoje-{dias}d")
    if limit is not None:
        filtro_desc.append(f"LIMIT {limit}")
    filtro_str = " | ".join(filtro_desc) if filtro_desc else "sem filtro"

    resultado = {"tabela": tabela, "inseridos": 0, "ignorados": 0, "erros": 0, "erro": None}

    try:
        # Cada worker tem seu próprio par de conexões
        with (
            psycopg2.connect(**PROD) as conn_prod,
            psycopg2.connect(**DEV)  as conn_dev,
        ):
            conn_prod.autocommit = True
            conn_dev.autocommit  = False

            with (
                conn_prod.cursor(cursor_factory=RealDictCursor) as cur_prod,
                conn_dev.cursor()                               as cur_dev,
            ):
                if not tabela_existe(cur_prod, tabela):
                    tprint(f"[AVISO] {tabela}: não existe em produção, pulando.")
                    return resultado

                registros = buscar_registros(cur_prod, tabela, coluna_data, dias, limit)
                tprint(f"\n{'─'*60}")
                tprint(f"[{tabela}] {filtro_str} | {len(registros)} registro(s)")

                ja_inseridos:  set[tuple[str, int]] = set()   # local por worker
                cache_colunas: dict[str, list[str]] = {}      # local por worker

                inseridos = 0
                ignorados = 0
                erros     = 0

                for i, reg in enumerate(registros):
                    antes = len(ja_inseridos)
                    inserir_com_deps(cur_prod, cur_dev, tabela, reg,
                                     ja_inseridos, cache_colunas, dry_run, mapa_tabelas)

                    novos = len(ja_inseridos) - antes
                    if novos > 0:
                        inseridos += novos
                    else:
                        ignorados += 1

                    # Commit a cada batch_size registros
                    if not dry_run and (i + 1) % batch_size == 0:
                        conn_dev.commit()

                    pbar_total.update(1)

                # Commit do restante
                if not dry_run:
                    conn_dev.commit()

                resultado["inseridos"] = inseridos
                resultado["ignorados"] = ignorados
                resultado["erros"]     = erros
                tprint(f"[{tabela}] ✔ {inseridos} inserido(s), {ignorados} já existia(m), {erros} erro(s) ignorado(s)")

    except Exception as e:
        resultado["erro"] = str(e)
        tprint(f"[{tabela}] ✖ ERRO: {e}")

    return resultado

# =============================================================
# MAIN
# =============================================================
def main():
    parser = argparse.ArgumentParser(description="Replica dados de produção para dev via INSERT paralelo.")
    default_config = Path(__file__).parent / "tabelas.conf"
    parser.add_argument("--config",     default=str(default_config))
    parser.add_argument("--dry-run",    action="store_true",           help="Simula sem inserir nada")
    parser.add_argument("--workers",    type=int, default=MAX_WORKERS, help=f"Nº de tabelas em paralelo (padrão: {MAX_WORKERS})")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE,  help=f"Commit a cada N registros (padrão: {BATCH_SIZE})")
    args = parser.parse_args()

    if args.dry_run:
        print("*** MODO DRY-RUN: nenhum dado será inserido ***\n")

    tabelas_conf, mapa_tabelas, workers_conf = ler_config(Path(args.config))

    # Prioridade: --workers (CLI) > @workers (conf) > MAX_WORKERS (padrão)
    workers = min(
        args.workers if args.workers != MAX_WORKERS else (workers_conf or MAX_WORKERS),
        len(tabelas_conf)
    )

    print(f"Configuração: {len(tabelas_conf)} tabela(s) | {workers} worker(s) | batch {args.batch_size}")
    if workers_conf:
        print(f"  (workers definido via @workers no conf)")
    if mapa_tabelas:
        print("Mapeamentos ativos:")
        for origem, entry in mapa_tabelas.items():
            pk_info = f" (pk: {entry['pk']})" if entry["pk"] else ""
            print(f"  {origem} → {entry['destino']}{pk_info}")
    print()

    with tqdm(desc="Registros processados", unit="reg", position=0) as pbar_total:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(processar_tabela, item, args.dry_run,
                                pbar_total, mapa_tabelas, args.batch_size): item["tabela"]
                for item in tabelas_conf
            }

            resultados = []
            for future in as_completed(futures):
                resultados.append(future.result())

    # Resumo final
    print(f"\n{'═'*70}")
    print(f"{'Tabela':<30} {'Inseridos':>10} {'Ignorados':>10} {'Erros':>8} {'Status':>8}")
    print(f"{'─'*70}")

    total_inseridos = 0
    total_erros     = 0
    for r in sorted(resultados, key=lambda x: x["tabela"]):
        status = "✖ ERRO" if r["erro"] else "✔ OK"
        erros_insert = r.get("erros", 0)
        print(f"{r['tabela']:<30} {r['inseridos']:>10} {r['ignorados']:>10} {erros_insert:>8} {status:>8}")
        total_inseridos += r["inseridos"]
        if r["erro"]:
            total_erros += 1
            print(f"  └ {r['erro']}")

    print(f"{'═'*70}")
    print(f"Total inserido : {total_inseridos}")
    print(f"Tabelas com erro: {total_erros}")
    print("Concluído ✅" if total_erros == 0 else "Concluído com erros ⚠️")

if __name__ == "__main__":
    main()