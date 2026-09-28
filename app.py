import streamlit as st
import random
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# ==============================================
# 知识库 源自《紫微斗数精成》大德山人
# ==============================================
knowledge_intro = """
> 📖 理论来源：《紫微斗数精成》大德山人
**核心规则：本命盘为【体】（先天静盘，格局根基）；大限、流年为【用】（后天动运）**
1. 大限(大运)：每一宫管10年；阳男阴女顺行，阴男阳女逆行；起运岁数由五行局决定，使用虚岁。
2. 论大限：重点看大限本宫 + 三方四正；看主星庙旺失陷、四化禄权科忌、六吉六煞组合。
3. 论流年：流年不能独立论吉凶！流年吉凶依附当前大限。大限吉，流年凶只是短暂波折；大限凶，流年吉多镜花水月。
4. 三方四正：本宫+三合三宫叫三方；对宫叫四正；论命论限必须参看。
5. 四化：化禄(财缘机遇)、化权(权力竞争)、化科(名声贵人)、化忌(阻滞是非损耗)。
"""

# 十四主星简易释义（取自斗数精成第八章）
main_star_dict = {
    "紫微":"帝王星，主领导、尊贵；庙旺有为，落陷容易主观固执。",
    "天机":"智慧谋略星，主思虑变动；喜逢科星，见煞多思虑纠结。",
    "太阳":"光明事业星；庙旺贵气，落陷辛劳，主是非口舌。",
    "武曲":"财星，主实干求财；逢煞易竞争纠纷。",
    "天同":"福星，享受温和；落陷容易懒散，怕煞星激发。",
    "廉贞":"次桃花、事业多变星；吉则才华，煞多官非感情困扰。",
    "天府":"库星，财库积蓄；稳重保守，喜吉星来扶。",
    "太阴":"财星、感情星；庙旺柔美，落陷多内耗。",
    "贪狼":"欲望桃花机遇星；火贪格可横发，煞多欲望泛滥。",
    "巨门":"口舌星；化科善言，化忌口舌官非是非。",
    "天相":"印星，辅佐；喜吉星，遇煞容易受牵连。",
    "天梁":"荫星，贵人长辈；庙旺解厄，煞多操心劳碌。",
    "七杀":"将星开创；庙旺魄力，煞重坎坷波折。",
    "破军":"变革星；主破旧立新，逢吉革新，逢煞破败损耗。"
}

# 四化释义
four_hua = {
    "化禄":"【化禄】机遇、财源、享受，代表机缘收获。",
    "化权":"【化权】竞争、权力、主见，同时代表压力斗争。",
    "化科":"【化科】名声、贵人、缓和灾厄，利考试声誉。",
    "化忌":"【化忌】阻滞、损耗、是非、纠结；要看落在哪一宫。"
}

# 十二宫人事含义（斗数精成第五章）
palace_info = {
    "命宫":"代表本人性格天赋，全盘太极点。",
    "兄弟宫":"兄弟姐妹、平辈朋友伙伴。",
    "夫妻宫":"感情婚姻，配偶情况。",
    "子女宫":"晚辈、孩子、下属。",
    "财帛宫":"求财、收入、现金钱财。",
    "疾厄宫":"身体隐患，病痛灾厄。",
    "迁移宫":"外出机遇，社会对外际遇。",
    "奴仆宫":"下属朋友，小人贵人。",
    "官禄宫":"事业、工作、功名。",
    "田宅宫":"房产、家庭、库藏积蓄。",
    "福德宫":"精神享受，福气心态。",
    "父母宫":"长辈、文书契约、出身。"
}

# 大限阶段参考（提示，真实要五行局+顺逆排盘）
dayun_stage = [
    {"age_start":2,"age_end":11,"note":"初限，少年根基，看家庭父母宫。"},
    {"age_start":12,"age_end":21,"note":"少年青年，求学、启蒙，看命宫福德。"},
    {"age_start":22,"age_end":31,"note":"青年阶段，恋爱择业，官禄夫妻为重。"},
    {"age_start":32,"age_end":41,"note":"壮年大限，事业拼搏，财帛官禄。"},
    {"age_start":42,"age_end":51,"note":"中年，守成为主，兼顾疾厄健康。"},
    {"age_start":52,"age_end":61,"note":"中晚年，田宅福德优先。"},
    {"age_start":62,"age_end":99,"note":"晚限，安养，重福德田宅。"},
]

