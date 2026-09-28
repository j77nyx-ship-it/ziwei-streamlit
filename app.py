import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="紫微斗数解析",
    page_icon="🔮",
    layout="centered"
)

html_file = Path(__file__).parent / "index.html"

if not html_file.exists():
    st.error("找不到 index.html，请确认 index.html 和 app.py 在同一个目录。")
    st.stop()

html_code = html_file.read_text(encoding="utf-8")

components.html(
    html_code,
    height=1800,
    scrolling=True
)
