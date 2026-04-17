import re
import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime

from core.constants import BASE_OUTPUT, MONTHS_PT, MONTHS_PARSE
from utils.string_helpers import safe_str, short_name, full_name_title


def extract_name_from_page(page: fitz.Page) -> str | None:
    """
    Extrai o nome completo do funcionário da página.
    No layout real, o nome aparece NA LINHA ANTERIOR ao rótulo
    'Nome do Funcionário', não depois.
    """
    text  = page.get_text("text")
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    IGNORAR = {"HONOR AUTOMATION LTDA", "HONOR AUTOMATION", "LTDA", "S.A.", "EIRELI"}

    # Estratégia 1: pega a linha ANTERIOR ao rótulo "Nome do Funcionário"
    for i, line in enumerate(lines):
        if re.search(r"nome\s+do\s+funcion", line, re.IGNORECASE):
            for candidate in reversed(lines[max(0, i - 5): i]):
                if candidate.upper() in IGNORAR:
                    continue
                if re.match(r"^[A-ZÁÉÍÓÚÂÊÎÔÛÃÕÀÜÇ\s]{5,70}$", candidate):
                    return candidate.strip()
            for candidate in lines[i + 1: i + 5]:
                if candidate.upper() in IGNORAR:
                    continue
                if re.match(r"^[A-ZÁÉÍÓÚÂÊÎÔÛÃÕÀÜÇ\s]{5,70}$", candidate):
                    return candidate.strip()

    # Estratégia 2: linha em CAPS com 3+ palavras ignorando empresa
    for line in lines:
        if line.upper() in IGNORAR:
            continue
        if re.match(r"^([A-ZÁÉÍÓÚÂÊÎÔÛÃÕÀÜÇ]{2,}\s){2,}[A-ZÁÉÍÓÚÂÊÎÔÛÃÕÀÜÇ]{2,}$", line):
            return line.strip()

    return None


def extract_period_from_page(page: fitz.Page) -> tuple[str, str]:
    """Retorna (year, month_num) ex: ('2026', '02')."""
    text = page.get_text("text")
    pattern = (
        r"(janeiro|fevereiro|mar[cç]o|abril|maio|junho|"
        r"julho|agosto|setembro|outubro|novembro|dezembro)"
        r"\s+de\s+(\d{4})"
    )
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        raw   = match.group(1).lower().replace("ç", "c")
        year  = match.group(2)
        month = MONTHS_PARSE.get(raw, "01")
        return year, month

    now = datetime.now()
    return str(now.year), f"{now.month:02d}"


def extract_type_from_page(page: fitz.Page) -> str:
    """Detecta se é 'Adiantamento' ou 'Pagamento'."""
    text = page.get_text("text")
    if re.search(r"adiantamento", text, re.IGNORECASE):
        return "Adiantamento"
    return "Pagamento"


def split_pdf(pdf_bytes: bytes) -> list[dict]:
    """
    Divide o PDF em holerites individuais.
    Funcionários com múltiplas páginas no mesmo período/tipo
    são automaticamente agrupados em um único PDF.
    """
    doc    = fitz.open(stream=pdf_bytes, filetype="pdf")
    groups = {}

    for page_num in range(len(doc)):
        page        = doc[page_num]
        name        = extract_name_from_page(page)
        year, month = extract_period_from_page(page)
        htype       = extract_type_from_page(page)

        key = (name or f"FUNCIONARIO PAGINA {page_num + 1}", year, month, htype)

        if key not in groups:
            groups[key] = {
                "name":          key[0],
                "name_detected": name is not None,
                "year":          year,
                "month":         month,
                "type":          htype,
                "pages":         [],
            }
        groups[key]["pages"].append(page_num)

    results = []
    for key, group in groups.items():
        new_doc = fitz.open()
        for page_num in group["pages"]:
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        page_bytes = new_doc.tobytes()
        new_doc.close()

        n_pages = len(group["pages"])
        results.append({
            "page_num":      group["pages"][0] + 1,
            "name":          group["name"],
            "name_detected": group["name_detected"],
            "year":          group["year"],
            "month":         group["month"],
            "type":          group["type"],
            "pdf_bytes":     page_bytes,
            "total_pages":   n_pages,
        })

    doc.close()
    return results


def save_holerites(holerites: list[dict]) -> list[dict]:
    """
    Estrutura: /Holerites/2026/Fevereiro/Gustavo Felizardo/Adiantamento/
               Gustavo Henrique Camargo Felizardo.pdf
    """
    saved = []
    for h in holerites:
        month_folder = safe_str(MONTHS_PT.get(h["month"], h["month"]))
        folder_name  = safe_str(short_name(h["name"]))
        pdf_name     = safe_str(full_name_title(h["name"])) + ".pdf"

        target_dir = (
            BASE_OUTPUT
            / safe_str(h["year"])
            / month_folder
            / folder_name
            / safe_str(h["type"])
        )
        target_dir.mkdir(parents=True, exist_ok=True)
        filepath = target_dir / pdf_name

        with open(filepath, "wb") as f:
            f.write(h["pdf_bytes"])

        saved.append({
            **h,
            "filepath": str(filepath),
            "filename": pdf_name,
        })
    return saved