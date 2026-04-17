import json
from core.constants import CONFIG_FILE, EMPLOYEES_FILE
from core.crypto import encrypt_password, decrypt_password


def load_config() -> dict:
    """Carrega configurações salvas."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["app_password"] = decrypt_password(data.get("app_password_enc", ""))
        return data
    return {
        "sender_email": "",
        "app_password": "",
        "signature_html": "",
        "signature_mode": "image",
    }


def save_config(data: dict):
    """Salva configurações — senha sempre criptografada."""
    to_save = {k: v for k, v in data.items() if k != "app_password"}
    to_save["app_password_enc"] = encrypt_password(data.get("app_password", ""))
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(to_save, f, ensure_ascii=False, indent=2)


def load_employees() -> dict:
    """Carrega {NOME_MAIUSCULO: email}."""
    if EMPLOYEES_FILE.exists():
        with open(EMPLOYEES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_employees(data: dict):
    with open(EMPLOYEES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)