---
format: 1080x1920
duration: 59s
message: "盛世只剩四年——AI 演满朝文武，你来当唐玄宗，能不能救下大唐？"
arc: Hook（倒计时 + 两条路）→ 你就是玄宗 → 玩法演示（奏疏 / 召对 → 廷议 → 拟诏 / 兵部）→ 低谷：历史重演 → 反转：AI 驱动、大唐可救 → CTA（开源、接入 Codex / Claude Code）
audience: 抖音 / 小红书 / 视频号的历史、策略游戏玩家，AI 圈
music: tense epic Chinese orchestral, guzheng and taiko drums, building to a climax then a hopeful resolve
language: zh-CN
captions: on (Chinese, burned in)
---

## Video direction

- **This is the 9:16 cut of the approved 16:9 promo** — same narration, music, timing, story and assets; only the layout is re-composed for a 1080×1920 phone screen.
- **Portrait layout system:** a top title band (y ≈ 140–420) carries the slammed display words; the middle (y ≈ 440–1560) carries the picture — a screenshot crop or painting; the bottom ~17% (y > 1600) is the caption band — nothing important there. Phone UI covers the very top ~120px and the right edge ~120px on some apps: keep key text inside x 60–960.
- **Screenshots in portrait:** the game screenshots are 1920×1080. Never shrink a whole screenshot to 1080 wide (it becomes unreadably small). Show a **region crop** of the real screenshot, scaled ~1.4–2.2× into a tall or square gold-hairline window (e.g. 1000×1000 or 1000×1200), chosen to contain the thing the VO names; move between regions with zoom-to-target / pan inside the window. Crops stay faithful — never re-draw UI.
- **Paintings (1344×896) in portrait:** cover-crop to full height around the subject (the figure / the fire / the road), scrim for type.
- **Palette (frame.md roles):** ground = lacquer black `{colors.dark}` #17110e; paper = parchment `{colors.bg}` #e6d3a3; accent = vermilion `{colors.red}` #c0392b — ONE accent per frame; gold `{colors.light}` #c9a24b only for hairline frames, seal rims and the 「天宝」 ornament. Never tint screenshots or paintings; dim with a black scrim only.
- **Type (frame.md roles, CJK):** display = Noto Serif SC 900 (tilts −6°…+2° on statement words only); body = Noto Serif SC 400/500; chrome labels = Noto Sans SC 600. Local fonts in `assets/fonts/`. Display words are 2–6 characters and sized so one line stays ≤ ~900px wide.
- **Motion grammar:** long-tail power3 settles, no bounce (one overshoot allowed: the 「否 / 可」 seals in Frame 5). Reveals paced to the voiceover phrase timings below — never front-load. Internal seams are velocity-matched cuts. On a hold only a subtle low-amplitude jitter; no breathing, no back-half pan/push.
- **Rhythm / held frames:** Frames 1–2 percussive; Frame 3 a breather; Frames 4–6 a brisk UI montage; Frame 7 accelerates then drops to stillness on 「盛世，就此终结」; Frame 8 lifts; Frame 9 holds on the question and URL (last ~3s still).
- **Caption band:** bottom ~17% (y > ~1600px) is reserved for burned-in captions.
- **Negative list:** no purple/blue "AI" gradients, no bokeh, no stock shapes, no fake UI, no Latin display fonts, no emoji; no slideshow and no screensaver. Never show raw ids or turn codes. Never put a label on a screenshot that the screenshot does not support (e.g. no 「延期」 on a row marked 施行).

## Frame 1 — 倒计时

- scene: 竖屏：玄宗背影的标题原画（裁出人物与远处黑烟），上方大字「公元751年」，「4 年」砸下来
- voiceover: "公元七五一年。离安史之乱，只剩四年。"
- duration: 4.8s
- transition_in: cut
- status: animated
- src: compositions/frames/01-countdown.html
- type: hook
- persuasion: Scarcity/urgency
- beat: tension
- blueprint: kinetic-type-beats (Adapt)
- asset_candidates: assets/01-title.png — 标题画面：右侧玄宗黄袍背影立于宫阙栏边，远处地平线有黑烟；左侧是墨块「天宝」标志与菜单
- focal: assets/01-title.png
- roles: 01-title = background (cover-crop to the right ~60% of the image: Xuanzong + the smoke on the horizon; scrim ~45%; the logo/menu side must not show)
- sfx: taiko-hit, low-boom

