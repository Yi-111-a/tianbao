# -*- coding: utf-8 -*-
"""Job definitions for Tianbao asset generation. id -> dict(kind, aspect, subject, ref?)."""
NOTEXT = " Absolutely no text, no characters, no letters, no numbers anywhere in the image."
WHITE = " Isolated on a plain flat pure white background (#FFFFFF) with generous empty margin around, soft contact shadow only."

LAND = "Landscape 3:2 aspect ratio (1536x1024)."
PORT = "Portrait 2:3 aspect ratio (1024x1536)."

JOBS = {}


def add(id, group, aspect, subject, ref=None, outkind=None):
    JOBS[id] = dict(id=id, group=group, aspect=aspect, subject=subject + NOTEXT, ref=ref,
                    kind=outkind or id.split(".")[0])


# ------------------------------------------------------------------ MAP + UI
add("map.base", "map", LAND,
    "SUBJECT: A full-bleed flat top-down hand-painted silk map of the Tang empire in 751 AD, no perspective, no desk, no frame, painted edge to edge on aged silk. "
    "Territory: from the Western Regions oasis deserts and the Tianshan edge at far left, the high Tibetan plateau (snowy blue-white mountains, outside the empire) at lower left, the Guanzhong plain and Qinling mountain range in the centre, the Taihang mountains running north-south, the Yellow River with its great northern bend, the Yangtze River in the south, the Grand Canal and Bian canal drawn as thin straight waterways joining the Yellow River plain to the Yangtze delta, the narrow Tongguan pass gorge where the Yellow River turns east near the centre, northern steppes and the Liaodong forest at the top right, the Sichuan basin at lower centre-left, the misty Yunnan highlands at lower left, the southern coast at lower right. "
    "The eastern and southern sea is only a plain calm blue-green expanse along the right and bottom edges with simple wave scrolls: NO islands, NO Taiwan, NO Japan, NO Korea detail, NO modern coastline emphasis. "
    "Mountains painted in azurite blue and malachite green blue-green landscape style, farmland and plains in warm ochre and silk-yellow, deserts pale sand, steppes muted olive. Tiny palace and city-wall icons for about ten cities (blank, no labels), small camel caravans in the west, faint dotted road lines. Soft cloud and mist wisps in gold leaf at the edges, fading naturally to silk at the borders. "
    "NO text, NO labels, NO map legend, NO compass, NO cartouche, NO border lines with writing.")

add("title.scroll", "ui", LAND,
    "SUBJECT: Title screen painting. Ink-wash and gold-leaf panorama of Chang'an city at dusk seen from a high terrace of Hanyuan Hall of Daming Palace, vermilion pillars and grey-tiled eaves in the foreground at the edges, rows of city wards and grid avenues receding below into evening haze, golden cloud banks, a lone aged emperor in an ochre-yellow robe and a soft folded-top cap seen from behind at the far right of the terrace, blooming peonies in the foreground lower right, and on the far northeast horizon one thin ominous column of dark smoke. The entire left third of the image is left calm and uncluttered (soft golden clouds and distant rooftops) as an empty space for a title to be added later. No dragons on the robe or railings.")

add("ui.desk", "ui", LAND,
    "SUBJECT: UI background texture: top-down view of a Tang imperial desk surface. Deep dark reddish-brown lacquered wood grain across the centre, framed all around by a wide woven brocade table runner border with baoxiang flower rosettes and cuancao scrolling vines in gold, azurite and cinnabar on dark indigo ground. The centre area is calm and empty and evenly lit for panels to be placed over it. Maybe a tiny hint of a brass paperweight in each corner, nothing else. Flat top-down, no perspective.")

add("ui.paper", "ui", LAND,
    "SUBJECT: UI texture: a single sheet of aged yellowish hemp paper (huangma paper) with visible fibres, filling the image almost to the edge, slightly irregular deckled torn ink-wash edges, faint mottled stains, soft vignette; the surface is completely blank and empty, evenly lit, flat top-down. Plain very dark brown background visible only in the thin corner gaps.")

