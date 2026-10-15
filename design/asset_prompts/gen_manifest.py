# -*- coding: utf-8 -*-
import os, sys, hashlib, yaml, time
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jobs import JOBS
ROOT = r"C:\Users\yiyin\Desktop\新建文件夹\tianbao"
SC = os.path.join(ROOT, "scenarios", "tianbao_751")
NEG = "text, characters, calligraphy, letters, numbers, watermark, logo, dragon, dragon robe, Ming wing hat, mandarin square, modern, photo, 3d render, anime"
NOMINAL = {"portrait": [768, 1152], "event": [1344, 896], "ending": [1344, 896], "map": [2048, 1365]}
RES = "treasury grain authority morale corruption frontier_pressure an_ambition fanzhen_power court_strife rebellion_risk".split()
entries = []

def used_by(i):
    p = i.split(".")
    if p[0] == "portrait": return f"character:{p[1]}:portrait" + ("" if p[2] == "default" else ":armor")
    if p[0] == "event": return f"event:{p[1]}:illustration"
    if p[0] == "ending": return f"ending:{p[1]}:illustration"
    if p[0] == "map": return "map:base"
    if p[0] == "title": return "ui:title:background"
    if p[0] == "icon": return f"resource:{p[1]}:icon"
    return "ui:" + p[1]

def add(i, kind, prompt, ref=None):
    rel = f"assets/{kind}/{i}.webp"
    fp = os.path.join(SC, rel)
    ok = os.path.exists(fp)
    if ok:
        size = list(Image.open(fp).size); sha = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    else:
        size = NOMINAL.get(kind, [0, 0]); sha = None
    e = dict(id=i, kind=kind, used_by=used_by(i), path=rel, size=size, format="webp",
             prompt=prompt, negative_prompt=NEG, style_ref="design/STYLE_GUIDE.md §5 shared style block",
             model="codex-image", sha256=sha, status="generated" if ok else "missing", version=1)
    if ref: e["reference_image"] = ref
    entries.append(e)

for i, j in JOBS.items():
    if i == "icon.sheet":
        for r in RES: add(f"icon.{r}", "icon", j["subject"] + " (one cell of the 10-icon sprite sheet, cropped and keyed)")
        continue
    add(i, j["kind"], j["subject"], j.get("ref"))
yaml.safe_dump({"manifest_version": 1, "entries": entries}, open(os.path.join(SC, "assets.yaml"), "w", encoding="utf8"), allow_unicode=True, sort_keys=False, width=200)
print(len(entries), sum(e["status"] == "generated" for e in entries))
