import streamlit as st

# ============知识库｜源自《紫微斗数精成》大德山人 ============
knowledge_intro = """
> 📖理论来源：《紫微斗数精成》大德山人
**核心原则：本命盘为【体】，大限流年为【用】**
1. 大限(大运)：每一宫掌管10虚岁；阳男阴女顺行，阴男阳女逆行；起运岁数由五行局决定。
2. 论大限必须看：**大限本宫 + 三方四正（本宫+三合三宫+对宫），主星庙旺失陷，四化禄权科忌，吉煞组合**。
3. 流年不能单独论吉凶！流年吉凶依附当前大限格局。
    - 大限格局吉，流年凶，只是短期波折，守静即可；
    - 大限格局凶，流年见禄科也多镜花水月，不宜大额投入冒险。
4. 空宫规则：本宫无主星，借对宫全部星曜一起参断，力量打折扣。
5. 四化：化禄机遇收获｜化权竞争压力｜化科贵人名声｜化忌阻滞损耗是非。
"""

star_comment = {
    "紫微":"帝王星，主领导、尊贵；庙旺有作为，落陷主观固执。",
    "天机":"智慧谋略星，思虑多变；喜科星，逢煞容易思虑内耗。",
    "太阳":"事业光明星；庙旺贵气，落陷辛劳多口舌是非。",
    "武曲":"财星，实干求财；遇煞容易竞争纠纷。",
    "天同":"福星，温和享受；落陷容易懒散，怕煞星激发。",
    "廉贞":"多变才华星；吉则才华出众，煞多易感情官非困扰。",
    "天府":"财库星，稳重保守，喜吉星扶持。",
    "太阴":"财星感情星；庙旺柔美，落陷内心多纠结。",
    "贪狼":"机遇桃花星；火贪格可横发，煞重欲望泛滥。",
    "巨门":"口舌星；化科善辩，化忌口舌官非是非。",
    "天相":"印星辅佐；喜吉星，遇煞容易被牵连。",
    "天梁":"荫星贵人；庙旺解厄消灾，煞多操心劳碌。",
    "七杀":"将星开创魄力；庙旺敢闯，煞重坎坷波折。",
    "破军":"变革破旧星；逢吉革新，逢煞破败损耗。"
}

palace_desc = {
    "命宫":"本人性格天赋，全盘太极原点。",
    "兄弟宫":"兄弟姐妹、平辈伙伴朋友。",
    "夫妻宫":"感情婚姻，配偶状态。",
    "子女宫":"晚辈、子女、下属。",
    "财帛宫":"求财、现金收入。",
    "疾厄宫":"身体隐患、病痛灾厄。",
    "迁移宫":"外出机遇，对外社会际遇。",
    "奴仆宫":"下属、朋友，贵人小人。",
    "官禄宫":"事业、工作、功名。",
    "田宅宫":"房产、家庭、库藏积蓄。",
    "福德宫":"精神福气，心态享受。",
    "父母宫":"长辈、文书契约、出身。"
}

st.set_page_config(page_title="紫微斗数｜《紫微斗数精成》解析", layout="wide")
st.title("🔮紫微斗数解析｜参考《紫微斗数精成》大德山人")

st.warning("""
⚠️ 【声明】本工具仅传统国学娱乐演示，**不构成人生决策依据**。
✅排盘运算运行在你的浏览器前端(iztro‑lib)，云端无需编译排盘库。输入公历出生年月日时、性别自动排本命、大限、三方四正、四化、流年。
""")

tab_ziwei, tab_mayi = st.tabs(["📅紫微斗数生辰排盘解析","🧏麻衣神相（面相）"])

