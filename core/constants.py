from pathlib import Path

# ── Arquivos de configuração e credenciais ───────────────────────────────────
SCOPES         = ["https://www.googleapis.com/auth/gmail.send"]
TOKEN_FILE     = Path("token.json")
CREDS_FILE     = Path("credentials.json")
SIGNATURE_IMG  = Path("assinatura.png")
KEY_FILE       = Path(".secret.key")

# ── Arquivos de dados ────────────────────────────────────────────────────────
BASE_OUTPUT    = Path("Holerites")
EMPLOYEES_FILE = Path("funcionarios.json")
CONFIG_FILE    = Path("config.json")

# ── Mapeamentos de meses ─────────────────────────────────────────────────────
MONTHS_PT = {
    "01": "Janeiro",  "02": "Fevereiro", "03": "Marco",    "04": "Abril",
    "05": "Maio",     "06": "Junho",     "07": "Julho",    "08": "Agosto",
    "09": "Setembro", "10": "Outubro",   "11": "Novembro", "12": "Dezembro",
}

MONTHS_PT_DISPLAY = {
    "01": "Janeiro",  "02": "Fevereiro", "03": "Março",    "04": "Abril",
    "05": "Maio",     "06": "Junho",     "07": "Julho",    "08": "Agosto",
    "09": "Setembro", "10": "Outubro",   "11": "Novembro", "12": "Dezembro",
}

MONTHS_PARSE = {
    "janeiro": "01", "fevereiro": "02", "marco": "03", "março": "03",
    "abril": "04", "maio": "05", "junho": "06", "julho": "07",
    "agosto": "08", "setembro": "09", "outubro": "10",
    "novembro": "11", "dezembro": "12",
}