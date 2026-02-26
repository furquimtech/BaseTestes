import re
import os
import subprocess
from pathlib import Path
from datetime import datetime

# =========================
# CONFIG (variáveis locais)
# =========================

import platform

# Binários do PostgreSQL — detecta automaticamente Windows ou Linux
if platform.system() == "Windows":
    PG_BIN  = r"C:\Program Files\PostgreSQL\15\bin"
    PSQL    = str(Path(PG_BIN) / "psql.exe")
    PG_DUMP = str(Path(PG_BIN) / "pg_dump.exe")
else:
    PSQL    = "/usr/bin/psql"
    PG_DUMP = "/usr/bin/pg_dump"

# PRODUÇÃO (origem)
PROD_HOST = "10.80.91.30"
PROD_PORT = 5432
PROD_DB   = "10.50.13.22_eleva"
PROD_USER = "mrfamos"
PROD_PASS = "Mikael1811!"

# LOCAL/HML (destino)
LOCAL_HOST       = "localhost"
LOCAL_PORT       = 5432
LOCAL_ADMIN_DB   = "postgres"
LOCAL_ADMIN_USER = "postgres"
LOCAL_ADMIN_PASS = "f5vcn32k"

TARGET_DB = "10.50.13.22_eleva_teste"   # database que será recriado no local

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
        "-c", f"SELECT 1 FROM pg_database WHERE datname = '{dbname}';",
    ]
    p = subprocess.run(cmd, env=env, text=True, capture_output=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"Erro checando existência do DB.\nSTDERR:\n{p.stderr}")
    return p.stdout.strip() == "1"


def drop_database(dbname: str) -> None:
    terminate_sql = f"""
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = '{dbname}'
      AND pid <> pg_backend_pid();
    """
    psql_exec(terminate_sql)
    psql_exec(f'DROP DATABASE IF EXISTS "{dbname}";')


def create_database(dbname: str) -> None:
    psql_exec(f'CREATE DATABASE "{dbname}";')
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


def dump_schema_only() -> None:
    """Gera dump SOMENTE do schema (sem CREATE DATABASE)."""
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
    run_cmd(cmd, env=env)

    # sanitize_dump_remove_extensions(DUMP_FILE, EXTENSIONS_TO_SKIP)
    sanitize_dump_remove_incompatible_settings(DUMP_FILE)

    print(f"OK: dump gerado em {DUMP_FILE}")


def restore_schema_to_target_db() -> None:
    """Restaura o schema conectando direto no TARGET_DB."""
    env = os.environ.copy()
    env["PGPASSWORD"] = LOCAL_ADMIN_PASS

    cmd = [
        PSQL,
        "-h", LOCAL_HOST,
        "-p", str(LOCAL_PORT),
        "-U", LOCAL_ADMIN_USER,
        "-d", TARGET_DB,
        "-v", "ON_ERROR_STOP=1",
        "-f", str(DUMP_FILE),
    ]
    run_cmd(cmd, env=env)
    print(f"OK: schema restaurado no DB {TARGET_DB}")


def main():
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
    dump_schema_only()

    print("Restaurando schema no banco local...")
    restore_schema_to_target_db()

    print("Concluído ✅")


if __name__ == "__main__":
    main()