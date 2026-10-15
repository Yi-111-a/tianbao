# 《天宝》剧本美术清单（tianbao_751）

本清单列出剧本 YAML 引用的全部资产 id，作为美术的定稿依据，由剧本作者维护。资产登记（`assets.yaml`）和出图由美术负责。

## 总体要求

风格以 `design/STYLE_GUIDE.md` 为准，所有图像都不带文字。

### 服色

| 品级 | 袍色 |
|---|---|
| 三品以上 | 紫 |
| 四、五品 | 绯（四品深绯，五品浅绯） |
| 六、七品 | 绿 |
| 八、九品 | 碧（青） |

依据见 `docs/FACT_CHECK.md` #36。

### 常服形制

- 头戴黑色软脚幞头，身穿圆领缺胯袍。
- 腰系革带（带銙），足穿乌皮靴。
- 五品以上执象笏。
- 三品以上佩金鱼袋，五品以上佩银鱼袋。

### 皇帝

- 穿赭黄（柘黄）袍，戴折上巾。
- 不画龙纹或团龙，不画明代乌纱帽的硬翅，不画补子。

### 推定的服色

本清单有几处服色是推定的，未经核实，下表中注为「拟」。凡标「拟」的，美术可以按最接近的品级出图，但不要在图上画出可辨认的官印、文字。

## 已知的 id 冲突（需协调）

- 美术提交的立绘 id 用 `portrait.<id>.default` 和 `.armor`，剧本 YAML 也以此为准。但引擎 `sim validate` 现在要求的 id 是 `character.<id>.portrait`、`region.<id>.card`、`ui.topbar.background`、`ui.edict.parchment`、`ui.court.backdrop`、`ui.map.base`、`ui.memorial.banner`。
- 建议 `assets.yaml` 把同一个文件同时登记在两个 id 下。即每张 `.default` 立绘再加一条 `character.<id>.portrait`，`map.base` 再加一条 `ui.map.base`。另一个办法是由引擎负责人放宽校验。

## 1. 人物立绘（768×1024；armor/purple 为第二套）

| id | 人物 | 画面 |
|---|---|---|
| portrait.xuanzong.default | 玄宗李隆基 | 66 岁，须发斑白，神情倦怠而有威仪。身穿赭黄圆领袍，戴折上巾，系革带。背景是华清宫温泉殿的帷幔，雾气淡淡。 |
| portrait.li_linfu.default | 李林甫 | 年老，面容和煦，眼神阴冷。紫袍，佩金鱼袋，执象笏。背景是中书省的案牍和卷轴。 |
| portrait.yang_guozhong.default | 杨国忠（751） | 中年，精明外露，手拿账簿和算筹。绯袍（兵部侍郎，正四品），佩银鱼袋，戴软脚幞头。 |
| portrait.yang_guozhong.purple | 杨国忠（拜相后） | 同一人物，改穿紫袍，佩金鱼袋，神态更加倨傲。背景是政事堂。 |
| portrait.yang_guifei.default | 杨贵妃 | 体态丰腴。高髻上饰花钗，额贴花钿，穿高腰长裙，披帛轻扬，手执团扇或琵琶。背景是梨园的帷幕。不画成媚态。 |
| portrait.gao_lishi.default | 高力士 | 内侍，面白无须，年近七十，神情沉静。紫袍（骠骑大将军），双手拢在袖中。背景是宫门廊下。 |
| portrait.li_heng.default | 太子李亨 | 四十岁上下，面带忧色，举止拘谨。紫袍（皇太子燕服紫），戴幞头。背景是东宫的庭院。 |
| portrait.chen_xilie.default | 陈希烈 | 年长文臣，神态唯诺，微微躬身。紫袍，执笏，案上放着道经。 |
| portrait.an_lushan.default | 安禄山（朝服） | 体态极为肥硕，粟特与突厥混血的面相，须髯浓密，笑容憨厚而目光精明。紫袍（东平郡王），佩金鱼袋。背景是宫中宴席。 |
| portrait.an_lushan.armor | 安禄山（起兵后） | 同一人物，穿唐式明光铠，外罩紫色战袍，立于幽州城头。背景有夜色和烽火，不画旗上的文字。 |
| portrait.shi_siming.default | 史思明 | 胡将，身形瘦削，鹰视，须髯稀疏。穿戎装札甲，配胡式弓韬。背景是营州的草原。 |
| portrait.shi_siming.armor | 史思明（起兵后） | 同一人物，穿札甲、戴兜鍪，持弓立于营州城外的骑阵前。 |
| portrait.ji_wen.default | 吉温 | 中年文吏，眼神机巧，面带笑意。绯袍（拟），执笏。背景是御史台的廊庑。 |
| portrait.geshu_han.default | 哥舒翰（朝服） | 突骑施裔，高鼻深目，须髯粗豪，手持酒盏。紫袍（节度使，拟）。 |
| portrait.geshu_han.armor | 哥舒翰（戎装） | 穿明光铠，持长枪，身后是青海湖畔的营帐。 |
| portrait.gao_xianzhi.default | 高仙芝（朝服） | 高句丽裔，面容英俊，身姿挺拔。紫袍（开府仪同三司）。背景隐约可见献俘的仪仗。 |
| portrait.gao_xianzhi.armor | 高仙芝（戎装） | 穿明光铠，骑白马，背景是葱岭雪山。 |
| portrait.feng_changqing.default | 封常清（朝服） | 身材细瘦，一足偏短，相貌平常而目光锐利，手里拿着文书。绿袍（判官，拟）。 |
| portrait.feng_changqing.armor | 封常清（戎装） | 穿轻甲，站在洛阳城上指挥新募的士卒。 |
| portrait.an_sishun.default | 安思顺 | 粟特裔边帅，神态稳重而略带惶恐。紫袍（节度使，拟）。背景是河西的城堡和驼队。 |
| portrait.guo_ziyi.default | 郭子仪（朝服） | 年过半百，面相宽厚。绯袍（军使，拟）。背景是朔方的营垒。 |
| portrait.guo_ziyi.armor | 郭子仪（戎装） | 穿明光铠，神情沉稳，身后有骑兵队列。 |
| portrait.li_guangbi.default | 李光弼（朝服） | 契丹裔将门之子，面容冷峻，嘴唇紧抿。绯袍（节度副使，拟）。 |
| portrait.li_guangbi.armor | 李光弼（戎装） | 穿札甲，按剑而立，背景是太原的城门。 |
| portrait.yan_zhenqing.default | 颜真卿 | 四十出头，方正端严。绿袍（殿中侍御史，从七品上），执笏。背景是御史台，案上有笔砚。 |
| portrait.yan_gaoqing.default | 颜杲卿 | 中年文吏，外表恭顺，目光坚毅。绿袍（幕府僚佐，拟）。背景是幽州幕府的廊下。 |
| portrait.xianyu_zhongtong.default | 鲜于仲通 | 蜀中豪族出身，神情自负急躁。紫袍（节度使，拟）。背景是成都的城楼和蜀山。 |
| portrait.bian_lingcheng.default | 边令诚 | 宦官，面白无须，身形瘦小，神情谨小而倨傲。绿袍（拟），手里拿着敕书卷轴（卷轴上无字）。 |

