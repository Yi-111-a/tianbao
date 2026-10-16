# Asset inventory — 《天宝》 promo

Every asset is real: screenshots and screen recordings of the game running against its engine
(1920×1080, `tests/e2e/promo_capture.spec.ts`), plus the game's own scenario art (Codex-generated).
No mock-ups. Palette of the UI: lacquer black, gold leaf (泥金 #c9a24b), vermilion (#c0392b), parchment.

## Screenshots — opening season (天宝十载春, a fresh 史实 game)

- 01-title.png — title screen: Xuanzong in yellow robe on a palace balcony at sunset overlooking Chang'an, smoke rising on the horizon; ink-blot logo 「天宝」, menu, tagline 「盛世只剩最后四年。你能阻止安史之乱吗？」. Hero image, wide.
- 02-newgame.png — new-game scroll: scenario intro, difficulty choice (演义/史实/地狱), character portraits.
- 03-desk-tutorial.png — main desk with the tutorial note open (bottom-left).
- 04-desk.png — THE main screen: painted map of Tang China framed on a brocade desk; top resource bar (国库 3,000 / 太仓 2,500 / 君威 68 / 民心 62 …); four faction ribbons (安、杨、高、李) hanging at top; crisis gauge 「渔阳鼙鼓 27–36 承平」 top-right; 范阳/平卢 tinted teal as 安禄山所领; 奏疏 book bottom-left, 拟诏 scroll and 推演本季 button bottom-right.
- 05-map-zoom.png — map zoomed in on 河北 / 范阳 / 潼关 / 京畿 (wheel zoom), region tooltip open.
- 06-memorial.png — 奏疏 panel: memorial list on the left, 「禄山在京未归」 open with ministers' advice and options.
- 07-audience.png — 召对 安禄山: big portrait of An Lushan (fat, smiling, purple robe, hat in hand) left; dialogue on parchment right; agenda counter 「召对 1/3 · 廷议 0/1」. (Retaken after a fix: his reply now refers to his own army in the first person.)
- 08-debate-setup.png — 廷议 setup: pick topic and ministers (only those in the capital can attend).
- 09-debate.png — 廷议 result: three ministers' portraits (李林甫 附议, 杨国忠 反对, 颜真卿 反对), each with their argued option and speech, tally bar at bottom. (Retaken after a fix: the topic line no longer shows option ids.)
- 10-army.png — 兵部 panel: list of armies with strength, commander, location; map on the right.
- 11-cards.png — 拟诏 with the policy-card picker open (27 cards: 赈灾, 修城, 团结兵…).
- 12-edict.png — 门下 edict scroll: adopted memorial options + a policy card, sections.
- 13-receipt.png — edict preview receipt: each clause marked 即行 / 延期 (courier delay), red 颁布 seal button.
- 14-result.png — 推演结果 scroll after the first season: event art left (禄山留京), chronicle text, ledger column right with ▲▼ changes, 下一季 button.
- 15-result-ledger.png — same scroll scrolled down to the itemized ledger and crisis breakdown.

## Screenshots — the rebellion (a game where nothing was done, 天宝十四载冬 → 十五载冬)

- 20-desk-before.png — desk one season before the rebellion; red banner 「下次结算即终局」, crisis gauge high.
- 21-crisis.png — crisis gauge breakdown popover 「渔阳鼙鼓·鼙鼓动地」: what pushes the crisis each season.
- 22-war-result-0.png — 推演结果 天宝十四载冬: 「范阳起兵」 — chronicle 「安禄山发所部及同罗、奚、契丹、室韦兵十五万，号二十万……反于范阳」. (Its illustration frame was still loading in this take; retaken.)
- 22-war-result-1.png — next season's result: 河东兵从乱 / 叛军游骑掠境, battle art.
- 22-war-result-2.png — 东都陷落 (Luoyang falls), burning-city art.
- 22-war-result-3.png — 潼关失守 / 车驾西幸, war-council art.
- 22-war-result-4.png — final season result 渔阳鼙鼓·历史重演 / 马嵬驿, rainy mountain road art.
- 24-war-desk-0.png … 24-war-desk-3.png — desk during the war: 范阳、平卢、河北、都畿 painted RED as rebel-held, rebel march routes (dashed red) toward 洛阳 and 潼关, crisis gauge 85–94 「鼙鼓动地」, crisis breakdown open. The red spreads season by season (0 → 3).
- 25-ending-bad.png — ending screen 「渔阳鼙鼓·历史重演」 over dark rain art of the imperial flight on a plank road; text 「潼关失守，銮舆西幸。马嵬驿前，六军不发……盛世自此终结。」; review card: 弭兵 已失 / 皇权在握 已失; 君威 6.8, 民心 22.5.
- 26-ending-bad-review.png — same ending with the review expanded.

## Screenshots — the good ending (GPT's game, 天宝十四载冬)

- 30-desk-good.png — desk one season before the good ending: map calm, no red.
- 30-result-good.png — final result scroll with ending art.
- 31-ending-good.png — ending screen 「天宝中兴·夺镇弭兵」 over bright art (court ladies, peonies, palace at sunrise, cranes); all three goals 达成; 君威 79.3, 民心 67.7.
- 32-ending-good-review.png — same, review expanded.

## Game art (scenario assets, 1344×896 events / 768×1152 portraits)

- event.fanyang_uprising.webp — the uprising: An Lushan's army marching out of Fanyang at night, torches.
- event.fanyang_armoury.webp — Fanyang armoury, weapons stockpiled.
- event.tongguan_battle.webp — battle at Tongguan pass.
- event.mawei.webp — Mawei station: the six armies refuse to march.
- ending.e4_history.webp — bad ending art (imperial flight on the plank road, rain).
- ending.fail_changan.webp — Chang'an falls.
- ending.e1_zhongxing.webp — good ending art (peonies, court, sunrise).
- portrait.an_lushan.default.webp — An Lushan in court robe, smiling (portrait, tall).
- portrait.an_lushan.armor.webp — An Lushan in armour.
- portrait.xuanzong.default.webp — Emperor Xuanzong.
- portrait.yang_guifei.default.webp — Yang Guifei.
- title.scroll.webp — decorative scroll art.

## Screen recordings [video] (1920×1080, no audio)

- clip-a-opening.mp4 [video] — 98.8 s: title screen animates in (0–4 s) → new game → desk appears (~8 s) → map wheel-zoom toward 范阳 and drag (~14–20 s) → 奏疏 panel → 召对安禄山 and his reply → 廷议 set-up and result → 兵部 → back to 奏疏, adopt options → 拟诏 + policy card picker → receipt → 颁布 → 推演结果 scroll unrolls and scrolls (last ~15 s).
- clip-b-rebellion.mp4 [video] — 74.7 s: resume the doomed game → crisis breakdown → 推演本季 → 范阳起兵 result → the map turns red season by season, rebel routes extend → 东都陷落 → 潼关失守 → ending 「渔阳鼙鼓·历史重演」 fades in (last ~20 s held).
- clip-c-good.mp4 [video] — 35.3 s: resume GPT's game → 推演本季 → final result → ending 「天宝中兴·夺镇弭兵」 fades in.
