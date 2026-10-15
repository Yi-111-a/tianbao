# Tianbao (751 AD) UI concept images - prompts and review

Generated with Codex CLI 0.159.2 (ChatGPT login, built-in `image_generation`), 2026-10-16. All images 1536x1024 PNG (+1024px-wide webp copies, `contact_sheet.jpg`).

Batches: 3 codex processes in parallel x 3 rounds (3+3+2). No failures, no retries needed. Each image is one `codex exec` call; wall-clock per call 63-75 s (parallel). Total wall-clock about 4 min.

## Command recipe

```
codex exec --skip-git-repo-check --json -C "<outdir>" -s workspace-write -c windows.sandbox="unelevated" "Use your image generation tool to create ONE image: <PROMPT> Landscape 3:2 (1536x1024). After generating, copy the resulting PNG into the current working directory as <name>.png and print its absolute path and pixel size. Do not do anything else." > <name>.jsonl
```

## Shared style block (appended to every screen prompt)

```
A game UI screenshot mockup for a polished high-end PC historical strategy game set in the Tang dynasty, year 751 AD (Tianbao 10th year, Emperor Xuanzong). Diegetic "emperor's desk" interface: the screen is a Tang imperial desk, entry points are physical objects (rolled scrolls, a bound memorial book, an ink stone, seals, tri-colour sancai ceramics, silver and gold Tang vessels). Panels are aged paper or silk with deckled ink-wash edges, calligraphic titles, ink-block buttons. Authentic Tang aesthetic, NOT Ming: palette from Dunhuang murals and Tang silk painting, azurite blue, malachite green, ochre, cinnabar red, gold leaf on aged silk and paper; flowing Tang scrolling-vine (cuancao) and baoxiang flower ornaments, no Ming dragon squares. Tang officials wear round-collar robes (yuanling pao) with soft futou caps, purple, scarlet or green by rank; absolutely no Ming black gauze hats with wing flaps and no mandarin-square badges. Original artwork, not imitating any existing game. Very little visible text: only short large Chinese titles; body text shown as blank lines or placeholder brush strokes. No watermark, no logos. Crisp, readable, game-ready UI composition.
```

Full prompt sent = `<SCREEN text>` + space + `<style block>`.

## 01_title

- File: `01_title.png` (1536x1024), `01_title.webp` (1024 wide)
- Time: 73 s (ran in parallel with 2 other generations)
- Retry: none
- Critique: Strong: dusk Chang'an panorama, gold-leaf clouds, smoke on NE horizon, big gold 天宝 title with clean menu buttons. Off: emperor's robe has a Ming-style dragon roundel and a flat-topped crown instead of a futou; the menu pills are legible but plain; desk objects crowd the bottom.

SCREEN prompt:

```
SCREEN: Title screen. Ink-wash and gold-leaf panorama of Chang'an city at dusk seen from the terrace of Hanyuan Hall of Daming Palace, vermilion pillars and tiled eaves, an aged emperor in a yellow robe seen from behind standing on the terrace, blooming peonies in the foreground, rows of city wards and avenues receding below, and on the far northeast horizon a thin ominous column of smoke hinting at a coming rebellion. At the left, a huge calligraphic title in Chinese characters "天宝" in brush script with gold highlights, and beneath it a short vertical menu list of four ink-block buttons (placeholder short labels such as 开始, 继续, 设置, 退出).
```

## 02_main_map_a

- File: `02_main_map_a.png` (1536x1024), `02_main_map_a.webp` (1024 wide)
- Time: 71 s (ran in parallel with 2 other generations)
- Retry: none
- Critique: Strong: legible silk map with ten circuits and jiedushi labels, Fanyang/Youzhou glowing red, lacquer resource bar with 5 icons/numbers, ink medallion column, scroll and memorial book in the right corners. Off: labels use traditional characters (fine for flavour); coastline and Taiwan look like modern China, not Tang; the medallion icons are small and generic; edict scroll is cropped at the corner.

SCREEN prompt:

