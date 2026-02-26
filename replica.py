"""
replica.py
-------
Executa o ambiente de testes de forma sequencial:

  1. base_testes_schema.py   — recria a estrutura do banco dev a partir de prod
  2. replicar_dados_semcopy.py — replica os dados de prod para dev via INSERT

Uso:
    python3 replica.py
    python3 replica.py --apenas-schema
    python3 replica.py --apenas-dados
    python3 replica.py --dry-run
"""

import subprocess
import sys
import argparse
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

SCHEMA  = SCRIPTS_DIR / "base_testes_schema.py"
DADOS   = SCRIPTS_DIR / "base_testes_replicar_dados_semcopy.py"

def separador(titulo: str) -> None:
    print(f"\n{'═'*60}")
    print(f"  {titulo}")
    print(f"{'═'*60}\n")

def executar(script: Path, args_extras: list[str] = []) -> None:
    cmd = [sys.executable, str(script)] + args_extras
    print(f">> {' '.join(cmd)}\n")

    resultado = subprocess.run(cmd)

    if resultado.returncode != 0:
        print(f"\n✖ Falha em {script.name} (código {resultado.returncode}). Abortando.")
        sys.exit(resultado.returncode)

    print(f"\n✔ {script.name} concluído com sucesso.")

def replica():
    parser = argparse.ArgumentParser(description="Executa schema + replicação de dados sequencialmente.")
    parser.add_argument("--apenas-schema", action="store_true", help="Executa apenas o schema")
    parser.add_argument("--apenas-dados",  action="store_true", help="Executa apenas a replicação de dados")
    parser.add_argument("--dry-run",       action="store_true", help="Passa --dry-run para o script de dados")
    parser.add_argument("--workers",       type=int, default=5, help="Número de workers paralelos para o script de dados")
    args = parser.parse_args()

    args_dados = []
    if args.dry_run:
        args_dados.append("--dry-run")
    if args.workers:
        args_dados += ["--workers", str(args.workers)]

    # Valida que os scripts existem
    for script in [SCHEMA, DADOS]:
        if not script.exists():
            print(f"✖ Script não encontrado: {script}")
            sys.exit(1)

    print("╔══════════════════════════════════════════════════════╗")
    print("║         AMBIENTE DE TESTES — SETUP COMPLETO          ║")
    print("╚══════════════════════════════════════════════════════╝")

    # Etapa 1: Schema
    if not args.apenas_dados:
        separador("ETAPA 1/2 — Estrutura do banco (schema)")
        executar(SCHEMA)

    # Etapa 2: Dados
    if not args.apenas_schema:
        separador("ETAPA 2/2 — Replicação de dados")
        executar(DADOS, args_dados)

    print(f"\n{'═'*60}")
    print("  SETUP CONCLUÍDO ✅")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    replica()