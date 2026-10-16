---
format: 1920x1080
duration: 59s
message: "盛世只剩四年——AI 演满朝文武，你来当唐玄宗，能不能救下大唐？"
arc: Hook（倒计时 + 两条路）→ 你就是玄宗 → 玩法演示（奏疏 / 召对 → 廷议 → 拟诏 / 兵部）→ 低谷：历史重演 → 反转：AI 驱动、大唐可救 → CTA（开源、接入 Codex / Claude Code）
audience: B站 / 抖音的历史、策略游戏玩家，AI 圈
music: tense epic Chinese orchestral, guzheng and taiko drums, building to a climax then a hopeful resolve
language: zh-CN
captions: on (Chinese, burned in)
---

## Video direction

- **Palette (frame.md roles):** ground = lacquer black `{colors.dark}` #17110e for title/statement cards and the dark half of contrasts; paper = parchment `{colors.bg}` #e6d3a3 for cards and the hopeful half; accent = vermilion `{colors.red}` #c0392b — ONE accent per frame (a seal, a slammed word, the red map); gold `{colors.light}` #c9a24b only for hairline frames around screenshots, seal rims and the single 「天宝」 ornament. Game screenshots and paintings carry their own color — never tint or recolor them; dim backgrounds with a black scrim only.
- **Type (frame.md roles, CJK):** display = Noto Serif SC 900 (the poster slab; tilts −6°…+2° allowed on statement words, never on body); body = Noto Serif SC 400/500; chrome labels = Noto Sans SC 600. Fonts are local (`assets/fonts/`). Big Chinese display words are 2–6 characters; never set a whole sentence in display size — the captions carry the sentence.
- **Screenshot presentation:** a game screenshot is the real product — show it as-is inside a thin gold hairline frame with a soft drop toward the lacquer ground, or full-bleed under a scrim; never re-draw UI. Zoom into a region with a zoom-to-target camera move to make small UI readable; crops stay faithful.
- **Motion grammar:** long-tail `power3` settles, no bounce (one overshoot allowed in the whole film: the 「否 / 可」 seals in Frame 5). Reveals are paced to the voiceover phrase timings given per frame — at t=0 only what the VO is saying enters; never front-load. Seams inside a frame are velocity-matched (cut the curve). The only aliveness on a hold is subtle low-amplitude jitter — no breathing, no back-half pan/push.
- **Rhythm / held frames:** Frames 1–2 are percussive (slams on each phrase). Frame 3 is the first breather (title card holds). Frames 4–6 are a brisk UI montage (one surface per phrase). Frame 7 accelerates (four slams in four seconds) then drops to near-stillness on 「盛世，就此终结」 — the deliberate dead air before the turn. Frame 8 lifts (light returns). Frame 9 holds on the final question.
- **Caption band:** bottom ~17% (y > ~896px) is reserved for burned-in Chinese captions — plan all content into the top ~83%.
- **Negative list:** no purple/blue "AI" gradients, no bokeh, no generic stock shapes, no fake UI, no Latin display fonts, no emoji; no slideshow (dump-then-freeze) and no screensaver (everything floating). Never show raw ids, turn codes or English UI strings that aren't in the screenshots.

## Frame 1 — 倒计时

- scene: 标题画面上的玄宗背影；大字「公元751年」，倒计时「距安史之乱 4 年」砸下来
- voiceover: "公元七五一年。离安史之乱，只剩四年。"
- duration: 4.8s
- transition_in: cut
- status: animated
- src: compositions/frames/01-countdown.html
- type: hook
- persuasion: Scarcity/urgency
- beat: tension
- blueprint: kinetic-type-beats (Adapt)
- asset_candidates: assets/01-title.png — 标题画面：玄宗立于宫阙栏边远眺长安，地平线有黑烟
- focal: assets/01-title.png
- roles: 01-title = background (full-bleed, black scrim ~45%; the left logo/menu side darkened further so the type owns it)
- sfx: taiko-hit, low-boom

