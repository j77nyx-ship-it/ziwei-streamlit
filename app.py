import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import urllib.request
import re

st.set_page_config(
    page_title="紫微斗数研究排盘",
    page_icon="☯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "index.html"

# 固定使用 iztro 2.6.1
IZTRO_URL = (
    "https://cdn.jsdelivr.net/npm/"
    "iztro@2.6.1/dist/iztro-v2.6.1.min.js"
)

# =========================================================
# 1. 检查 index.html
# =========================================================

if not HTML_FILE.exists():
    st.error(
        "找不到 index.html。\n\n"
        "请确认 GitHub 根目录至少存在：\n\n"
        "app.py\n"
        "index.html\n"
        "requirements.txt"
    )
    st.stop()

try:
    html = HTML_FILE.read_text(encoding="utf-8")
except Exception as e:
    st.error(f"读取 index.html 失败：{e}")
    st.stop()


# =========================================================
# 2. 从官方 CDN 获取 iztro
# =========================================================

try:
    request = urllib.request.Request(
        IZTRO_URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        js_code = response.read().decode("utf-8", errors="ignore")

except Exception as e:
    st.error(
        "无法从官方 CDN 获取 iztro 2.6.1。\n\n"
        f"错误：{e}\n\n"
        "请稍后刷新页面。"
    )
    st.stop()


# =========================================================
# 3. 检查下载结果
# =========================================================

js_length = len(js_code)

if js_length < 10000:
    st.error(
        "iztro 2.6.1 下载结果异常。\n\n"
        f"当前读取到：{js_length} 个字符。\n\n"
        "正常的 iztro 独立 JS 文件应该明显大于这个大小。"
    )
    st.stop()


# =========================================================
# 4. 删除 index.html 中可能残留的旧 iztro CDN
# =========================================================

html = re.sub(
    r'<script[^>]*src=["\'][^"\']*iztro[^"\']*["\'][^>]*>\s*</script>',
    "",
    html,
    flags=re.IGNORECASE
)


# =========================================================
# 5. 将官方 iztro 直接注入 HTML
# =========================================================

iztro_script = f"""
<script>
/* =========================================================
   IZTRO 2.6.1
   Loaded automatically by Streamlit
   ========================================================= */

{js_code}

/* =========================================================
   END IZTRO 2.6.1
   ========================================================= */

console.log(
    "[紫微斗数] iztro 2.6.1 已加载，文件长度：{js_length}"
);

if (
    typeof window.iztro !== "undefined" &&
    window.iztro &&
    window.iztro.astro &&
    typeof window.iztro.astro.bySolar === "function"
) {{
    window.__IZTRO_READY__ = true;

    console.log(
        "[紫微斗数] 排盘引擎初始化成功"
    );
}} else {{
    window.__IZTRO_READY__ = false;

    console.error(
        "[紫微斗数] JS 已执行，但 window.iztro 不存在"
    );
}}
</script>
"""


# =========================================================
# 6. 把 iztro 放到 head 中
# =========================================================

if "</head>" in html:

    html = html.replace(
        "</head>",
        iztro_script + "\n</head>",
        1
    )

else:

    html = iztro_script + html


# =========================================================
# 7. 增加诊断信息
# =========================================================

diagnostic_script = """
<script>

window.addEventListener("load", function () {

    setTimeout(function () {

        const status =
            document.getElementById("status");

        if (!status) {
            return;
        }

        if (
            window.__IZTRO_READY__ &&
            window.iztro &&
            window.iztro.astro
        ) {

            status.textContent =
                "排盘引擎已加载，请输入出生资料。";

            status.className = "status";

            console.log(
                "[紫微斗数] 排盘引擎准备完成"
            );

        } else {

            status.innerHTML =
                "❌ 排盘引擎初始化失败。"
                + "<br><br>"
                + "iztro 文件已经成功读取，"
                + "但浏览器没有检测到 window.iztro。"
                + "<br><br>"
                + "请打开 F12 → Console 查看错误。";

            status.className =
                "status error";
        }

    }, 500);

});

</script>
"""


# =========================================================
# 8. 插入诊断代码
# =========================================================

if "</body>" in html:

    html = html.replace(
        "</body>",
        diagnostic_script + "\n</body>",
        1
    )

else:

    html += diagnostic_script


# =========================================================
# 9. 显示页面
# =========================================================

components.html(
    html,
    height=15000,
    scrolling=True,
)
