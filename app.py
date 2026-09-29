import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="紫微斗数排盘研究工具",
    page_icon="☯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

html_path = Path(__file__).parent / "index.html"

if not html_path.exists():
    st.error("找不到 index.html，请确认 app.py 和 index.html 在同一个目录。")
else:
    html = html_path.read_text(encoding="utf-8")

    components.html(
        html,
        height=6200,
        scrolling=True
    )