Adapt: keep the statement-builds-across-beats signature (each phrase its own slam); the canvas is the title painting instead of a flat field.
Scene 1 (0.0–1.4s): full-bleed title painting under scrim; a short push toward the smoke on the horizon (done by 1.4s). 「公元751年」 slams in at the left third in display 900 parchment, slight −2° tilt (`kinetic-beat-slam`) on 「公元七五一年」 (0.10s).
Scene 2 (2.0–3.1s): on 「离安史之乱」 (2.0s) a vermilion rule draws under the year (`svg-path-draw`) and a Noto Sans label 「距 · 安史之乱」 types beneath it.
Scene 3 (3.25–4.8s): on 「只剩四年」 (3.25s) a giant vermilion 「4」 (stat-big, −6°) slams into the right-center over the smoke with a camera kick, and 「年」 lands beside it a beat later; hold still to the cut (subtle jitter on the 「4」 only).

## Frame 2 — 两条路

- scene: 画面一分为二：左半暗——坏结局插画（雨夜栈道、车驾西幸），压字「等待历史重演？」；右半亮——好结局插画（牡丹、宫阙、日出），压字「励精图治」；末拍右半推满全屏，叠「阻止安史之乱？」
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
- roles: ending.e4_history = supporting (left card, desaturated + darkened) · ending.e1_zhongxing = supporting → background (right card that finally fills the frame)
- sfx: whoosh, riser

Adapt: keep the split-tilt entry from opposite wings (signature); the two cards arrive one per question instead of together, and the right card wins by expanding to full frame instead of badges.
Scene 1 (0.0–1.0s): lacquer ground; 「什么都不做？」 in display 900 parchment centered in the upper third, per-word reveal (`dynamic-content-sequencing`).
Scene 2 (1.14–2.9s): on 「等待历史重演」 the left card (bad-ending painting, desaturated, dark) swings in from the left wing with a mirrored rotateY tilt (`split-tilt-cards`); the headline slides up to make room; a vermilion caption 「等待历史重演？」 sits on the card's lower edge.
Scene 3 (3.0–4.5s): on 「还是励精图治」 the right card (good-ending painting, full color) swings in from the right wing, mirrored tilt; 「励精图治」 in display 900 lands on it with a gold hairline underline. Right card slightly larger.
Scene 4 (4.54–6.456s): on 「阻止安史之乱」 the right card flattens its tilt and expands to full frame (`card-morph-anchor`, uniform scale) while the left card slides out; 「阻止安史之乱？」 settles in display 900 over the painting with a dark scrim behind the type; hold.

## Frame 3 — 你就是玄宗

- scene: 主界面整屏出现：舆图、势力绸带、危机计「渔阳鼙鼓」；「天宝」印落下
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
- roles: 04-desk = supporting (framed screenshot, gold hairline, ~85% width within the top 83%)

Adapt: keep the single restrained move + still hold (signature); the card is the game's main screen with a seal stamped on it.
Scene 1 (0.0–1.5s): the main screen eases up into place (slide-up crossfade, `gsap-effects`, power3) on 「这是」; on 「天宝」 (0.45s) a square vermilion seal 「天宝」 (two characters stacked, gold rim) stamps onto the upper-left corner of the screenshot — scale 1.15→1 with a short shadow kick.
Scene 2 (1.55–3.816s): on 「这一次，你是唐玄宗」 a lacquer label card slides in at the upper right reading 「你是 · 唐玄宗」 (display 900 for 唐玄宗); hold still.

## Frame 4 — 奏疏与召对

- scene: 奏疏面板滑入（远地奏疏标「迟到之报」）→ 切到召对：安禄山大幅立像，对话逐字出现
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
- roles: 06-memorial = supporting (framed screenshot, first surface) · 07-audience = supporting (framed screenshot, second surface, zoomed)

