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

# ------------------------------------------------------------------ ART ROUND 2 (events3 + seasons)
EV3 = {
    "changan_falls": "Dawn at the great southern gate tower of Chang'an: the huge gate wide open, a long column of rebel horsemen in dark lamellar armour with plain dark banners riding in along the empty avenue, a few abandoned lanterns and dropped parasols on the road, palace roofs in the haze behind with thin smoke, no people harmed, hushed and ominous, cold grey-gold light.",
    "canal_cut": "A great canal at the Bian waterway near the eastern capital: dozens of laden grain barges moored idle and stuck in a long row beneath a stone bridge, boatmen sitting hopelessly on the decks, sacks of grain stacked on the bank, a broken chain barrier across the water and distant smoke on the horizon, evening light.",
    "city_walls": "A northern city wall being hastily repaired and manned: labourers hauling rammed-earth baskets and timbers up scaffolding, militia in simple armour with spears, an officer in a green round-collar robe with a futou cap pointing at the gate tower, stacked stones and crossbows, plain banners, a hard bright afternoon sky.",
    "winter_clothing": "A frontier depot in early winter: clerks and quartermaster officers in green robes handing out bolts of silk and padded winter coats to rows of Tang soldiers in lamellar armour, stacked silk bundles tied with cord on a long table, braziers, first snow falling, warm yellow light against cold blue.",
    "an_gallops_away": "A mounted general of very large build in a purple round-collar robe galloping out of a mountain pass gate on a strong horse with a small band of Hu riders, whipping the horse, cloaks streaming, the pass gate and towers behind, dust and low sun, a sense of escape.",
    "chancellor_appointed": "A solemn hall interior with vermilion pillars: a kneeling official in a purple robe with a gold fish-pouch holding up both hands to receive a yellow silk edict from a court herald, a eunuch holding a lacquer box seal beside him, rows of officials in scarlet and green bowing in the background, warm lamplight.",
    "zhengshi_hall": "The chancellors' deliberation hall (Zhengshi Hall): a long lacquered table with five ministers seated and standing around it, all wearing black futou caps and round-collar robes in ONLY purple, scarlet and green (nobody in yellow or gold, no emperor, no guards), conferring over an unrolled blank map scroll, blank memorials and wooden counting rods, a large painted landscape screen behind them, grey light from lattice windows, tense heads close together, a plain bronze incense burner.",
    "coverup_report": "A palace audience: an official in a scarlet-and-purple robe kneeling before an emperor in ochre-yellow and holding up a glowing report tied with gold ribbon, while behind him a large painted map screen shows a rain-soaked southern mountain and in the shadowed corner by the pillar a wounded soldier on crutches stands unseen by the throne, irony and concealment.",
    "nanzhao_tubo": "A mountain-top highland hall of the Nanzhao kingdom in the southwest: a Nanzhao king in layered ethnic robes with a gold-ornamented headband receiving a Tibetan envoy in a red felt hat and fur-trimmed robe who offers a golden seal on a cushion, misty Cangshan peaks and a lake outside the open hall, yak-tail banners without symbols.",
    "jiedu_appointment": "A ceremony of appointing a military governor (jiedushi): a general in lamellar armour with a cloak kneeling to receive the ceremonial tally (a pair of tiger-shaped bronze halves) and the staff of command (a pole hung with tiers of yak-tail tassels) and a ceremonial axe from a court envoy in a scarlet robe, rows of soldiers with plain banners in a courtyard, bright morning.",
    "luoyang_recovered": "The recaptured eastern capital Luoyang at dawn: Tang cavalry in lamellar armour riding through a scorched but standing city gate, townspeople emerging cautiously to watch from the ruins, smoke fading, a plain red banner rising on the gate tower, fragile relief.",
    "recruit_levy": "A recruiting station in Chang'an: young city men in plain tunics lining up at long tables where officers in green robes register names on blank paper rolls, new recruits being handed spears and leather armour, an officer drilling a small squad, plain banners, dusty warm afternoon.",
    "loyalist_courier": "A lone messenger in plain disguised travel clothes, with a small sealed bamboo tube hidden in his bundle, slipping along a moonlit mountain pass track at night toward a distant tiny fire-lit city wall, wary of a rebel patrol far in the valley below, dark blue and silver tones with one warm lantern glow.",
    "refugees_granary": "A public granary gate: crowds of refugees with bundles and children queuing before a government granary where officials in green robes supervise sacks of millet being doled out into bowls, an old woman receiving a ladle of grain, a long tide of exhausted travellers on the road behind, grey sky, compassion and strain.",
    "court_festival": "A grand imperial court reception in a vast palace courtyard: ambassadors from many lands in varied costume (Turkic, Tibetan, Sogdian, Persian) presenting tribute of horses, ivory, brocade and golden vessels before a distant dais with the emperor in ochre-yellow, ceremonial fans and drums, banners of plain colour, festive golden light.",
    "lychee_courier": "A rider in a green courier's round-collar robe galloping at full speed along a dusty post road with a lacquered basket of fresh lychees strapped to his back, a blown exhausted spare horse resting by the roadside and a peasant family scattering aside, lush southern green hills behind and a distant palace roof on the horizon, urgent.",
    "yang_cavalcade": "A glamorous spring procession of the Yang sisters' households: ladies in high-waisted skirts of vivid silk and pibo shawls with high buns riding fine horses side by side with attendants and servants, their retinue taking the middle of a wide avenue, commoners stepping aside and a merchant's cart pushed to the gutter, bright peach blossoms, extravagant and a little arrogant.",
    "censorate_inquiry": "A tribunal hall of the Censorate: a senior censor in a green robe seated behind a long desk with a blank ledger, clerks standing with documents, a petitioner kneeling before him and an official in scarlet standing aside uneasy, rows of document racks in the background, severe cold light.",
    "eunuch_overseer": "An imperial eunuch overseer-commissioner in a scarlet robe with a smooth beardless face and a black futou cap standing at a military review beside a general in lamellar armour, holding a yellow silk tally and observing the ranks with a calculating gaze, the general stiff beside him, plain banners, afternoon sun.",
    "huaqing_winter": "Huaqing Palace on Mount Li in winter: terraced grey-tiled pavilions around steaming hot spring pools, white mist, bare plum branches, a procession of palanquins and mounted attendants of the court arriving through the gate under plain banners, ladies in furs and silk, lamplight beginning to glow in the dusk.",
    "tax_treasury": "The Zuozang treasury hall: officials in green robes counting strings of copper cash and stacked bolts of silk, a clerk with a blank ledger and a row of counting rods, wooden crates and sacks of grain, shafts of light from high windows on piles of coin, a sense of abundance but careful accounts.",
    "anxi_triumph": "A palace ceremony of presenting captives: a Tang general in lamellar armour and a purple cloak leading a line of foreign prisoners (an unfamiliar king in Central Asian dress in white robes, hands bound) before the emperor on a dais, trophies of horses and gold vessels at the foot of the steps, rows of courtiers in purple and scarlet, solemn triumphant light.",
    "gao_lishi_counsel": "A late-night private audience in a lamp-lit palace study: the aged emperor in an ochre-yellow robe sitting heavily by a lacquered desk looking out a window at rain, and beside him the elder eunuch Gao Lishi in a plain purple robe standing with folded hands and a concerned bow, a single lamp and a distant dark sky, quiet intimacy and unease.",
    "fanyang_armoury": "A night forge yard in a northern fortress: armourers hammering lamellar plates by glowing furnaces, stacks of helmets and halberds, a long line of fine horses being shod by torchlight, soldiers stacking sacks of grain in a storehouse, red glow and shadows, quietly threatening preparation, plain banners.",
    "envoy_in_fanyang": "A banquet in a northern fortress: a hugely stout Hu general in a purple round-collar robe lavishly pouring wine for a smooth-faced eunuch envoy in a scarlet robe seated at the place of honour, a servant carrying a lacquered chest of gold and a bolt of silk toward the envoy's side, armoured officers watching in the shadows, warm candlelight, flattery and corruption.",
    "princess_wedding": "A Tang wedding procession at dusk: a young bride in an ornate red-and-gold wedding gown with a fan veil on a carried palanquin accompanied by torch-bearing attendants and musicians with pipa, drums and flutes, a young groom in a scarlet robe on horseback leading, lanterns lining the avenue of Chang'an, festive but with a hint of political calculation.",
    "palace_exam": "A grand imperial examination in an open palace courtyard: dozens of candidates in plain white scholar robes sitting in rows on mats, writing on blank paper with brushes, examiners in green and scarlet robes pacing the aisles, and the emperor in ochre-yellow high on a balcony tower overlooking them, bright spring light.",
}
for eid, desc in EV3.items():
    add(f"event.{eid}", "events3", LAND,
        "SUBJECT: Narrative game illustration, wide cinematic composition, painterly Tang style. " + desc + " Plain banners and flags without any symbols or glyphs.", outkind="event")

