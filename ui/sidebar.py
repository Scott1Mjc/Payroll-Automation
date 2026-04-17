import streamlit as st
from core.storage import load_employees, save_employees


def render_sidebar():
    with st.sidebar:
        st.header("👥 Funcionários")
        employees = load_employees()

        with st.expander("➕ Adicionar funcionário", expanded=False):
            new_name  = st.text_input("Nome", placeholder="")
            new_email = st.text_input("Email", placeholder="")
            if st.button("Adicionar", use_container_width=True):
                if new_name and new_email:
                    new_email_clean    = new_email.strip().lower()
                    new_name_clean     = new_name.upper().strip()
                    emails_cadastrados = [e.lower() for e in employees.values()]
                    if new_name_clean in employees:
                        st.warning("⚠️ Já existe um funcionário com esse nome.")
                    elif new_email_clean in emails_cadastrados:
                        st.warning("⚠️ Esse e-mail já está cadastrado para outro funcionário.")
                    else:
                        employees[new_name_clean] = new_email_clean
                        save_employees(employees)
                        st.success(f"✅ {new_name.title()} adicionado!")
                        st.rerun()
                else:
                    st.warning("Preencha nome e e-mail.")

        if employees:
            st.markdown(f"**{len(employees)} funcionário(s) cadastrado(s):**")
            busca = st.text_input(
                "🔍 Pesquisar", placeholder="Digite o nome...", key="busca_func"
            )
            funcionarios_filtrados = {
                name: email
                for name, email in sorted(employees.items())
                if busca.upper().strip() in name
            }
            if busca and not funcionarios_filtrados:
                st.caption("Nenhum funcionário encontrado.")
            for name, email in funcionarios_filtrados.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(
                        f"<small>**{name.title()}**<br>{email}</small>",
                        unsafe_allow_html=True,
                    )
                with col2:
                    if st.button("🗑️", key=f"del_{name}", help="Remover"):
                        del employees[name]
                        save_employees(employees)
                        st.rerun()
        else:
            st.info("Nenhum funcionário cadastrado ainda.")