Adapt: keep "one real surface held as hero while its screens advance through the flow" (signature: cursorless stepwise flow); two real screenshots replace a device mockup.
Scene 1 (0.0–1.7s): the memorial screenshot rises into a gold-framed window (~80% width, within the top 83%); a lacquer chip 「奏疏」 sits at its top-left.
Scene 2 (1.8–2.6s): on 「会迟到」 a vermilion stamp 「迟到之报」 (Noto Sans 600 in a vermilion outline box, −4°) thumps onto the memorial list area.
Scene 3 (3.1–5.2s): on 「召安禄山入殿」 the surface advances: velocity-matched push LEFT to the audience screenshot (`cut-catalog.md` cut-the-curve); then `zoom-to-target` onto An Lushan's portrait half (left ~45%) as 「当面问他」 is spoken.
Scene 4 (5.3–7.896s): on 「范阳的兵」 the camera re-targets to the dialogue area (right half); the player's question 「卿以为范阳之兵如何？」 gets a vermilion marker underline (`css-marker-patterns`) and the reply bubble is revealed top-to-bottom with a soft wipe as 「到底听谁的」 lands; hold.

## Frame 5 — 廷议

- scene: 廷议：三位大臣画像依次翻出，「可 / 否」印章盖下，底部计票
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
- roles: 09-debate = supporting (framed screenshot; the three portrait regions are cropped from it as cards)