add("ui.silk", "ui", LAND,
    "SUBJECT: UI texture: tileable seamless aged silk brocade fill, flat top-down, filling the entire frame edge to edge. Pale gold-ochre silk ground with a subtle regular woven pattern of baoxiang flower rosettes and cuancao scrolling vines and pearl roundels in slightly darker gold tone and a few azurite and malachite accents; low contrast so text can sit over it. No border, no vignette, no focal object.")

add("ui.edict_paper", "ui", LAND,
    "SUBJECT: A horizontally unrolled imperial edict scroll, centred, taking nearly the whole frame: bright yellow-tinted hemp paper (imperial yellow) surface with a very faint baoxiang flower watermark pattern, a gold and brocade silk border of cuancao scrolling vines top and bottom, round wooden rollers capped with gold at left and right ends, completely blank empty writing surface, soft shadow on a dark desk backdrop. Flat frontal view.")

add("ui.lacquer_bar", "ui", LAND,
    "SUBJECT: UI element: a very wide horizontal dark black-lacquer resource bar with thin gold inlay border, gold baoxiang flower corner ornaments at both ends and a subtle cuancao scroll line inside the edge, five empty round recessed circular medallion sockets evenly spaced along it with thin gold rims, and long empty dark space beside each socket. The bar spans the full width of the image, centred vertically, height about one quarter of the image, perfectly straight and flat frontal view, with a plain flat pure white background above and below it.")

add("ui.ink_button", "ui", LAND,
    "SUBJECT: UI element: a single rectangular Chinese ink stick (ink block) used as a button, black ink with a faintly glossy surface, slightly rounded top and bottom edges with one corner gently bevelled, thin gold line border, completely plain empty flat face with only a very faint embossed cuancao vine pattern at both ends and a blank centre, shown straight on, flat frontal view, filling about 60% of the image width." + WHITE)

add("ui.seal", "ui", LAND,
    "SUBJECT: UI element: a single round cinnabar-red seal ink-paste stamp shape, slightly irregular rough edges with dry-brush flying-white texture, plain empty blank centre (no glyph, no carving), thin slightly darker rim, flat frontal view, filling about 55% of the image height, centred." + WHITE)

add("ui.crisis_drum", "ui", LAND,
    "SUBJECT: UI element: a Tang dynasty war drum (large barrel drum with studded hide drumheads and a red-lacquered body with gold bands) seen from slightly the front-left, with two wooden drumsticks crossed in front of it. The drumhead face is divided into four equal pie quadrants tinted in a gradient from calm malachite green, to gold, to burnt orange, to cinnabar red, as a four-stage threat gauge. No dragons. Flat clean game-icon rendering, centred." + WHITE)

for f, desc, col in [
    ("xiang", "deep purple silk (#5B3A6B) with gold thread, hanging banner for the chancellor's faction", "purple"),
    ("yang", "cinnabar red silk (#C0392B) with gold thread, hanging banner for the Yang consort-kin faction", "red"),
    ("fanyang", "malachite green silk (#3E7F6B) with gold thread, hanging banner for the Fanyang frontier army faction", "green"),
    ("neiting", "azurite blue silk (#2F5D8A) with gold thread, hanging banner for the inner-palace eunuch faction", "blue"),
]:
    add(f"ui.ribbon_{f}", "ribbons", PORT,
        f"SUBJECT: UI element: a single vertical hanging silk banner ribbon filling the whole image, straight frontal view, {desc}. Pearl roundel (lianzhu) border down both long edges, a round empty gold medallion disc with a blank baoxiang flower rosette in the upper third (no glyph), cuancao vine pattern woven below it, and a swallow-tail (V-notched) bottom hem with a short gold tassel at the tip; the top has a slim dark wooden hanging bar. The silk fills the frame edge to edge on a plain flat pure white background in the narrow gaps only. No text.",
        outkind="ui")

