"""
replicar_dados.py
-----------------
Fase 1 - GERAR: Conecta em produção, busca os registros configurados em
         tabelas.conf, resolve dependências e gera um arquivo .sql com
         comandos COPY pronto para ser aplicado.

Fase 2 - APLICAR: Executa o .sql gerado no banco dev via psql em uma
         única transação.

Uso:
    python replicar_dados.py                   # gera e aplica
    python replicar_dados.py --apenas-gerar    # só gera o .sql
    python replicar_dados.py --apenas-aplicar  # aplica o último .sql gerado
    python replicar_dados.py --dry-run         # gera o .sql mas não aplica
"""

import re
import os
import subprocess
import argparse
import datetime as dt
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor
from tqdm import tqdm

# =============================================================
# CONEXÕES
# =============================================================
PROD = dict(
    host     = "10.80.91.30",
    port     = 5432,
    dbname   = "10.50.13.22_eleva",
    user     = "mrfamos",
    password = "Mikael1811!",
)

DEV = dict(
    host     = "localhost",
    port     = 5432,
    dbname   = "10.50.13.22_eleva_teste",
    user     = "postgres",
    password = "f5vcn32k",
)

PG_BIN = r"C:\Program Files\PostgreSQL\15\bin"
PSQL   = str(Path(PG_BIN) / "psql.exe")

SCHEMA = "public"

# Tabelas que NÃO devem ser resolvidas como dependência
DEPENDENCIA_IGNORAR: set[str] = set()

# Pasta de saída dos arquivos .sql gerados
OUT_DIR = Path("./out")

# =============================================================
# LEITURA DO ARQUIVO DE CONFIGURAÇÃO
# =============================================================
def ler_config(path: Path) -> list[dict]:
    """
    Formatos aceitos por linha:
        tabela
        tabela | coluna_data | dias
        tabela | coluna_data | dias | limit
        tabela | | | limit
    """
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {path}")

    items = []
    for numero, linha in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue

        partes = [p.strip() for p in linha.split("|")]
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

    return items

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

# =============================================================
# COLETA E GERAÇÃO DO .SQL
# =============================================================
def valor_para_copy(v) -> str:
    """Converte valor Python para o formato texto do COPY."""
    if v is None:
        return r"\N"
    if isinstance(v, bool):
        return "t" if v else "f"
    if isinstance(v, (dt.date, dt.datetime)):
        return v.isoformat()
    return (
        str(v)
        .replace("\\", "\\\\")
        .replace("\t", "\\t")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )

def gerar_bloco_copy(tabela: str, colunas: list[str], registros: list[dict]) -> str:
    """Gera bloco COPY ... FROM stdin com os registros."""
    cols_sql = ", ".join(colunas)
    linhas   = [
        "\t".join(valor_para_copy(reg.get(c)) for c in colunas)
        for reg in registros
    ]
    return (
        f"-- {tabela}: {len(registros)} registro(s)\n"
        f"COPY {qname(tabela)} ({cols_sql}) FROM stdin;\n"
        + "\n".join(linhas)
        + "\n\\.\n"
    )

def coletar_com_deps(cur_prod, tabela: str, registro: dict,
                     ja_coletados: set, cache_colunas: dict,
                     buffer: dict) -> None:
    """
    Coleta registro e todas as suas dependências no buffer.
    O buffer é indexado por (tabela, pk_val) garantindo que
    nenhum registro seja escrito duas vezes no .sql.
    """
    pk_val = registro.get(pk_de(tabela))
    if pk_val is None:
        return

    chave = (tabela, int(pk_val))
    if chave in ja_coletados:
        return

    ja_coletados.add(chave)

    # 1) Coleta dependências primeiro (recursivo)
    for coluna_fk, tabela_dep in dependencias_de(cur_prod, tabela, cache_colunas):
        id_dep = registro.get(coluna_fk)
        if id_dep is None:
            continue

        registro_dep = buscar_por_pk(cur_prod, tabela_dep, id_dep)
        if registro_dep is None:
            tqdm.write(f"   [AVISO] {tabela}.{coluna_fk}={id_dep} → {tabela_dep} não encontrado, ignorando.")
            continue

        coletar_com_deps(cur_prod, tabela_dep, registro_dep,
                         ja_coletados, cache_colunas, buffer)

    # 2) Adiciona ao buffer indexado por pk — garante unicidade no .sql
    # buffer = { tabela: { pk_val: registro } }
    buffer.setdefault(tabela, {})[int(pk_val)] = registro

