import re


def short_name(full_name: str) -> str:
    """Primeiro + Último nome para a pasta. Ex: 'Gustavo Felizardo'"""
    parts = full_name.strip().title().split()
    if len(parts) >= 2:
        return f"{parts[0]} {parts[-1]}"
    return parts[0] if parts else full_name.title()


def full_name_title(full_name: str) -> str:
    return full_name.strip().title()


def safe_str(s: str) -> str:
    """Remove caracteres inválidos para nomes de arquivo/pasta no Windows."""
    return re.sub(r'[\\/:*?"<>|]', "", s).strip()