add("icon.sheet", "icons", LAND,
    "SUBJECT: A sprite sheet of TEN separate round medallion game icons arranged in two rows of five, evenly spaced with wide gaps on a plain flat pure white background; each icon is a circular dark lacquer disc with thin gold rim containing a simple bold gold-and-colour emblem painted in Tang style, in this exact order. Row 1, left to right: (1) a stack of Tang copper coins and a silver ingot (treasury); (2) a round grain sack with ears of millet (grain); (3) a square jade imperial seal block with tassel (imperial authority); (4) two folk figures in simple clothes holding hands, people's morale; (5) a coin purse eaten by moths with a worm, corruption. Row 2: (6) a frontier watchtower with a thin rising smoke beacon column and a crossed spear (frontier pressure); (7) a stylised wolf head in profile with a small red glow eye (ambition of a warlord); (8) a lamellar helmet with a red plume over a tally banner (military governors' power); (9) two crossed ivory court tablets (hu) facing each other with sparks (court strife); (10) a roaring beacon fire flame under a drum (rebellion risk). Same size, same style, no text, no numbers.",
    outkind="icon")

# ------------------------------------------------------------------ PORTRAITS
PW = " Half-length vertical portrait of a single person, centred, from head to mid-thigh, facing three-quarter view, painted on silk in Tang court-portrait style with gold line work, background is a softly misted ink-wash scene fading to the edges. Face clearly visible, expressive, individualised. "

