import argparse
import datetime as dt
import hashlib
import os
import random
import re
from pathlib import Path


def _mascarar_palavra(palavra: str) -> str:
    if len(palavra) == 1:
        return "*"
    if len(palavra) == 2:
        return palavra[0] + "*"
    return palavra[0] + ("*" * (len(palavra) - 2)) + palavra[-1]


def mascarar_nome(valor, manter_primeira_palavra: bool = False):
    if valor is None or not isinstance(valor, str):
        return valor

    if not manter_primeira_palavra:
        return re.sub(r"[A-Za-zÀ-ÿ]+", lambda m: _mascarar_palavra(m.group(0)), valor)

    partes = re.split(r"(\s+)", valor)
    primeira_encontrada = False
    resultado = []
    for parte in partes:
        if not parte or parte.isspace():
            resultado.append(parte)
            continue
        if re.search(r"[A-Za-zÀ-ÿ]", parte):
            if not primeira_encontrada:
                resultado.append(parte)
                primeira_encontrada = True
            else:
                resultado.append(re.sub(r"[A-Za-zÀ-ÿ]+", lambda m: _mascarar_palavra(m.group(0)), parte))
        else:
            resultado.append(parte)
    return "".join(resultado)


def mascarar_documento(valor):
    if valor is None:
        return valor
    texto = str(valor)
    return "".join("0" if ch.isdigit() else "X" if ch.isalpha() else ch for ch in texto)


def _cpf_dv(cpf9: str) -> str:
    nums = [int(c) for c in cpf9]
    soma1 = sum(n * w for n, w in zip(nums, range(10, 1, -1)))
    d1 = (soma1 * 10) % 11
    d1 = 0 if d1 == 10 else d1

    soma2 = sum(n * w for n, w in zip(nums + [d1], range(11, 1, -1)))
    d2 = (soma2 * 10) % 11
    d2 = 0 if d2 == 10 else d2
    return f"{d1}{d2}"


def mascarar_cpf(valor):
    if valor is None:
        return valor

    if isinstance(valor, bool):
        return valor

    original = str(valor).strip()
    if not original:
        return valor

    digitos = re.sub(r"\D", "", original)
    if len(digitos) != 11:
        return valor

    h = hashlib.sha256(digitos.encode("utf-8")).hexdigest()
    base9 = str(int(h[:16], 16) % 1_000_000_000).zfill(9)
    cpf = base9 + _cpf_dv(base9)

    if re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", original):
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf


def mascarar_rg(valor):
    if valor is None:
        return valor
    if isinstance(valor, bool):
        return valor

    original = str(valor)
    if not original.strip():
        return valor

    alnum = re.sub(r"[^0-9A-Za-z]", "", original).upper()
    if len(alnum) < 5:
        return valor

    h = hashlib.sha256(alnum.encode("utf-8")).hexdigest()
    base_num = int(h, 16)

    chars = []
    for i, ch in enumerate(original):
        if ch.isdigit():
            chars.append(str((base_num >> (i % 64)) % 10))
        elif ch.isalpha():
            chars.append(chr(ord("A") + ((base_num >> (i % 64)) % 26)))
        else:
            chars.append(ch)
    return "".join(chars)


def mascarar_telefone(valor):
    if valor is None:
        return valor
    if isinstance(valor, bool):
        return valor

    original = str(valor)
    if not original.strip():
        return valor

    rng = random.SystemRandom()
    chars = []
    for ch in original:
        if ch.isdigit():
            chars.append(str(rng.randrange(10)))
        elif ch.isalpha():
            chars.append(chr(ord("A") + rng.randrange(26)))
        else:
            chars.append(ch)
    return "".join(chars)


def coluna_parece_rg(coluna: str) -> bool:
    c = coluna.lower()
    return bool(
        c.startswith("rg")
        or c.endswith("_rg")
        or "_rg_" in c
        or re.search(r"(^|[^a-z0-9])rg([^a-z0-9]|$)", c)
    )


def mascarar_registro_sensivel(registro: dict) -> dict:
    mascarado = dict(registro)
    for coluna, valor in mascarado.items():
        c = coluna.lower()
        if "cpf" in c:
            mascarado[coluna] = mascarar_cpf(valor)
        elif coluna_parece_rg(c):
            mascarado[coluna] = mascarar_rg(valor)
        elif "logradouro" in c:
            mascarado[coluna] = mascarar_nome(valor)
        elif "endereco" in c:
            mascarado[coluna] = mascarar_nome(valor, manter_primeira_palavra=True)
        elif "telefone" in c:
            mascarado[coluna] = mascarar_telefone(valor)
        elif "avalista" in c:
            mascarado[coluna] = mascarar_nome(valor, manter_primeira_palavra=True)
        elif "mae" in c or "mãe" in c:
            mascarado[coluna] = mascarar_nome(valor, manter_primeira_palavra=True)
        elif "pai" in c:
            mascarado[coluna] = mascarar_nome(valor, manter_primeira_palavra=True)
        elif "nome" in c:
            mascarado[coluna] = mascarar_nome(valor, manter_primeira_palavra=True)
    return mascarado


def int_positivo(valor: str) -> int:
    try:
        inteiro = int(valor)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Valor inválido: {valor}") from exc
    if inteiro <= 0:
        raise argparse.ArgumentTypeError(f"Valor deve ser > 0: {valor}")
    return inteiro


