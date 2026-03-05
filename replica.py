"""
replica.py
----------
Executa o ambiente de testes de forma sequencial:

  1. base_testes_schema.py - recria a estrutura do banco dev a partir de prod
  2. base_testes_replicar_dados_parquet.py - replica os dados de prod para dev via Parquet

Uso:
    python3 replica.py
    python3 replica.py --apenas-schema
    python3 replica.py --apenas-dados
    python3 replica.py --dry-run
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

SCHEMA = SCRIPTS_DIR / "base_testes_schema.py"
DADOS = SCRIPTS_DIR / "base_testes_replicar_dados_parquet.py"


def separador(titulo: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}\n")


def executar(script: Path, args_extras: list[str] | None = None) -> None:
    args_extras = args_extras or []
    cmd = [sys.executable, str(script)] + args_extras
    print(f">> {' '.join(cmd)}\n")

    resultado = subprocess.run(cmd)

    if resultado.returncode != 0:
        print(f"\nFalha em {script.name} (codigo {resultado.returncode}). Abortando.")
        sys.exit(resultado.returncode)

    print(f"\nOK {script.name} concluido com sucesso.")


def replica():
    parser = argparse.ArgumentParser(description="Executa schema + replicacao de dados sequencialmente.")
    grupo_execucao = parser.add_mutually_exclusive_group()
    grupo_execucao.add_argument("--apenas-schema", action="store_true", help="Executa apenas o schema")
    grupo_execucao.add_argument("--apenas-dados", action="store_true", help="Executa apenas a replicacao de dados")
    parser.add_argument("--dry-run", action="store_true", help="Passa --dry-run para o script de dados")
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Numero de workers paralelos para o script de dados (se omitido, usa o default do script de dados)",
    )
    args = parser.parse_args()

    args_dados = []
    if args.dry_run:
        args_dados.append("--dry-run")
    if args.workers is not None:
        args_dados += ["--workers", str(args.workers)]

    for script in [SCHEMA, DADOS]:
        if not script.exists():
            print(f"Script nao encontrado: {script}")
            sys.exit(1)

    print("=" * 60)
    print("  AMBIENTE DE TESTES - SETUP COMPLETO")
    print("=" * 60)

    if not args.apenas_dados:
        separador("ETAPA 1/2 - Estrutura do banco (schema)")
        executar(SCHEMA)

    if not args.apenas_schema:
        separador("ETAPA 2/2 - Replicacao de dados")
        executar(DADOS, args_dados)

    print(f"\n{'=' * 60}")
    print("  SETUP CONCLUIDO")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    replica()