SEASONS = {
    "spring": "Spring: the imperial desk by an open lattice window in the Daming Palace, a lacquered desk with a blank unrolled scroll, brush rest, ink stone, a celadon vase with blooming peach and peony, pink petals drifting, soft green willow branches and a glimpse of vermilion pillars and garden outside, fresh warm morning light.",
    "summer": "Summer: the imperial desk on a shaded palace veranda, a lacquered desk with blank scrolls and an ink stone, a bronze basin of ice and a palm-leaf fan, lotus pond with pink lotus flowers beyond the railing, dense green plane trees and heat haze, a glimpse of distant Chang'an rooftops, deep green and gold light.",
    "autumn": "Autumn: the imperial desk in the lamp-lit evening of Daming Palace, a lacquered desk with blank scrolls and an ink stone, a gold-and-silver wine ewer, chrysanthemums in a bowl, red maple and ginkgo leaves drifting through an open window, flights of wild geese in a copper sunset over distant rooftops, a faint sense of unease.",
    "winter": "Winter: the imperial desk in a warm palace room, a lacquered desk with blank scrolls and an ink stone, a bronze brazier glowing with charcoal beside it, a plum blossom branch in a vase, lattice windows with snow falling outside on grey-tiled roofs and a snowy Chang'an in the distance, silent cold blue dusk against warm lamp light.",
}
for sid, desc in SEASONS.items():
    add(f"ui.season.{sid}", "seasons", LAND,
        "SUBJECT: Wide atmospheric scene illustration of the emperor's seat of power in Chang'an, in painterly Tang style, no people, empty chair. " + desc + " Calm composition with an open area suitable for overlaying game panels.", outkind="ui")
