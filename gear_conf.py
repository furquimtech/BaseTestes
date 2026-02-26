"""
gerar_conf.py
-------------
Gera o arquivo tabelas.conf automaticamente conectando ao banco de produção.

Etapas:
  1. Executa o SELECT para obter tabelas e seus filtros
  2. Carrega todas as foreign keys entre as tabelas selecionadas
  3. Ordena topologicamente (dependências primeiro via Kahn's algorithm)
  4. Grava o tabelas.conf ordenado

Uso:
    python3 gerar_conf.py
    python3 gerar_conf.py --output outro_arquivo.conf
    python3 gerar_conf.py --dry-run   # exibe no terminal sem gravar
"""

import os
import argparse
from collections import defaultdict, deque
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# =============================================================
# CARREGA CREDENCIAIS DO .env
# =============================================================
_env_path = Path(__file__).parent / ".env"
if not _env_path.exists():
    _env_path = Path(__file__).parent.parent / ".env"
if not _env_path.exists():
    raise FileNotFoundError(
        "Arquivo .env não encontrado. Crie-o a partir do .env.example."
    )
load_dotenv(_env_path)

PROD = dict(
    host     = os.environ["PROD_HOST"],
    port     = int(os.environ.get("PROD_PORT", 5432)),
    dbname   = os.environ["PROD_DB"],
    user     = os.environ["PROD_USER"],
    password = os.environ["PROD_PASS"],
)

# =============================================================
# SQL BASE — mesma lógica do SELECT fornecido
# =============================================================
SQL_TABELAS = """
SELECT
    table_name,
    table_name ||
    CASE
        WHEN table_name = 'cbfollowup'    THEN ' | data_dat    | 365 | 500'
        WHEN table_name = 'cbitembordero' THEN ' | emissao_dat | 365 | 500'
        WHEN table_name = 'cbbordero'     THEN ' | data_dat    | 365 | 500'
        WHEN table_name LIKE 'cb%'        THEN ' |  |  | 100'
        WHEN table_name LIKE 'geql%'      THEN ' |  |  | 100'
        ELSE                                   ' |  |  | 500'
    END AS conf
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog', 'information_schema')
  AND (
        table_name LIKE 'ge%' OR
        table_name LIKE 'fi%' OR
        table_name LIKE 'cb%'
      )
ORDER BY table_schema, table_name;
"""

# =============================================================
# BUSCA FOREIGN KEYS entre as tabelas selecionadas
# =============================================================
SQL_FKS = """
SELECT
    kcu.table_name      AS tabela_origem,
    ccu.table_name      AS tabela_destino
FROM information_schema.table_constraints       AS tc
JOIN information_schema.key_column_usage        AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema   = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema   = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema NOT IN ('pg_catalog', 'information_schema')
  AND kcu.table_name  IN %s
  AND ccu.table_name  IN %s
  AND kcu.table_name != ccu.table_name
"""

# =============================================================
# ORDENAÇÃO TOPOLÓGICA (Kahn's Algorithm)
# =============================================================
def ordenar_topologicamente(tabelas: list, fks: list) -> list:
    """
    Ordena tabelas de forma que as dependências venham primeiro.

    fks = lista de (tabela_origem, tabela_destino)
    onde tabela_destino deve ser inserida ANTES de tabela_origem.

    Usa o algoritmo de Kahn para detecção de ciclos e ordenação.
    """
    tabelas_set  = set(tabelas)
    grafo        = defaultdict(set)  # grafo[dep] = tabelas que dependem de dep
    in_degree    = defaultdict(int)  # nº de dependências de cada tabela

    for origem, destino in fks:
        if origem in tabelas_set and destino in tabelas_set:
            grafo[destino].add(origem)
            in_degree[origem] += 1

    # Fila inicial: tabelas sem dependências
    fila      = deque(sorted([t for t in tabelas if in_degree[t] == 0]))
    ordenadas = []

    while fila:
        tabela = fila.popleft()
        ordenadas.append(tabela)

        for dependente in sorted(grafo[tabela]):
            in_degree[dependente] -= 1
            if in_degree[dependente] == 0:
                fila.append(dependente)

    # Tabelas em ciclo — não resolvidas pelo algoritmo
    nao_resolvidas = [t for t in tabelas if t not in set(ordenadas)]
    if nao_resolvidas:
        print(f"\n[AVISO] {len(nao_resolvidas)} tabela(s) com ciclo de FK — adicionadas ao final:")
        for t in sorted(nao_resolvidas):
            print(f"  - {t}")
        ordenadas.extend(sorted(nao_resolvidas))

    return ordenadas


# =============================================================
# MAIN
# =============================================================
def main():
    parser = argparse.ArgumentParser(description="Gera tabelas.conf com ordenação por FK.")
    default_output = Path(__file__).parent / "tabelas.conf"
    parser.add_argument("--output",  default=str(default_output), help="Caminho do arquivo de saída")
    parser.add_argument("--dry-run", action="store_true",          help="Exibe no terminal sem gravar")
    args = parser.parse_args()

    print(f"Conectando em {PROD['host']}/{PROD['dbname']}...")

    with psycopg2.connect(**PROD) as conn:
        conn.autocommit = True

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            # 1) Busca tabelas e filtros
            cur.execute(SQL_TABELAS)
            rows = cur.fetchall()

            if not rows:
                print("Nenhuma tabela encontrada com os filtros configurados.")
                return

            tabelas  = [r["table_name"] for r in rows]
            conf_map = {r["table_name"]: r["conf"] for r in rows}

            print(f"\n{len(tabelas)} tabela(s) encontrada(s).")

            # 2) Busca foreign keys entre as tabelas selecionadas
            tabelas_tup = tuple(tabelas)
            cur.execute(SQL_FKS, (tabelas_tup, tabelas_tup))
            fks = [(r["tabela_origem"], r["tabela_destino"]) for r in cur.fetchall()]

            print(f"{len(fks)} FK(s) encontrada(s) entre as tabelas selecionadas.")

    # 3) Ordena topologicamente
    print("\nOrdenando tabelas por dependência de FK...")
    tabelas_ordenadas = ordenar_topologicamente(tabelas, fks)

    # 4) Monta conteúdo do conf
    linhas = [
        "# =============================================================",
        "# tabelas.conf — gerado automaticamente por gerar_conf.py",
        "# Formato: tabela | coluna_data | dias | limit",
        "# =============================================================",
        "",
    ]
    for tabela in tabelas_ordenadas:
        linhas.append(conf_map[tabela])

    conteudo = "\n".join(linhas) + "\n"

    # 5) Exibe ou grava
    if args.dry_run:
        print(f"\n{'─'*60}")
        print(conteudo)
        print(f"{'─'*60}")
        print("Modo --dry-run: arquivo não gravado.")
    else:
        output = Path(args.output)
        output.write_text(conteudo, encoding="utf-8")
        print(f"\n✔ Arquivo gerado: {output}")
        print(f"  Tabelas ordenadas: {len(tabelas_ordenadas)}")

if __name__ == "__main__":
    main()