P = {}
P["xuanzong"] = ("Emperor Xuanzong of Tang, age 66, white-streaked hair and a long thin white-flecked beard, weary yet majestic expression, wearing an ochre-yellow (zheshi) round-collar robe with a soft folded-top cloth cap (zheshang jin) and a jade-plaqued belt, hands folded in sleeves. Background: misted Huaqing Palace hot-spring halls and Mount Li. No dragon embroidery on the robe, only subtle baoxiang rosettes.")
P["li_linfu"] = ("Li Linfu, chancellor, age 70, thin elegant face, soft pleasant smile but cold calculating eyes, thin moustache and a wispy beard, purple round-collar robe with a gold fish-pouch at the belt, black soft-legged futou cap, holding an ivory hu tablet. Background: soft-focus Secretariat office with towering shelves of paper scrolls.")
P["yang_guozhong"] = ("Yang Guozhong, finance official, age 52, stocky, shrewd sharp eyes, thin moustache, smug expression, scarlet round-collar robe with a silver fish-pouch, black futou cap, holding a handful of counting rods in one hand and an open account ledger in the other. Background: blurred treasury hall with rows of cash strings.")
P["yang_guifei"] = ("Yang Yuhuan (Consort Yang), age 32, plump full-faced Tang beauty, gentle playful smile, high-waisted pleated long skirt in cinnabar and green, short bare-shouldered jacket, a long pibo shawl, a high bun with gold hairpins and flowers, red huadian on the forehead, holding a round silk fan. Background: misted peony garden by a palace pavilion.")
P["gao_lishi"] = ("Gao Lishi, senior palace eunuch, age 66, tall, beardless pale smooth face, calm and composed, purple round-collar robe with a gold fish-pouch, black soft futou cap, hands folded in sleeves. Background: soft vermilion palace corridor with hanging lanterns.")
P["li_heng"] = ("Li Heng, crown prince, age 40, anxious, wary and restrained expression, short beard, dusky deep-red round-collar robe with a soft black futou cap, hands tucked in sleeves. Background: dim lamp-lit Eastern Palace study with bookshelves.")
P["chen_xilie"] = ("Chen Xilie, left chancellor, age 55, timid meek round face, thin beard, purple round-collar robe with gold fish-pouch, soft black futou cap, holding an ivory hu tablet loosely, stooped. Background: soft-focus Chancellery hall.")
P["an_lushan"] = ("An Lushan, frontier military governor, age 48, extremely obese Sogdian-Turkic man, huge round belly pressing the belt, round face with a thick black curly beard, small shrewd smiling eyes, jovial cunning expression, purple round-collar robe straining across the belly with a gold fish-pouch, holding a felt hat in one hand. Background: silk-draped palace banquet hall with warm lamplight.")
P["shi_siming"] = ("Shi Siming, frontier general, age 48, lean wiry, hawk-like narrow eyes, sparse beard, a dark military round-collar robe with leather bands, a bow case on the back, felt-wrapped head cloth. Background: dusty northern fortress yard under a grey sky.")
P["ji_wen"] = ("Ji Wen, scheming official, age 50, narrow cunning face, thin lips, scarlet round-collar robe, black soft futou cap, one hand holding a bamboo-slip dossier. Background: gloomy censorate chamber with lamps.")
P["geshu_han"] = ("Geshu Han, northwestern military governor, age 55, burly broad-shouldered, hearty bold expression, big black beard, ruddy face, descendant of Turkic Tujue nobility, purple round-collar robe with gold fish-pouch, bareheaded with a topknot and a plain futou. Background: Longyou plateau with snow mountains and a mounted guard.")
P["gao_xianzhi"] = ("Gao Xianzhi, Anxi military governor, age 46, handsome Goguryeo-descended man, sharp confident eyes, short moustache, purple round-collar robe with gold fish-pouch, black futou cap. Background: Silk Road oasis fortress with a distant camel caravan.")
P["feng_changqing"] = ("Feng Changqing, staff officer, age 45, small thin plain-looking man with a slight limp stance leaning on a cane, sharp clever eyes, sparse thin beard, green round-collar robe, black soft futou cap, holding a rolled document. Background: Anxi garrison desert fort at dawn.")
P["an_sishun"] = ("An Sishun, Hexi military governor, age 50, stocky Sogdian-descended man with a high nose, thick curly beard, guarded expression, purple round-collar robe with gold fish-pouch, black futou cap. Background: Hexi corridor Gansu fort with Qilian mountains.")
P["guo_ziyi"] = ("Guo Ziyi, Shuofang army officer, age 54, tall, broad, kind steady face, full neat beard, warm dignified expression, scarlet round-collar robe with belt plaques, black futou cap, hand resting on the sword hilt. Background: Shuofang frontier camp with tents.")
P["li_guangbi"] = ("Li Guangbi, army officer, age 46, Khitan-descended, stern taciturn face, thin lips, short sparse beard, intense eyes, scarlet round-collar robe with belt plaques, black futou cap, arms crossed in sleeves. Background: grey frontier fort wall at dusk.")
P["yan_zhenqing"] = ("Yan Zhenqing, censor, age 42, square upright face, full black beard, firm righteous gaze, green round-collar robe, black futou cap, holding an ivory hu tablet upright. Background: soft-focus censorate hall with brush stands and bamboo slips.")
P["yan_gaoqing"] = ("Yan Gaoqing, provincial secretary, age 54, scholarly gentle face with a modest outward smile and hidden resolve in the eyes, short grey beard, green round-collar robe, black futou cap, hand tucked in sleeve. Background: lamp-lit Fanyang office with document shelves.")
P["xianyu_zhongtong"] = ("Xianyu Zhongtong, Jiannan military governor, age 55, plump self-satisfied face, small moustache, purple round-collar robe with gold fish-pouch, black futou cap. Background: misty southwest mountains and a rope bridge.")
P["bian_lingcheng"] = ("Bian Lingcheng, military supervisor eunuch, age 45, beardless smooth face, obsequious sly smile, scarlet round-collar robe, black soft cap, holding a yellow silk imperial tally (blank). Background: military camp tents.")

for cid, desc in P.items():
    add(f"portrait.{cid}.default", "portraits", PORT, "SUBJECT:" + PW + desc, outkind="portrait")

