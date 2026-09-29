import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64


# ============================================================
# Streamlit 基础设置
# ============================================================

st.set_page_config(
    page_title="紫微斗数研究排盘",
    page_icon="☯",
    layout="wide",
    initial_sidebar_state="collapsed",
)


BASE_DIR = Path(__file__).parent
HTML_FILE = BASE_DIR / "index.html"
IZTRO_FILE = BASE_DIR / "iztro-v2.6.1.min.js"


# ============================================================
# 检查 HTML
# ============================================================

if not HTML_FILE.exists():
    st.error(
        "找不到 index.html。\n\n"
        "请确认以下文件在 GitHub 根目录：\n"
        "app.py\n"
        "index.html\n"
        "requirements.txt"
    )
    st.stop()


# ============================================================
# 读取 HTML
# ============================================================

try:
    html = HTML_FILE.read_text(encoding="utf-8")
except Exception as e:
    st.error(f"读取 index.html 失败：{e}")
    st.stop()


# ============================================================
# 读取本地 iztro
# ============================================================

iztro_loaded = False

if IZTRO_FILE.exists():

    try:

        js_code = IZTRO_FILE.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        if len(js_code) > 10000:

            # 直接内嵌 JS
            injection = f"""
<script>
/* =========================================================
   LOCAL IZTRO 2.6.1
   ========================================================= */

{js_code}

/* =========================================================
   END LOCAL IZTRO
   ========================================================= */
</script>
"""

            if "</head>" in html:

                html = html.replace(
                    "</head>",
                    injection + "\n</head>",
                    1
                )

            else:

                html = injection + html

            iztro_loaded = True

    except Exception as e:

        st.warning(
            f"读取本地 iztro 文件失败：{e}"
        )


# ============================================================
# 如果没有本地 iztro
# ============================================================

if not iztro_loaded:

    warning_script = """
<script>
window.__IZTRO_LOCAL_MISSING__ = true;
</script>
"""

    if "</head>" in html:

        html = html.replace(
            "</head>",
            warning_script + "\n</head>",
            1
        )

    else:

        html = warning_script + html


# ============================================================
# 重要：
# 不再依赖 index.html 自己加载 CDN
# ============================================================

import re

html = re.sub(
    r'<script[^>]*src=["\'][^"\']*iztro[^"\']*["\'][^>]*>\s*</script>',
    "",
    html,
    flags=re.IGNORECASE
)


# ============================================================
# 页面
# ============================================================

components.html(
    html,
    height=14000,
    scrolling=True,
)
