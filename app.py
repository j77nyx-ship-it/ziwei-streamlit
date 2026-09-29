import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import html as html_lib


# ============================================================
# Streamlit 基础设置
# ============================================================

st.set_page_config(
    page_title="紫微斗数研究排盘",
    page_icon="☯",
    layout="wide",
    initial_sidebar_state="collapsed",
)


BASE_DIR = Path(__file__).resolve().parent

HTML_FILE = BASE_DIR / "index.html"
IZTRO_FILE = BASE_DIR / "iztro-v2.6.1.min.js"


# ============================================================
# 文件检查
# ============================================================

if not HTML_FILE.exists():
    st.error(
        """
        找不到 index.html。

        请确认 GitHub 根目录存在：

        app.py
        index.html
        iztro-v2.6.1.min.js
        requirements.txt
        """
    )
    st.stop()


if not IZTRO_FILE.exists():
    st.error(
        """
        找不到 iztro-v2.6.1.min.js。

        请确认它和 app.py 位于同一个 GitHub 根目录。
        """
    )
    st.stop()


# ============================================================
# 读取 index.html
# ============================================================

try:
    page_html = HTML_FILE.read_text(
        encoding="utf-8"
    )
except Exception as e:

    st.error(
        f"读取 index.html 失败：{e}"
    )

    st.stop()


# ============================================================
# 读取 iztro
# ============================================================

try:

    js_code = IZTRO_FILE.read_text(
        encoding="utf-8",
        errors="ignore"
    )

except Exception as e:

    st.error(
        f"读取 iztro-v2.6.1.min.js 失败：{e}"
    )

    st.stop()


# ============================================================
# 基本检查
# ============================================================

js_size = len(js_code)

if js_size < 10000:

    st.error(
        f"""
        iztro-v2.6.1.min.js 文件内容异常。

        当前读取到的字符数：
        {js_size}

        正常的 iztro 压缩版 JS 应该明显大于这个大小。

        请检查 GitHub 中的
        iztro-v2.6.1.min.js
        是否真的上传了完整文件。
        """
    )

    st.stop()


# ============================================================
# Base64 编码
#
# 避免巨大的 JS 直接嵌入 <script>
# 同时避免 JS 中出现 </script> 导致 HTML 被截断。
# ============================================================

js_base64 = base64.b64encode(
    js_code.encode("utf-8")
).decode("ascii")


# ============================================================
# 运行时加载 iztro
#
# 这里不再使用：
#
# <script>
# 大量 JS
# </script>
#
# 而是：
#
# Base64 → 解码 → Function() 同步执行
# ============================================================

loader_script = f"""
<script>
(function () {{

    try {{

        const encoded = "{js_base64}";

        const decoded = atob(encoded);

        /*
         * 将 UTF-8 Base64 正确还原成 Unicode 字符串
         */
        const bytes = Uint8Array.from(
            decoded,
            c => c.charCodeAt(0)
        );

        const js = new TextDecoder(
            "utf-8"
        ).decode(bytes);


        /*
         * 同步执行 iztro
         */
        const runIztro = new Function(
            js + "\\n//# sourceURL=iztro-v2.6.1.min.js"
        );

        runIztro();


        /*
         * 检查全局对象
         */
        if (
            typeof window.iztro !== "undefined"
            &&
            window.iztro
            &&
            window.iztro.astro
            &&
            typeof window.iztro.astro.bySolar === "function"
        ) {{

            window.__IZTRO_READY__ = true;

            console.log(
                "[紫微斗数] iztro 2.6.1 加载成功"
            );

        }} else {{

            window.__IZTRO_READY__ = false;

            console.error(
                "[紫微斗数] iztro 文件执行完成，但 window.iztro 不存在"
            );

        }}

    }} catch (error) {{

        window.__IZTRO_READY__ = false;

        window.__IZTRO_ERROR__ =
            error && error.message
                ? error.message
                : String(error);

        console.error(
            "[紫微斗数] iztro 加载失败",
            error
        );

    }}

}})();
</script>
"""


# ============================================================
# 将加载器放到 index.html 的业务 JS 之前
#
# 你的 index.html 当前只有一个主要 <script>
# ============================================================

marker = "<script>"

if marker not in page_html:

    st.error(
        "index.html 中没有找到页面 JavaScript。"
    )

    st.stop()


page_html = page_html.replace(
    marker,
    loader_script + "\n<script>",
    1
)


# ============================================================
# 给页面加入启动诊断
#
# 如果 iztro 没加载成功，不再只是说“检查网络”。
# ============================================================

diagnostic_script = """
<script>
(function () {

    window.addEventListener(
        "load",
        function () {

            setTimeout(
                function () {

                    const status =
                        document.getElementById("status");

                    if (!status) {
                        return;
                    }

                    /*
                     * 已经成功
                     */
                    if (
                        window.__IZTRO_READY__
                        &&
                        window.iztro
                        &&
                        window.iztro.astro
                    ) {

                        console.log(
                            "[紫微斗数] 排盘引擎已准备完成"
                        );

                        status.textContent =
                            "排盘引擎已加载，请输入出生资料。";

                        status.className =
                            "status";

                        return;
                    }


                    /*
                     * 加载失败
                     */
                    let detail =
                        window.__IZTRO_ERROR__
                        ||
                        "未知错误";


                    status.innerHTML =
                        "❌ 排盘引擎初始化失败。"
                        +
                        "<br>"
                        +
                        "错误："
                        +
                        detail
                        +
                        "<br><br>"
                        +
                        "如果你已经上传 "
                        +
                        "iztro-v2.6.1.min.js，"
                        +
                        "说明问题已经不是 GitHub 文件位置，"
                        +
                        "而是 JS 文件执行阶段。"
                        +
                        "<br><br>"
                        +
                        "请打开浏览器 F12 → Console 查看详细错误。";

                    status.className =
                        "status error";

                },
                300
            );

        }
    );

})();
</script>
"""


page_html = page_html.replace(
    "</body>",
    diagnostic_script + "\n</body>",
    1
)


# ============================================================
# 最终渲染
# ============================================================

components.html(
    page_html,
    height=15000,
    scrolling=True,
)
