# 剧本大纲：天宝十载（751）

> **一句话钩子**：盛世只剩最后四年。你是唐玄宗，你能阻止安史之乱吗？
>
> 场景 id：`tianbao_751`　回合单位：季　标准局 20 季（751 春 → 755 冬）＋最多 4 季「乱局终章」（756）　延长模式见 §2.4。

**标注约定**

- 【史】：史籍可考的事实，写作时仍应对照《资治通鉴》卷 216–218、两《唐书》本传。
- 【虚】：本游戏的设计虚构，包括数值、概率、反事实分支和台词。
- [待核实]：作者没有把握的日期、官衔或数字。在核实之前，不要写进 YAML 的 `persona` 或者奏疏正文。
- **回合记法**：本文 `Tn` 一律指引擎 `state.turn = n`，等同于 `when: {turn: n}`，即「结算进入第 n 回合时」。开局状态是 T0（天宝十载春），所以 T0 的奏疏属于序章脚本，不是事件。

| 年 | 春 | 夏 | 秋 | 冬 |
|---|---|---|---|---|
| 751 天宝十载 | T0 | T1 | T2 | T3 |
| 752 天宝十一载 | T4 | T5 | T6 | T7 |
| 753 天宝十二载 | T8 | T9 | T10 | T11 |
| 754 天宝十三载 | T12 | T13 | T14 | T15 |
| 755 天宝十四载 | T16 | T17 | T18 | **T19 起兵** |
| 756 天宝十五载／至德元载 | T20 | T21 马嵬 | T22 灵武 | T23 |

季与农历月的对应：春为正月至三月，夏为四月至六月，秋为七月至九月，冬为十月至十二月。

---

## 1. 历史底稿

### 1.1 751 年的帝国态势【史】

| 主题 | 要点 | 可信度 |
|---|---|---|
| 宰相 | 李林甫任右相（天宝元年中书令改称右相）。他自开元末独揽相权，打击政敌，屡兴大狱。陈希烈任左相，凡事附和。 | 【史】 |
| 李林甫之死 | 天宝十一载（752）十一月卒。杨国忠继任右相，此后追削李林甫官爵（753 年初，[待核实]月）。 | 【史】，追削月份待核实 |
| 杨国忠 | 本名杨钊，杨贵妃从祖兄，天宝九载（750）赐名「国忠」[待核实月]。751 年以御史中丞、判度支等身份兼领多使 [待核实具体衔]。曾奏报府库充盈，深得玄宗信任。 | 部分待核实 |
| 杨氏外戚 | 天宝四载（745）册杨玉环为贵妃。三位姊妹封韩国、虢国、秦国夫人（748，[待核实]）。杨铦、杨锜等亲族同样显贵。 | 【史】 |
| 高力士 | 内廷第一人，章奏多先经他手；天宝七载（748）加骠骑大将军 [待核实]。754 年秋霖期间，他向玄宗谏言宰相专权、边将兵权过盛 [待核实时间]。 | 【史】 |
| 安禄山 | 天宝元年（742）任平卢节度使，天宝三载（744）兼范阳，天宝十载（751）二月再兼河东。天宝九载（750）封东平郡王 [待核实]。751 年正月过生日时，贵妃以「洗儿」戏之 [待核实日]。旗下有曳落河约八千人，由同罗、奚、契丹降众组成。 | 年份可靠，月日待核实 |
| 安禄山对契丹 | 751 年秋讨伐契丹，在土护真水大败 [待核实月、兵力]。 | 部分待核实 |
| 哥舒翰 | 天宝六载（747）起任陇右节度使。天宝八载（749）攻下石堡城，士卒死亡数万。752 年前后兼河西 [待核实]，后封西平郡王 [待核实]。与安禄山不和。755 年中风，留居长安 [待核实月]。 | 部分待核实 |
| 高仙芝·怛罗斯 | 时任安西四镇节度使。751 年初入朝献俘，朝廷一度想调他去河西，引发「河西诸胡割耳请留安思顺」的风波 [待核实]。751 年在怛罗斯被大食击败，葛逻禄临阵倒戈 [待核实月]。唐军兵力，《通鉴》作「三万」，其他史料说法不一。 | 年份可靠，细节待核实 |
| 南诏 | 云南太守张虔陀凌辱南诏王阁罗凤，阁罗凤反攻姚州 [待核实]。天宝十载（751）四月，鲜于仲通领兵约八万征讨，在西洱河（泸南）大败，死亡约六万 [待核实数字]。杨国忠掩盖败绩、反为其叙功。752 年南诏改附吐蕃 [待核实]。754 年李宓再征南诏，全军覆没 [待核实月、兵力]。 | 主干可靠 |
| 王忠嗣 | 天宝五载（746）一度兼领河西、陇右、朔方、河东四镇。747 年不肯强攻石堡，被李林甫诬陷「欲奉太子」，下狱后贬官。天宝八载（749）卒 [待核实]。 | 【史】 |
| 用蕃将 | 天宝六载（747）前后，李林甫建议以「寒族、胡人」为边帅，以杜绝出将入相之路。 | 【史】 |
| 安思顺 | 安禄山的族兄 [亲属关系待核实]。751 年任河西节度使 [待核实]。752 年李林甫辞去遥领的朔方，荐安思顺接任 [待核实]。755 年冬被召还任户部尚书，756 年被杀 [待核实]。 | 多处待核实 |
| 封常清 | 751 年是高仙芝的判官 [待核实]，此后升任安西、北庭节度使（753–754，[待核实]）。755 年入朝时乱起，他在洛阳招募新兵，兵败。 | 部分待核实 |
| 郭子仪、李光弼 | 郭子仪 751 年为朔方军将 [待核实具体职]。755 年冬接替安思顺任朔方节度使。李光弼 751 年在河西、朔方军中任副使一类职务 [待核实]。756 年初经郭子仪举荐，任河东节度使。 | 部分待核实 |
| 颜氏兄弟 | 颜真卿 753 年被排挤出京，任平原太守。颜杲卿原在范阳幕府 [待核实职]，后任常山太守 [待核实年]。756 年正月常山陷落，颜杲卿殉国。 | 【史】 |
| 太子李亨 | 开元二十六年（738）立为太子。天宝五载至六载（746–747）间，韦坚案、杜有邻案相继牵连东宫，太子两度离弃妃嫔以求自保。756 年七月在灵武即位。 | 【史】 |
| 兵制 | 府兵制逐渐瓦解。开元年间先改为募兵宿卫（彍骑），再于边镇设「长征健儿」。天宝八载（749）停止折冲府上下鱼书 [待核实]。 | 【史】 |
| 外重内轻 | 天宝元年（742），沿边十节度及经略使共有镇兵约 49 万、战马约 8 万（见《通鉴》卷 215）。京畿宿卫早已名存实亡。 | 742 年数据；751 年实数 [待核实] |
| 户籍与漕运 | 均田制和租庸调制逐渐松弛，开元年间宇文融主持括户。关中依赖江淮漕粮：裴耀卿改革漕运（734 前后），韦坚开广运潭（743）。天宝八载（749），诸仓储粮合计约 9600 万石（据《通典》，[待核实]）。754–755 年在籍约 900 万户、5290 万口 [待核实]。 | 待核实 |

