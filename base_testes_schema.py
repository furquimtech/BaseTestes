import re
import os
import argparse
import subprocess
import platform
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

import psycopg2
from psycopg2 import sql

# =========================
# CARREGA CREDENCIAIS DO .env.scripts
# =========================
_ENV_PATH = Path(__file__).parent / ".env"
if not _ENV_PATH.exists():
    _ENV_PATH = Path(__file__).parent.parent / ".env.scripts"
if not _ENV_PATH.exists():
    raise FileNotFoundError(
        "Arquivo .env.scripts não encontrado. Crie-o a partir do .env.scripts.example:\n"
        "  cp .env.scripts.example .env.scripts"
    )
load_dotenv(_ENV_PATH)

# =========================
# CONFIG
# =========================

# Binários do PostgreSQL — detecta automaticamente Windows ou Linux
if platform.system() == "Windows":
    PG_BIN  = r"C:\Program Files\PostgreSQL\15\bin"
    PSQL    = str(Path(PG_BIN) / "psql.exe")
    PG_DUMP = str(Path(PG_BIN) / "pg_dump.exe")
else:
    PSQL    = "/usr/bin/psql"
    PG_DUMP = "/usr/bin/pg_dump"

# PRODUÇÃO (origem)
PROD_HOST = os.environ["PROD_HOST"]
PROD_PORT = int(os.environ.get("PROD_PORT", 5432))
PROD_DB   = os.environ["PROD_DB"]
PROD_USER = os.environ["PROD_USER"]
PROD_PASS = os.environ["PROD_PASS"]

# LOCAL/Dev (destino)
LOCAL_HOST       = os.environ.get("DEV_HOST", "localhost")
LOCAL_PORT       = int(os.environ.get("DEV_PORT", 5432))
LOCAL_ADMIN_DB   = os.environ.get("DEV_ADMIN_DB", "postgres")
LOCAL_ADMIN_USER = os.environ["DEV_USER"]
LOCAL_ADMIN_PASS = os.environ["DEV_PASS"]
TARGET_DB        = os.environ["DEV_DB"]

EXTENSIONS_TO_SKIP = [
    "adminpack",
    "pg_similarity",
]

INCOMPATIBLE_SETTINGS = [
    "idle_in_transaction_session_timeout",
    "transaction_timeout",
]

# Dump output
OUT_DIR   = Path("./out")
OUT_DIR.mkdir(parents=True, exist_ok=True)
DUMP_FILE = OUT_DIR / f"schema_{PROD_HOST}_{PROD_DB}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"


# =========================
# Helpers
# =========================

def sanitize_dump_remove_extensions(dump_path: Path, extensions_to_skip: list[str]) -> None:
    txt = dump_path.read_text(encoding="utf-8", errors="replace")

    for ext in extensions_to_skip:
        txt = re.sub(
            rf'^\s*CREATE\s+EXTENSION\b.*?\b{re.escape(ext)}\b.*?;\s*$',
            '', txt, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL
        )
        txt = re.sub(
            rf'^\s*COMMENT\s+ON\s+EXTENSION\s+{re.escape(ext)}\s+IS\s+.*?;\s*$',
            '', txt, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL
        )
        txt = re.sub(
            rf'^\s*ALTER\s+EXTENSION\s+{re.escape(ext)}\b.*?;\s*$',
            '', txt, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL
        )

    txt = re.sub(r'\n{3,}', '\n\n', txt)
    dump_path.write_text(txt, encoding="utf-8")
    print(f"OK: dump sanitizado (extensões removidas): {', '.join(extensions_to_skip)}")


def sanitize_dump_remove_incompatible_settings(dump_path: Path) -> None:
    txt = dump_path.read_text(encoding="utf-8", errors="replace")

    for setting in INCOMPATIBLE_SETTINGS:
        txt = re.sub(
            rf'^\s*SET\s+{re.escape(setting)}\s*=\s*.*?;\s*$',
            '', txt, flags=re.IGNORECASE | re.MULTILINE
        )

    txt = re.sub(r'\n{3,}', '\n\n', txt)
    dump_path.write_text(txt, encoding="utf-8")
    print(f"OK: removidos SET incompatíveis: {', '.join(INCOMPATIBLE_SETTINGS)}")


