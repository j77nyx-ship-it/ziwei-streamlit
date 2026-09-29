import re
import urllib.request
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="紫微斗数排盘研究工具",
    page_icon="☯",
    layout="wide",
    initial_sidebar_state="collapsed",
)


BASE_DIR = Path(__file__).parent
HTML_PATH = BASE_DIR / "index.html"


@st.cache_data(ttl=86400, show_spinner=False)
def get_iztro_js():
    """
    服务器端获取 iztro。
    浏览器不再直接依赖 CDN。
    """

    urls = [
        # 主地址
        "https://cdn.jsdelivr.net/npm/iztro@2.6.1/dist/iztro-v2.6.1.min.js",

        # 备用地址
        "https://unpkg.com/iztro@2.6.1/dist/iztro-v2.6.1.min.js",

        # 最后兼容 2.6.0
        "https://cdn.jsdelivr.net/npm/iztro@2.6.0/dist/iztro-v2.6.0.min.js",

        "https://unpkg.com/iztro@2.6.0/dist/iztro-v2.6.0.min.js",
    ]

    last_error = None

    for url in urls:
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
            )

            with urllib.request.urlopen(req, timeout=20) as response:
                data = response.read()

            if data and len(data) > 50000:
                return data.decode("utf-8")

        except Exception as e:
            last_error = e

    raise RuntimeError(
        f"无法从 CDN 获取 iztro 排盘引擎。最后错误：{last_error}"
    )


def inject_iztro(html: str, iztro_js: str) -> str:
    """
    把 index.html 里的外部 iztro script 替换成服务器已经获取好的
    本地内嵌 JS。

    这样浏览器端不需要访问 CDN。
    """

    # 删除原来的 iztro CDN script
    html = re.sub(
        r'<script[^>]+src=["\'][^"\']*iztro[^"\']*["\'][^>]*>\s*</script>',
        "",
        html,
        flags=re.IGNORECASE,
    )

    # 在 </head> 前插入真正的 iztro
    inject_code = f"""
<script>
/* ===== SERVER EMBEDDED IZTRO ===== */
{iztro_js}
/* ===== END IZTRO ===== */
</script>
"""

    if "</head>" in html:
        html = html.replace(
            "</head>",
            inject_code + "\n</head>",
            1,
        )
    else:
        html = inject_code + html

    return html


if not HTML_PATH.exists():
    st.error(
        "找不到 index.html。请确认 index.html 和 app.py 位于 GitHub 仓库根目录。"
    )
    st.stop()


try:
    html = HTML_PATH.read_text(encoding="utf-8")
except Exception as e:
    st.error(f"读取 index.html 失败：{e}")
    st.stop()


# 获取并内嵌 iztro
try:
    iztro_js = get_iztro_js()
    html = inject_iztro(html, iztro_js)

except Exception as e:
    # 如果服务器端也暂时无法访问 CDN，
    # 仍然把原网页显示出来，方便诊断。
    st.warning(
        "服务器暂时无法获取 iztro 排盘引擎。"
        "如果网页本身还有 CDN 引入，则可能仍然无法排盘。"
    )

    st.code(
        str(e),
        language="text",
    )


components.html(
    html,
    height=12000,
    scrolling=True,
)