### 1.2 通往 755 的事件链【史】

| 时间 | 事件 | 游戏 T |
|---|---|---|
| 751 二月 | 安禄山兼河东节度使，以吉温为副使 [待核实] | T0 序章抉择 |
| 751 四月 | 西洱河之败 | T1 |
| 751 秋 | 怛罗斯之战；土护真水之败 | T2 |
| 752 | 阿布思叛逃 [待核实月]；李林甫辞朔方 | T4–T6 |
| 752 冬 | 玄宗调解哥舒翰与安禄山，二人在宴上失和 [待核实] | T7 |
| 752 十一月 | 李林甫卒，杨国忠拜相 | T7 |
| 754 正月 | 安禄山到华清宫入朝，加左仆射；杨国忠阻止其拜相；随后安禄山匆忙返回范阳 | T12 |
| 754 八月 | 陈希烈罢相，韦见素入相 | T14 |
| 755 二月 | 安禄山请以蕃将三十二人取代汉将，玄宗准许 | T16 |
| 755 [待核实月] | 杨国忠派京兆尹包围安禄山在长安的宅邸，捕杀其门客 | T17–T18 |
| 755 七月 | 安禄山请献马三千匹；达奚珣疑其有诈；中使冯神威召其入朝，被拒 | T18 |
| 755 十一月 | 安禄山在范阳起兵，所部约十五万，号称二十万，以「奉密旨讨杨国忠」为名 | **T19** |
| 755 十二月 | 东都洛阳陷落；封常清、高仙芝被斩 | T19 |
| 756 正月 | 安禄山在洛阳称大燕皇帝；颜杲卿据常山起兵 | T20 |
| 756 六月 | 潼关失守，玄宗出奔，马嵬兵变 | T21 |
| 756 七月 | 太子在灵武即位，改元至德 | T22 |

**本剧本的核心判断**【虚，基于史实的解读】：安禄山起兵，需要三个条件同时成立：他手握过重的兵权（外重内轻），他害怕失去现有地位（杨国忠的逼迫，以及太子即位后可能清算），而且朝廷看起来可以攻取（京畿空虚、朝堂内斗）。玩家可以分别削弱这三个条件，把起兵概率压下去。也可以选择不阻止起兵，转而加强长安、洛阳和潼关的防务，让叛乱很快失败。

---

## 2. 玩家身份与胜负

**身份**：唐玄宗李隆基，751 年时 66 岁（685 年生），已在位近四十年。帝王自身的倦怠用「君威」的缓慢下滑来体现。

### 2.1 三大主目标（常驻于 UI 顶栏）

| # | 目标 | 判定 |
|---|---|---|
| ① 弭兵 | 让「渔阳鼙鼓」不变红。如果叛乱已经发生，守住潼关和长安 | T19 结束时 `rebellion_started` 未发生，且 `rebellion_risk < 60`；或者已经起兵，但到 T23 时京畿和潼关未失守 |
| ② 足食足兵 | 国库与粮储全程不枯竭 | `treasury > 0` 且 `grain > 500`，连续两季归零即触发失败 |
| ③ 皇权在握 | 你在终局时仍掌朝政 | `authority ≥ 50`，未内禅，未发生马嵬之变 |

### 2.2 失败状态（立即终局）

| id | 名称 | 条件 |
|---|---|---|
| fail_changan | 长安不守 | 叛军占据京畿，且皇帝仍在京畿（需要新机制：区域控制权） |
| fail_bankrupt | 帑竭兵变 | `treasury = 0` 与 `grain ≤ 200` 同时持续两季（需要新机制：连续状态计数） |
| fail_regicide | 龙驭宾天【虚】 | 马嵬兵变中，玩家拒绝处置杨氏，且 `authority < 20` |

### 2.3 结局（按优先级依次判定，命中第一个即结束）

| # | 结局 | 触发条件（状态语言） | 性质 |
|---|---|---|---|
| E1 | **天宝中兴·消弭兵祸** | T19 末未起兵；`rebellion_risk < 60`；`authority ≥ 50`；`treasury > 0` | 最佳，【虚】 |
| E2 | **削藩而边陲失** | T19 末未起兵；`fanzhen_power ≤ 40`；`frontier_pressure ≥ 80` | 苦涩，【虚】 |
| E3 | **再造唐室** | 已起兵；到 T23 时潼关和京畿未失守，且东都已收复，或叛军总兵力低于起兵时的一半 | 【虚】 |
| E4 | **渔阳鼙鼓·历史重演** | 已起兵；`tongguan_lost`；马嵬兵变中玩家处置了杨氏 → 退为太上皇 | 【史】 |
| E5 | **杨氏擅国 / 北司掌兵** | 未起兵；`authority ≤ 25`；`court_strife ≥ 80`。若杨国忠在相位，出「杨氏擅国」版本；若 `eunuch_army` 为真，出「北司掌兵」版本 | 【虚】 |
| E6 | **传位东宫** | 玩家主动内禅，或者 `authority ≤ 15` 且太子在世 | 【虚】，提前收场 |
| — | **山雨欲来**（开放结局） | 未起兵，但 `rebellion_risk ≥ 60`：提示玩家进入延长模式 | 【虚】 |

### 2.4 局长

- **标准局**：T0–T19，共 20 季。若叛乱爆发，追加乱局终章，最晚到 T23。
- **延长模式**：到广德元年春（763，史朝义败亡）为止，约 49 季。启用回纥、至德年号，以及安庆绪、史思明的继承事件。需要支持按年号切换「载」与「年」：乾元年间改回称「年」[待核实具体时间]。

---

## 3. 资源与指标（共 10 项）

| id | 名称 | 初值 | 范围 | 主要来源与去向 | 可见性 |
|---|---|---|---|---|---|
| treasury | 国库（万贯，游戏折算） | 3000 | 0– | 各道税基收入；边镇军费（recurring）、赏赐、营建、征伐 | 明 |
| grain | 太仓粮储（万石，游戏折算） | 2500 | 0– | 江淮漕运、和籴；赈济、军粮 | 明 |
| authority | 君威 | 68 | 0–100 | 处置得当则上升；朝争和败报使其下降；每季 −0.3（倦政漂移） | 明 |
| morale | 民心 | 62 | 0–100 | 赈济、减赋使其上升；腐败、边患、强制募兵使其下降 | 明 |
| corruption | 吏治积弊 | 55 | 0–100 | 外戚聚敛、掩败叙功使其上升；御史出巡、罢免贪官使其下降 | 明 |
| frontier_pressure | 边患 | 45 | 0–100 | 吐蕃、南诏、契丹、大食动向；边镇兵力削弱则上升 | 明 |
| an_ambition | 禄山异志 | 40 | 0–100 | 加官、兼镇、被逼迫都会使其上升；入朝留京、真实恩信可使其下降 | **暗**：UI 只显示「风闻区间」 |
| fanzhen_power | 外重内轻（节度兵权集中度） | 70 | 0–100 | 兼镇、蕃将替换汉将使其上升；分镇、整训禁军、调兵入内地使其下降 | 明 |
| court_strife | 朝堂倾轧 | 50 | 0–100 | 相党、外戚、东宫、边帅之间的敌意，包括太子与宰相的关系、杨国忠与安禄山的关系 | 明 |
| **rebellion_risk** | **渔阳鼙鼓（危机计）** | 30 | 0–100 | 由漂移公式综合上述指标，事件另外施加冲击 | 明（显示分项贡献） |