## 2. 事件插画（1344×768）

| id | 使用者 | 画面 |
|---|---|---|
| event.xi_er | 奏疏 t0_xier | 宫中锦帐之内，众宫人围拢嬉笑，一个肥硕的胡将被锦绣襁褓戏裹。表现宫廷宴乐的荒诞，不猎奇，不画裸露。 |
| event.hedong_grant | hedong_grant、an_returns、奏疏 t0_hedong | 殿前，内侍捧出三副旌节（旌节上无字），远处是太行山与幽燕的轮廓。 |
| event.xier_defeat | xier_defeat、nanzhao_to_tubo、guozhong_coverup、奏疏 t1_xier_report | 苍山洱海之间，唐军溃兵在雨雾中退却，丢弃的旗帜（无字）倒伏在泥中。 |
| event.nanzhao_tribute | nanzhao_tribute | 南诏使者穿本族服饰，在鸿胪寺的阶下献上方物。 |
| event.talas | talas、奏疏 t2_west | 中亚河谷，夕照下两军对阵，侧翼有骑兵掉转马头。远景，不画特写的厮杀。 |
| event.khitan_defeat | khitan_defeat、an_rebuilds | 暴雨中的草原河谷，范阳骑兵弓弦湿透，阵形散乱。 |
| event.abusi_revolt | abusi_revolt | 同罗部的帐幕在夜里拔营北去，牛羊车队消失在漠北的风沙中。 |
| event.donggong_framed | donggong_framed_1、donggong_framed_2 | 东宫的院落里，太子独自跪在庭前，廊下有御史的身影。光线晦暗。 |
| event.li_linfu_death | li_linfu_death、linfu_resigns_shuofang、linfu_posthumous | 空无一人的相府书房，烛台已经熄灭，案上的笏板和卷轴整整齐齐。 |
| event.guozhong_chancellor | guozhong_chancellor、chen_promoted、zhenqing_promoted、xilie_dismissed | 政事堂内，新任宰相升座，紫袍群臣分列两侧，堂外的车马喧阗。 |
| event.geshu_an_quarrel | geshu_an_quarrel、geshu_stroke | 城东的池亭宴席，两位边帅隔案怒目，内侍居中劝止，酒盏倾倒。 |
| event.zhenqing_to_pingyuan | zhenqing_to_pingyuan | 一个文官骑马出城东行，随从很少，远处是华北平原的城郭。 |
| event.an_court_visit | an_sets_out、an_court_visit、an_flees_back、summon_obeyed | 冬日的骊山华清宫，温泉的雾气缭绕，一个肥硕的胡将在殿前拜舞。 |
| event.li_mi_disaster | li_mi_disaster | 南方的湿热山林，疫气弥漫，唐军营帐残破，士卒相扶而行。克制表现。 |
| event.autumn_rains | autumn_rains | 长安城外连绵的阴雨，渭水泛涨，田间禾稼倒伏，农夫披着蓑衣。 |
| event.fanjiang_swap | fanjiang_swap | 范阳校场上换了旗帜（纯色，无字），胡将们列队受印，汉将默然退立。 |
| event.guozhong_raid | guozhong_raid | 长安坊里的夜色，京兆府吏卒举着火把围住一座大宅，宅门半开。 |
| event.horse_tribute | horse_tribute、envoy_bribed、envoy_truth | 驿道上数千匹战马蜿蜒而行，押马的胡兵很多。远处有一个中使在马上回望。 |
| event.summon_refused | summon_refused | 幽州的节堂，主帅踞坐不起，宣旨的中使捧着敕书（无字）站在阶下，神色惶然。 |
| event.fanyang_uprising | fanyang_uprising、early_uprising、fanyang_mutiny、hedong_defects、奏疏 r_luoyang | 夜色中的幽州城外，鼙鼓与烽火，铁骑南下，扬起尘土。旗帜纯色，无字。 |
| event.duji_falls | duji_falls、duji_recovered | 洛阳城门洞开，宫城上空烟尘升起，城下兵马纷乱。远景。 |
| event.changshan_rising | changshan_rising、changshan_rising_prepared、changshan_falls、hebei_recovered | 常山郡城头，太守与士民举火为号，太行山麓的城镇遥相呼应。 |
| event.feng_gao_executed | feng_gao_executed | 陕州的军营，监军宦官手持敕书（无字），两位将军卸甲肃立。不画行刑。 |
| event.tongguan_battle | tongguan_falls、奏疏 r_tongguan | 黄河峡谷中的潼关，关城上烽火四起，隘口里兵马拥塞。远景。 |
| event.mawei | court_flees、mawei | 马嵬驿的佛堂外，六军驻马不前，禁军将领在车驾前请命，梨花零落。不直接描绘死亡。 |
| event.frontier_raid | frontier_raid | 陇右的山口，吐蕃骑兵掠走畜群，烽燧上狼烟升起。 |

