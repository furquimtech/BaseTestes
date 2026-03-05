import argparse
import hashlib
import random
import re


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