**危机计设计**【虚】：危机计用 `formulas.drift` 计算，现有引擎已能表达。

```text
rebellion_risk += 0.08*(an_ambition-40) + 0.05*(fanzhen_power-55)
                + 0.05*(court_strife-45) - 0.04*(authority-60)
```

| 区间 | 名称 | 后果 |
|---|---|---|
| 0–39 | 承平 | 无 |
| 40–59 | 风闻 | 奏疏开始出现告变条目 |
| 60–79 | 山雨欲来 | T19 的历史起兵事件可以触发 |
| 80–100 | 鼙鼓动地 | 每季都可能提前起兵，≥90 时 gravity 为 0.5 |

UI 用柱条显示四个分项各自的贡献，让玩家看出这一季的风险是被谁推高的。所有系数都需要用 `balance-and-replay-testing` 做重放调参。调参目标：玩家完全不作为时，T19 的值落在 75–90 之间。

其余漂移公式：

- `an_ambition`：`0.03*(fanzhen_power-60)+0.04*(court_strife-50)-0.03*(authority-60)`
- `morale`：`-max(0,corruption-45)*0.04-max(0,frontier_pressure-60)*0.03`
- `authority`：`-0.3-max(0,court_strife-60)*0.03`

---

## 4. 势力与人物

**势力**（`factions.yaml`）：

| id | 名称 | 对唐廷关系 |
|---|---|---|
| tang | 唐廷 | — |
| yan | 大燕（起兵后启用） | — |
| tubo | 吐蕃 | −50 |
| nanzhao | 南诏 | −20，开战后 −60 |
| khitan_xi | 契丹·奚 | −60 |
| dashi | 大食 | −30 |
| huihe | 回纥（延长模式启用） | +20 |

朝内派系不建 faction，而是给人物加一个 `bloc` 标签（loader 会忽略这个额外字段，只供 LLM 使用）：

| bloc | 派系 |
|---|---|
| xiang | 相党 |
| yang | 杨氏外戚 |
| donggong | 东宫 |
| neiting | 内廷 |
| fanyang | 范阳系 |
| xibei | 西北边帅 |
| qingliu | 清流 |

### 4.1 人物基础表

traits 的三项能力值均为【虚】。

| id | 姓名 | 751 年官职 | bloc | 能 / 忠 / 野 | 起始地 | 历史结局 → 事件 |
|---|---|---|---|---|---|---|
| xuanzong | 李隆基 | 皇帝（玩家） | — | 7/–/– | jingji | 756 年入蜀 |
| li_linfu | 李林甫 | 右相，遥领朔方 [待核实] | xiang | 8/6/7 | jingji | 752 十一月卒 → `li_linfu_death` T7，g0.9 |
| yang_guozhong | 杨国忠 | 御史中丞、判度支等 [待核实] | yang | 5/5/8 | jingji | 752 拜相；756 马嵬被杀 → `guozhong_chancellor` 等 |
| yang_guifei | 杨玉环 | 贵妃 | yang | 4/8/2 | jingji | 756 马嵬赐死 |
| gao_lishi | 高力士 | 骠骑大将军，知内侍省 [待核实] | neiting | 7/10/3 | jingji | 延长模式内卒（762） |
| li_heng | 李亨 | 皇太子 | donggong | 6/7/5 | jingji | 756 灵武即位 → `lingwu_accession` |
| chen_xilie | 陈希烈 | 左相 | xiang | 4/5/3 | jingji | 754 罢相 → `xilie_dismissed` T14，g0.6 |
| an_lushan | 安禄山 | 平卢、范阳节度使，东平郡王 | fanyang | 8/4/资源 | **jingji**（正月在京，[待核实]），T1 返回范阳 | 755 起兵 |
| shi_siming | 史思明 | 安禄山部将 [待核实职] | fanyang | 8/3/7 | pinglu | 叛军第二号人物 |
| ji_wen | 吉温 | 求任河东节度副使 [待核实] | fanyang | 5/3/6 | jingji | 755 贬死 [待核实] |
| geshu_han | 哥舒翰 | 陇右节度使 | xibei | 8/7/4 | longyou | 755 中风；756 潼关被俘 |
| gao_xianzhi | 高仙芝 | 安西四镇节度使 | xibei | 8/7/4 | **jingji**（入朝献俘，[待核实]） | 755 十二月被斩 → `feng_gao_executed` |
| feng_changqing | 封常清 | 安西节度判官 [待核实] | xibei | 8/9/3 | anxi | 同上 |
| an_sishun | 安思顺 | 河西节度使 [待核实] | xibei | 6/7/3 | hexi | 756 被杀 [待核实] |
| guo_ziyi | 郭子仪 | 朔方军将 [待核实] | xibei | 9/9/2 | shuofang | 755 任朔方节度使 |
| li_guangbi | 李光弼 | 河西或朔方副将 [待核实] | xibei | 9/8/3 | shuofang | 756 任河东节度使 |
| yan_zhenqing | 颜真卿 | 京官，殿中侍御史等 [待核实] | qingliu | 7/10/2 | jingji | 753 出任平原太守 → `zhenqing_to_pingyuan` T8，g0.6 |
| yan_gaoqing | 颜杲卿 | 范阳幕府属官 [待核实] | qingliu | 7/10/1 | fanyang | 756 正月殉国 |
| xianyu_zhongtong | 鲜于仲通 | 剑南节度使 | yang | 4/6/4 | jiannan | 751 西洱河之败 |
| bian_lingcheng | 边令诚 | 宦官，监军 | neiting | 4/6/5 | jingji | 755 构陷封常清、高仙芝 |

### 4.2 LLM 扮演卡

persona 与口吻都是【虚】的写作，不得引用未经核实的原话。

