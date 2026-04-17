import streamlit as st
from core.constants import MONTHS_PT, MONTHS_PT_DISPLAY
from core.pdf_processor import split_pdf, save_holerites
from core.storage import load_employees
from utils.string_helpers import safe_str, short_name, full_name_title


def render_tab_split():
    st.subheader("Upload do PDF de Holerites")
    st.markdown(
        "Faça o upload do PDF completo recebido da contabilidade. "
        "O sistema separará automaticamente cada holerite."
    )

    if "upload_key" not in st.session_state:
        st.session_state["upload_key"] = 0

    uploaded_file = st.file_uploader(
        "Selecione o PDF",
        type="pdf",
        key=f"pdf_upload_{st.session_state['upload_key']}",
    )

    if uploaded_file:
        st.markdown(f"**Arquivo:** `{uploaded_file.name}` ({uploaded_file.size / 1024:.1f} KB)")

        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            processar = st.button("🔍 Processar PDF", type="primary", use_container_width=True)
        with col_btn2:
            if st.button("🔄 Limpar", use_container_width=True, help="Remove o arquivo e reinicia"):
                st.session_state["upload_key"] += 1
                st.session_state.pop("holerites_raw", None)
                st.session_state.pop("holerites_edited", None)
                st.session_state.pop("holerites_saved", None)
                st.rerun()

        if processar:
            with st.spinner("Analisando e separando holerites..."):
                pdf_bytes = uploaded_file.read()
                holerites = split_pdf(pdf_bytes)
            st.session_state["holerites_raw"] = holerites
            st.success(f"✅ {len(holerites)} holerite(s) identificado(s)!")

    if "holerites_raw" in st.session_state:
        holerites = st.session_state["holerites_raw"]
        employees = load_employees()

        st.markdown("### Revisão — Confirme antes de salvar")

        edited = []
        for i, h in enumerate(holerites):
            with st.container(border=True):
                cols = st.columns([0.4, 3, 1.5, 1.5, 1])

                with cols[0]:
                    st.markdown(f"**Pág. {h['page_num']}**")

                with cols[1]:
                    status      = "✅" if h["name_detected"] else "⚠️"
                    name_edited = st.text_input(
                        f"{status} Nome do funcionário",
                        value=h["name"],
                        key=f"name_{i}",
                        help="⚠️ Nome não detectado automaticamente — verifique",
                    )
                    if h.get("total_pages", 1) > 1:
                        st.caption(f"📎 {h['total_pages']} páginas mescladas em 1 PDF")

                with cols[2]:
                    month_display = MONTHS_PT_DISPLAY.get(h["month"], h["month"])
                    st.markdown(
                        f"**Período**<br>{month_display} / {h['year']}",
                        unsafe_allow_html=True,
                    )

                with cols[3]:
                    type_edited = st.selectbox(
                        "Tipo",
                        options=["Adiantamento", "Pagamento"],
                        index=0 if h["type"] == "Adiantamento" else 1,
                        key=f"type_{i}",
                    )

                with cols[4]:
                    in_db = name_edited.upper().strip() in employees
                    st.markdown(
                        "<span style='color:#22c55e'>✅ Cad.</span>"
                        if in_db
                        else "<span style='color:#ef4444'>❌ S/email</span>",
                        unsafe_allow_html=True,
                    )

                edited.append({**h, "name": name_edited.upper().strip(), "type": type_edited})

        st.session_state["holerites_edited"] = edited

        n_sem_email = sum(1 for h in edited if h["name"].upper() not in employees)
        if n_sem_email > 0:
            st.warning(
                f"⚠️ {n_sem_email} funcionário(s) sem e-mail — adicione na barra lateral antes de enviar."
            )

        with st.expander("📁 Preview da estrutura de pastas que será criada"):
            for h in edited:
                ml   = MONTHS_PT.get(h["month"], h["month"])
                fn   = safe_str(short_name(h["name"]))
                pdfn = safe_str(full_name_title(h["name"])) + ".pdf"
                st.code(
                    f"Holerites / {h['year']} / {ml} / {fn} / {h['type']} / {pdfn}",
                    language="text",
                )

        if st.button("💾 Salvar Holerites em Pastas", type="primary", use_container_width=True):
            with st.spinner("Salvando arquivos..."):
                saved = save_holerites(edited)
            st.session_state["holerites_saved"] = saved
            st.success(f"✅ {len(saved)} arquivo(s) salvo(s) em `Holerites/`")
            st.balloons()