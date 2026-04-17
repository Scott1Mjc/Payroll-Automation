from pathlib import Path
from core.constants import KEY_FILE


def get_or_create_key() -> bytes:
    """Gera ou carrega a chave de criptografia local da máquina."""
    from cryptography.fernet import Fernet

    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    # Esconde o arquivo no Windows
    try:
        import subprocess
        subprocess.run(["attrib", "+H", str(KEY_FILE)], check=False)
    except Exception:
        pass
    return key


def encrypt_password(plain: str) -> str:
    from cryptography.fernet import Fernet

    if not plain:
        return ""
    f = Fernet(get_or_create_key())
    return f.encrypt(plain.encode()).decode()


def decrypt_password(encrypted: str) -> str:
    from cryptography.fernet import Fernet

    if not encrypted:
        return ""
    try:
        f = Fernet(get_or_create_key())
        return f.decrypt(encrypted.encode()).decode()
    except Exception:
        return ""