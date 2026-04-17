import streamlit as st

from ui.sidebar import render_sidebar
from ui.tab_split import render_tab_split
from ui.tab_email import render_tab_email
from ui.tab_files import render_tab_files

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Holerites Automáticos",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h2 style="margin:0">📄 Automação de Holerites</h2>
    <p style="margin:0.3rem 0 0; opacity:0.85">Separação automática e envio por e-mail via Gmail</p>
</div>
""", unsafe_allow_html=True)

render_sidebar()

tab1, tab2, tab3 = st.tabs(["📂 1. Separar PDF", "✉️ 2. Enviar E-mails", "📁 3. Arquivos Gerados"])

with tab1:
    render_tab_split()

with tab2:
    render_tab_email()

with tab3:
    render_tab_files()