# ===================== 图像处理OCR =====================
def preprocess_img(img):
    img = img.convert("L")
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    return img

def ocr_star_map(img):
    try:
        proc_img = preprocess_img(img)
        custom_config = r'--psm 6'
        result_text = pytesseract.image_to_string(proc_img, lang="chi_sim+eng", config=custom_config)
        return result_text.strip()
    except Exception as err:
        return f"识别失败：{str(err)}"

# 关键词扫描OCR文本
def scan_ocr_text(txt):
    hit_stars = [k for k in main_star_dict.keys() if k in txt]
    hit_hua = [k for k in four_hua.keys() if k in txt]
    hit_palace = [k for k in palace_info.keys() if k in txt]
    has_dayun = "大限" in txt or "大限宫" in txt
    has_liunian = "流年" in txt or "流月" in txt
    return hit_stars, hit_hua, hit_palace, has_dayun, has_liunian

# ===================== Streamlit页面 =====================
st.set_page_config(page_title="紫微斗数｜《紫微斗数精成》解析演示", layout="wide")
st.title("🔮紫微斗数解析（参考《紫微斗数精成》大德山人）")

st.warning("""
⚠️ 【重要声明】本程序仅为传统国学科普演示，**不是专业排盘软件**。
真正完整断盘需要：出生年月日时（农历/公历）、性别，推算五行局、顺逆行大限、布全部星曜。
> 上传文墨天机截图仅做OCR文字提取关键词，不能代替人工看盘；仅供娱乐，勿作为人生重大决策依据。
""")

tab_ziwei, tab_mayi = st.tabs(["📅紫微斗数｜星盘&大限流年", "🧏麻衣神相（人脸面相）"])

with tab_ziwei:
    st.markdown(knowledge_intro)
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📌参考大限阶段（虚岁，演示用，真实需五行局顺逆排盘）")
        age_input = st.number_input("输入你的虚岁", min_value=2, max_value=99, value=28)
        btn_dayun = st.button("查看对应阶段参考解读")
        if btn_dayun:
            sel = None
            for s in dayun_stage:
                if s["age_start"] <= age_input <= s["age_end"]:
                    sel = s
            st.success(f"虚岁 {age_input}，属于 {sel['age_start']}‑{sel['age_end']}岁阶段\n👉阶段提示：{sel['note']}")
            st.info("⚠️注意：真实大限要看【五行局+阳男阴女顺逆行】，本处仅阶段参考，不等同正式排盘结果。")

    with col_b:
        st.subheader("📅流年参考提示")
        year_in = st.number_input("输入查询流年", min_value=1920, max_value=2100, value=2026)
        st.markdown("""
        > 根据斗数精成理论：**流年吉凶不能孤立看，必须依附当前大限的格局。**
        > - 大限吉+流年凶：只是短暂波折，守静即可
        > - 大限凶+流年吉：机会看着好，容易镜花水月，不宜大举投入
        """)

    st.divider()
    st.subheader("🖼️上传文墨天机紫微星盘截图（OCR提取文字）")
    st.info("上传文墨天机截图，程序OCR提取图片文字，扫描识别主星、四化、宫位关键词。\n建议：截图裁剪掉手机状态栏，只保留盘面，提高识别率。")
    up_img = st.file_uploader("上传星盘截图 png/jpg/jpeg", type=["png","jpg","jpeg"])
    ocr_out = ""
    if up_img is not None:
        img_obj = Image.open(up_img)
        st.image(img_obj, caption="上传星盘", width="stretch")
        with st.spinner("正在OCR识别图片文字..."):
            ocr_out = ocr_star_map(img_obj)
        st.text_area("OCR识别得到的盘面文字", value=ocr_out, height=240)

    user_text = st.text_area("粘贴星盘文本，执行关键词扫描", height=200, value=ocr_out)
    if st.button("🔍扫描星盘关键词（取自斗数精成知识库）"):
        if len(user_text.strip()) < 3:
            st.warning("请粘贴星盘识别后的文字")
        else:
            stars, huas, palaces, has_dy, has_ln = scan_ocr_text(user_text)
            st.success("关键词扫描结果")
            if stars:
                st.markdown("**识别到主星：**")
                for s in stars:
                    st.write(f"- {s}：{main_star_dict[s]}")
            else:
                st.write("未识别到十四主星，截图文字清晰度不足。")

            if huas:
                st.markdown("**识别到四化：**")
                for h in huas:
                    st.write(f"- {four_hua[h]}")
            else:
                st.write("未识别四化关键词")

            if palaces:
                st.markdown(f"识别到宫位：{','.join(palaces)}")
            else:
                st.write("未识别十二宫关键词")

            st.markdown(f"""
            {'✅检测文本包含【大限】' if has_dy else '❌文本没有大限相关文字'}
            {'✅检测文本包含【流年】' if has_ln else '❌文本没有流年相关文字'}
            """)
            st.info("💡操作建议：找到截图里面【大限走到XX宫】，结合《紫微斗数精成》理论：看该宫主星、四化，加上三方四正综合分析，流年依附大限论吉凶。")

    st.divider()
    with st.expander("📖知识库：斗数精成重点摘录"):
        st.markdown("""
**三方四正**
> 本宫的三合宫叫三方；对宫（六冲）叫四正。论大限流年，不能只看本宫，三方四正吉凶要一起参合。

**庙旺‑失陷**
> 庙旺：星曜力量充分发挥，吉星更吉，凶星杀伤力降低；
> 失陷：星曜力量衰弱，吉星无力，煞星破坏力放大。

**大限论断原则（斗数精成原文）**
> 大限管十年祸福；大限为体，流年为用。大限格局差，流年再好，也难真正获取大利。
""")