Adapt: keep the statement-builds-across-beats signature; the canvas is a portrait crop of the title painting.
Scene 1 (0.0–1.4s): portrait crop of the painting (Xuanzong's back at lower right, the smoke column mid-frame) under scrim; a short push toward the smoke (done by 1.4s). 「公元751年」 slams into the top title band in display 900 parchment, −2° (`kinetic-beat-slam`) at 0.10s.
Scene 2 (2.0–3.1s): on 「离安史之乱」 a vermilion rule draws under the year (`svg-path-draw`) and a Noto Sans label 「距 · 安史之乱」 types beneath it.
Scene 3 (3.25–4.8s): on 「只剩四年」 a giant vermilion 「4」 (stat-big, −6°, ~620px tall) slams in at mid-frame over the smoke with a camera kick, 「年」 lands beside it a beat later; hold (subtle jitter on the 「4」 only).

## Frame 2 — 两条路

- scene: 竖屏上下对照：上半暗——坏结局插画（雨夜栈道），压字「等待历史重演？」；下半亮——好结局插画（牡丹宫阙日出），压字「励精图治」；末拍下半推满全屏，叠「阻止安史之乱？」
- voiceover: "什么都不做，等待历史重演？还是励精图治，阻止安史之乱？"
- duration: 6.456s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/02-choice.html
- type: hook
- persuasion: Negative contrast
- beat: tension → aspiration
- blueprint: comparison-split (Adapt)
- asset_candidates: assets/ending.e4_history.webp — 坏结局插画（雨夜栈道、车驾西幸）; assets/ending.e1_zhongxing.webp — 好结局插画（牡丹、宫阙、日出、白鹤）
- focal: assets/ending.e1_zhongxing.webp
- roles: ending.e4_history = supporting (upper card, desaturated + darkened) · ending.e1_zhongxing = supporting → background (lower card that finally fills the frame)
- sfx: whoosh, riser

Adapt: keep the split entry from opposite sides with mirrored tilt (signature), rotated for portrait: the cards stack vertically — the bad card enters from the top/left with a rotateX/rotateY book tilt, the good card from the bottom/right; the good card wins by expanding to full frame.
Scene 1 (0.0–1.0s): lacquer ground; 「什么都不做？」 in display 900 parchment in the top title band, per-word reveal (`dynamic-content-sequencing`).
Scene 2 (1.14–2.9s): on 「等待历史重演」 the upper card (bad-ending painting, desaturated, dark, ~1000×620) swings in with a mirrored tilt (`split-tilt-cards`); vermilion tag 「等待历史重演？」 on its lower edge.
Scene 3 (3.0–4.5s): on 「还是励精图治」 the lower card (good-ending painting, full color, slightly larger) swings in from the opposite side; 「励精图治」 in display 900 lands on it with a gold hairline underline.
Scene 4 (4.54–6.456s): on 「阻止安史之乱」 the lower card flattens and expands to full frame (`card-morph-anchor`, uniform scale; cover-crop on the palace and sunrise), the upper card slides out; 「阻止安史之乱？」 settles in display 900 (two lines if needed) on a dark band in the upper-middle; hold.

## Frame 3 — 你就是玄宗

- scene: 竖屏：主界面舆图区域放大成竖窗（舆图 + 右侧危机计），「天宝」印落下，「你是 · 唐玄宗」
- voiceover: "这是《天宝》。这一次，你是唐玄宗。"
- duration: 3.816s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/03-intro.html
- type: product_intro
- persuasion: Future pacing
- beat: curiosity
- blueprint: titlecard-reveal (Adapt)
- asset_candidates: assets/04-desk.png — 主界面：舆图、资源栏、四条势力绸带、危机计
- focal: assets/04-desk.png
- roles: 04-desk = supporting (region crop: the map plus the faction ribbons and the crisis dial, roughly x 1000–1900, y 0–950 of the screenshot, shown in a tall gold-hairline window ~1000×1060)

Adapt: keep the single restrained move + still hold (signature).
Scene 1 (0.0–1.5s): the cropped main-screen window eases up into the middle (slide-up crossfade, power3) on 「这是」; on 「天宝」 (0.45s) a square vermilion seal 「天宝」 (stacked, gold rim) stamps onto the window's upper-left corner.
Scene 2 (1.55–3.816s): on 「这一次，你是唐玄宗」 a lacquer label slides into the top title band: 「你是 · 唐玄宗」 (display 900 for 唐玄宗); hold still.

## Frame 4 — 奏疏与召对

- scene: 竖屏：奏疏列表竖窗（盖「迟到之报」）→ 推到召对：安禄山立像竖窗 → 对话气泡
- voiceover: "奏疏从千里外送来，会迟到。召安禄山入殿，当面问他：范阳的兵，到底听谁的？"
- duration: 7.896s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/04-audience.html
- type: feature_showcase
- persuasion: Show-don't-tell proof
- beat: intrigue
- blueprint: device-surface-showcase (Adapt)
- asset_candidates: assets/06-memorial.png — 奏疏面板：禄山在京未归、群臣谏言与选项; assets/07-audience.png — 召对安禄山：大幅立像 + 对话
- focal: assets/07-audience.png
- roles: 06-memorial = supporting (region crop of the memorial list + open memorial, tall window) · 07-audience = supporting (region crops: first the portrait half, then the dialogue)

Adapt: keep the cursorless stepwise flow on one real surface (signature); portrait windows of region crops.
Scene 1 (0.0–1.7s): a tall gold-framed window (~1000×1250) rises in the middle showing the memorial panel crop; lacquer chip 「奏疏」 at its top-left.
Scene 2 (1.8–2.6s): on 「会迟到」 a vermilion outline stamp 「迟到之报」 (Noto Sans 600, −4°) thumps onto the list.
Scene 3 (3.1–5.2s): on 「召安禄山入殿」 velocity-matched push LEFT to the audience screenshot, cropped to An Lushan's full-length portrait (tall crop fits the window naturally); chip changes to 「召对」.
Scene 4 (5.3–7.896s): on 「范阳的兵」 pan/zoom inside the window to the dialogue: the question 「卿以为范阳之兵如何？」 gets a vermilion marker underline and the reply bubble is revealed top-to-bottom with a soft wipe on 「到底听谁的」 (reply text is a crop of the real bubble — readable, ≥ 1.6×); hold.

## Frame 5 — 廷议

- scene: 竖屏：三位大臣画像竖排依次落下，「可 / 否」印章，底部计票
- voiceover: "廷议上，谁附议、谁反对，一目了然。"
- duration: 4.056s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/05-debate.html
- type: feature_showcase
- persuasion: Show-don't-tell proof
- beat: clarity
- blueprint: grid-card-assemble (Adapt)
- asset_candidates: assets/09-debate.png — 廷议：三位大臣画像、立场印章、主张与发言、计票
- focal: assets/09-debate.png
- roles: 09-debate = supporting (dimmed full-height ground crop + three portrait crops as cards)

Adapt: keep the staggered cascade that holds (signature); in portrait the three cards cascade into a vertical column (or a 1-over-2 pyramid) instead of a row.
Scene 1 (0.0–0.8s): the debate screenshot as a dimmed (~45%) cover-cropped ground; header chip 「廷议」 in the top band.
Scene 2 (0.84–2.5s): three portrait crops (portrait + its stance label from the screenshot, each ~1.4×) cascade in one per beat: 李林甫 on 「谁附议」 with a green 「可」 seal; 杨国忠 then 颜真卿 on 「谁反对」 each with a vermilion 「否」 seal (the film's one allowed overshoot).
Scene 3 (2.64–4.056s): on 「一目了然」 the real tally line (赞成 1 · 反对 2), cropped from the screenshot, slides up as a parchment bar under the cards (above y 1600); hold.

## Frame 6 — 拟诏与兵部

- scene: 竖屏：诏书 → 政策卡 → 兵部 三个竖窗接力 → 舆图路线 + 回执「需 4 季」
- voiceover: "拟诏、发政策卡、调兵遣将。千里之外，军令要走好几季。"
- duration: 6.288s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/06-edict.html
- type: feature_showcase
- persuasion: Feature-to-benefit translation
- beat: control
- blueprint: compose
- asset_candidates: assets/12-edict.png — 门下诏书; assets/11-cards.png — 政策卡拾取器; assets/10-army.png — 兵部：诸军兵力、统帅; assets/13-receipt.png — 回执：每条标「施行」，其中「兴工『禁军整训』4 季」一行; assets/05-map-zoom.png — 舆图放大到河北、范阳、潼关、京畿
- focal: assets/13-receipt.png
- roles: 12-edict = supporting · 11-cards = supporting · 10-army = supporting · 13-receipt = supporting (hero of the back half) · 05-map-zoom = background (dimmed, full height under the last scene)

Compose: a three-beat relay of region crops through one tall gold window, landing on the receipt over the map.
Scene 1 (0.0–0.7s): on 「拟诏」 the edict scroll crop rises into the window; chip 「拟诏」.
Scene 2 (0.77–1.7s): on 「发政策卡」 push-left to the card-grid crop of 11-cards; chip 「政策卡 ×27」.
Scene 3 (1.77–2.9s): on 「调兵遣将」 push-left to the army-list crop of 10-army; chip 「兵部」.
Scene 4 (3.25–6.288s): on 「千里之外」 the map fades in full-frame behind at ~40% (cover-crop on 京畿 → 潼关 → 范阳) and a dashed vermilion route self-draws from 京畿 to 范阳 (`svg-path-draw`, on the map's own labels); on 「军令要走好几季」 a crop of the receipt with the 禁军整训 4 季 row drops in as a card in the lower-middle, and a vermilion stamp 「需 4 季」 lands beside that row; hold.

## Frame 7 — 历史重演

- scene: 竖屏：「范阳起兵」→ 舆图染红 → 「东都陷落」「潼关失守」「马嵬驿」连砸 → 坏结局「渔阳鼙鼓·历史重演」
- voiceover: "可一步走错：范阳起兵，东都陷落，潼关失守，马嵬驿……盛世，就此终结。"
- duration: 7.608s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/07-collapse.html
- type: pain_point
- persuasion: Pain agitation
- beat: overwhelm
- blueprint: kinetic-type-beats (Adapt)
- asset_candidates: assets/22-war-result-0.png — 结算：范阳起兵（左侧起兵插图、纪事、时事）; assets/24-war-desk-0.png — 战局舆图（初染红）; assets/24-war-desk-3.png — 战局舆图（大片红、叛军路线）; assets/event.fanyang_uprising.webp — 范阳起兵原画; assets/event.tongguan_battle.webp — 潼关之战原画; assets/event.mawei.webp — 马嵬驿原画; assets/25-ending-bad.png — 坏结局画面
- focal: assets/24-war-desk-3.png
- roles: event.fanyang_uprising = background · 22-war-result-0 = supporting · 24-war-desk-0 = supporting · 24-war-desk-3 = supporting (hero) · event.tongguan_battle = background · event.mawei = background · 25-ending-bad = supporting (final hold; crop the parchment ending card with its title)
- sfx: impact-heavy, war-drum, low-boom

Adapt: keep the escalating statement-across-beats with a locked finale (signature: each place name its own slam), over portrait crops.
Scene 1 (0.0–1.2s): on 「可一步走错」 hard cut to lacquer; 「一步走错」 per-word reveal in the top band; slight camera shake begins.
Scene 2 (1.25–2.2s): on 「范阳起兵」 the uprising painting slams in full-height (cover-crop on the torches and the war drum, scrim ~35%); 「范阳起兵」 slams in vermilion display 900, −5°, in the top band; a small crop of the 22-war-result-0 scroll (its 「范阳起兵」 entry) cuts in at lower-middle as proof.
Scene 3 (2.26–3.2s): on 「东都陷落」 cut to a tall crop of the war map (the red bloc over 范阳 / 河北 / 都畿) from 24-war-desk-0, crossfading to 24-war-desk-3 so the red visibly spreads; 「东都陷落」 slams.
Scene 4 (3.27–4.3s): on 「潼关失守」 cut to the Tongguan painting (portrait crop); slam 「潼关失守」.
Scene 5 (4.35–5.1s): on 「马嵬驿」 cut to the Mawei painting, desaturating to grey; slam 「马嵬驿」.
Scene 6 (5.22–7.608s): music drops; on 「盛世，就此终结」 the bad-ending card (crop of 25-ending-bad's parchment card with 「渔阳鼙鼓·历史重演」 readable) fades up centered and still over the dark ending painting; vignette; hold.

## Frame 8 — AI 驱动

- scene: 竖屏：召对回话竖窗 →「AI 驱动」→ 三张廷议发言卡竖排 → 好结局卡片（标题 + 三个「达成」）
- voiceover: "这是一款 AI 驱动的历史模拟。接上大模型，满朝文武，都由 AI 来演。"
- duration: 7.368s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/08-ai.html
- type: benefit_highlight
- persuasion: Feature-to-benefit translation
- beat: relief + awe
- blueprint: video-text-pivot (Adapt)
- asset_candidates: assets/07-audience.png — 召对安禄山：大幅立像 + 对话; assets/09-debate.png — 廷议：三位大臣画像、立场、发言; assets/31-ending-good.png — 好结局「天宝中兴·夺镇弭兵」（左侧羊皮纸卡片 + 右侧复盘卡，三目标达成）
- focal: assets/31-ending-good.png
- roles: 07-audience = supporting · 09-debate = supporting · 31-ending-good = background (cover-crop) → hero (the two cards re-stacked: title card on top, review card below)

Adapt: keep the "surface yields → statement takes the center → sealed" pivot (signature).
Scene 1 (0.0–2.7s): light returns: a crop of An Lushan's reply bubble (≥1.6×) rises in a gold frame in the middle; a lacquer label types 「AI 驱动」 in display 900 in the top band (type-on with caret).
Scene 2 (3.29–5.4s): on 「接上大模型，满朝文武」 the reply slides up and three speech cards (crops of the three portraits + their speeches from 09-debate) fan in one by one in a vertical stack; chip 「每位大臣由大模型扮演」.
Scene 3 (5.57–7.368s): on 「都由 AI 来演」 everything clears; the good-ending painting blooms full-frame (cover-crop) and the two real cards from 31-ending-good appear stacked — the parchment title card 「天宝中兴·夺镇弭兵」 in the upper half, the review card's 目标 rows below — the title stays fully readable to the end; the three 「达成」 rows each get a gold tick in sequence, the last by ~6.9s; hold.

## Frame 9 — 你能吗

- scene: 竖屏：「天宝」墨块标志在上；三条卖点竖排（开源免费 / 打开网页就能玩 / 直接接入 Codex · Claude Code + 一行命令）；推穿墨块后「你，能救大唐吗？」+ 仓库地址，定格约 3 秒
- voiceover: "开源免费，打开网页就能玩，还能直接接入 Codex 和 Claude Code。你，能救大唐吗？"
- duration: 10.28s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/09-cta.html
- type: cta
- persuasion: Risk reversal
- beat: urgency-to-act
- blueprint: logo-assemble-lockup (Adapt)
- asset_candidates: assets/01-title.png — 标题画面（左侧墨块「天宝」标志 x 115–470, y 90–640）; assets/title.scroll.webp — 卷轴装饰
- focal: assets/01-title.png
- roles: 01-title = background (cover-crop on Xuanzong, heavy scrim ~60%) + the ink-blot 「天宝」 logo crop as the mark · title.scroll = supporting (parchment strip behind the three lines)
- sfx: whoosh, taiko-hit

Adapt: keep the CTA push-through signature (camera pushes through the mark into the final question + URL).
Scene 1 (0.0–1.0s): the painting under heavy scrim; the ink-blot 「天宝」 mark (crop) settles in the upper third, centered; 「开源免费」 lands below it as the first parchment line, with a small vermilion 「免费」 seal.
Scene 2 (1.12–2.5s): 「打开网页就能玩」 reveals beneath (per-word).
Scene 3 (2.58–5.8s): 「接入 Codex · Claude Code」 reveals, then a lacquer terminal pill types `codex mcp add tianbao -- tianbao-server mcp` (wrap to two lines if needed to stay within x 60–1020); 「Codex」 and 「Claude Code」 get a short gold glow as each is spoken.
Scene 4 (6.3–10.28s): on 「你，能救大唐吗」 a fast camera push-through the ink blot (horizontal motion blur) resolves to lacquer ground with 「你，能救大唐吗？」 in display 900 on two lines (「大唐」 vermilion, −4°, smooth settle — no overshoot) in the upper-middle, and 「github.com/Yi-111-a/tianbao」 wiping in beneath by ~7.0s (Noto Sans 600, gold, sized to fit within x 60–1020); hold still until a short fade to black from ~9.9s (the film's exit).