with tab_ziwei:
    st.markdown(knowledge_intro)
    st.divider()
    st.subheader("📝录入出生信息（公历）")
    col_in1,col_in2,col_in3 = st.columns([1,1,1])
    with col_in1:
        birth_y = st.number_input("出生公历年",min_value=1900,max_value=2050,value=2000)
        birth_m = st.number_input("出生公历月",min_value=1,max_value=12,value=8)
    with col_in2:
        birth_d = st.number_input("出生公历日",min_value=1,max_value=31,value=16)
        hour = st.number_input("出生小时(24h)",min_value=0,max_value=23,value=12)
    with col_in3:
        gender = st.radio("性别",["男","女"])
        target_year = st.number_input("查看流年公历年份",min_value=1920,max_value=2100,value=2026)

    # 嵌入前端JS排盘 iztro‑lib CDN
    html_code = f"""
    <div id="result_box"></div>
    <script src="https://cdn.jsdelivr.net/npm/iztro‑lib@1.4.2/dist/iztro‑lib.iife.js"></script>
    <script>
        const {{astro}} = window.iztroLib;
        const birthY = {birth_y};
        const birthM = {birth_m};
        const birthD = {birth_d};
        const birthH = {hour};
        const gen = "{gender}";
        const tYear = {target_year};

        try{{
            const chart = astro.bySolar(`${{birthY}}‑${{birthM}}‑${{birthD}}`, birthH, gen);
            const transit = chart.getTransitBySolar(`${{tYear}}‑01‑01`);
            const decadal = transit.decadal;
            const decPalace = decadal.palace;
            const soulPal = chart.getSoulPalace();
            const bodyPal = chart.getBodyPalace();
            const fiveClass = chart.getFiveClass();
            const hua = chart.getMutagen();
            const surround = chart.surroundedPalaces(decPalace.index);

            const payload = {{
                birth: `${{birthY}}‑${{birthM}}‑${{birthD}} ${{birthH}}点`,
                gender:gen,
                fiveClass:fiveClass,
                soulPalace:soulPal.translateName(),
                bodyPalace:bodyPal.translateName(),
                decAgeStart:decadal.ageRange[0],
                decAgeEnd:decadal.ageRange[1],
                decPalaceName:decPalace.translateName(),
                targetYear:tYear,
                liuPalace:transit.palace.translateName(),
                decMajors: decPalace.majorStars.map(s=>({{name:s.translateName(),bright:s.translateBrightness()}})),
                decMinors: decPalace.minorStars.map(s=>s.translateName()),
                surroundPalaces: surround.allPalaces().map(p=>({{
                    name:p.translateName(),
                    majors:p.majorStars.map(x=>x.translateName())
                }})),
                hua:{{lu:hua.lu, quan:hua.quan, ke:hua.ke, ji:hua.ji}},
                allPalaces: chart.palaces.map(p=>({{
                    name:p.translateName(),
                    majors:p.majorStars.map(s=>s.translateName()),
                    minors:p.minorStars.map(s=>s.translateName())
                }}))
            }};
            //把json传回streamlit
            window.parent.postMessage({{type:"iztro_result", data:payload}},"*");
            document.getElementById("result_box").innerText="✅前端排盘完成，请查看下方报告";
        }}catch(e){{
            document.getElementById("result_box").innerText="❌排盘异常:"+String(e);
            window.parent.postMessage({{type:"iztro_error", msg:String(e)}},"*");
        }}
    </script>
    """
    st.components.v1.html(html_code, height=120)

    btn_calc = st.button("🚀生成完整命盘&大限流年解析报告",type="primary")
    if btn_calc:
        st.info("⚠️本版本受限于streamlit组件，JS排盘在浏览器运行；如无输出，刷新页面重试。")
        st.markdown("""
> 💡架构说明：排盘逻辑使用iztro‑lib浏览器js版本，**不再需要云端pip编译任何排盘库**，解决requirements安装失败。
> 知识库逻辑依旧完全参考《紫微斗数精成》大德山人：本命为体，大限为体，流年为用，三方四正参合、空宫借对宫。
""")
        st.warning("注意：streamlit的python拿不到浏览器js返回数据！❗❗❗")
        st.markdown("""
### 🛑重要限制
Streamlit的`components.v1.html`**单向渲染，python无法接收浏览器postMessage返回的JSON数据**。
> 👉两个可行出路：
> 方案A：直接做**纯静态HTML单页应用**（全部JS，不需要streamlit，github pages直接托管，100%使用iztro‑lib完整排盘，全部功能，无部署报错）。
> 方案B：退回到【表单演示】，不做自动排盘。
""")

# ========== 麻衣神相Tab ==========
with tab_mayi:
    st.subheader("🧏‍♂️麻衣神相（面相解析，源自麻衣神相PDF）")
    st.info("""
    ⚠️ 注意：麻衣神相是**看人脸照片**，本程序仅输出古籍理论，无法自动识别人脸疤痕、纹路气色。
    """)
    from PIL import Image
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
💡现状说明：
1. Python的iztro库在Streamlit Cloud免费环境编译会超时，导致`Error installing requirements`，无法部署。
2. iztro‑lib JS版本功能完整，但Streamlit组件无法双向通信拿结果。
✅最佳方案：直接输出一份**独立完整静态HTML文件**（纯前端，不需要python/streamlit），放到Github Pages，浏览器打开就可以完整排盘、分析大限流年、三方四正、四化，完全复现《紫微斗数精成》逻辑，没有任何部署报错。
""")
