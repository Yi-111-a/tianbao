# 《天宝》美术风格指南 (Style Guide) v1

时代：天宝十载（公元 751 年），盛唐，玄宗朝。界面隐喻：**御案**（diegetic imperial desk）。
主界面方向：概念图 A（平铺全幅设色绢本地图）+ 概念图 B 的**派系丝带**与**危机计**。
所有生产图片**一律无文字**（无汉字、无书法、无印章字、无地图标注）；一切文字由前端渲染。

## 1. 色板 (Palette tokens)

取自敦煌壁画与唐代绢本设色：矿物颜料 + 泥金 + 黄麻纸。

| token | 名称 | hex | 用途 |
|---|---|---|---|
| `--shiqing` | 石青 (azurite) | `#2F5D8A` | 山体冷色、海水、奏疏封面、太子/清流 |
| `--shilv` | 石绿 (malachite) | `#3E7F6B` | 山林、河流、绿袍、范阳派系带 |
| `--zheshi` | 赭石 (ochre/sienna) | `#A5642E` | 皇帝赭黄袍、木器、地图陆地暖色 |
| `--zhusha` | 朱砂 (cinnabar) | `#C0392B` | 印、危机警示、杨氏派系带、绯袍 |
| `--nijin` | 泥金 (gold) | `#C9A24B` | 描金边、宝相花、按钮金边 |
| `--huangma` | 黄麻纸 (hemp paper) | `#E6D3A3` | 诏敕纸、纸面底色 |
| `--mo` | 墨 (ink) | `#1E1B18` | 文字、墨块按钮、漆条 |
| `--zise` | 紫袍 (purple robe) | `#5B3A6B` | 三品以上官服、相党派系带 |
| `--lacquer` | 黑漆 (lacquer) | `#17110E` | 资源条底、御案 |
| `--silk` | 绢色 (aged silk) | `#D9C08A` | 地图底、绢面 |

危机计四段变色：平静 `#3E7F6B` → 风闻 `#C9A24B` → 山雨 `#D2742F` → 烽火 `#C0392B`。

## 2. 字体 (Typography)

| 角色 | 字体 | 许可 |
|---|---|---|
| 标题/印章/按钮 | **霞鹜文楷 LXGW WenKai** | OFL |
| 正文/奏疏/对话 | **思源宋体 Source Han Serif / Noto Serif SC** | OFL |
| 数字 | 思源宋体 tabular-nums，资源条用 600 字重 | OFL |

字重：标题 500-700，正文 400；行高正文 1.75；奏疏正文 16-18 px；标题大字间距 0.08em。

## 3. 纹样词汇 (Ornament vocabulary)

- **宝相花 (baoxiang flower)**：多瓣叠晕团花，用于顶栏、印章边、锦缎底纹。
- **卷草纹 (cuancao)**：连续波状藤蔓，用于边框、卷轴包边、地毯。
- **联珠纹 (lianzhu)**：圆珠环，用于波斯/粟特风织锦、丝带边。
- **云纹/祥云**：金箔云，用于标题画与过场。
- 山水：青绿山水，勾勒填色，无透视大阴影。
- **禁用**：龙纹/龙团（明清）、团龙补子、云龙柱、翼善冠/乌纱帽硬翅、补子方胜、回纹窗格满铺。

## 4. 组件形状 (Component shapes)

| 组件 | 形状与材质 |
|---|---|
| **墨锭按钮** `ui.ink_button` | 长方形墨锭，黑墨色，上下边缘微圆，细泥金描边，右上角略有斜削，hover 时泥金边亮起。 |
| **印章按钮** `ui.seal` | 圆形或方形朱砂印泥块，边缘不规则飞白，内部留空供文字（前端渲染），按下时压深。 |
| **卷轴面板** `ui.paper` / `ui.edict_paper` | 黄麻纸，毛边（deckled），上下木轴泥金端帽；诏书纸偏明黄并有宝相花暗纹。 |
| **丝带** `ui.ribbon_*` | 竖向悬挂绢带，下端燕尾，联珠边，色=派系：相党紫、杨氏朱、范阳绿、内廷/高氏石青泥金。 |
| **资源条** `ui.lacquer_bar` | 黑漆横条，泥金宝相花角饰，圆形图标凹槽。 |
| **危机计** `ui.crisis_drum` | 皮鼓+鼓槌，鼓面分 4 段变色（平静/风闻/山雨/烽火）。 |
| **御案** `ui.desk` | 深色木案面 + 织锦桌毯边，供叠放面板。 |