def encontrar_env() -> Path:
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


def conexoes_env() -> tuple[dict, dict]:
    prod = dict(
        host=os.environ["PROD_HOST"],
        port=int(os.environ.get("PROD_PORT", 5432)),
        dbname=os.environ["PROD_DB"],
        user=os.environ["PROD_USER"],
        password=os.environ["PROD_PASS"],
    )
    dev = dict(
        host=os.environ.get("DEV_HOST", "localhost"),
        port=int(os.environ.get("DEV_PORT", 5432)),
        dbname=os.environ["DEV_DB"],
        user=os.environ["DEV_USER"],
        password=os.environ["DEV_PASS"],
    )
    return prod, dev


def ler_config_tabelas(path: Path) -> list[dict]:
    items, _ = ler_config_tabelas_e_workers(path)
    return items


def ler_config_tabelas_e_workers(path: Path) -> tuple[list[dict], int | None]:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuracao nao encontrado: {path}")

    items = []
    workers = None
    for numero, linha in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue

        partes = [p.strip() for p in linha.split("|")]
        if partes and partes[0] == "@workers":
            if len(partes) != 2:
                raise ValueError(f"Linha {numero}: '@workers' requer '@workers | N'.")
            try:
                workers = int(partes[1])
            except ValueError as exc:
                raise ValueError(f"Linha {numero}: '@workers' deve ser inteiro.") from exc
            if workers <= 0:
                raise ValueError(f"Linha {numero}: '@workers' deve ser > 0.")
            continue

        # Compatibilidade com diretiva de mapeamento usada por outros scripts.
        if partes and partes[0] == "@mapa":
            continue

        if len(partes) > 4:
            raise ValueError(f"Linha {numero} invalida: '{linha}'")

        while len(partes) < 4:
            partes.append("")

        tabela, coluna_data, dias, limit = partes

        if bool(coluna_data) != bool(dias):
            raise ValueError(f"Linha {numero}: 'coluna_data' e 'dias' devem ser preenchidos juntos.")

        try:
            dias_int = int(dias) if dias else None
        except ValueError as exc:
            raise ValueError(f"Linha {numero}: 'dias' deve ser inteiro.") from exc
        if dias_int is not None and dias_int < 0:
            raise ValueError(f"Linha {numero}: 'dias' deve ser >= 0.")

        try:
            limit_int = int(limit) if limit else None
        except ValueError as exc:
            raise ValueError(f"Linha {numero}: 'limit' deve ser inteiro.") from exc
        if limit_int is not None and limit_int <= 0:
            raise ValueError(f"Linha {numero}: 'limit' deve ser > 0.")

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
    return items, workers


def qname(schema: str, tabela: str) -> str:
    return f"{schema}.{tabela}"


def pk_de(tabela: str) -> str:
    return f"id_{tabela}_int"


def tabela_existe(cur, schema: str, tabela: str) -> bool:
    cur.execute("SELECT to_regclass(%s) AS oid", (qname(schema, tabela),))
    row = cur.fetchone()
    return row is not None and row["oid"] is not None


def colunas_de(cur, schema: str, tabela: str) -> list[str]:
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
        """,
        (schema, tabela),
    )
    cols = []
    for r in cur.fetchall():
        if isinstance(r, dict):
            cols.append(r["column_name"])
        else:
            cols.append(r[0])
    return cols


RE_COLUNA_DEP = re.compile(r"^id_([a-z0-9]+)_int$", re.IGNORECASE)


def dependencias_de(cur, schema: str, tabela: str, cache_colunas: dict, dependencia_ignorar: set[str] | None = None) -> list[tuple[str, str]]:
    ignorar = dependencia_ignorar or set()

    if tabela not in cache_colunas:
        cache_colunas[tabela] = colunas_de(cur, schema, tabela)

    deps = []
    for col in cache_colunas[tabela]:
        match = RE_COLUNA_DEP.match(col)
        if not match:
            continue

        tabela_ref = match.group(1).lower()
        if tabela_ref == tabela.lower():
            continue
        if tabela_ref in ignorar:
            continue
        if tabela_existe(cur, schema, tabela_ref):
            deps.append((col, tabela_ref))
    return deps


def buscar_registros(
    cur,
    schema: str,
    tabela: str,
    coluna_data: str | None,
    dias: int | None,
    limit: int | None,
    pk_coluna: str | None = None,
) -> list[dict]:
    sql = f"SELECT * FROM {qname(schema, tabela)}"
    params = []

    if coluna_data and dias is not None:
        cutoff = dt.date.today() - dt.timedelta(days=dias)
        sql += f" WHERE {coluna_data} >= %s"
        params.append(cutoff)

    sql += f" ORDER BY {pk_coluna or pk_de(tabela)} DESC"

    if limit is not None:
        sql += " LIMIT %s"
        params.append(limit)

    cur.execute(sql, params)
    return cur.fetchall()


def buscar_por_pk(cur, schema: str, tabela: str, pk_valor, pk_coluna: str | None = None) -> dict | None:
    pk = pk_coluna or pk_de(tabela)
    cur.execute(f"SELECT * FROM {qname(schema, tabela)} WHERE {pk} = %s", (pk_valor,))
    return cur.fetchone()