def gerar_sql(config_path: Path, sql_path: Path) -> int:
    """Fase 1: coleta dados de produção e gera o .sql."""
    tabelas_conf  = ler_config(config_path)
    buffer:        dict[str, list[dict]] = {}
    ja_coletados:  set[tuple[str, int]]  = set()
    cache_colunas: dict[str, list[str]]  = {}

    with psycopg2.connect(**PROD) as conn_prod:
        conn_prod.autocommit = True

        with conn_prod.cursor(cursor_factory=RealDictCursor) as cur_prod:
            for item in tqdm(tabelas_conf, desc="Coletando tabelas", unit="tabela", position=0):
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

                tqdm.write(f"\n{'─'*60}")
                tqdm.write(f"Tabela: {tabela} | {filtro_str}")

                if not tabela_existe(cur_prod, tabela):
                    tqdm.write(f"   [AVISO] Tabela não existe em produção, pulando.")
                    continue

                registros = buscar_registros(cur_prod, tabela, coluna_data, dias, limit)
                tqdm.write(f"   {len(registros)} registro(s) encontrado(s)")

                with tqdm(total=len(registros), desc=f"  {tabela}",
                          unit="reg", position=1, leave=False) as pbar:
                    for reg in registros:
                        coletar_com_deps(cur_prod, tabela, reg,
                                         ja_coletados, cache_colunas, buffer)
                        pbar.update(1)

    # Grava o .sql
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total = sum(len(v) for v in buffer.values())

    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("-- =================================================\n")
        f.write(f"-- Gerado em : {dt.datetime.now().isoformat()}\n")
        f.write(f"-- Origem    : {PROD['host']} / {PROD['dbname']}\n")
        f.write(f"-- Destino   : {DEV['host']} / {DEV['dbname']}\n")
        f.write(f"-- Registros : {total}\n")
        f.write("-- =================================================\n\n")
        f.write("BEGIN;\n\n")

        for tabela, registros_dict in buffer.items():
            registros = list(registros_dict.values())
            colunas   = list(registros[0].keys())
            f.write(gerar_bloco_copy(tabela, colunas, registros))
            f.write("\n")

        f.write("COMMIT;\n")

    tqdm.write(f"\n{'═'*60}")
    tqdm.write(f"✔ .sql gerado : {sql_path}")
    tqdm.write(f"  Tabelas     : {len(buffer)}")
    tqdm.write(f"  Registros   : {total}")
    return total

# =============================================================
# APLICAÇÃO DO .SQL
# =============================================================
def aplicar_sql(sql_path: Path) -> None:
    """Fase 2: aplica o .sql no banco dev via psql em uma única transação."""
    if not sql_path.exists():
        raise FileNotFoundError(f".sql não encontrado: {sql_path}")

    if not Path(PSQL).exists():
        raise FileNotFoundError(f"psql não encontrado: {PSQL}\nAjuste PG_BIN no script.")

    env = os.environ.copy()
    env["PGPASSWORD"] = DEV["password"]

    cmd = [
        PSQL,
        "-h", DEV["host"],
        "-p", str(DEV["port"]),
        "-U", DEV["user"],
        "-d", DEV["dbname"],
        "-v", "ON_ERROR_STOP=1",
        "-f", str(sql_path),
    ]

    print(f"\nAplicando {sql_path.name} no banco dev...")
    p = subprocess.run(cmd, env=env, text=True, capture_output=True,
                       encoding="utf-8", errors="replace")

    if p.returncode != 0:
        raise RuntimeError(
            f"Erro ao aplicar o .sql:\n\nSTDOUT:\n{p.stdout}\n\nSTDERR:\n{p.stderr}"
        )

    print("✔ Aplicado com sucesso!")

# =============================================================
# MAIN
# =============================================================
def main():
    parser = argparse.ArgumentParser(description="Replica dados de produção para dev via .sql.")
    default_config = Path(__file__).parent / "tabelas.conf"
    parser.add_argument("--config",         default=str(default_config))
    parser.add_argument("--dry-run",        action="store_true", help="Gera o .sql mas não aplica")
    parser.add_argument("--apenas-gerar",   action="store_true", help="Só gera o .sql")
    parser.add_argument("--apenas-aplicar", action="store_true", help="Aplica o último .sql gerado")
    args = parser.parse_args()

    ts       = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    sql_path = OUT_DIR / f"dados_{ts}.sql"

    # Modo: só aplicar o .sql mais recente
    if args.apenas_aplicar:
        sqls = sorted(OUT_DIR.glob("dados_*.sql"), reverse=True)
        if not sqls:
            raise FileNotFoundError(f"Nenhum .sql encontrado em {OUT_DIR}")
        sql_path = sqls[0]
        print(f"Usando .sql mais recente: {sql_path}")
        aplicar_sql(sql_path)
        return

    # Fase 1: gera o .sql
    gerar_sql(Path(args.config), sql_path)

    if args.dry_run or args.apenas_gerar:
        print("\n.sql gerado mas não aplicado (--dry-run / --apenas-gerar).")
        return

    # Fase 2: aplica o .sql
    aplicar_sql(sql_path)

    print(f"\n{'═'*60}")
    print("Concluído ✅")

if __name__ == "__main__":
    main()