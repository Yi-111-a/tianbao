# -*- coding: utf-8 -*-
"""Convert PNG originals in design/asset_src to webp in scenarios/tianbao_751/assets. Usage: python process.py [ids...]"""
import os, sys, json, hashlib
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jobs import JOBS

ROOT = r"C:\Users\yiyin\Desktop\新建文件夹\tianbao"
SRC = os.path.join(ROOT, "design", "asset_src")
OUT = os.path.join(ROOT, "scenarios", "tianbao_751", "assets")
WIDTH = {"portrait": 768, "event": 1344, "ending": 1344, "map": 2048}
KEYED = {"ui.ink_button", "ui.seal", "ui.crisis_drum", "ui.ribbon_xiang", "ui.ribbon_yang", "ui.ribbon_fanyang", "ui.ribbon_neiting"}


def key_white(im, thr=240):
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    near = a.min(axis=2) >= thr
    lab, n = ndi.label(near)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    # soft alpha: erode bg a touch, feather
    fg = ~bg
    fg = ndi.binary_opening(fg, iterations=1)
    alpha = ndi.gaussian_filter(fg.astype(np.float32), 0.8)
    out = im.convert("RGBA")
    arr = np.asarray(out).copy()
    arr[..., 3] = (alpha * 255).astype(np.uint8)
    return Image.fromarray(arr), fg


def crop_alpha(im, pad=4):
    bb = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    l, t, r, b = bb
    return im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad)))


def save(im, path, q=84):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "WEBP", quality=q, method=6)
    return im.size


def outpath(jid):
    kind = JOBS[jid]["kind"]
    return os.path.join(OUT, kind, jid + ".webp")


def do(jid):
    src = os.path.join(SRC, JOBS[jid]["kind"], jid + ".png")
    if not os.path.exists(src):
        return {}
    im = Image.open(src)
    res = {}
    kind = JOBS[jid]["kind"]
    if jid == "icon.sheet":
        rgba, fg = key_white(im, 235)
        fg = ndi.binary_opening(fg, iterations=3)
        lab, n = ndi.label(fg)
        objs = ndi.find_objects(lab)
        sizes = ndi.sum(fg, lab, range(1, n + 1))
        keep = [i for i in np.argsort(sizes)[::-1][:10]]
        boxes = []
        for i in keep:
            sl = objs[i]
            cy = (sl[0].start + sl[0].stop) / 2
            cx = (sl[1].start + sl[1].stop) / 2
            boxes.append((cy, cx, sl))
        boxes.sort(key=lambda b: b[0])
        row1 = sorted(boxes[:5], key=lambda b: b[1])
        row2 = sorted(boxes[5:], key=lambda b: b[1])
        ids = ["treasury", "grain", "authority", "morale", "corruption", "frontier_pressure", "an_ambition",
               "fanzhen_power", "court_strife", "rebellion_risk"]
        for rid, (cy, cx, sl) in zip(ids, row1 + row2):
            crop = rgba.crop((sl[1].start - 3, sl[0].start - 3, sl[1].stop + 3, sl[0].stop + 3))
            s = max(crop.size)
            sq = Image.new("RGBA", (s, s), (0, 0, 0, 0))
            sq.paste(crop, ((s - crop.width) // 2, (s - crop.height) // 2))
            sq = sq.resize((256, 256), Image.LANCZOS)
            p = os.path.join(OUT, "icon", f"icon.{rid}.webp")
            res[f"icon.{rid}"] = dict(path=p, size=list(save(sq, p, 90)))
        return res
    if jid == "ui.lacquer_bar":
        rgba, fg = key_white(im, 240)
        out = crop_alpha(rgba, 6)
    elif jid in KEYED:
        rgba, fg = key_white(im, 238)
        out = crop_alpha(rgba, 6)
        if out.width > 1100:
            out = out.resize((1100, round(out.height * 1100 / out.width)), Image.LANCZOS)
    else:
        w = WIDTH.get(kind)
        out = im.convert("RGB")
        if w and out.width != w:
            out = out.resize((w, round(out.height * w / out.width)), Image.LANCZOS)
        elif jid == "title.scroll":
            pass
        elif kind == "ui" and out.width > 1536:
            pass
    p = outpath(jid)
    res[jid] = dict(path=p, size=list(save(out, p)))
    return res


if __name__ == "__main__":
    ids = sys.argv[1:] or list(JOBS)
    allres = {}
    for j in ids:
        allres.update(do(j))
    for k, v in allres.items():
        print(k, v["size"])