圆角：纸面 0-2 px（毛边为主），按钮 2-4 px，图标槽圆形。投影：暖色低饱和，`rgba(30,20,10,.35)`。

## 5. 共享图像风格块 (Shared image style block)

每条生成提示词必须以下面这段**逐字**开头（`design/asset_prompts/_style_block.txt` 同内容）：

```
STYLE BLOCK: Original hand-painted artwork for a polished high-end historical strategy game set in Tang dynasty China, year 751 AD (Tianbao era, High Tang, Emperor Xuanzong). Visual language of Dunhuang murals and Tang silk and court painting: mineral pigments (azurite blue, malachite green, ochre, cinnabar red), gold leaf and gold line work on aged hemp paper and silk, soft ink-wash modelling, warm candle-lit tones, fine brush outlines. Authentic Tang material culture, NOT Ming or Qing: officials wear round-collar robes (yuanling pao) with soft-legged black futou caps, robe colour by rank (purple, scarlet, green), leather belts with plaques, black boots; the emperor wears an ochre-yellow robe; women wear high-waisted skirts, pibo shawls, high buns and forehead huadian flower marks. Ornament: baoxiang flower rosettes, cuancao scrolling vines, pearl roundels. Strictly NO dragons or dragon roundels, NO Ming black gauze hats with wing flaps, NO mandarin-square badges. ABSOLUTELY NO TEXT of any kind: no Chinese characters, no calligraphy, no letters, no numbers, no seal script, no labels, no captions, no watermark, no logo; any seal or plaque must be a blank abstract shape. Original art, not imitating any existing game or franchise.
```

负面提示词（记入 manifest）：`text, characters, calligraphy, letters, numbers, watermark, logo, dragon, dragon robe, Ming wing hat, mandarin square, modern, photo, 3d render, anime`。

## 6. 构图规范

- 人物立绘 2:3 竖幅（输出 1024×1536，发布 768 宽），半身至膝上，居中，背景为淡化的场景（与人物身份相关），柔和雾化，边缘留渐隐以便前端叠加。
- 事件插画 3:2（1536×1024，发布 1344 宽），克制，不直接描绘死亡与血腥，无文字旌旗（旗帜纯色/纹样）。
- 地图底图 3:2，唐疆域；平铺全幅，无文字、无国界线以外的现代海岸强调；地图边缘自然淡出为绢面。
- UI 纹理：可平铺或可九宫格拉伸，边缘清晰。

## 7. Do / Don't

**Do**
- 矿物颜料 + 泥金，绢本/麻纸肌理，毛边与做旧。
- 官员：圆领袍 + 软脚幞头；紫/绯/绿（青）分品级；皇帝赭黄。
- 女性：高腰襦裙、披帛、高髻、花钿。
- 铠甲：明光铠 / 山文甲，兜鍪，披风；旗帜仅用纯色或纹样。
- 图中无任何文字；若生成图出现类文字笔画，**重生成**。
- 武备、器物参考唐代：三彩、金银器、胡瓶、莲花纹。

**Don't**
- 龙纹、团龙、云龙柱、龙椅雕刻（明清）。
- 明代乌纱帽（硬翅）、补子、官帽翅、明式衣冠。
- 现代海岸线强调（台湾、日本细节）、现代国界线。
- 抄袭任何现有游戏的 UI 与图标。
- 血腥特写、直接死亡画面（马嵬驿等必须克制）。
- 任何可读文字、印章字、地图地名。

## 8. 资产 ID 与产出说明 (batch 1)

- 全部清单见 `scenarios/tianbao_751/assets.yaml`（89 条）；提示词原文在 `design/asset_prompts/<id>.txt`，质检在 `asset_prompts/QA.md`，生成/转换脚本 `run_jobs.py` `process.py` `gen_manifest.py`。
- 立绘 768×1152 webp（2:3）；事件/结局 1344×896 webp（3:2，非 16:9，前端用 object-fit: cover）；地图 2048×1365；图标 256×256 带 alpha；墨锭、印、鼓、丝带、资源条已去白底带 alpha。
- 派系丝带 id：`ui.ribbon_xiang`（相党·紫）、`ui.ribbon_yang`（杨氏·朱）、`ui.ribbon_fanyang`（范阳·绿）、`ui.ribbon_neiting`（内廷·石青）。丝带中央金盘与印章中心均为空白，文字由前端叠加。