| id | 人设·口吻 | 想要什么 | 知道什么 | 对玩家的反应 |
|---|---|---|---|---|
| li_linfu | 阴柔周密，口蜜腹剑；说话滴水不漏，常以「陛下圣明」开头再转折 | 固位；压制东宫；继续以蕃将守边 | 百官阴事、东宫过失、边镇奏报 | 顺从时全力办事；被疏远时罗织他的政敌 |
| yang_guozhong | 精于算账、急于立功；夸张、爱表功，好用数字压人 | 相位；扳倒安禄山；聚敛财赋 | 度支账目（会粉饰）；剑南军情（会掩败） | 被重用后愈发跋扈，逼迫安禄山会使 `court_strife↑` 与 `an_ambition↑` |
| yang_guifei | 娇憨而不干政；口语亲昵，谈宴乐、诗与荔枝 | 恩宠，以及家族富贵 | 宫中闲话、安禄山入宫的情形 | 被冷落时杨氏会请托；可间接替安禄山说话 |
| gao_lishi | 老成忠谨；话不多，「老奴」自称，点到为止 | 主上安稳 | 内廷耳目，以及各方真实的风声 | 只在被单独召见时才说真话；是玩家最可靠的情报来源 |
| li_heng | 隐忍谨慎；回答之前先请罪，绝不议论边事 | 保住储位 | 东宫被构陷的旧案 | 受到庇护后忠诚上升；若君威崩塌，他身边的人会劝他自立 |
| an_lushan | 憨直诙谐，以胡人自居，「臣只知有陛下」；拜见时先拜贵妃 | 兵权、恩宠、退路 | 范阳实力；朝中谁要害他 | 表面恭顺。可从三个信号判断他的真实心态：是否奉召、是否请增兵、言谈中是否提到杨国忠 |
| geshu_han | 豪爽刚烈，酒后直言，鄙视安禄山 | 军功与封爵 | 陇右与吐蕃军情 | 可以用来牵制安禄山，但会加剧朝争 |
| gao_xianzhi | 骁勇而贪功，说话简短 | 西域武功 | 西域、大食、葛逻禄 | 主张深入作战（导向怛罗斯之败） |
| feng_changqing | 貌陋而有干才，文辞犀利，务实 | 被赏识 | 安西的兵马与粮储 | 忠诚度极高，适合派到东都主持防务 |
| guo_ziyi / li_guangbi | 前者宽厚稳重，后者严厉寡言 | 职守 | 朔方兵马 | 被破格提拔后，可在 755 年之前提前布局 |
| yan_zhenqing | 刚直，引经据典，不避权贵 | 整肃吏治 | 御史台的弹章 | 敢直言安禄山、杨国忠之事；可派往河北任职 |
| yan_gaoqing | 外表恭顺，内心忠义 | 报国 | **范阳内情**（游戏核心情报源，【虚】） | 若玩家秘密联络他，可在范阳布下暗线 |
| bian_lingcheng | 谨小慎微，借皇命狐假虎威 | 邀功，自保 | 监军时听到的风闻 | 若授他监军之权，`feng_gao_executed` 的触发概率会上升 |

---

## 5. 地图

### 5.1 区域

stats 字段为：繁荣 / 治安 / 防务 / 税基 / 粮产。所有 stat 值、坐标和行程季数都是【虚】。

| id | 名称 | 治所 | stats | 驻军（strength） |
|---|---|---|---|---|
| jingji | 京畿 | 长安 | 80/75/45/20/10 | 京师禁军 40000（北衙与彍骑残部，【虚】，实数 [待核实]） |
| tongguan | 潼关 | — | 30/70/85/2/0 | 无 |
| duji | 都畿 | 洛阳 | 78/70/40/16/12 | 东都留守兵 10000【虚】 |
| hedong | 河东 | 太原 | 60/65/65/10/8 | 河东军 55000 |
| fanyang | 范阳 | 幽州 | 55/70/80/8/6 | 范阳军 91400 |
| pinglu | 平卢 | 营州 | 35/65/70/3/3 | 平卢军 37500 |
| hebei | 河北诸郡 | 魏州、常山、平原 | 70/68/30/14/12 | 无 |
| henan | 河南道 | 汴州、睢阳 | 72/70/30/15/14 | 无 |
| huainan | 淮南 | 扬州 | 75/72/25/14/16 | 无 |
| jiangnan | 江南 | 润州、洪州 | 70/72/20/15/18 | 无 |
| shannan | 山南 | 襄阳、汉中 | 55/68/30/8/8 | 无 |
| jiannan | 剑南 | 成都 | 65/62/50/10/10 | 剑南军 30900 |
| longyou | 陇右 | 鄯州 | 40/65/75/4/4 | 陇右军 75000 |
| hexi | 河西 | 凉州 | 45/66/72/4/5 | 河西军 73000 |
| shuofang | 朔方 | 灵州 | 40/66/72/4/4 | 朔方军 64700 |
| anxi | 安西 | 龟兹 | 35/60/65/2/2 | 安西四镇 24000 |
| beiting | 北庭 | 庭州 | 30/60/62/2/2 | 北庭军 20000 |
| lingnan | 岭南 | 广州 | 55/60/30/6/6 | 岭南五府 15400 |
| tubo | 吐蕃（外） | — | — | 吐蕃军 80000【虚】 |
| nanzhao | 南诏（外） | — | — | 南诏军 40000【虚】 |
| khitan_xi | 契丹·奚（外） | — | — | 契丹·奚 50000【虚】 |
| huihe | 回纥（外，延长模式） | — | — | 未定 |

十节度和经略使的兵数取自《通鉴》天宝元年（742）条，属【史】。751 年的实数 [待核实]，游戏以 742 年的数据作初值，并在 UI 中注明。

### 5.2 邻接与行程

单位为季：1 表示一季之内可以抵达；方括号中是对向邻接的说明。

| 区域 | 邻接 |
|---|---|
| jingji | tongguan 1，shuofang 1，hedong 1，shannan 1，longyou 2，hexi 2，jiannan 2（蜀道） |
| tongguan | jingji 1，duji 1，hedong 1 |
| duji | tongguan 1，henan 1，hebei 1，hedong 1，shannan 1 |
| hedong | jingji 1，tongguan 1，duji 1，hebei 1，fanyang 1，shuofang 1 |
| fanyang | hebei 1，hedong 1，pinglu 1，khitan_xi 1 |
| pinglu | fanyang 1，khitan_xi 1 |
| hebei | fanyang 1，hedong 1，duji 1，henan 1 |
| henan | duji 1，hebei 1，huainan 1，shannan 1 |
| huainan | henan 1，jiangnan 1，shannan 1 |
| jiangnan | huainan 1，shannan 2，lingnan 2 |
| shannan | jiannan 2，此外与 jingji、duji、henan、huainan 各 1 |
| jiannan | longyou 2，nanzhao 2，tubo 2 |
| longyou | hexi 1，tubo 1 |
| hexi | shuofang 1，tubo 1，beiting 2，anxi 3 |
| shuofang | huihe 1 |
| anxi | beiting 1，tubo 2 |
| lingnan | nanzhao 3 |

**地缘要点**：

