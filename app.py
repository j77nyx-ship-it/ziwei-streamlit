<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>紫微斗数解析</title>

    <!-- 使用 iztro -->
    <script src="https://cdn.jsdelivr.net/npm/iztro@2.6.0/dist/iztro-v2.6.0.min.js"></script>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background: #f7f3ee;
            font-family:
                "Microsoft YaHei",
                "PingFang SC",
                system-ui,
                sans-serif;
            padding: 24px;
            color: #2c2c2c;
            line-height: 1.7;
        }

        .container {
            max-width: 920px;
            margin: 0 auto;
            background: #fff;
            padding: 32px;
            border-radius: 14px;
            box-shadow: 0 2px 14px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            color: #8b4513;
            margin-bottom: 12px;
            font-size: 28px;
        }

        .warn {
            background: #fff2dc;
            border-left: 4px solid #cd853f;
            padding: 14px 16px;
            margin: 16px 0 22px;
            border-radius: 6px;
        }

        .tab-wrap {
            margin: 20px 0;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        .tab-btn {
            padding: 10px 18px;
            background: #e9d9c8;
            border: none;
            font-size: 16px;
            cursor: pointer;
            border-radius: 6px;
        }

        .tab-btn.active {
            background: #9b5928;
            color: #fff;
        }

        .tab-panel {
            display: none;
            margin-top: 18px;
        }

        .tab-panel.show {
            display: block;
        }

        .row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 14px;
            margin-bottom: 14px;
        }

        @media (max-width: 700px) {
            .row {
                grid-template-columns: 1fr;
            }
        }

        label {
            display: block;
            margin: 8px 0 4px;
            font-weight: 500;
        }

        input,
        select {
            width: 100%;
            padding: 9px 12px;
            border: 1px solid #d4c5b4;
            border-radius: 6px;
            font-size: 15px;
        }

        button#calcBtn {
            margin-top: 12px;
            padding: 11px 22px;
            background: #9b5928;
            color: #fff;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
        }

        button#calcBtn:hover {
            background: #7d461e;
        }

        .report {
            margin-top: 20px;
            padding: 18px;
            background: #faf6f1;
            border-radius: 10px;
            white-space: pre-wrap;
            overflow: auto;
        }

        .expand {
            background: #f6f1ec;
            padding: 16px;
            border-radius: 8px;
            margin-top: 14px;
        }

        h2 {
            color: #703810;
            margin: 24px 0 10px;
            font-size: 20px;
            border-bottom: 2px solid #e9d9c8;
            padding-bottom: 6px;
        }

        .small {
            font-size: 13px;
            color: #777;
            margin-top: 8px;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>🔮 紫微斗数解析</h1>

    <div class="warn">
        ⚠️ 民俗国学娱乐演示，不构成人生决策依据。
        排盘运算在浏览器本地完成，不上传你的生辰数据。
    </div>

    <!-- TAB -->
    <div class="tab-wrap">

        <button
            class="tab-btn active"
            data-tab="tab-ziwei">
            📅 紫微斗数生辰排盘
        </button>

        <button
            class="tab-btn"
            data-tab="tab-mayi">
            🧏 麻衣神相识限歌
        </button>

    </div>


    <!-- ================= 紫微斗数 ================= -->

    <div id="tab-ziwei" class="tab-panel show">

        <div class="expand">

            <h3>📖 核心理论</h3>

            <p>
                <strong>
                    本命盘为【体】，大限流年为【用】。
                </strong>
            </p>

            <ul>

                <li>
                    大限每宫管10虚岁；
                    阳男阴女顺行，
                    阴男阳女逆行。
                </li>

                <li>
                    论大限参合三方四正：
                    本宫 + 三合宫 + 对宫。
                </li>

                <li>
                    流年不能单独论吉凶，
                    需要结合当前大限。
                </li>

                <li>
                    空宫需要借对宫星曜参断。
                </li>

                <li>
                    化禄=机遇收获｜
                    化权=竞争压力｜
                    化科=贵人名声｜
                    化忌=阻滞损耗是非。
                </li>

            </ul>

        </div>


        <h2>📝 输入公历出生信息</h2>


        <div class="row">

            <div>

                <label>
                    出生公历年
                </label>

                <input
                    id="birthY"
                    type="number"
                    value="2000"
                    min="1900"
                    max="2050">

            </div>


            <div>

                <label>
                    出生公历月
                </label>

                <input
                    id="birthM"
                    type="number"
                    value="8"
                    min="1"
                    max="12">

            </div>


            <div>

                <label>
                    出生公历日
                </label>

                <input
                    id="birthD"
                    type="number"
                    value="16"
                    min="1"
                    max="31">

            </div>

        </div>


        <div class="row">

            <div>

                <label>
                    出生小时（24小时制）
                </label>

                <input
                    id="birthH"
                    type="number"
                    value="12"
                    min="0"
                    max="23">

            </div>


            <div>

                <label>
                    性别
                </label>

                <select id="genderSel">

                    <option value="男">
                        男
                    </option>

                    <option value="女">
                        女
                    </option>

                </select>

            </div>


            <div>

                <label>
                    查询流年公历年份
                </label>

                <input
                    id="targetY"
                    type="number"
                    value="2026"
                    min="1920"
                    max="2100">

            </div>

        </div>


        <button id="calcBtn">
            🚀 生成完整大限流年解析报告
        </button>


        <p class="small">
            0点按早子时，23点按晚子时，
            其他时间自动转换为对应时辰。
        </p>


        <div
            class="report"
            id="reportBox">
            请输入出生信息后点击按钮。
        </div>

    </div>


    <!-- ================= 麻衣神相 ================= -->

    <div
        id="tab-mayi"
        class="tab-panel">

        <h2>
            🧏 麻衣神相 · 识限歌
        </h2>

        <p>
            依据页面原有条文；
            实际相法需要人工观察面部特征。
        </p>


        <label>
            输入周岁
        </label>


        <input
            id="mayiAge"
            type="number"
            value="28"
            min="1"
            max="100">


        <button
            id="mayiBtn"
            style="
                margin-top:12px;
                padding:10px 18px;
                background:#9b5928;
                color:#fff;
                border:0;
                border-radius:6px;
            ">

            解析面相大限

        </button>


        <div
            class="report"
            id="mayiReport">
        </div>

    </div>

</div>


<script>

"use strict";


/* =========================================================
   星曜解释
========================================================= */

const starDict = {

    "紫微":
        "帝王星，主领导、尊贵；庙旺有作为，落陷主观固执。",

    "天机":
        "智慧谋略星，思虑多变；喜科星，逢煞容易思虑内耗。",

    "太阳":
        "事业光明星；庙旺贵气，落陷辛劳多口舌是非。",

    "武曲":
        "财星，实干求财；遇煞容易竞争纠纷。",

    "天同":
        "福星，温和享受；落陷容易懒散，怕煞星激发。",

    "廉贞":
        "多变才华星；吉则才华出众，煞多易感情官非困扰。",

    "天府":
        "财库星，稳重保守，喜吉星扶持。",

    "太阴":
        "财星感情星；庙旺柔美，落陷内心多纠结。",

    "贪狼":
        "机遇桃花星；火贪格可横发，煞重欲望泛滥。",

    "巨门":
        "口舌星；化科善辩，化忌口舌官非是非。",

    "天相":
        "印星辅佐；喜吉星，遇煞容易被牵连。",

    "天梁":
        "荫星贵人；庙旺解厄消灾，煞多操心劳碌。",

    "七杀":
        "将星开创魄力；庙旺敢闯，煞重坎坷波折。",

    "破军":
        "变革破旧星；逢吉革新，逢煞破败损耗。"

};


/* =========================================================
   十二宫解释
========================================================= */

const palaceDict = {

    "命宫":
        "本人性格天赋，全盘太极原点。",

    "兄弟":
        "兄弟姐妹、平辈伙伴朋友。",

    "夫妻":
        "感情婚姻，配偶状态。",

    "子女":
        "晚辈、子女、下属。",

    "财帛":
        "求财、现金收入。",

    "疾厄":
        "身体隐患、病痛灾厄。",

    "迁移":
        "外出机遇，对外社会际遇。",

    "仆役":
        "下属、朋友，贵人小人。",

    "官禄":
        "事业、工作、功名。",

    "田宅":
        "房产、家庭、库藏积蓄。",

    "福德":
        "精神福气，心态享受。",

    "父母":
        "长辈、文书契约、出身。"

};


/* =========================================================
   24小时 → iztro时辰序号
========================================================= */

function hourToTimeIndex(hour) {

    hour = Number(hour);

    if (hour === 0) {
        return 0;
    }

    if (hour === 23) {
        return 12;
    }

    return Math.floor((hour + 1) / 2);

}


/* =========================================================
   安全取得名称
========================================================= */

function safeName(obj) {

    if (!obj) {
        return "未知";
    }

    if (typeof obj === "string") {
        return obj;
    }

    if (typeof obj.translateName === "function") {
        return obj.translateName();
    }

    return obj.name || "未知";

}


/* =========================================================
   根据索引取得宫位
========================================================= */

function getPalaceByIndex(chart, index) {

    return chart.palaces[
        ((index % 12) + 12) % 12
    ];

}


/* =========================================================
   宫位文字
========================================================= */

function palaceLine(p) {

    const major =
        (p.majorStars || []).length
        ?
        p.majorStars
            .map(s => safeName(s))
            .join(",")
        :
        "无主星";


    const minor =
        (p.minorStars || []).length
        ?
        p.minorStars
            .map(s => safeName(s))
            .join(",")
        :
        "无辅煞";


    return `${safeName(p)}｜主星：${major}｜辅煞：${minor}`;

}


/* =========================================================
   生年四化
========================================================= */

function fourTransformations(chart) {

    const result = {

        lu: "未取到",
        quan: "未取到",
        ke: "未取到",
        ji: "未取到"

    };


    const map = {

        "禄": "lu",
        "权": "quan",
        "科": "ke",
        "忌": "ji"

    };


    chart.palaces.forEach(p => {

        [
            ...(p.majorStars || []),
            ...(p.minorStars || [])

        ].forEach(s => {

            const m = s.mutagen;

            if (
                m &&
                map[m] &&
                result[map[m]] === "未取到"
            ) {

                result[map[m]] =
                    safeName(s);

            }

        });

    });


    return result;

}


/* =========================================================
   TAB
========================================================= */

document
    .querySelectorAll(".tab-btn")
    .forEach(btn => {

        btn.addEventListener(
            "click",
            () => {

                document
                    .querySelectorAll(".tab-btn")
                    .forEach(
                        b =>
                            b.classList
                                .remove("active")
                    );


                document
                    .querySelectorAll(".tab-panel")
                    .forEach(
                        p =>
                            p.classList
                                .remove("show")
                    );


                btn.classList.add("active");


                document
                    .getElementById(
                        btn.dataset.tab
                    )
                    .classList.add("show");

            }
        );

    });


/* =========================================================
   紫微排盘
========================================================= */

document
    .getElementById("calcBtn")
    .addEventListener(
        "click",
        () => {

            const reportDom =
                document.getElementById(
                    "reportBox"
                );


            try {

                /* 检查 iztro */

                if (
                    !window.iztro ||
                    !window.iztro.astro
                ) {

                    throw new Error(
                        "iztro 未成功加载，请检查网络连接或 CDN。"
                    );

                }


                /* 获取输入 */

                const birthY =
                    Number(
                        document
                            .getElementById(
                                "birthY"
                            )
                            .value
                    );


                const birthM =
                    Number(
                        document
                            .getElementById(
                                "birthM"
                            )
                            .value
                    );


                const birthD =
                    Number(
                        document
                            .getElementById(
                                "birthD"
                            )
                            .value
                    );


                const birthH =
                    Number(
                        document
                            .getElementById(
                                "birthH"
                            )
                            .value
                    );


                const gender =
                    document
                        .getElementById(
                            "genderSel"
                        )
                        .value;


                const targetY =
                    Number(
                        document
                            .getElementById(
                                "targetY"
                            )
                            .value
                    );


                /* 检查 */

                if (
                    !Number.isInteger(birthY) ||
                    !Number.isInteger(birthM) ||
                    !Number.isInteger(birthD) ||
                    !Number.isInteger(birthH) ||
                    !Number.isInteger(targetY)
                ) {

                    throw new Error(
                        "出生年月日、小时和查询年份必须是整数。"
                    );

                }


                if (
                    birthH < 0 ||
                    birthH > 23
                ) {

                    throw new Error(
                        "出生小时必须为0-23。"
                    );

                }


                /* 日期 */

                const dateStr =
                    `${birthY}-${birthM}-${birthD}`;


                /* 24小时转时辰 */

                const timeIndex =
                    hourToTimeIndex(
                        birthH
                    );


                /*
                 * iztro 排盘
                 *
                 * bySolar(
                 *     日期,
                 *     时辰序号,
                 *     性别
                 * )
                 */

                const chart =
                    window
                        .iztro
                        .astro
                        .bySolar(
                            dateStr,
                            timeIndex,
                            gender,
                            true,
                            "zh-CN"
                        );


                /* 获取流年 */

                const horoscope =
                    chart.horoscope(
                        `${targetY}-01-01`
                    );


                const dec =
                    horoscope.decadal;


                const year =
                    horoscope.yearly;


                if (
                    !dec ||
                    !year
                ) {

                    throw new Error(
                        "没有取得大限或流年数据。"
                    );

                }


                /* 当前大限宫 */

                const decPal =
                    getPalaceByIndex(
                        chart,
                        dec.index
                    );


                /* 当前流年宫 */

                const yearPal =
                    getPalaceByIndex(
                        chart,
                        year.index
                    );


                /* 命宫 */

                const soulPal =
                    chart.palaces.find(
                        p =>
                            p.name === "命宫"
                    ) ||
                    chart.palaces[0];


                /* 身宫 */

                const bodyPal =
                    chart.palaces.find(
                        p =>
                            p.isBodyPalace
                    );


                /* 四化 */

                const hua =
                    fourTransformations(
                        chart
                    );


                /* =================================================
                   开始报告
                ================================================= */

                let txt =
                    "======= 紫微斗数解析报告 =======\n";


                txt +=
                    `公历生辰：${birthY}-${birthM}-${birthD} ${birthH}点｜性别：${gender}\n`;


                txt +=
                    `时辰序号：${timeIndex}\n`;


                txt +=
                    `农历：${chart.lunarDate || ""}\n`;


                txt +=
                    `干支：${chart.chineseDate || ""}\n`;


                txt +=
                    `五行局：${chart.fiveElementsClass || ""}\n`;


                txt +=
                    `本命命宫：${safeName(soulPal)}｜身宫：${
                        bodyPal
                            ? safeName(bodyPal)
                            : "未知"
                    }\n`;


                txt +=
                    `当前大限：${
                        dec.ageRange
                            ?
                            dec.ageRange[0]
                            + "-"
                            + dec.ageRange[1]
                            : "未知"
                    }虚岁\n`;


                txt +=
                    `大限落宫：【${safeName(decPal)}】\n`;


                txt +=
                    `${targetY}年流年命宫：【${safeName(yearPal)}】\n\n`;


                /* 大限 */

                txt +=
                    "【一、当前大限分析】\n";


                txt +=
                    `大限本宫含义：${
                        palaceDict[
                            safeName(decPal)
                        ]
                        ||
                        "无记录"
                    }\n\n`;


                txt +=
                    "👉大限本宫主星：\n";


                if (
                    (decPal.majorStars || [])
                        .length
                ) {

                    decPal.majorStars
                        .forEach(
                            s => {

                                const n =
                                    safeName(s);


                                txt +=
                                    `- ${n}：${
                                        starDict[n]
                                        ||
                                        "暂无释义"
                                    }\n`;

                            }
                        );

                } else {

                    txt +=
                        "⚠️大限本宫为空宫，需要借对宫星曜一起参断。\n";

                }


                txt +=
                    "\n👉大限宫内辅煞星：\n";


                if (
                    (decPal.minorStars || [])
                        .length
                ) {

                    txt +=
                        decPal.minorStars
                            .map(
                                s =>
                                    safeName(s)
                            )
                            .join("、")
                        +
                        "\n";

                } else {

                    txt +=
                        "大限宫内无辅煞星\n";

                }


                /* 三方四正 */

                txt +=
                    "\n👉大限三方四正：\n";


                const indexes = [

                    dec.index,

                    dec.index + 4,

                    dec.index + 8,

                    dec.index + 6

                ];


                const labels = [

                    "本宫",

                    "三合一",

                    "三合二",

                    "对宫"

                ];


                indexes.forEach(
                    (index, i) => {

                        const p =
                            getPalaceByIndex(
                                chart,
                                index
                            );


                        txt +=
                            `▪${labels[i]}：${palaceLine(p)}\n`;

                    }
                );


                /* 四化 */

                txt +=
                    "\n【二、生年四化】\n";


                txt +=
                    `化禄：${hua.lu}｜化权：${hua.quan}｜化科：${hua.ke}｜化忌：${hua.ji}\n`;


                txt +=
                    "化禄=机缘收获｜化权=竞争压力｜化科=贵人名声｜化忌=阻滞损耗是非\n\n";


                /* 流年 */

                txt +=
                    "【三、大限-流年综合】\n";


                txt +=
                    `当前大限：${
                        dec.ageRange
                            ?
                            dec.ageRange[0]
                            + "-"
                            + dec.ageRange[1]
                            : "未知"
                    }虚岁\n`;


                txt +=
                    `大限宫位：【${safeName(decPal)}】\n`;


                txt +=
                    `${targetY}年流年宫位：【${safeName(yearPal)}】\n`;


                txt +=
                    `流年干支：${
                        year.heavenlyStem || ""
                    }${
                        year.earthlyBranch || ""
                    }\n`;


                txt +=
                    `大限四化：${
                        (dec.mutagen || [])
                            .join("、")
                        ||
                        "无"
                    }\n`;


                txt +=
                    `流年四化：${
                        (year.mutagen || [])
                            .join("、")
                        ||
                        "无"
                    }\n`;


                txt +=
                    "流年用于观察当年的触发点，具体解释仍需结合本命、大限、三方四正及四化。\n\n";


                /* 十二宫 */

                txt +=
                    "【四、本命十二宫简览】\n";


                chart.palaces
                    .forEach(
                        p => {

                            txt +=
                                palaceLine(p)
                                +
                                "\n";

                        }
                    );


                txt +=
                    "\n====报告结束====\n";


                txt +=
                    "提示：仅供国学娱乐参考。";


                reportDom.textContent =
                    txt;

            }


            catch (err) {

                console.error(err);


                reportDom.textContent =
                    "排盘异常：" +
                    (
                        err &&
                        err.message
                            ?
                            err.message
                            :
                            String(err)
                    );

            }

        }
    );


/* =========================================================
   麻衣神相
========================================================= */

document
    .getElementById("mayiBtn")
    .addEventListener(
        "click",
        () => {

            const age =
                Number(
                    document
                        .getElementById(
                            "mayiAge"
                        )
                        .value
                );


            const reportDom =
                document
                    .getElementById(
                        "mayiReport"
                    );


            const list = [

                {
                    name:
                        "第一大限：8-28岁｜上停（发际线-山根，额头为主）",

                    a1: 8,

                    a2: 28,

                    desc:
                        "【识限歌】八岁十八二十八，下至山根上至发。有无活计两头消，三十印堂莫带杀。\n看额头、印堂，光洁无疤纹少年运佳。"
                },


                {
                    name:
                        "第二大限：32-52岁｜中停（山根-准头，鼻子颧骨）",

                    a1: 32,

                    a2: 52,

                    desc:
                        "【识限歌】三二四二五十二，山根上下准头止。禾仓禄马要相当，不识之人莫乱指。\n看鼻子颧骨，宜饱满不宜凹陷断裂。"
                },


                {
                    name:
                        "第三大限：53-73岁｜下停（人中-地阁，嘴巴下巴）",

                    a1: 53,

                    a2: 73,

                    desc:
                        "【识限歌】五三六三七十三，人面排来地阁间。逐一推详看祸福火星百岁印堂添。\n看地阁下巴，宜方圆饱满。"
                }

            ];


            const hit =
                list.find(
                    item =>
                        age >= item.a1 &&
                        age <= item.a2
                );


            if (hit) {

                reportDom.textContent =
                    `### 当前麻衣面相大限：${hit.name}\n\n${hit.desc}\n\n> 实际看相需要肉眼观察面部特征。`;

            } else {

                reportDom.textContent =
                    "不在识限歌三段核心区间，参看过渡岁数，结合相邻部位综合参考。";

            }

        }
    );

</script>

</body>
</html>
