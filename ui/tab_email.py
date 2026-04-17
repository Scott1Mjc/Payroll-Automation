import time
import streamlit as st
import pandas as pd

from core.constants import TOKEN_FILE, CREDS_FILE, SIGNATURE_IMG, MONTHS_PT_DISPLAY
from core.storage import load_employees, load_config, save_config
from core.email_sender import get_gmail_credentials, send_email_gmail
from utils.string_helpers import full_name_title


def render_tab_email():
    st.subheader("Envio de Holerites por E-mail")

    if "holerites_saved" not in st.session_state:
        st.info("⬅️ Primeiro processe e salve os holerites na aba **1. Separar PDF**.")
        return

    saved     = st.session_state["holerites_saved"]
    employees = load_employees()
    config    = load_config()

    # ── Credenciais do remetente ──────────────────────────────────────────────
    st.markdown("### 🔑 Remetente")

    sender_email = st.text_input(
        "E-mail do remetente",
        value=config.get("sender_email", ""),
        placeholder="coordenador@empresa.com.br",
        key="sender_email",
    )

    if not CREDS_FILE.exists() or "COLE_SEU" in CREDS_FILE.read_text():
        st.error(
            "⚠️ Arquivo `credentials.json` não configurado. "
            "Edite o arquivo com seu Client ID e Client Secret."
        )
    elif TOKEN_FILE.exists():
        st.success("✅ Conta Google autorizada. Pronto para enviar.")
        if st.button("🔄 Revogar autorização", help="Remove o token salvo e pede login novamente"):
            TOKEN_FILE.unlink()
            st.rerun()
    else:
        st.warning("⚠️ Conta Google ainda não autorizada.")
        if st.button("🔐 Autorizar conta Google", type="primary"):
            try:
                get_gmail_credentials()
                st.success("✅ Autorizado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")

    # ── Assinatura ────────────────────────────────────────────────────────────
    st.markdown("### ✍️ Assinatura")
    sig_mode = st.radio(
        "Tipo de assinatura",
        options=["image", "html"],
        format_func=lambda x: "🖼️ Imagem (PNG/JPG)" if x == "image" else "💻 HTML + CSS",
        index=0 if config.get("signature_mode", "image") == "image" else 1,
        horizontal=True,
        key="sig_mode",
    )

    if sig_mode == "image":
        if SIGNATURE_IMG.exists():
            st.success(f"✅ Imagem salva: `{SIGNATURE_IMG.name}`")
            col_prev, col_del = st.columns([3, 1])
            with col_prev:
                st.image(str(SIGNATURE_IMG), width=300)
            with col_del:
                if st.button("🗑️ Remover", key="del_sig"):
                    SIGNATURE_IMG.unlink()
                    st.rerun()
        else:
            st.info("Nenhuma imagem de assinatura carregada.")

        sig_upload = st.file_uploader(
            "Upload da assinatura",
            type=["png", "jpg", "jpeg"],
            key="sig_upload",
        )
        if sig_upload:
            SIGNATURE_IMG.write_bytes(sig_upload.read())
            st.success("✅ Assinatura salva!")
            st.rerun()
        signature_html = config.get("signature_html", "")

    else:
        signature_html = st.text_area(
            "Código HTML da assinatura",
            value=config.get("signature_html", ""),
            placeholder='<table><tr><td><b>João Silva</b><br>RH - HONOR AUTOMATION</td></tr></table>',
            height=150,
            key="signature_html",
        )

    new_config = {
        "sender_email":   sender_email,
        "app_password":   "",
        "signature_mode": sig_mode,
        "signature_html": signature_html if sig_mode == "html" else config.get("signature_html", ""),
    }
    save_config(new_config)

    st.divider()

    # ── Campos editáveis de e-mail ────────────────────────────────────────────
    st.markdown("### ✏️ Mensagem do E-mail")
    st.caption("Escreva o título e o corpo que serão enviados para todos os funcionários.")

    email_subject = st.text_input(
        "Assunto",
        placeholder="Ex: Holerites de 2026",
        key="email_subject",
    )
    email_body = st.text_area(
        "Corpo da mensagem",
        placeholder=(
            "Ex:\n"
            "Olá,\n\n"
            "Segue em anexo o seu holerite.\n\n"
            "Atenciosamente,\n"
            "Departamento de Recursos Humanos"
        ),
        height=220,
        key="email_body",
    )

    st.divider()

    # ── Tabela de destinatários ───────────────────────────────────────────────
    st.markdown("### 📋 Destinatários")

    send_data = []
    for h in saved:
        email     = employees.get(h["name"].upper(), "")
        month_lbl = MONTHS_PT_DISPLAY.get(h["month"], h["month"])
        send_data.append({
            "Funcionário": full_name_title(h["name"]),
            "Tipo":        h["type"],
            "Período":     f"{month_lbl} / {h['year']}",
            "E-mail":      email or "❌ Não cadastrado",
            "Arquivo":     h["filename"],
            "filepath":    h["filepath"],
            "has_email":   bool(email),
            "email_addr":  email,
        })

    st.dataframe(
        pd.DataFrame(send_data)[["Funcionário", "Tipo", "Período", "E-mail", "Arquivo"]],
        use_container_width=True,
        hide_index=True,
    )

    ready     = sum(1 for r in send_data if r["has_email"])
    not_ready = len(send_data) - ready

    c1, c2, c3 = st.columns(3)
    c1.metric("Total",              len(send_data))
    c2.metric("Prontos para envio", ready)
    c3.metric("Sem e-mail",         not_ready)

    if not_ready > 0:
        st.warning(f"⚠️ {not_ready} holerite(s) não serão enviados por falta de e-mail cadastrado.")

    if ready == 0:
        st.error("Nenhum funcionário com e-mail cadastrado. Adicione na barra lateral.")
        return

    can_send = (
        bool(email_subject.strip())
        and bool(email_body.strip())
        and bool(sender_email.strip())
        and TOKEN_FILE.exists()
    )
    if not TOKEN_FILE.exists():
        st.warning("⚠️ Autorize a conta Google acima antes de enviar.")
    elif not can_send:
        st.warning("⚠️ Preencha o e-mail remetente, o assunto e o corpo para habilitar o envio.")

    if st.button(
        f"📧 Enviar {ready} e-mail(s)",
        type="primary",
        use_container_width=True,
        disabled=not can_send,
    ):
        progress_bar     = st.progress(0)
        status_container = st.empty()
        results          = []
        ready_list       = [r for r in send_data if r["has_email"]]

        DELAY_SECONDS = 1
        total = len(ready_list)

        for idx, row in enumerate(ready_list):
            remaining = total - idx
            eta = remaining * DELAY_SECONDS
            status_container.markdown(
                f"Enviando **{idx + 1}/{total}** → **{row['Funcionário']}**  "
                f"&nbsp;&nbsp;⏱️ Tempo restante estimado: ~{eta}s"
            )
            success, msg = send_email_gmail(
                to_email       = row["email_addr"],
                pdf_path       = row["filepath"],
                subject        = email_subject.strip(),
                body           = email_body.strip(),
                sender_email   = sender_email.strip(),
                signature_mode = sig_mode,
                signature_html = signature_html,
            )
            results.append({
                "Funcionário": row["Funcionário"],
                "E-mail":      row["email_addr"],
                "Status":      "✅ Enviado" if success else f"❌ {msg}",
            })
            progress_bar.progress((idx + 1) / total)
            if idx < total - 1:
                time.sleep(DELAY_SECONDS)

        status_container.empty()
        st.markdown("### Resultado do Envio")
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)

        n_ok = sum(1 for r in results if "Enviado" in r["Status"])
        if n_ok == len(ready_list):
            st.success(f"✅ Todos os {n_ok} e-mails enviados com sucesso!")
            st.balloons()
        else:
            st.warning(f"⚠️ {n_ok}/{len(ready_list)} enviados. Verifique os erros acima.")