- **漕运线**：江南 → 淮南 → 河南（汴河）→ 都畿 → 潼关 → 京畿。只要叛军占据河南或都畿任意一处，粮产收入就打对折（需要新机制）。
- **叛军历史路线**：范阳 → 河北 → 都畿 → 潼关 → 京畿。

---

## 6. 事件表

事件的基本语义（引擎现行规则）：

- 每个事件只会触发一次。
- 带 `when` 的事件只有一次触发机会；不带 `when` 的条件事件，每季都会重新掷 gravity。
- `choices` 目前引擎尚未执行（见 §8）。

缩写：`res` = adjust_resource，`flag` = set_flag，`st` = set_character_status，`mv` = move_character；`*` 表示需要新机制。

| # | id | 标题 | when / 条件 | g | effects | choices |
|---|---|---|---|---|---|---|
| 1 | hedong_grant | 河东归禄山 | T1；not `hedong_denied` | 0.95 | `res fanzhen_power +8`；`res an_ambition +3`；`flag hedong_to_an` | — |
| 2 | an_returns | 禄山辞归范阳 | T1；not `an_detained` | 0.9 | `mv an_lushan→fanyang` | — |
| 3 | xier_defeat | 西洱河之败 | T1；`nanzhao_campaign` | 0.8 | `res grain −150`；`res morale −4`；`res frontier_pressure +6`；剑南军兵力 −30000*；`flag xier_defeat` | — |
| 4 | guozhong_coverup | 掩败叙功 | `xier_defeat`；not `guozhong_restrained` | 0.7 | `res corruption +4`；`res authority −2` | 追究仲通：`authority +3`，`court_strife +4` ／ 默许：无 |
| 5 | nanzhao_tribute | 南诏请和 | T1；`nanzhao_appeased` | 0.7 | `res frontier_pressure −4`；`adjust_relation tang↔nanzhao +20` | — |
| 6 | talas | 怛罗斯之战 | T2；`anxi_deep_campaign` | 0.75 | 安西四镇兵力 −15000*；`res frontier_pressure +5`；`res authority −2` | — |
| 7 | khitan_defeat | 土护真水之败 | T2；not `an_forbidden_khitan` | 0.7 | 范阳军兵力 −20000*；`flag an_weakened` | 遣使问罪：`authority +3`，`an_ambition +4` ／ 优诏慰抚：`an_ambition −2`，`authority −2` ／ 乘机分平卢：`fanzhen_power −8`，`an_ambition +6` |
| 8 | abusi_revolt | 阿布思叛逃 | T5 | 0.6 | `res frontier_pressure +5`；`flag abusi_gone` | 准禄山收其部众：`fanzhen_power +4` ／ 归朔方：`fanzhen_power −2` |
| 9 | li_linfu_death | 李林甫薨 | T7 | 0.9 | `st li_linfu dead`；`res court_strife +5`；`flag chancellor_vacant` | — |
| 10 | guozhong_chancellor | 杨国忠拜右相 | T7；`chancellor_vacant`；not `chancellor_chosen` | 0.85 | `appoint yang_guozhong you_xiang`；`res court_strife +8`；`res an_ambition +4` | — |
| 11 | linfu_posthumous | 追削李林甫 | T8；`guozhong_in_power` | 0.7 | `res court_strife +3`；`res an_ambition +3`（禄山兔死狐悲，【虚】） | — |
| 12 | geshu_an_quarrel | 哥安廷争 | T7；`geshu_an_feast` | 0.5 | `res court_strife +4` | — |
| 13 | an_court_visit | 禄山华清宫入朝 | T12；`rebellion_risk < 75` | 0.7 | `mv an_lushan→jingji`；`flag an_at_court` | 留京授相：`an_detained`，`fanzhen_power −10`，`an_ambition +6`，范阳军哗变风险*；纵其归镇：无；加官厚赐：`an_ambition −4`，`treasury −120`，`fanzhen_power +3` |
| 14 | an_flees_back | 禄山疾驰归范阳 | T13；`an_at_court`；not `an_detained` | 0.8 | `mv an_lushan→fanyang`；`res rebellion_risk +3` | — |
| 15 | li_mi_disaster | 李宓南诏覆没 | T13；`guozhong_in_power`；not `nanzhao_appeased` | 0.6 | `res grain −200`；`res morale −6`；`res frontier_pressure +6` | — |
| 16 | autumn_rains | 关中霖雨·力士进言 | T14 | 0.6 | `res grain −120`；`res morale −3`；`remember gao_lishi "边将兵权过盛"` | — |
| 17 | fanjiang_swap | 请以蕃将代汉将 | T16；`rebellion_risk ≥ 50` | 0.85 | — | 准：`fanzhen_power +6`，`rebellion_risk +6` ／ 驳：`an_ambition +3`，`rebellion_risk +2` |
| 18 | guozhong_raid | 京兆围禄山宅 | T17；`guozhong_in_power`；not `guozhong_restrained` | 0.6 | `res rebellion_risk +10`；`res court_strife +5` | — |
| 19 | horse_tribute | 禄山献马三千 | T18；`rebellion_risk ≥ 55` | 0.8 | — | 依达奚珣之议，缓至冬季：`rebellion_risk +2` ／ 受马：京畿防务 −10，`rebellion_risk +4` |
| 20 | summon_refused | 召而不至 | `an_summoned`；`rebellion_risk ≥ 60`（不设 when） | 0.8 | `res authority −5`；`res rebellion_risk +8` | — |
| 21 | fanyang_uprising | **范阳起兵** | T19；`rebellion_risk ≥ 60`；not `rebellion_started` | 0.9 | `flag rebellion_started`；范阳、平卢军改隶 yan*；河东军按 `hedong_to_an` 判定是否跟从*；河北治安 −30；`res authority −10` | — |
| 22 | early_uprising | 禄山提前举兵 | 不设 when；`rebellion_risk ≥ 90`；not `rebellion_started` | 0.5 | 同 #21 | — |
| 23 | feng_gao_executed | 边令诚构陷 | `duji_lost`；not `commanders_trusted` | 0.7 | `st feng_changqing dead`；`st gao_xianzhi dead`；`res authority −4` | — |
| 24 | changshan_rising | 颜杲卿常山举义 | `rebellion_started`；`gaoqing_contacted`，或 g 0.5 | 0.7 | 河北治安 +10；叛军补给 −* | — |
| 25 | mawei | 马嵬驿 | `tongguan_lost` | 0.85 | `flag mawei_mutiny` | 赐死杨氏：转入 E4 ／ 拒绝：若 `authority < 20` 则转入 fail_regicide |

**拆解点**：玩家可以在以下环节阻断历史链。

