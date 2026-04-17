import shutil
import streamlit as st
from core.constants import BASE_OUTPUT


def render_tab_files():
    st.subheader("Arquivos Gerados")

    if not BASE_OUTPUT.exists():
        st.info("Nenhum arquivo gerado ainda. Processe um PDF na aba 1.")
        return

    years = sorted([d for d in BASE_OUTPUT.iterdir() if d.is_dir()], reverse=True)

    if not years:
        st.info("Nenhum arquivo encontrado.")
        return

    for year_dir in years:
        st.markdown(f"### 📅 {year_dir.name}")
        months = sorted([d for d in year_dir.iterdir() if d.is_dir()])
        for month_dir in months:
            with st.expander(f"📆 {month_dir.name}", expanded=True):
                func_dirs = sorted([d for d in month_dir.iterdir() if d.is_dir()])
                for func_dir in func_dirs:
                    st.markdown(f"**👤 {func_dir.name}**")
                    type_dirs = sorted([d for d in func_dir.iterdir() if d.is_dir()])
                    for type_dir in type_dirs:
                        pdfs = list(type_dir.glob("*.pdf"))
                        for pdf in pdfs:
                            c1, c2, c3, c4 = st.columns([0.9, 2.5, 0.7, 0.9])
                            with c1:
                                st.markdown(f"`{type_dir.name}`")
                            with c2:
                                st.markdown(f"📄 `{pdf.name}`")
                            with c3:
                                st.markdown(f"{pdf.stat().st_size / 1024:.1f} KB")
                            with c4:
                                with open(pdf, "rb") as f:
                                    st.download_button(
                                        "⬇️ Baixar",
                                        data=f.read(),
                                        file_name=pdf.name,
                                        mime="application/pdf",
                                        key=f"dl_{pdf}",
                                    )

    st.divider()
    if st.button("🗑️ Limpar todos os arquivos gerados", type="secondary"):
        shutil.rmtree(BASE_OUTPUT)
        st.success("Arquivos removidos.")
        st.rerun()