```
SCREEN: Main desk and map screen, variant A. Full-bleed hand-painted silk map of the Tang empire showing the ten circuits and the frontier military governorships (jiedushi), mountains and rivers in azurite and malachite on aged silk; Chang'an and Luoyang marked with small palace icons, and Fanyang/Youzhou in the northeast highlighted in a warning red glow. Along the top edge a dark lacquer-and-gold resource bar with five round icons and numbers: treasury coins, grain sack, popular support (people), imperial authority (seal), frontier army strength (sword). Along the right edge a vertical column of round ink medallion buttons with simple glyph icons. Bottom-right: a rolled imperial edict scroll tied with yellow silk cord as the "write edict" entry. Bottom-left: a stack of bound memorial books. Desk objects (ink stone, brush rest, sancai horse figurine, seal) visible at the screen edges.
```

## 03_main_map_b

- File: `03_main_map_b.png` (1536x1024), `03_main_map_b.webp` (1024 wide)
- Time: 75 s (ran in parallel with 2 other generations)
- Retry: none
- Critique: Strong: warm lamplight, angled map, incense-stick gauge (安禄山) is a clever readout, faction silk banners (李/杨/安/高) clear and well coloured. Off: the resource bar is thinner and uses small text, the map has a modern-China coastline (incl. Taiwan, Japan), a dragon-carved chair back at the bottom, and the right-edge medallions (吏/军/外/内) are a short partial column.

SCREEN prompt:

```
SCREEN: Main desk screen, variant B, alternative composition. The silk map of the Tang empire lies on a dark wooden desk at a slight angle, warm oil-lamp lamplight casting soft shadows, corners weighted by bronze paperweights. On the left a bronze vessel with a burning incense stick acting as an "An Lushan threat" gauge, with graduated marks and the burn level near the top, tinted red. Across the top, four coloured silk ribbons hanging like faction influence bands in different lengths: purple, red, green and blue-gold, each with a small round seal glyph (李 杨 安 高). A lacquer-and-gold resource bar with five icons and numbers at the top. Rolled edict scroll bottom-right, bound memorial book bottom-left, round ink medallion buttons along the right edge. Northeast region of the map glows warning red.
```

## 04_memorial

- File: `04_memorial.png` (1536x1024), `04_memorial.webp` (1024 wide)
- Time: 69 s (ran in parallel with 2 other generations)
- Retry: none
- Critique: Strong: clean composition, 奏疏 title, five circular ink vignettes, both ink-block buttons 召见群臣 / 朕已阅 are crisp. Off: the 'dimmed map' behind is barely visible and the panel is a bit sparse; vignette layout is 2+2+1 so the last row is off-centre; no section headings.

SCREEN prompt:

```
SCREEN: Memorial reading panel. A large unfolded memorial (zoushu) on cream silk with brocade border fills the centre, laid over the dimmed, blurred silk map of the empire. Title at top in large brush characters "奏疏". Below, four or five regional report sections, each with a small circular ink-wash vignette illustration (frontier fortress in snow, flooded farmland, caravan on the Silk Road, southwest mountain battle, palace garden) and blank placeholder text lines. At the bottom two large ink-block buttons side by side: left one reading "召见群臣" (cinnabar red), right one reading "朕已阅" (dark ink with gold trim).
```

## 05_edict

- File: `05_edict.png` (1536x1024), `05_edict.webp` (1024 wide)
- Time: 63 s (ran in parallel with 2 other generations)
- Retry: none
- Critique: Strong: the most usable layout: 门下 title, 2x2 input sections with cinnabar seal glyphs 军务/内政/外交/其他 all correct, wooden-gold rollers, advice slips on the left, 廷议/润色 buttons, round red 颁布 seal button. Off: section frames are plain pale rectangles inside the gold silk, and the 颁布 seal button sits tight against the right screen edge.

SCREEN prompt:

```
SCREEN: Edict writing screen. A horizontally unrolled imperial edict scroll in yellow-tinted silk with wooden rollers capped with gold at both ends, over the dimmed desk. Heading at top centre in large brush characters "门下". Four input sections arranged in a 2x2 grid, each marked by a large cinnabar seal glyph in a square seal: 军务, 内政, 外交, 其他, each with blank ruled writing lines. A left column of saved advice slips, small paper tags tied with cords. On the right side a vertical stack of two ink-block buttons: 廷议 and 润色. At bottom-right a big round cinnabar-red seal-stamp button with the characters "颁布" in white seal script.
```

## 06_audience