## 3. 结局图（1344×768）

| id | 结局 | 画面 |
|---|---|---|
| ending.e1_zhongxing | 天宝中兴·消弭兵祸 | 上元夜的长安，灯火满城，朱雀大街士女游观。远处的范阳方向一片宁静。 |
| ending.e2_frontier_lost | 削藩而边陲失 | 西陲的烽燧连绵燃起，空荡的城堡外，吐蕃的骑兵越过界碑（无字）。 |
| ending.e3_restoration | 再造唐室（含潼关相持） | 潼关城头的唐军旗帜（纯色）在朝阳下猎猎作响，关外的叛军营火渐稀。 |
| ending.e4_history | 渔阳鼙鼓·历史重演 | 蜀道栈阁上，銮舆在雨中西行，回望秦川，只有云雾。 |
| ending.e5_yang | 杨氏擅国 | 杨氏的宅第灯火辉煌，车马盈门；大明宫的殿宇冷落。 |
| ending.e5_beisi | 北司掌兵 | 北衙禁军的营门由宦官掌钥，禁军士卒在宦官面前列队。 |
| ending.e6_abdication | 传位东宫 | 兴庆宫的花萼相辉楼，老皇帝独自凭栏，远处的新君仪仗渐行渐远。 |
| ending.fail_changan | 长安不守 | 长安城破，宫阙上空烟尘升起，百官四散奔逃。远景，不画屠戮。 |
| ending.fail_regicide | 龙驭宾天 | 马嵬驿夜色沉沉，御帐倾斜，火光映照禁军的剪影。暗示即可，不直接描绘死亡。 |
| ending.fail_bankrupt | 帑竭兵变 | 左藏库门大开，库内空空；宫门外卫士聚集喧哗。 |
| ending.open_storm | 山雨欲来 | 岁暮，骊山上空乌云压城，华清宫的灯火依稀，东北天际隐约有闪电。 |

## 4. 地区卡（1024×576；引擎校验要求 `region.<id>.card`）