# ========== 麻衣神相Tab ==========
with tab_mayi:
    st.subheader("🧏‍♂️麻衣神相（面相解析，源自麻衣神相PDF）")
    st.info("""
    ⚠️ 注意：麻衣神相是**看人脸照片**！！不要上传紫微星盘截图。
    依据：识限歌三段大限，十三部位流年歌，三停十二宫。
    本程序无法AI视觉识别人脸疤痕、纹路，仅输出古籍理论框架。
    """)
    up_face = st.file_uploader("上传人脸正面照片", type=["png","jpg","jpeg"])
    if up_face is not None:
        faceimg = Image.open(up_face)
        st.image(faceimg, caption="上传人脸照片", width="stretch")
    mayi_age = st.number_input("输入周岁", min_value=1, max_value=100, value=28)
    btn_mayi = st.button("解析麻衣面相大限（识限歌）")
    if btn_mayi:
        mayi_data = [
            {"name":"第一大限：8‑28岁｜上停（发际线‑山根，额头为主）","a1":8,"a2":28,"desc":"【识限歌】八岁十八二十八，下至山根上至发。有无活计两头消，三十印堂莫带杀。看额头、印堂，光洁无疤纹少年运佳。"},
            {"name":"第二大限：32‑52岁｜中停（山根‑准头，鼻子颧骨）","a1":32,"a2":52,"desc":"【识限歌】三二四二五十二，山根上下准头止。禾仓禄马要相当，不识之人莫乱指。看鼻子颧骨，宜饱满不宜凹陷断裂。"},
            {"name":"第三大限：53‑73岁｜下停（人中‑地阁，嘴巴下巴）","a1":53,"a2":73,"desc":"【识限歌】五三六三七十三，人面排来地阁间。逐一推详看祸福火星百岁印堂添。看地阁下巴，宜方圆饱满。"}
        ]
        hit = None
        for item in mayi_data:
            if item["a1"] <= mayi_age <= item["a2"]:
                hit = item
        if hit:
            st.success(f"""
### 当前麻衣面相大限：{hit['name']}
{hit['desc']}
> 📝提示：实际看相需要肉眼观察你面部对应区域的饱满、痣、疤痕、气色。
""")
        else:
            st.info("不在识限歌三段核心区间，参看过渡岁数，结合相邻部位综合参考。")

st.divider()
st.markdown("""
> 💡两套体系区分：
> - 紫微斗数：出生时间排盘，看星盘（文墨天机），《紫微斗数精成》；大限=十宫轮走，虚岁起运，阳男阴女顺逆。
> - 麻衣神相：看真人脸部照片，识限歌分三段面相大限。
""")
