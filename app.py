import streamlit as st
import random
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# ====================== 紫微斗数知识库（大运流年逻辑） ======================
great_luck_list = [
    {"start":5, "end":14, "name":"少年运（少年求学大运）",
     "desc":"这个阶段重点是家庭、读书学习。主要看长辈助力，适合沉淀学习，不要强求事业钱财。容易受家庭环境影响心态。"},
    {"start":15, "end":24, "name":"青年启蒙大运",
     "desc":"自我意识觉醒，学业、初次踏入社会，人际、朋友变得重要。容易迷茫纠结，多试错积累经验，不适合过早下定终身。"},
    {"start":25, "end":34, "name":"立业成家大运",
     "desc":"人生最重要的十年！事业起步、恋爱结婚、买房大多集中这个区间。机遇多压力也巨大，抉择会影响往后大半人生。"},
    {"start":35, "end":44, "name":"中年拼搏大运",
     "desc":"事业黄金期，承担家庭重担，上有老下有小。重点守财，同时事业往上冲，也要格外注意身体健康问题。"},
    {"start":45, "end":54, "name":"沉淀守成大运",
     "desc":"不再适合激进冒险，适合守成果。人际关系格局定型，多关注身体、家庭，减少高风险投资。"},
    {"start":55, "end":64, "name":"后福修养大运",
     "desc":"宜静不宜动，享受人生成果，保养身心，不要折腾大投资，重视家人健康。"},
    {"start":65, "end":120, "name":"暮年享福大运",
     "desc":"安养为主，看淡得失，保重身体，家庭亲情是核心。"},
]

year_luck_list = [
    {"tag":"平稳普通", "desc":"属于平平淡淡的一年，没有特大惊喜，也没有大灾大难。适合按部就班过日子，稳步积累，不要期待一夜暴富。"},
    {"tag":"机遇进取", "desc":"机会较多，有新的机会出现，适合主动争取，但是切记不要冒进。机会来了也要评估风险，不能盲目all in。"},
    {"tag":"开销耗财", "desc":"容易花钱、意外支出多，钱财留不住。一定要做好储蓄，少冲动消费，规避高风险理财。"},
    {"tag":"人际是非", "desc":"容易与人产生矛盾，小人是非变多。少掺和别人是非，少吵架，遇事多忍让，减少社交纠纷。"},
    {"tag":"感情波动", "desc":"感情容易发生变化，恋爱分手、婚姻矛盾高发，多沟通，重大感情决定谨慎思考。"},
    {"tag":"注意健康", "desc":"身体需要重点保养，不要熬夜透支，定期体检，不要硬扛病痛。"},
    {"tag":"变动奔波", "desc":"容易出现变动，换工作、搬家、出差奔波，环境发生变化，顺势而为，不要抗拒变化。"},
]

palace_text = """
**十二宫通俗含义（大运走到此宫代表十年主线）**
- **命宫大运**：自我变化最大的十年，心态、三观、人生想法会发生很大改变，容易转型。
- **财帛宫大运**：重点围绕钱财，赚钱机会多，但也容易开销巨大，看星曜是进财还是耗财。
- **官禄宫大运**：事业工作的十年，跳槽、升职、创业，事业是生活主线。
- **迁移宫大运**：外出、变动，出差、远行、换城市，对外人际变化大。
- **交友宫大运**：人际关系、同事朋友，贵人或者小人集中出现在这十年。
- **田宅宫大运**：房产、家庭，买房装修，家庭内部事情多。
- **福德宫大运**：精神享受，内心感受，开心还是内耗，福气享受。
- **父母宫大运**：长辈、文书证件，和父母缘分，考试证书手续。
- **子女宫大运**：孩子、晚辈，生育，下属晚辈问题。
- **夫妻宫大运**：感情婚姻主线，恋爱结婚、矛盾分开大多容易发生在这个大运。
- **疾厄宫大运**：身体健康要重点注意，容易多病痛，保养为主。
"""

combine_rule = """
### 📚 大运流年4种组合核心判断规则
> 核心：**大运为体，流年为用。大运是十年底色，流年是当年触发事件。**
1. ✅ **大运吉 + 流年吉**：双重加持，该年容易机会落地，做事事半功倍，适合进取。
2. ⚠️ **大运吉 + 流年凶**：底子很好，流年只是短暂波折，熬过去即可；不适合高风险投资。
3. ⚠️ **大运凶 + 流年吉**：表面机会好看，镜花水月，很难落地；宜守不宜攻，切勿大额投入。
4. ❌ **大运凶 + 流年凶**：双重压力，凡事求稳，不折腾，重大决策延后，防守避险优先。
"""

# 图片预处理：灰度+增强对比度，专门优化文墨天机紫微盘
def preprocess_img(img):
    img = img.convert("L") #转灰度
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0) #提高对比度
    img = img.filter(ImageFilter.SMOOTH_MORE)
    return img

# OCR识别星盘图片文字函数，增加psm6适配表格文字
def ocr_star_map(img):
    try:
        processed_img = preprocess_img(img)
        # psm6：假设图片是一块规整表格文字，适合文墨天机宫格盘面
        custom_config = r'--psm 6'
        result_text = pytesseract.image_to_string(processed_img, lang="chi_sim+eng", config=custom_config)
        return result_text.strip()
    except Exception as err:
        return f"识别失败：{str(err)}"