| id | 画面 |
|---|---|
| region.jingji.card | 长安城的远景：棋盘式的坊市，大明宫含元殿雄踞龙首原。 |
| region.tongguan.card | 黄河在此折而向东，关城扼守在崤函古道上，秦岭耸立。 |
| region.duji.card | 洛阳宫城和天津桥，洛水穿城而过，含嘉仓的仓窖成排。 |
| region.hedong.card | 太原晋阳城，汾水，表里山河的地势。 |
| region.fanyang.card | 幽州城和燕山，城外有骑兵演练的校场。 |
| region.pinglu.card | 营州的边城，辽西的草原和群山，帐幕与城垣交错。 |
| region.hebei.card | 华北平原上的郡城，桑田和运渠，太行山在远处。 |
| region.henan.card | 汴州和汴河，漕船首尾相接。 |
| region.huainan.card | 扬州的运河和市舶，江淮之间的稻田。 |
| region.jiangnan.card | 润州长江渡口，江南的水乡和茶山。 |
| region.shannan.card | 襄阳城和汉水，舟楫往来。 |
| region.jiannan.card | 成都平原和锦江，远处是雪山和蜀道。 |
| region.longyou.card | 鄯州的城堡和青海湖，戍楼与烽燧相望。 |
| region.hexi.card | 凉州的绿洲城池，祁连山的雪线，驼队。 |
| region.shuofang.card | 灵州和黄河河套，草原上有骑兵营垒。 |
| region.anxi.card | 龟兹城，天山南麓的绿洲，佛寺与石窟。 |
| region.beiting.card | 庭州城，天山北麓的草原，雪山。 |
| region.lingnan.card | 广州港，海船和榕树，岭南的湿热气象。 |
| region.tubo.card | 青藏高原的雪山和牦牛群，吐蕃的营帐。 |
| region.nanzhao.card | 苍山洱海，太和城的城墙。 |
| region.khitan_xi.card | 潢水流域的草原，契丹的车帐和猎骑。 |
| region.huihe.card | 漠北草原，回纥牙帐，鄂尔浑河。 |

## 5. 地图与 UI

| id | 用途与画面 |
|---|---|
| map.base | 底图（2048×1536，无文字）：盛唐疆域，绢本青绿设色。画出黄河、长江、汴河漕运线，标示秦岭、太行、潼关峡谷，以及西域、吐蕃高原的边缘。区域坐标见 `regions.yaml` 的 map 字段（百分比坐标）。 |
| ui.map.base | 引擎校验要求的别名，与 map.base 是同一个文件。 |
| ui.topbar.background | 顶栏：黑漆底，饰泥金宝相花与卷草纹。 |
| ui.edict.parchment | 诏书纸：明黄色的黄麻纸，带宝相花暗纹，毛边，上下有木轴（同 ui.edict_paper）。 |
| ui.edict_paper | 美术规范中的诏书纸 id，与上一条是同一个文件。 |
| ui.court.backdrop | 朝堂背景：大明宫含元殿的远景，晨雾中的龙尾道。 |
| ui.memorial.banner | 奏疏横幅：石青色的绢面，泥金卷草边。 |
| ui.crisis_drum | 危机计：一面皮鼓配鼓槌，鼓面分四段，依次为石绿、泥金、橙赭、朱砂。 |
| ui.desk | 御案：深色木案面，边缘饰织锦桌毯。 |
| ui.paper | 通用卷轴纸面。 |
| ui.ink_button | 墨锭按钮。 |
| ui.seal | 朱砂印章按钮（印面留空，不刻字）。 |
| ui.lacquer_bar | 资源条：黑漆横条。 |
| ui.silk | 绢面底纹。 |
| title.scroll | 标题页的长卷画面。 |
| icon.sheet | 资源与派系的图标表。 |
| icon.treasury / icon.grain / icon.authority / icon.morale / icon.corruption / icon.frontier_pressure / icon.an_ambition / icon.fanzhen_power / icon.court_strife / icon.rebellion_risk | 十项资源的图标（与 scenario.yaml 的资源 id 一一对应）：钱贯、米斛、玉圭、民居、锈锁、烽燧、胡帽、节钺、对峙的笏板、鼙鼓。 |
| ui.ribbon_xiang / ui.ribbon_yang / ui.ribbon_fanyang / ui.ribbon_neiting | 派系绸带，依次对应相党（紫）、杨氏（朱）、范阳（绿）、内廷（石青泥金）。东宫、西北边帅、清流三条可以后补：donggong 石青、xibei 赭石、qingliu 墨。 |

共计：人物立绘 28 张（20 人，其中 8 人另有第二套），事件插画 26 张，结局图 11 张，地区卡 22 张，地图与 UI 16 项。