Adapt: keep the staggered cascade into a row that holds (signature); the three cards are crops of the real screenshot's three minister portraits (李林甫 / 杨国忠 / 颜真卿), not redrawn.
Scene 1 (0.0–0.8s): the debate screenshot sits dimmed (~45%) as the ground; header chip 「廷议」.
Scene 2 (0.84–2.5s): three portrait crops (each the portrait + its stance label, as in the screenshot) cascade up into a centered row, left→right, one per beat: 李林甫 on 「谁附议」 with a small green 「可」 seal on its corner; 杨国忠 then 颜真卿 on 「谁反对」 each with a vermilion 「否」 seal (the film's one allowed overshoot).
Scene 3 (2.64–4.056s): on 「一目了然」 the tally strip from the bottom of the screenshot (赞成 1 · 反对 2) slides up under the row as a parchment bar; hold.

## Frame 6 — 拟诏与兵部

- scene: 门下诏书 → 政策卡拾取器 → 兵部 → 舆图上调兵路线 + 回执上的「延期」
- voiceover: "拟诏、发政策卡、调兵遣将。千里之外，军令要走好几季。"
- duration: 6.288s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/06-edict.html
- type: feature_showcase
- persuasion: Feature-to-benefit translation
- beat: control
- blueprint: compose
- asset_candidates: assets/12-edict.png — 门下诏书; assets/11-cards.png — 政策卡拾取器; assets/10-army.png — 兵部：诸军兵力、统帅; assets/13-receipt.png — 回执：即行 / 延期; assets/05-map-zoom.png — 舆图放大到河北、范阳
- focal: assets/13-receipt.png
- roles: 12-edict = supporting · 11-cards = supporting · 10-army = supporting · 13-receipt = supporting (hero of the back half) · 05-map-zoom = background (dimmed under the last scene)

Compose: a three-beat surface relay (one screenshot per spoken verb) landing on a held receipt over the map; velocity-matched push-left seams between surfaces.
Scene 1 (0.0–0.7s): on 「拟诏」 the edict scroll screenshot (12-edict) rises into the gold frame; chip 「拟诏」.
Scene 2 (0.77–1.7s): on 「发政策卡」 push-left to the card picker (11-cards), `zoom-to-target` on the card grid; chip 「政策卡 ×27」.
Scene 3 (1.77–2.9s): on 「调兵遣将」 push-left to the 兵部 panel (10-army), zoom onto the army list; chip 「兵部」.
Scene 4 (3.25–6.288s): on 「千里之外」 the map (05-map-zoom) fades in full-bleed behind at ~40% and a dashed vermilion route self-draws from 京畿 toward 河北/范阳 (`svg-path-draw`, following the map's own labels); on 「军令要走好几季」 the receipt screenshot (13-receipt) drops in as a card on the right with `zoom-to-target` on its 延期 clause marks, and a vermilion label 「延期」 lands beside it; hold.

## Frame 7 — 历史重演

- scene: 节奏陡变：「范阳起兵」→ 舆图被染红 → 「东都陷落」「潼关失守」「马嵬驿」连砸 → 坏结局「渔阳鼙鼓·历史重演」
- voiceover: "可一步走错：范阳起兵，东都陷落，潼关失守，马嵬驿……盛世，就此终结。"
- duration: 7.608s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/07-collapse.html
- type: pain_point
- persuasion: Pain agitation
- beat: overwhelm
- blueprint: kinetic-type-beats (Adapt)
- asset_candidates: assets/22-war-result-0.png — 结算：范阳起兵; assets/24-war-desk-0.png — 战局舆图（初染红）; assets/24-war-desk-3.png — 战局舆图（大片红、叛军路线、危机计 85–94）; assets/event.fanyang_uprising.webp — 范阳起兵原画; assets/event.tongguan_battle.webp — 潼关之战原画; assets/event.mawei.webp — 马嵬驿原画; assets/25-ending-bad.png — 坏结局画面
- focal: assets/24-war-desk-3.png
- roles: event.fanyang_uprising = background · 22-war-result-0 = supporting · 24-war-desk-0 = supporting · 24-war-desk-3 = supporting (hero) · event.tongguan_battle = background · event.mawei = background · 25-ending-bad = supporting (final hold)
- sfx: impact-heavy, war-drum, low-boom

Adapt: keep the escalating statement-across-beats with a locked finale (signature: each place name its own slam); the beats ride over real game art and screenshots instead of a flat field.
Scene 1 (0.0–1.2s): on 「可一步走错」 hard cut to lacquer; a parchment line 「一步走错」 per-word reveal; a slight camera shake begins.
Scene 2 (1.25–2.2s): on 「范阳起兵」 the uprising painting slams in full-bleed (scrim ~35%) and 「范阳起兵」 slams in vermilion display 900, −5°, on a war-drum hit; the 22-war-result-0 scroll screenshot cuts in small at the right as proof.
Scene 3 (2.26–3.2s): on 「东都陷落」 cut to the war-map desk 24-war-desk-0, then crossfade to 24-war-desk-3 so the red visibly spreads over 河北 / 都畿 (`zoom-to-target` on the red mass); 「东都陷落」 slams.
Scene 4 (3.27–4.3s): on 「潼关失守」 cut to the Tongguan battle painting; slam 「潼关失守」.
Scene 5 (4.35–5.1s): on 「马嵬驿」 cut to the Mawei painting, desaturating toward grey; slam 「马嵬驿」.
Scene 6 (5.22–7.608s): music drops; on 「盛世，就此终结」 the bad-ending screen (25-ending-bad) fades up centered and still with its title 「渔阳鼙鼓·历史重演」 readable; edges fade toward black; hold in near-stillness.

## Frame 8 — AI 驱动

- scene: 从暗场抬起：召对里安禄山的回话 → 廷议三位大臣的发言卡依次弹出 → 好结局「天宝中兴·夺镇弭兵」亮起，三个目标「达成」逐个点亮；角落小字「每位大臣由大模型扮演」
- voiceover: "这是一款 AI 驱动的历史模拟。接上大模型，满朝文武，都由 AI 来演。"
- duration: 7.368s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/08-ai.html
- type: benefit_highlight
- persuasion: Feature-to-benefit translation
- beat: relief + awe
- blueprint: video-text-pivot (Adapt)
- asset_candidates: assets/07-audience.png — 召对安禄山：大幅立像 + 对话; assets/09-debate.png — 廷议：三位大臣画像、立场、发言; assets/31-ending-good.png — 好结局「天宝中兴·夺镇弭兵」与复盘（三目标达成）
- focal: assets/31-ending-good.png
- roles: 07-audience = supporting · 09-debate = supporting · 31-ending-good = background → hero (final)
- sfx: shimmer, riser-soft

Adapt: keep the "surface yields → statement takes the center → sealed" pivot (signature); the surface is the AI conversation, the statement is 「AI 驱动」, the seal is the good ending lighting up.
Scene 1 (0.0–2.7s): light returns: the audience screenshot rises in a gold frame; `zoom-to-target` on An Lushan's reply; a lacquer label types beside it 「AI 驱动」 in display 900 as 「这是一款 AI 驱动的历史模拟」 is spoken (type-on with caret, `discrete-text-sequence`).
Scene 2 (3.29–5.4s): on 「接上大模型，满朝文武」 the audience surface slides aside and the three speech cards (cropped from 09-debate: each portrait + its speech) fan in one by one at the right; a small Noto Sans chip 「每位大臣由大模型扮演」.
Scene 3 (5.57–7.368s): on 「都由 AI 来演」 both surfaces clear and the good-ending screen (31-ending-good) blooms up full-frame (`ambient-glow-bloom` behind it); `zoom-to-target` on its review card so the three 「达成」 marks read, each getting a gold tick in sequence; hold.

## Frame 9 — 你能吗

- scene: 「天宝」墨块标志落定；三行卖点逐条弹出（开源免费 / 打开网页就能玩 / 直接接入 Codex · Claude Code，配一行终端命令）；最后大字「你，能救大唐吗？」+ 仓库地址 github.com/Yi-111-a/tianbao
- voiceover: "开源免费，打开网页就能玩，还能直接接入 Codex 和 Claude Code。你，能救大唐吗？"
- duration: 10.28s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/09-cta.html
- type: cta
- persuasion: Risk reversal
- beat: urgency-to-act
- blueprint: logo-assemble-lockup (Adapt)
- asset_candidates: assets/01-title.png — 标题画面（取左侧墨块标志区域）; assets/title.scroll.webp — 卷轴装饰
- focal: assets/01-title.png
- roles: 01-title = background (full-bleed, heavy scrim ~60%; the ink-blot 「天宝」 logo region kept as the mark) · title.scroll = supporting (parchment strip behind the three lines)
- sfx: whoosh, taiko-hit

Adapt: keep the CTA push-through signature at the end (camera pushes through the mark into the final question + URL); the mark is the game's own ink-blot 「天宝」 crop.
Scene 1 (0.0–1.0s): the title painting under heavy scrim; the ink-blot 「天宝」 logo region (cropped from 01-title, left side) settles at left-center; 「开源免费」 lands as the first parchment line to its right (display 900, with a small vermilion seal 「免费」).
Scene 2 (1.12–2.5s): 「打开网页就能玩」 reveals beneath (per-word).
Scene 3 (2.58–5.8s): 「接入 Codex · Claude Code」 reveals, then a lacquer terminal pill types `codex mcp add tianbao -- tianbao-server mcp` (parchment text, caret); 「Codex」 and 「Claude Code」 get a short gold glow as each is spoken.
Scene 4 (6.3–8.28s): on 「你，能救大唐吗」 a fast camera push-through the logo's ink blot (`multi-phase-camera` push phase, with a horizontal motion blur on the push) resolves to lacquer ground with 「你，能救大唐吗？」 in display 900 (「大唐」 vermilion, −4°) centered in the upper two-thirds and the URL 「github.com/Yi-111-a/tianbao」 wiping in beneath (Noto Sans 600, gold); hold, then a short fade to black at the very end (the film's exit).