| 史事环节 | 玩家的阻断手段 |
|---|---|
| #1 河东 | T0 驳回，或另择河东留后 |
| #10 杨国忠拜相 | 李林甫死前先预置宰相，设 `chancellor_chosen` |
| #13 入朝 | 留京授相（高风险，高回报） |
| #18 京兆围宅 | 约束杨国忠，设 `guozhong_restrained` |
| #21 起兵 | 上述各环节综合把危机计压到 60 以下 |
| 起兵之后 | 在河南、都畿预置防务；授郭子仪、李光弼兵权；守潼关、不出战（设 `tongguan_hold`）；信任封常清、高仙芝（设 `commanders_trusted`） |

另外提供两条辅助事件链：

- **东宫被构**（T3、T6，条件为 `court_strife ≥ 60`）：影响 E6 的走向。
- **中使受贿**：派中使去察看安禄山时，`corruption ≥ 50` 则中使受贿回报「禄山忠」，同时把 `an_ambition` 的风闻区间读偏 [事件原型为辅璆琳，年份待核实]。

---

## 7. 前三季奏疏（教程）

每季的天下大势奏疏列出 3–5 条，每条附一句「谏言」。玩家可以把谏言存入谏言库，再在诏书中引用。

### T0 · 天宝十载春（序章）

| # | 奏疏 | 谏言 | 好诏（示例 ops） | 坏诏 |
|---|---|---|---|---|
| 1 | 河东节度出缺，安禄山请求兼领，并荐吉温为副使 | 李林甫：「蕃将无党援，可专任」【虚】；高力士：沉默，私下召见时才吐露担忧 | 驳回，另择河东留后：`flag hedong_denied`、`fanzhen_power −3`；同时赏赐金帛以安其心：`treasury −60`、`an_ambition −2` | 照准并赐铁券：`fanzhen_power +8`、`an_ambition +3` |
| 2 | 禄山生辰，贵妃请行「洗儿」之礼 | 杨国忠：厚赐以示恩宠；颜真卿：礼制不宜 | 依常例赏赐，不许其随意出入禁中 | 厚赐并许其出入宫禁：`corruption +2`、`court_strife +3` |
| 3 | 南诏攻陷姚州，鲜于仲通请发兵八万讨伐 | 杨国忠：主战；高仙芝：西南地势险恶，主张谨慎 | 遣使查办张虔陀之过，许南诏谢罪：`flag nanzhao_appeased` | 准征：`flag nanzhao_campaign`，T1 触发败报 |
| 4 | 高仙芝献俘；朝议欲调高仙芝镇河西，诸胡割耳请留安思顺 | 李林甫：留安思顺；哥舒翰：西北当用汉将【虚】 | 留安思顺于河西，命高仙芝不得擅启边衅：`flag anxi_restrained` | 准许高仙芝讨石国余党：`flag anxi_deep_campaign` |
| 5 | 度支奏府库充盈，请修缮华清宫 | 杨国忠：功在度支 | 拨款整训京畿禁军：`start_project 禁军整训 4 季`，完成后京畿防务 +10、禁军兵力 +10000* | 营建宫室：`treasury −100`、`corruption +3` |

**本季要教给玩家的事**：

- 危机计如何读，四个分项的含义。
- 「不作为就会走向历史」：#1 若不驳回，T1 就会自动触发 `hedong_grant`。
- 安禄山此时身在长安，是唯一一次可以低成本单独召见他的机会。

### T1 · 天宝十载夏

| # | 奏疏 | 好诏 | 坏诏 |
|---|---|---|---|
| 1 | 西洱河败报，杨国忠为鲜于仲通叙功，并请在两京分道募兵；或者南诏请和（取决于 T0 的选择） | 追究败责，罢兵议和 | 强征募兵：`morale −5`、`corruption +3` |
| 2 | 安禄山奏请讨伐契丹，并请调河东兵助战 | 禁止河东兵出境：`flag an_forbidden_khitan` | 准奏 |
| 3 | 关中夏粮不足，江淮漕运待发 | 增修漕运工程：粮产收入 +*；或在关中和籴：`treasury −80`、`grain +120` | 不作处置，秋季粮储吃紧 |
| 4 | 中书奏东宫属官交结边将（仿韦坚案，【虚】） | 庇护东宫，交大理寺复核：太子忠诚 +，`court_strife +2` | 默许李林甫办案：`court_strife +5`，太子关系恶化 |

### T2 · 天宝十载秋

| # | 奏疏 | 好诏 | 坏诏 |
|---|---|---|---|
| 1 | 土护真水败报（#7）：**削藩窗口** | 乘机将平卢另授他人，同时下优诏慰抚；先在京畿布防，以防反弹 | 一面问罪一面加赏，同时推高异志与外重内轻 |
| 2 | 怛罗斯败报，或西域安堵 | 稳守四镇，安抚葛逻禄 | 再次征发西域兵 |
| 3 | 朔方留后人选：李林甫遥领朔方，有意推荐安思顺 | 以郭子仪或李光弼知留后：`flag shuofang_reliable` | 照李林甫之意：`fanzhen_power +2` |
| 4 | 秋税入库；括户之议 | 派御史分道核查：`corruption −3`、`morale −1` | 让杨国忠「变造」轻货充库：`treasury +150`、`corruption +5` |

---

## 8. 新机制需求清单

引擎现状：

- 有资源、区域 stat、flag、turn 等值条件，以及资源漂移公式。
- 事件只触发一次。
- 每个人物只能任一个官职（违反时返回 `OFFICE_HELD`）。
- `Army` 不接受额外字段。
- `choices` 不会被执行。
- 收入只支持单一的 `income.tax`。
- 没有战斗结算。