- File: `06_audience.png` (1536x1024), `06_audience.webp` (1024 wide)
- Time: 67 s (ran in parallel with 2 other generations)
- Retry: none
- Critique: Strong: excellent Tang chancellor portrait (purple round-collar robe, futou with ribbon legs, hu tablet), alternating chat bubbles with portrait avatars, input bar with brush send button, 谏言库 tag. Off: the right paper panel butts straight against the portrait with no frame; bubble avatars are tiny and repeat; the desk props in the foreground are busy.

SCREEN prompt:

```
SCREEN: Minister audience and chat screen. Left 40% of the screen: a large ink-wash half-body portrait of an elderly Tang chancellor with a thin beard, wearing a purple round-collar robe (yuanling pao), a soft black futou cap with two short ribbon-like legs, holding an ivory hu tablet in both hands, painted in the style of Tang court portraits on silk with a soft mist background. Right 60%: elegant dialogue bubbles drawn as paper slips with deckled edges, alternating left/right, with placeholder brush lines instead of text; a text input field styled as a paper strip at the bottom with a small brush icon send button; in the top-right corner a small bookmark icon with the label "谏言库". Top-left name plate in large characters "宰相".
```

## 07_court_debate

- File: `07_court_debate.png` (1536x1024), `07_court_debate.webp` (1024 wide)
- Time: 66 s (ran in parallel with 2 other generations)
- Retry: none
- Critique: Strong: four portrait cards (purple/scarlet/green civil officials + armoured governor with red plume) read instantly, 廷议 scroll banner, 裁决 button and ruling bar. Off: the speech bubbles sit under the cards but do not clearly alternate left/right; hall pillars carry dragon reliefs (slightly Ming/Qing); the officials' hats are tall dark futou, acceptable but the three civil faces are near-identical.

SCREEN prompt:

```
SCREEN: Court debate screen. Top banner shaped as a hanging scroll with a debate topic title in brush characters "廷议". Below it a row of four minister portrait cards on silk with gold frames: three civil officials in round-collar robes (purple, scarlet, green) with soft futou caps, and one military governor in lamellar armour with a red cloak and a plain helmet, each with a nameplate strip. Between and beneath them, speech bubbles on paper alternating left and right, with placeholder brush lines instead of text. At the bottom a wide ruling input bar styled as a paper strip with an ink-block button "裁决" (the emperor's ruling). The backdrop is the dimmed pillared hall of Daming Palace in ink wash.
```

## 08_turn_result

- File: `08_turn_result.png` (1536x1024), `08_turn_result.webp` (1024 wide)
- Time: 73 s (ran in parallel with 2 other generations)
- Retry: none
- Critique: Strong: numbers are the most legible of any screen: red up-arrow +1200/+800/+15 and green down-arrow -350/-120 with clear icons; check/cross marks per clause; 推演结果 header; 下一年 button. Off: clause rows are blank lines only (no text, as asked); the Nanzhao vignette reads as generic misty mountain fortress; the desk-wide layout leaves the ledger and scroll as separate cards.

SCREEN prompt:

```
SCREEN: Turn result and chronicle screen. A central scroll titled "推演结果" in large brush characters. On it a list of five edict clauses, each a short blank-line row with a large cinnabar red check mark beside accepted clauses and a grey cross mark beside rejected ones. To the right a ledger column on silk showing five rows of icon plus clear large numbers, with up-arrows and positive numbers in red and down-arrows and negative numbers in green, highly legible. At bottom-left a small framed illustrated event vignette of a frontier battle in the misty Nanzhao mountains of the southwest, Tang soldiers in lamellar armour and banners. An ink-block button "下一年" bottom-right. Emphasise legibility of the numbers.
```

## Cross-cutting notes for the style guide

- The shared style block works: Tang palette (azurite/malachite/gold/cinnabar), 圆领袍 and futou were respected in 06 and 07. Residual Ming/Qing leakage: dragon roundels on the emperor's robe (01), dragon-carved chair back (03), dragon pillars (07). Add 'no dragons' to the style block to fix.
- Short Chinese titles (天宝, 奏疏, 门下, 廷议, 谏言库, 推演结果, 颁布, 召见群臣, 朕已阅) rendered correctly; 02/03 map labels also correct but in traditional characters. Placeholder strokes instead of body text worked.
- Maps follow modern-China coastline shape; prompt for 'Tang territory incl. Anxi/Beiting protectorates, Tibetan plateau outside borders' if geography matters.
- Numbers in 02/03/08 render legibly at this resolution; use these as the reference for the resource bar and ledger.