ARMOR = {
    "an_lushan": "Same person as the reference image (An Lushan, extremely obese, thick curly beard, Sogdian-Turkic face), but now in rebellion: wearing Tang lamellar armour (mingguang cuirass) with a black-and-red cloak, a plumed iron helmet, grim triumphant expression. Background: night at Fanyang with beacon fires and torches.",
    "geshu_han": "Same person as the reference image (Geshu Han, burly, big black beard), now in full Tang lamellar armour with red cloak and helmet, one hand on a sword, commanding expression. Background: Tongguan gorge and the Yellow River.",
    "gao_xianzhi": "Same person as the reference image (Gao Xianzhi, handsome, short moustache), now in full Tang lamellar armour with a white-and-blue cloak and plumed helmet. Background: Western Regions desert fort and tall mountains.",
    "guo_ziyi": "Same person as the reference image (Guo Ziyi, kind steady face, full neat beard), now in full Tang lamellar armour with a dark red cloak and plain helmet. Background: Shuofang frontier camp with banners (plain, no text).",
    "li_guangbi": "Same person as the reference image (Li Guangbi, stern thin lips, short beard), now in full Tang lamellar armour with a dark cloak and iron helmet. Background: Taiyuan city wall and grey sky.",
    "shi_siming": "Same person as the reference image (Shi Siming, lean, hawk eyes, sparse beard), now in full Tang lamellar armour with a dark cloak, helmet under arm. Background: northern fortress yard with torches.",
}
for cid, desc in ARMOR.items():
    add(f"portrait.{cid}.armor", "armor", PORT, "SUBJECT: Keep the face, age and identity of the attached reference portrait exactly." + PW + desc,
        ref=f"portrait.{cid}.default", outkind="portrait")

# ------------------------------------------------------------------ EVENTS
EV = {
    "hedong_grant": "Three jiedushi military-governor staffs (jiejie: tall poles hung with tiers of yak-tail tassels) planted beside an unrolled imperial edict with a yellow silk ribbon on a lacquered table, in a palace hall with vermilion pillars; blank blank paper, warm light.",
    "xi_er": "An imperial palace celebration of festive brocade splendour: court ladies in high-waisted skirts and pibo shawls carrying a very large embroidered silk cradle-litter between them across a courtyard, others laughing behind fans, Consort Yang in the background, silk streamers, tasteful and warm, nothing grotesque, a huge hu-man figure only partly hidden in silks.",
    "xier_defeat": "Misty Cangshan mountains and Erhai lake in Nanzhao in the southwest, Tang soldiers in lamellar armour fleeing in disarray along a muddy lake shore, broken spears and fallen plain banners, grey rain, low drifting cloud.",
    "talas": "A wide central Asian river valley with poplar trees and snow peaks, Tang armoured cavalry clashing with Abbasid riders under black flags (plain, without any symbols) across a shallow river, dust clouds, a tense dusk sky.",
    "khitan_defeat": "Cold snowy steppe along a frozen river in the northeast, the Fanyang army in lamellar armour retreating in the snow while Khitan horse archers fire from the ridge in the distance, plain banners, cold blue dusk light.",
    "li_linfu_death": "An empty chancellor's mansion hall at night, a purple official robe and a black futou cap laid on an empty seat, white funeral drapes, candles guttering, a lone servant in the doorway seen from behind, stillness and ambiguity.",
    "guozhong_chancellor": "A grand Secretariat hall with vermilion pillars: an official in a freshly bestowed purple robe receiving a lacquer box seal of office from a eunuch, rows of officials in scarlet and green bowing, seen from a distance in warm light.",
    "an_court_visit": "Huaqing Palace on Mount Li in winter mist: grey tiled pavilions around steaming hot spring pools, bare plum branches, a procession of mounted guards and an obese general on a horse arriving along a snowy path, soft pale fog.",
    "autumn_rains": "The Guanzhong plain in autumn: endless grey rain and flooded millet fields, peasants wading, a stalled ox cart, the walls and towers of Chang'an faint in the distance, wet reflective light.",
    "fanjiang_swap": "A military parade ground: a ceremony of exchanging banners, Hu-ethnic generals in lamellar armour receiving plain banners from a pavilion while Han officers in robes step aside, ranks of soldiers in the background, dust, tense atmosphere.",
    "horse_tribute": "Three thousand fine horses driven in a long dusty stream by Hu riders in felt hats across a plain towards the distant walls of Chang'an, a pavilion with court officials watching with unease, lowering sky.",
    "fanyang_uprising": "A night scene at Youzhou in the north: huge war drums being struck in a fortress courtyard, soldiers with torches massing, beacon fires burning on the tower, red glow on armour, cold black sky with sparks, the beginning of a rebellion.",
    "tongguan_battle": "The Yellow River gorge at Tongguan pass: a narrow valley between steep loess cliffs with a fortified pass gate, a Tang army marching out in lamellar armour along the river, dust and dark clouds gathering, dramatic but painterly.",
    "mawei": "A restrained scene: a quiet post-station courtyard at Mawei at dusk, a closed lacquered carriage with a yellow canopy, a ring of soldiers in armour silhouetted with lowered spears, one lone yellow silk pibo shawl draped over a bench, no death shown, heavy mood, red evening sky.",
}
for eid, desc in EV.items():
    add(f"event.{eid}", "events", LAND,
        "SUBJECT: Narrative game illustration, wide cinematic composition, painterly Tang style. " + desc + " Plain banners and flags without any symbols or glyphs.", outkind="event")