| # | 需求 | 最小数据模型 | 优先级 |
|---|---|---|---|
| 1 | 条件 DSL 扩展 | `{kind: turn, operator: gte, value: 17}`（复用 `_compare`）；`{kind: character_status, character, value}`；`{kind: character_trait, character, trait, operator, value}`；`{kind: army_strength, faction, operator, value}`；`{kind: office_holder, office, character}` | P0 |
| 2 | 事件抉择 | 事件命中后挂起 `pending_choice{event_id, options[]}`，下一季的诏书阶段由玩家选择，再执行该选项的 ops；超时则执行 `default` | P0 |
| 3 | 兼职 | `Character.offices: list[str]`，`office` 作为主职保留。`appoint` 取消 `OFFICE_HELD` 限制，改由场景配置 `max_concurrent_offices` 控制 | P0 |
| 4 | 结局判定 | 在 scenario.yaml 中加入 `endings: [{id, priority, conditions, title, epilogue_asset}]` 和 `fail_states`。每季结算末尾判定；计数类条件需要 `counter`（见 #10） | P0 |
| 5 | 军队归属与兵力操作 | `Army` 增加 `commander`、`loyal_to`、`quality`（0.5–1.3）；新增 op `adjust_army{army, delta}` 和 `set_army_faction{army, faction}` | P0 |
| 6 | 最小战斗规则 | 移动结算后，若敌对军队同处一个区域：战力 = 兵力 × quality × (1 + 守方区域防务/100 × 守方) × RNG(0.85–1.15)。败方损失 30% 兵力，并退往相邻的己方区域；胜方损失 10%。防务 ≥80 的关隘，攻方需要 2 倍战力，否则相持一季。无守军时攻方占领，需要 `Region.controller` 字段。叛军行军由脚本 AI 控制：沿历史路线前进，遇强敌则停止 | P1（战争居次） |
| 7 | 人物心态模型 | 先以资源 `an_ambition` 实现最小版。通用版在 traits 中加入 `ambition`、`fear`、`gratitude`、`favor`，新增 op `adjust_trait`；起兵倾向 = ambition + fear − gratitude。LLM 扮演时读取由心态派生的「态度标签」，不读原始数值 | P1 |
| 8 | 情报迷雾 | 资源加 `hidden: true` 与 `estimate: {noise_by: corruption, intel_flag}`。UI 只显示区间。召见高力士、颜杲卿暗线可以收窄区间 | P1 |
| 9 | 谏言库 | `advice[]: {id, character, turn, text, tags, cited_by_edict[]}`。仅属叙事，不进入 WorldState 哈希。诏书引用某条谏言时，原文会传给诏令解释器，该大臣 favor +1* | P1 |
| 10 | 计数器与延时 | `set_flag` 支持写入当前回合；新增条件 `flag_age ≥ n`；`counters{id: int}`，用于「连续两季国库为零」这类条件 | P1 |
| 11 | 多项收入、漕运 | `formulas.income` 支持多个键，例如 `grain: {resource: grain, formula: "grain * 3 * route_ok"}`。`route_ok` 由漕运线上各区域的控制方派生 | P2 |
| 12 | 时政任务（奏疏条目） | `memorial_items.yaml: {turn or conditions, title, summary, advisors:[{character, stance, line}], suggested_ops}`。作为教程与 UI 卡片，不直接改变状态 | P1 |
| 13 | 历法修补 | T0 的标签应按 `turn_format` 格式化，而不是显示原始 `start_date`；era 支持各自的 `turn_format`，以处理「载」与「年」的切换 | P2 |
| 14 | 朝议辩论 | `debate{topic, participants[2–4], stance_by_bloc}`。由 LLM 生成发言，结论只能作为谏言入库，不能直接变成 op | P2 |

---

## 9. YAML 落地映射（样例）

**scenario.yaml（节选）**。开局为 751 年正月；`pre_game_turns: 1` 使 T1 显示为「天宝十载夏」，T4 显示为「天宝十一载春」。

```yaml
id: tianbao_751
manifest_version: 1
version: "0.1.0"
requires_engine: ">=0.2.0"   # 依赖 §8 P0 机制
title: 天宝十载
era: 盛唐
start_date: "0751-01-01"
turn_unit: season
currency: 贯
calendar:
  eras:
    - {from_turn: 1, name: 天宝, start_year: 10}
  seasons: [春, 夏, 秋, 冬]
  turn_format: "{era}{year}载{season}"
  number_system: chinese
  pre_game_turns: 1
resources:
  - {id: treasury, name: 国库, initial: 3000, min: 0, unit: 万贯}
  - {id: grain, name: 太仓粮储, initial: 2500, min: 0, unit: 万石}
  - {id: authority, name: 君威, initial: 68, min: 0, max: 100, unit: 点}
  - {id: morale, name: 民心, initial: 62, min: 0, max: 100, unit: 点}
  - {id: corruption, name: 吏治积弊, initial: 55, min: 0, max: 100, unit: 点}
  - {id: frontier_pressure, name: 边患, initial: 45, min: 0, max: 100, unit: 点}
  - {id: an_ambition, name: 禄山异志, initial: 40, min: 0, max: 100, unit: 点, hidden: true}
  - {id: fanzhen_power, name: 外重内轻, initial: 70, min: 0, max: 100, unit: 点}
  - {id: court_strife, name: 朝堂倾轧, initial: 50, min: 0, max: 100, unit: 点}
  - {id: rebellion_risk, name: 渔阳鼙鼓, initial: 30, min: 0, max: 100, unit: 点}
stats:
  - {id: prosperity, name: 繁荣, range: [0, 100]}
  - {id: order, name: 治安, range: [0, 100]}
  - {id: defense, name: 防务, range: [0, 100]}
  - {id: tax, name: 税基, range: [0, 100]}
  - {id: grain, name: 粮产, range: [0, 100]}
offices:
  - {id: emperor, name: 皇帝}
  - {id: you_xiang, name: 右相, requires: {ability: 5}}
  - {id: zuo_xiang, name: 左相, requires: {ability: 3}}
  - {id: fanyang_jds, name: 范阳节度使, requires: {ability: 6}}
  - {id: hedong_jds, name: 河东节度使, requires: {ability: 6}}
  - {id: shuofang_jds, name: 朔方节度使, requires: {ability: 6}}
  - {id: jingzhao_yin, name: 京兆尹, requires: {ability: 4}}
edict_categories:
  - {id: military, name: 军务, hint: 节度、禁军、关防、征伐}
  - {id: interior, name: 内政, hint: 任免、财赋、漕运、赈济、吏治}
  - {id: diplomacy, name: 外交, hint: 吐蕃、南诏、契丹、大食、回纥}
  - {id: other, name: 其他, hint: 宫廷、礼仪、东宫、密旨}
formulas:
  income:
    tax: {resource: treasury, formula: "tax * 1.5"}
  drift:
    rebellion_risk: "0.08*(an_ambition-40) + 0.05*(fanzhen_power-55) + 0.05*(court_strife-45) - 0.04*(authority-60)"
    an_ambition: "0.03*(fanzhen_power-60) + 0.04*(court_strife-50) - 0.03*(authority-60)"
    authority: "-0.3 - max(0, court_strife-60)*0.03"
    morale: "-max(0, corruption-45)*0.04 - max(0, frontier_pressure-60)*0.03"
settings:
  afterlife_chat: false
  history_gravity_default: 0.6
  campaign_turns: 20
  epilogue_turns: 4
```

**characters.yaml（节选）**。安禄山因为兼任平卢、范阳，需要 §8 #3 的多职机制；在此之前先把主职写成 fanyang_jds。

```yaml
- id: an_lushan
  name: 安禄山
  faction: tang
  bloc: fanyang
  office: fanyang_jds
  region: jingji
  traits: {ability: 8, loyalty: 4}
  persona: 平卢、范阳节度使，东平郡王。体态肥硕，以胡人憨直自处，深得玄宗与贵妃宠信；手握东北重兵，畏惧宰相与东宫。
  speech_style: 自称"臣胡人"，言辞憨直诙谐，遇到问兵权的事就转而表忠心。
  knowledge: [范阳兵马, 契丹奚事, 朝中谁欲害己]
- id: li_linfu
  name: 李林甫
  faction: tang
  bloc: xiang
  office: you_xiang
  region: jingji
  traits: {ability: 8, loyalty: 6}
  persona: 右相，执政近二十年，善于揣摩上意，排斥异己，主张以蕃将镇守边疆。
  speech_style: 措辞周密，先颂圣而后转折，从不正面否定。
  knowledge: [百官阴事, 东宫旧案, 边镇奏报]
- id: gao_lishi
  name: 高力士
  faction: tang
  bloc: neiting
  region: jingji
  traits: {ability: 7, loyalty: 10}
  persona: 内廷宿老，侍奉陛下数十年，谨守本分，只在独对时才直言。
  speech_style: 自称"老奴"，话少而点到为止。
  knowledge: [内廷耳目, 各方风声]
```

