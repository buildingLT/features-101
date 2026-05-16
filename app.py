import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NRI Investment Readiness Calculator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
  #MainMenu, header, footer { display: none !important; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  .stApp { background: #0f1117; }
</style>
""", unsafe_allow_html=True)

with open("nri_calculator.html", "r") as f:
    html = f.read()

components.html(html, height=1100, scrolling=True)