END = {
    "e1_zhongxing": "Dawn over Chang'an: golden light on the vermilion pillars and tiled roofs of Daming Palace, peonies in bloom, frontier soldiers resting arms in a peaceful courtyard in the foreground, flocks of cranes rising, hopeful and serene.",
    "e2_frontier_lost": "A remote frontier fortress at the empire's edge, the garrison withdrawn, the beacon tower unlit, steppe horse riders streaming past under a dusky sky in the distance while Chang'an stands intact but shrunken far behind in the haze, bittersweet mood.",
    "e3_restoration": "Dawn at the recaptured eastern capital Luoyang: Tang cavalry in lamellar armour riding through a repaired city gate under plain red banners, hopeful dawn, smoke clearing from the ruins, a restored palace hall beyond.",
    "e4_history": "The Tang court fleeing west along a high plank road through the Qinling mountains in rain at dusk, a small convoy with a yellow-canopied carriage and weary soldiers, cliffs and mist, melancholy.",
    "e5_yang": "A dim imperial hall with an empty ochre-silk throne draped with a curtain; shadowy figures of scheming courtiers and eunuchs gathering at the pillars in the background, an unlit candelabra, sinister quiet, red-brown tones.",
    "e6_abdication": "A solemn dawn abdication ceremony in front of a grand hall: an aged emperor in ochre-yellow robe handing a lacquered box with a jade seal to a younger crown prince in a deep red robe on the stairs, courtiers bowing in rows far below, soft golden light.",
}
for eid, desc in END.items():
    add(f"ending.{eid}", "endings", LAND,
        "SUBJECT: Epilogue illustration for a game ending, wide cinematic composition, painterly Tang style. " + desc, outkind="ending")

EV2 = {
    "abusi_revolt": "A frontier camp at dusk: tribal cavalry in felt hats and furs riding away northward in a long column leaving abandoned tents, a Tang border garrison watching silently from a wall with plain banners, dust and low sun.",
    "changshan_rising": "Dawn at the gate of a northern city: townspeople and soldiers raising plain banners and spears, a scholar-official in a green round-collar robe standing resolute at the centre of the gate arch, torches paling in the morning light, a righteous uprising.",
    "donggong_framed": "A candle-lit palace corridor at night: an official in a scarlet robe whispering to a eunuch behind a carved screen, and in the foreground a lamp-lit prince's study desk with an unsealed memorial and a nervous silhouette, sinister secrecy.",
    "duji_falls": "The eastern capital Luoyang at night: flames over the city walls and gate towers, fleeing citizens crossing a stone bridge over the Luo river, rebel cavalry silhouettes on the horizon, smoke and red glow, restrained, no gore.",
    "feng_gao_executed": "Restrained scene: a military camp at dawn, two empty lamellar armour stands with two helmets resting on a mat before a command tent, a eunuch in a scarlet robe holding a yellow silk tally walking away, soldiers kneeling in the distance with bowed heads, no death shown, bleak grey light.",
    "frontier_raid": "A snowy frontier: mounted raiders in furs attacking a stone beacon tower while thick beacon smoke rises, a small Tang garrison in lamellar armour defending the rampart, plain banners, cold bright light.",
    "geshu_an_quarrel": "A palace banquet hall: a burly bearded general in a purple robe and a hugely obese general in a purple robe glare at each other across low tables, courtiers frozen, wine cups spilled, musicians stopped, an emperor in ochre-yellow watching from the dais, warm lamplight.",
    "guozhong_raid": "A Chang'an ward at night: armoured city guards with torches and spears surrounding the gate of a large mansion, neighbours peeking from doorways, sleepy lanterns, tense stand-off.",
    "li_mi_disaster": "A Yunnan jungle marsh near Erhai lake: a Tang army trapped in mud and mist, fevered soldiers sitting among abandoned wagons and fallen banners, dark humid foliage, grey-green light, bleak mood, no bodies shown.",
    "nanzhao_tribute": "A frontier hall: Nanzhao envoys in layered southwestern ethnic dress presenting gifts of gold, ivory and woven cloth, with a tame elephant outside in the courtyard, Tang officials receiving them in round-collar robes, peace and ceremony, misty mountains beyond.",
    "summon_refused": "A northern fortress gate closed: an imperial messenger in a scarlet robe on a horse before the shut gate and armoured guards on the wall looking down impassively, the yellow silk edict still in his hand, grey sky, standoff.",
    "zhenqing_to_pingyuan": "Dawn on a willow-lined road east of Chang'an: an official in a green round-collar robe riding out on horseback with a few servants and a baggage mule, a few farewell officials in purple and scarlet waving from a roadside pavilion, morning mist.",
}
for eid, desc in EV2.items():
    add(f"event.{eid}", "events2", LAND,
        "SUBJECT: Narrative game illustration, wide cinematic composition, painterly Tang style. " + desc + " Plain banners and flags without any symbols or glyphs.", outkind="event")

