import streamlit as st

# ====================== 知识库 源自《紫微斗数精成》大德山人 ======================
knowledge_intro = """
> 📖 理论来源：《紫微斗数精成》大德山人
**核心规则：本命盘为【体】（先天静盘，格局根基）；大限、流年为【用】（后天动运）**
1. 大限(大运)：每一宫管10年；**阳男阴女顺行，阴男阳女逆行**；起运岁数由五行局决定，全部使用虚岁。
2. 论大限：重点看大限本宫 + **三方四正**；看主星庙旺失陷、四化禄权科忌、六吉六煞组合。
3. 论流年：流年**不能独立论吉凶！流年吉凶依附当前大限。**
   - 大限吉，流年凶只是短暂波折；大限凶，流年吉多镜花水月，不宜大举投入。
4. 三方四正：本宫+三合三宫叫三方；对宫叫四正；论限运不能只看本宫，必须参合。
5. 空宫规则：本宫无主星，必须向对宫借星曜一起参断，吉凶打折扣。
6. 四化：化禄(财缘机遇)、化权(权力竞争)、化科(名声贵人)、化忌(阻滞是非损耗)。
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

st.set_page_config(page_title="紫微斗数｜《紫微斗数精成》录入解析", layout="wide")
st.title("🔮紫微斗数解析（参考《紫微斗数精成》大德山人）")

st.warning("""
⚠️ 重要说明：
1. 文墨天机APP复制文本**不包含动态大限、流年数据**；环形竖排截图开源OCR识别基本失效，本程序不再做图片识别。
2. 操作方式：打开文墨天机，**手动看盘，抄录大限、流年信息填入表单**；图片仅做预览对照。
3. 本程序为国学娱乐演示，不做人生重大决策依据。
""")

tab_ziwei, tab_mayi = st.tabs(["📅紫微斗数｜手动录入大限流年","🧏麻衣神相（人脸面相）"])

with tab_ziwei:
    st.markdown(knowledge_intro)
    st.divider()

    st.subheader("🖼️上传文墨天机截图（仅预览，程序不会识别图片）")
    up_img = st.file_uploader("上传星盘截图 png/jpg/jpeg", type=["png","jpg","jpeg"])
    if up_img is not None:
        from PIL import Image
        img_obj = Image.open(up_img)
        st.image(img_obj, caption="截图仅供你对照录入表单", width="stretch")

    st.divider()
    st.subheader("📝【第一步】本命基础信息录入（参考文墨天机）")
    col_base1,col_base2 = st.columns(2)
    with col_base1:
        gender_z = st.radio("性别",["男","女"])
        yang_yin_type = st.radio("出生年属性（决定大限顺逆行）",["阳年(阳男阴女顺行)","阴年(阴男阳女逆行)"])
        wu_xing_ju = st.selectbox("五行局（决定大限起运虚岁）",["水二局","木三局","金四局","土五局","火六局"])
    with col_base2:
        birth_note = st.text_input("生辰备注（仅给自己看，不参与运算）",placeholder="例：公历1990‑05‑20 辰时")

    st.divider()
    st.subheader("📝【第二步】录入当前【大限】信息（文墨天机底部切换到大限看）")
    col_d1,col_d2 = st.columns(2)
    with col_d1:
        d_start_age = st.number_input("大限开始虚岁",min_value=2,max_value=110,value=23)
        d_end_age = st.number_input("大限结束虚岁",min_value=3,max_value=120,value=32)
        d_palace = st.selectbox("大限所落宫",list(palace_info.keys()))
    with col_d2:
        d_stars = st.multiselect("大限宫内主星",list(main_star_dict.keys()))
        d_huas = st.multiselect("大限宫内四化",list(four_hua.keys()))

    st.divider()
    st.subheader("📝【第三步】录入流年信息（可选，依附大限判断）")
    col_l1,col_l2 = st.columns(2)
    with col_l1:
        in_year = st.number_input("要查看的流年公历年份",min_value=1900,max_value=2100,value=2026)
        liu_nian_palace = st.selectbox("流年命宫",list(palace_info.keys()))
    with col_l2:
        liu_huas = st.multiselect("流年四化",list(four_hua.keys()))

    st.divider()
    btn_run = st.button("🔍生成解析报告（依据紫微斗数精成）",type="primary")
    if btn_run:
        st.success("# 📜解析报告")
        st.markdown(f"""
> 基础信息：{gender_z}｜{yang_yin_type}｜{wu_xing_ju}
> 当前大限：虚岁 {d_start_age}‑{d_end_age}，大限落【{d_palace}】
> 流年参考：{in_year}年，流年命宫【{liu_nian_palace}】
""")
        st.info(f"**大限本宫本义：** {palace_info[d_palace]}")

        st.markdown("### ✨大限宫内主星解读")
        if len(d_stars)>0:
            for s in d_stars:
                st.write(f"- **{s}**：{main_star_dict[s]}")
        else:
            st.write("> ⚠️大限本宫无主星，【空宫】，必须借**对宫星曜**参合吉凶，格局力量打折扣。")

        st.markdown("### ✨大限宫内四化")
        if len(d_huas)>0:
            for h in d_huas:
                st.write(f"- {four_hua[h]}")
        else:
            st.write("大限宫内无四化。")

        st.divider()
        st.markdown("## 📖《紫微斗数精成》核心断语")
        st.markdown("""
1. 📌**大限为体，流年为用。** 不要单看流年好坏，根基看大限格局。
2. 看大限不能只看本宫，**必须参看三方四正（三合+对宫）综合评判格局高低。**
3. 流年只是触发事件：
    - 如果本大限整体格局吉：就算流年遇煞，只是短期波折，守静即可，不必恐慌；
    - 如果本大限格局差：流年看到禄、科也容易镜花水月，机会看得见拿不到，切忌大额投入、冒险变动。
4. 空宫借对宫：本宫没有主星，全盘分析必须把对宫主星、四化拿过来一起看。
""")
        if len(liu_huas)>0:
            st.markdown("### ✨流年四化提示")
            for lh in liu_huas:
                st.write(f"- {four_hua[lh]}")

        st.info("💡实操建议：回到文墨天机，点开【三方四正】，把三合宫、对宫的星星再记录，分析会更完整。")

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

**无主星（空宫）规则**
> 本宫没有主星，要向对宫借全部星曜来论断，吉凶打折扣。
""")

# ========== 麻衣神相Tab ==========
with tab_mayi:
    st.subheader("🧏‍♂️麻衣神相（面相解析，源自麻衣神相PDF）")
    st.info("""
    ⚠️ 注意：麻衣神相是**看人脸照片**！！不要上传紫微星盘截图。
    依据：识限歌三段大限，十三部位流年歌，三停十二宫。
    程序无法AI视觉识别人脸疤痕、纹路，仅输出古籍理论框架。
    """)
    up_face = st.file_uploader("上传人脸正面照片", type=["png","jpg","jpeg"])
    if up_face is not None:
        from PIL import Image
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
> - 紫微斗数：出生时间排盘（文墨天机），《紫微斗数精成》；大限=十宫轮走，虚岁起运，阳男阴女顺逆。
> - 麻衣神相：看真人脸部照片，识限歌分三段面相大限。

📌使用流程：
1. 文墨天机排盘；底部切换到大限，记下：大限虚岁区间、落哪一宫、宫内星星、四化；
2. 切换流年，记下流年命宫、流年四化；
3. 全部填入网页表单，点击生成解析报告。
""")