def run_cmd(cmd: list[str], env: dict | None = None) -> None:
    print(">>", " ".join(cmd))
    p = subprocess.run(cmd, env=env, text=True, capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(
            f"Falha no comando:\n{' '.join(cmd)}\n\nSTDOUT:\n{p.stdout}\n\nSTDERR:\n{p.stderr}"
        )


def quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def quote_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def psql_exec(sql: str) -> None:
    """Executa SQL no LOCAL_ADMIN_DB (postgres)."""
    env = os.environ.copy()
    env["PGPASSWORD"] = LOCAL_ADMIN_PASS

    cmd = [
        PSQL,
        "-h", LOCAL_HOST,
        "-p", str(LOCAL_PORT),
        "-U", LOCAL_ADMIN_USER,
        "-d", LOCAL_ADMIN_DB,
        "-v", "ON_ERROR_STOP=1",
        "-c", sql,
    ]
    run_cmd(cmd, env=env)


def database_exists(dbname: str) -> bool:
    env = os.environ.copy()
    env["PGPASSWORD"] = LOCAL_ADMIN_PASS

    cmd = [
        PSQL,
        "-h", LOCAL_HOST,
        "-p", str(LOCAL_PORT),
        "-U", LOCAL_ADMIN_USER,
        "-d", LOCAL_ADMIN_DB,
        "-t", "-A",
        "-v", "ON_ERROR_STOP=1",
        "-c", f"SELECT 1 FROM pg_database WHERE datname = {quote_literal(dbname)};",
    ]
    p = subprocess.run(cmd, env=env, text=True, capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"Erro checando existência do DB.\nSTDERR:\n{p.stderr}")
    return p.stdout.strip() == "1"


def drop_database(dbname: str) -> None:
    terminate_sql = f"""
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = {quote_literal(dbname)}
      AND pid <> pg_backend_pid();
    """
    psql_exec(terminate_sql)
    psql_exec(f"DROP DATABASE IF EXISTS {quote_ident(dbname)};")


def create_database(dbname: str) -> None:
    psql_exec(f"CREATE DATABASE {quote_ident(dbname)};")
    # Cria extensões necessárias no banco recém-criado
    psql_exec_on(dbname, 'CREATE EXTENSION IF NOT EXISTS dblink;')
    psql_exec_on(dbname, 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')


def psql_exec_on(dbname: str, sql: str) -> None:
    """Executa SQL em um banco específico."""
    env = os.environ.copy()
    env["PGPASSWORD"] = LOCAL_ADMIN_PASS

    cmd = [
        PSQL,
        "-h", LOCAL_HOST,
        "-p", str(LOCAL_PORT),
        "-U", LOCAL_ADMIN_USER,
        "-d", dbname,
        "-v", "ON_ERROR_STOP=1",
        "-c", sql,
    ]
    run_cmd(cmd, env=env)



def detectar_tabelas_sem_permissao() -> list[str]:
    """
    Conecta em produção via psycopg2 e testa SELECT 1 em cada tabela
    do schema public. Retorna a lista de tabelas onde o usuário não
    tem permissão de leitura.
    """
    print("Verificando permissões em produção...")

    conn = psycopg2.connect(
        host=PROD_HOST, port=PROD_PORT,
        dbname=PROD_DB, user=PROD_USER, password=PROD_PASS,
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Lista todas as tabelas do schema public
    cur.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename
    """)
    todas = [row[0] for row in cur.fetchall()]

    sem_permissao = []
    for tabela in todas:
        try:
            cur.execute(
                sql.SQL("SELECT 1 FROM public.{} LIMIT 1").format(sql.Identifier(tabela))
            )
        except psycopg2.errors.InsufficientPrivilege:
            sem_permissao.append(tabela)
            conn.rollback()  # limpa o estado de erro da conexão
        except psycopg2.Error as exc:
            conn.rollback()
            raise RuntimeError(
                f"Erro inesperado ao validar permissões da tabela public.{tabela}: {exc}"
            ) from exc

    cur.close()
    conn.close()

    if sem_permissao:
        print(f"  ⚠️  {len(sem_permissao)} tabela(s) sem permissão — serão excluídas do dump:")
        for t in sem_permissao:
            print(f"     - {t}")
    else:
        print("  ✅ Permissão de leitura confirmada em todas as tabelas.")

    return sem_permissao


def dump_schema_only(excluir_tabelas: list[str] | None = None) -> None:
    """
    Gera dump SOMENTE do schema (sem CREATE DATABASE).
    Tabelas em excluir_tabelas são passadas via --exclude-table ao pg_dump.
    """
    env = os.environ.copy()
    env["PGPASSWORD"] = PROD_PASS

    cmd = [
        PG_DUMP,
        "-h", PROD_HOST,
        "-p", str(PROD_PORT),
        "-U", PROD_USER,
        "-d", PROD_DB,
        "--schema-only",
        "--no-owner",
        "--no-acl",
        "--verbose",
        "-f", str(DUMP_FILE),
    ]

    # Exclui tabelas sem permissão para evitar erro de LOCK TABLE
    for tabela in (excluir_tabelas or []):
        cmd += ["--exclude-table", f"public.{tabela}"]

    run_cmd(cmd, env=env)

    # sanitize_dump_remove_extensions(DUMP_FILE, EXTENSIONS_TO_SKIP)
    sanitize_dump_remove_incompatible_settings(DUMP_FILE)

    print(f"OK: dump gerado em {DUMP_FILE}")


def restore_schema_to_target_db(excluir_tabelas: list[str] | None = None) -> None:
    """
    Restaura o schema conectando direto no TARGET_DB.
    Quando houve exclusão de tabelas no dump, o restore roda sem ON_ERROR_STOP
    para não interromper em objetos dependentes dessas tabelas.
    """
    env = os.environ.copy()
    env["PGPASSWORD"] = LOCAL_ADMIN_PASS
    modo_tolerante = bool(excluir_tabelas)
    on_error_stop = "0" if modo_tolerante else "1"

    cmd = [
        PSQL,
        "-h", LOCAL_HOST,
        "-p", str(LOCAL_PORT),
        "-U", LOCAL_ADMIN_USER,
        "-d", TARGET_DB,
        "-v", f"ON_ERROR_STOP={on_error_stop}",
        "-f", str(DUMP_FILE),
    ]
    p = subprocess.run(cmd, env=env, text=True, capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(
            f"Falha no comando:\n{' '.join(cmd)}\n\nSTDOUT:\n{p.stdout}\n\nSTDERR:\n{p.stderr}"
        )
    if modo_tolerante and "ERROR:" in p.stderr:
        total_erros = p.stderr.count("ERROR:")
        print(
            f"AVISO: restore concluído com {total_erros} erro(s) de objetos "
            "dependentes de tabelas excluídas por falta de permissão."
        )
    print(f"OK: schema restaurado no DB {TARGET_DB}")


def remove_dump_file() -> None:
    if DUMP_FILE.exists():
        DUMP_FILE.unlink()
        print(f"OK: arquivo de dump removido: {DUMP_FILE}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extrai schema de produção e restaura no banco local."
    )
    parser.add_argument(
        "--keep-dump",
        action="store_true",
        help="Não remove o arquivo de dump ao final (padrão: remover).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Valida se os binários existem antes de começar
    for bin_path in [PSQL, PG_DUMP]:
        if not Path(bin_path).exists():
            raise FileNotFoundError(
                f"Binário não encontrado: {bin_path}\n"
                f"Ajuste a variável PG_BIN no topo do script."
            )

    if database_exists(TARGET_DB):
        print(f"DB '{TARGET_DB}' já existe. Dropando...")
        drop_database(TARGET_DB)

    print(f"Criando DB '{TARGET_DB}' no local...")
    create_database(TARGET_DB)

    print("Extraindo schema da produção...")
    sem_permissao = detectar_tabelas_sem_permissao()
    dump_schema_only(excluir_tabelas=sem_permissao)

    print("Restaurando schema no banco local...")
    restore_schema_to_target_db(excluir_tabelas=sem_permissao)

    if args.keep_dump:
        print(f"OK: mantendo arquivo de dump: {DUMP_FILE}")
    else:
        remove_dump_file()

    print("Concluído ✅")


if __name__ == "__main__":
    main()
