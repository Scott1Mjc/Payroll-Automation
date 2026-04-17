from pathlib import Path
from core.constants import TOKEN_FILE, CREDS_FILE, SCOPES, SIGNATURE_IMG


def get_gmail_credentials():
    """Retorna credenciais OAuth2. Na primeira vez abre navegador para autorização."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow  = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    return creds


def send_email_gmail(
    to_email: str,
    pdf_path: str,
    subject: str,
    body: str,
    sender_email: str,
    signature_mode: str = "image",
    signature_html: str = "",
) -> tuple[bool, str]:
    """Envia e-mail via Gmail API com OAuth2."""
    try:
        import base64
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email.mime.image import MIMEImage
        from email import encoders
        from googleapiclient.discovery import build

        creds   = get_gmail_credentials()
        service = build("gmail", "v1", credentials=creds)

        body_html = body.replace("\n", "<br>")
        if signature_mode == "image" and SIGNATURE_IMG.exists():
            sig_section = '<br><br>--<br><img src="cid:assinatura" style="max-width:400px">'
            has_image   = True
        elif signature_mode == "html" and signature_html.strip():
            sig_section = f"<br><br>--<br>{signature_html}"
            has_image   = False
        else:
            sig_section = ""
            has_image   = False

        html_body = f"<div style='font-family:sans-serif'><p>{body_html}</p>{sig_section}</div>"

        outer = MIMEMultipart("mixed")
        outer["From"]    = sender_email
        outer["To"]      = to_email
        outer["Subject"] = subject

        alt = MIMEMultipart("related")
        alt.attach(MIMEText(html_body, "html", "utf-8"))

        if has_image:
            with open(SIGNATURE_IMG, "rb") as img_f:
                img = MIMEImage(img_f.read())
            img.add_header("Content-ID", "<assinatura>")
            img.add_header("Content-Disposition", "inline", filename="assinatura.png")
            alt.attach(img)

        outer.attach(alt)

        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={Path(pdf_path).name}",
        )
        outer.attach(part)

        raw = base64.urlsafe_b64encode(outer.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw}).execute()

        return True, "Enviado com sucesso"
    except Exception as e:
        return False, str(e)