# 从OCR星盘文本里提取大运、流年关键词
def parse_star_text(raw_text):
    keywords_dayun = ["大运", "大限", "命宫", "财帛", "官禄", "夫妻", "福德", "田宅", "迁移", "疾厄"]
    keywords_liunian = ["流年", "岁", "流月", "流日", "2024","2025","2026","2027","2028"]
    star_keywords = ["紫微","天机","太阳","武曲","天同","廉贞","天府","太阴","贪狼","巨门","天相","天梁","七杀","破军"]

    found_dayun = [w for w in keywords_dayun if w in raw_text]
    found_liunian = [w for w in keywords_liunian if w in raw_text]
    found_stars = [w for w in star_keywords if w in raw_text]
    return found_dayun, found_liunian, found_stars


# ========= Streamlit页面开始 =========
st.set_page_config(page_title="紫微斗数｜星盘截图解析", layout="wide")
st.title("🔮 紫微斗数 · 大运流年解析（支持文墨天机星盘截图上传）")

st.warning("""
⚠️ **民俗文化娱乐工具，仅供科普！不具备科学预测效力。人生取决于努力、环境、个人选择，请勿拿本结果做重大人生决策。**
""")

tab1, tab2 = st.tabs(["📝手动输入解析", "🖼️上传紫微星盘截图识别"])

# Tab1 手动输入
with tab1:
    st.markdown("""
## 💡核心逻辑大白话
- **大运（10年周期）：你的十年大环境底色。决定阶段上限。**
- **流年（单一年份）：每一年临时发生的事情。**
> 比喻：大运就像房子，流年是天气。房子好，下雨只是小事；房子漏雨，一点点小雨家里就遭殃。
> **先看大运底色，再看流年，不能单独拿某一年下定论！**
""")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📌 查询当前十年大运")
        age = st.number_input("输入你的周岁年龄", min_value=1, max_value=120, value=28)
        run_da_yun = st.button("解析大运")
        if run_da_yun:
            res = None
            for item in great_luck_list:
                if item["start"] <= age <= item["end"]:
                    res = item
            st.success(f"""
**当前大运：{res['name']}（{res['start']}‑{res['end']}周岁）**

{res['desc']}

> 💡：这就是你这十年的整体底色，分析每一年流年，都要结合这个结果！
            """)

    with col2:
        st.subheader("📅 查询流年状态")
        in_year = st.number_input("输入查询公历年份", min_value=1900, max_value=2100, value=2026)
        run_nian = st.button("解析流年")
        if run_nian:
            pick = random.choice(year_luck_list)
            st.info(f"""
**{in_year}年模拟流年：【{pick['tag']}】**

解读：{pick['desc']}

> ⚠️提醒：流年吉凶不能孤立看，必须对照你的大运底色，参考下面组合规则综合判断。本结果仅演示逻辑，非专业排盘。
            """)
    st.divider()
    st.markdown(combine_rule)
    st.divider()
    st.markdown(palace_text)

# Tab2 【核心：星盘截图上传 + OCR识别】
with tab2:
    st.subheader("🖼️ 上传文墨天机紫微星盘截图")
    st.info("✅ 直接上传文墨天机排盘截图（png/jpg/jpeg），程序自动增强图片对比度，提取星盘文字，扫描大运、流年、主星。\n> 小提示：截图尽量只截取盘面主体，不要保留多余手机顶部状态栏，减少干扰文字。")

    # 上传图片控件
    uploaded_star_img = st.file_uploader("上传星盘截图", type=["png","jpg","jpeg"])
    ocr_result_text = ""
    if uploaded_star_img is not None:
        # 打开图片
        star_img = Image.open(uploaded_star_img)
        # ✅修复！替换废弃参数 use_column_width → width="stretch"
        st.image(star_img, caption="你上传的紫微星盘", width="stretch")
        with st.spinner("正在增强图片并识别星盘文字，请等待..."):
            ocr_result_text = ocr_star_map(star_img)
        st.text_area("✅ OCR识别出来的星盘原文", value=ocr_result_text, height=240)

    st.markdown("### 星盘文本关键词解析")
    star_text_input = st.text_area("粘贴识别出的星盘文字在这里，进行关键词解析", height=200, value=ocr_result_text)

    if st.button("🔍 解析星盘大运&流年"):
        if len(star_text_input.strip()) < 5:
            st.warning("请上传星盘图片或者粘贴识别后的星盘文字！")
        else:
            dayun_keys, liunian_keys, star_keys = parse_star_text(star_text_input)
            st.success("✅ 星盘关键词扫描完成（娱乐参考）")
            if dayun_keys:
                st.write(f"📌 检测到大运/宫位关键词：`{','.join(dayun_keys)}`")
            else:
                st.write("📌 未检测到大运、宫位相关文字，建议裁剪截图，只保留星盘主体")

            if liunian_keys:
                st.write(f"📅 检测到流年关键词：`{','.join(liunian_keys)}`")
            else:
                st.write("📅 没有找到流年相关文字")

            if star_keys:
                st.write(f"⭐ 识别到星曜：`{','.join(star_keys)}`")
            else:
                st.write("⭐ 未识别到主星名称")

            st.info("💡 建议：记下识别出来的大运宫位，切换到【手动输入解析】标签，结合年龄看大运解读。\n> ⚠️本工具只是读取图片文字关键词，不能全自动完整解盘。")


st.divider()
st.subheader("📖 使用小贴士")
st.markdown("""
1. 优先看懂**大运底色**，这是根基，不要被单一年份好坏过度牵动情绪。
2. 同样的流年，放在不同大运下，吉凶会完全反转。
3. 命理讲究趋吉避凶，吉运把握机会，凶运减少折腾，不是坐等命运。
4. 完整专业排盘，需要出生公/农历、时辰、性别、出生地。本程序只演示分析逻辑。
5. ✨文墨天机截图技巧：截图时裁掉手机顶部时间状态栏，只保留中间星盘格子，识别效果大幅提升。
""")