**events.yaml（节选）**。条件只使用现行 DSL 能表达的部分；`choices` 要等 §8 #2 实现后才会生效。

```yaml
- id: hedong_grant
  title: 河东归禄山
  kind: scheduled
  when: {turn: 1}
  conditions: {not: {kind: flag, key: hedong_denied, value: true}}
  gravity: 0.95
  effects:
    - {op: adjust_resource, resource: fanzhen_power, delta: 8, reason: 安禄山兼领三镇}
    - {op: adjust_resource, resource: an_ambition, delta: 3, reason: 兵权日重}
    - {op: set_flag, key: hedong_to_an, value: true}
  illustration: event.hedong_grant.illustration
- id: li_linfu_death
  title: 李林甫薨
  kind: scheduled
  when: {turn: 7}
  gravity: 0.9
  effects:
    - {op: set_character_status, character: li_linfu, status: dead, cause: 病卒}
    - {op: adjust_resource, resource: court_strife, delta: 5, reason: 相位出缺}
    - {op: set_flag, key: chancellor_vacant, value: true}
  illustration: event.li_linfu_death.illustration
- id: fanyang_uprising
  title: 范阳起兵
  kind: scheduled
  when: {turn: 19}
  conditions:
    all:
      - {kind: resource, id: rebellion_risk, operator: gte, value: 60}
      - {not: {kind: flag, key: rebellion_started, value: true}}
  gravity: 0.9
  effects:
    - {op: set_flag, key: rebellion_started, value: true}
    - {op: adjust_region, region: hebei, stat: order, delta: -30}
    - {op: adjust_resource, resource: authority, delta: -10, reason: 渔阳鼙鼓动地来}
    # 待 §8 #5：set_army_faction fanyang_army→yan, pinglu_army→yan
  illustration: event.fanyang_uprising.illustration
```

**armies.yaml（节选）**。`Army` 是 `extra=forbid`，所以 commander 字段要等 §8 #5 实现后才能添加。

```yaml
- {id: fanyang_army, name: 范阳军, faction: tang, region: fanyang, strength: 91400}
- {id: jinjun, name: 京师禁军, faction: tang, region: jingji, strength: 40000}
```

---

## 10. 美术需求

### 10.1 服制（盛唐常服）

- **品级与袍色**【史】：三品以上服紫，四品、五品服绯，六品、七品服绿，八品、九品服青（上元年间又细分深浅 [待核实]）。
- **常服形制**：头戴黑色幞头（盛唐多为软脚），身着圆领缺胯袍，腰系革带（有銙），足蹬乌皮靴。
- **鱼袋与笏板**：三品以上佩金鱼袋，五品以上佩银鱼袋。五品以上执象笏，六品以下执竹木笏 [待核实]。
- **皇帝**：常服为赭黄（柘黄）袍，配折上巾。

### 10.2 人物立绘（768×1024）

| 人物 | 服色 | 要点 |
|---|---|---|
| 玄宗 | 赭黄 | 66 岁，须发斑白，倦怠而威严；背景为华清宫 |
| 李林甫 | 紫，金鱼袋 | 面容和煦而眼神阴冷；背景为中书省的案牍 |
| 杨国忠 | 绯，后期转紫 | 精明外露，手持算筹或账簿；拜相后换紫袍立绘 |
| 杨贵妃 | — | 盛唐女装：高腰长裙、披帛、高髻、花钿，体态丰腴 |
| 高力士 | 紫 | 内侍，面白无须，神情沉静 |
| 太子李亨 | [待核实] | 东宫服色待核实；神情忧惧 |
| 陈希烈 | 紫 | 唯诺 |
| 安禄山 | 紫 | 体态极肥硕，胡人面相；另备一张身着铠甲的「起兵后」立绘 |
| 史思明 | — | 戎装，瘦削鹰视 |
| 吉温 | 绯或绿 [待核实] | — |
| 哥舒翰 | 紫，备铠甲版 | 突骑施后裔，豪迈 |
| 高仙芝 | 紫，备铠甲版 | 高句丽后裔，英俊 |
| 封常清 | 绿或绯 [待核实] | 瘦小跛足 [待核实] |
| 安思顺 | 紫 | 粟特裔边帅 |
| 郭子仪、李光弼 | 751 年品级 [待核实] | 各备戎装版 |
| 颜真卿 | 绿 [待核实] | 方正端严，持笏 |
| 颜杲卿 | 绿 | 幕府文吏 |
| 鲜于仲通 | 紫 | — |
| 边令诚 | 绿或绯 | 宦官监军 |

### 10.3 事件插画（1344×768，共 14 张）

| 事件 | 画面 |
|---|---|
| 河东归禄山 | 诏书与三镇旌节 |
| 禄山生辰·洗儿 | 宫中锦绣，避免猎奇 |
| 西洱河之败 | 苍山洱海与溃兵 |
| 怛罗斯之战 | 中亚河谷 |
| 土护真水之败 | — |
| 李林甫薨 | 空置的相府 |
| 杨国忠拜相 | — |
| 华清宫入朝 | 骊山温泉、冬雾 |
| 关中霖雨 | — |
| 蕃将代汉将 | 校场易帜 |
| 献马三千 | — |
| 范阳起兵 | 夜色中的鼙鼓与烽火 |
| 潼关之战 | 黄河峡谷 |
| 马嵬驿 | 克制表现，不直接描绘死亡 |

另需各结局的终章图 6 张。

### 10.4 地图

- **底图**：盛唐疆域，2048×1536，无文字。画出黄河、长江、汴河漕运线，标示秦岭、太行、潼关峡谷，以及西域、吐蕃高原的边缘。
- **区域多边形**：按 §5 的 22 个区域绘制。
- **图层**：节度辖区着色；军队棋子；漕运线（受阻时变红）；危机计状态下的「烽燧」动画点（风闻及以上阶段）。
- **区域卡**：22 张，1024×576。

### 10.5 UI

| 元素 | 用途 |
|---|---|
| 顶栏 | 唐代宝相花与卷草纹 |
| 诏书纸 | 黄麻纸纹理（唐代诏敕用黄麻纸） |
| 朝堂背景 | 含元殿或大明宫远景 |
| 奏疏横幅 | — |
| 危机计 | 皮鼓与鼓槌图标，按 4 段区间变色 |