END2 = {
    "e5_beisi": "A dim imperial hall: armoured palace guards lining the walls around a feeble ochre-silk throne with the emperor slumped small upon it, a eunuch general in a purple robe standing at its side holding a yellow silk tally, torches, cold red-brown tones, military dominance of the inner court.",
    "fail_changan": "Chang'an falling at night: the roofs of the great palace and city gate towers ablaze, rebel torches pouring through the streets, a column of refugees on the road in the foreground, smoke over the moon, restrained, no gore.",
    "fail_regicide": "A dark palace hall at night: rows of armoured soldiers with lowered spears standing before an empty ochre-silk throne, torchlight, a discarded imperial futou cap on the steps, no violence shown, heavy silence.",
    "fail_bankrupt": "An empty imperial treasury storehouse: rows of open empty chests, scattered copper cash strings and cobwebs, one lone clerk with a ledger in grey light, unpaid soldiers waiting silently outside the doorway, bleak.",
    "open_storm": "Chang'an in a calm golden afternoon with peonies on a palace terrace, but over the northeast horizon a black storm front is gathering with faint beacon smoke columns rising, a lone figure in an ochre-yellow robe at the railing looking toward it, the quiet before the storm.",
}
for eid, desc in END2.items():
    add(f"ending.{eid}", "endings2", LAND,
        "SUBJECT: Epilogue illustration for a game ending, wide cinematic composition, painterly Tang style. " + desc, outkind="ending")

add("portrait.feng_changqing.armor", "armor2", PORT, "SUBJECT: Keep the face, age and identity of the attached reference portrait exactly." + PW + "Same person as the reference image (Feng Changqing, small thin plain-looking man, sparse thin beard, sharp clever eyes, leaning slightly on a cane), now in simple practical Tang lamellar armour with a dark green cloak and an iron helmet, resolute expression. Background: eastern capital Luoyang city wall under a stormy sky, hastily recruited soldiers drilling.", ref="portrait.feng_changqing.default", outkind="portrait")
add("portrait.yang_guozhong.purple", "armor2", PORT, "SUBJECT: Keep the face, age and identity of the attached reference portrait exactly." + PW + "Same person as the reference image (Yang Guozhong, stocky, shrewd eyes, thin moustache), now promoted to chancellor: wearing a purple round-collar robe with a gold fish-pouch and a black soft futou cap, more arrogant and self-satisfied, holding the account ledger and counting rods. Background: the Secretariat hall with towering shelves.", ref="portrait.yang_guozhong.default", outkind="portrait")
