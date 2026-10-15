"""《天宝》剧本内容静态检查（scenarios/tianbao_751）。

用法（在 tianbao/ 下）：

    .venv/Scripts/python tools/content_lint.py            # 检查，发现问题时退出码 1
    .venv/Scripts/python tools/content_lint.py --pack <剧本目录>

检查项（与引擎 `sim validate` 互补：validate 管结构与引用，本工具管「文字与状态是否相符」）：

1. 人物引用：奏疏谏言人、选项 memory、各 op 的 character 字段都须是 characters.yaml 中的人物。
2. 题文相符：奏疏选项 label、事件选项 text 提到「任 / 另择 / 授」等任免字样，就须真有任免
   （appoint 或 set_army_commander），或以 `appoints_via: <事件 id>` 指向一个确有任免的后续抉择。
   明说不任命的写法（「不任命」「不另任」「专任将帅」「预定…继任」「授官加赏」「颁授 / 自授告身」）不算。
3. 史事有据：奏疏标题 / summary / 谏言、事件标题 / 正文提到具名史事（西洱河、怛罗斯、土护真水、霖雨……），
   其 conditions 须正向包含该史事的旗标（不在 not 之内）；定义该旗标的事件本身除外。
4. 情报上限：凡设置 intel:* 旗标的选项 / 事件，提示或正文须写明「只减半一次 / 不叠加」。
5. 易逝人物：在其可能亡故之后仍可见的奏疏若以其为谏言人，须带「此人在世」条件或谏言 `requires`。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Iterator

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "scenarios" / "tianbao_751"

# ---- 规则表 ----
APPOINT_WORDS = re.compile(r"任|另择|另简|授|代镇|久镇")
# 明说不任命或并非官职任免的固定说法：先从标题里剔除，再判断
APPOINT_EXEMPT = re.compile(r"不任命|留任|不另任|不另任要员|专任将帅|预定\S{0,6}继任|授官加赏|颁授|自授|不改官职")
APPOINT_OPS = {"appoint", "set_army_commander"}

# 具名史事 → 可作依据的旗标（任一正向出现即可）。"yan_control" 表示条件里有「某地归叛军」。
WAR = ["rebellion_started", "rebellion_quelled", "mutiny_rebellion", "duji_lost", "tongguan_lost", "yan_control"]
NAMED_EVENTS: list[tuple[str, list[str]]] = [
    (r"西洱河", ["xier_defeat"]),
    (r"怛罗斯", ["talas_defeat"]),
    (r"土护真水|新经战阵|一败之后", ["an_weakened"]),
    (r"阿布思", ["abusi_gone"]),
    (r"霖雨", ["autumn_rains"]),
    (r"风疾", ["geshu_ill"]),
    (r"丧师", ["xier_defeat", "li_mi_defeat"]),
    (r"南诏.{0,3}寇|南诏与吐蕃合", ["xier_defeat", "nanzhao_tubo", "li_mi_defeat"]),
    (r"潼关已失|潼关失守|潼关不守", ["tongguan_lost", "yan_control"]),
    (r"东都失守|东都陷|入东都|顿兵陕郡", ["duji_lost", "yan_control"]),
    (r"范阳兵起|范阳兵已起|叛军|讨贼|贼势|乱后", WAR),
    (r"叛乱既平|乱既平|乱平", ["rebellion_quelled"]),
]
INTEL_CAP = re.compile(r"只减半一次|不叠加|不再收窄")
# 可能中途亡故的人物：{人物: 最早亡故回合}（李林甫病卒事件自 T7 起掷骰）
MORTAL_FROM = {"li_linfu": 7}


# ---- 读取 ----
def load(pack: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for name in ("scenario", "characters", "events", "memorials"):
        file = pack / f"{name}.yaml"
        data[name] = yaml.safe_load(file.read_text(encoding="utf-8")) if file.is_file() else []
    return data


# ---- 条件遍历 ----
def positive_evidence(cond: Any, negated: bool = False) -> set[str]:
    """条件里正向出现的旗标（flag / flag_age 的 key），以及 yan_control（某地归 yan）。"""
    found: set[str] = set()
    if isinstance(cond, list):
        for row in cond:
            found |= positive_evidence(row, negated)
        return found
    if not isinstance(cond, dict):
        return found
    for key in ("all", "any"):
        if key in cond:
            return positive_evidence(cond[key], negated)
    if "not" in cond:
        return positive_evidence(cond["not"], not negated)
    if negated:
        return found
    kind = cond.get("kind")
    if kind == "flag":
        if cond.get("operator") == "absent" or cond.get("value", True) in (False, None):
            return found
        found.add(str(cond.get("key")))
    elif kind == "flag_age":
        found.add(str(cond.get("key")))
    elif kind == "region_controller" and cond.get("faction") == "yan":
        found.add("yan_control")
    return found


def alive_condition(cond: Any, character: str, negated: bool = False) -> bool:
    if isinstance(cond, list):
        return any(alive_condition(row, character, negated) for row in cond)
    if not isinstance(cond, dict):
        return False
    if "all" in cond:
        return any(alive_condition(row, character, negated) for row in cond["all"])
    if "any" in cond:
        return all(alive_condition(row, character, negated) for row in cond["any"])
    if "not" in cond:
        return alive_condition(cond["not"], character, not negated)
    return (not negated and cond.get("kind") == "character_status" and cond.get("character") == character
            and cond.get("value", "alive") == "alive")


def earliest_turn(item: dict[str, Any]) -> int:
    if item.get("turn") is not None:
        return int(item["turn"])
    lows = [0]

    def walk(cond: Any) -> None:
        if isinstance(cond, list):
            for row in cond:
                walk(row)
        elif isinstance(cond, dict):
            if "all" in cond:
                walk(cond["all"])
            elif cond.get("kind") == "turn" and cond.get("operator", "eq") in ("eq", "gte", "gt"):
                lows.append(int(cond["value"]) + (1 if cond.get("operator") == "gt" else 0))
            elif cond.get("kind") == "flag_age" and cond.get("key") == "rebellion_started":
                lows.append(8)  # 最早起兵在 T8 以后
    walk(item.get("conditions"))
    return max(lows)


def ops_of(rows: Any) -> Iterator[dict[str, Any]]:
    for op in rows or []:
        if isinstance(op, dict):
            yield op
            yield from ops_of(op.get("on_complete"))


def memories(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value]
    return [row for row in value or [] if isinstance(row, dict)]


# ---- 检查 ----
def lint(pack: Path) -> list[str]:
    data = load(pack)
    chars = {c["id"] for c in data["characters"] or []}
    events = {e["id"]: e for e in data["events"] or []}
    memos = data["memorials"] or []
    problems: list[str] = []

    def check_char(cid: Any, where: str) -> None:
        if cid is not None and cid not in chars:
            problems.append(f"[人物] {where} 引用不存在的人物：{cid}")

    def has_appoint(rows: Any) -> bool:
        return any(op.get("op") in APPOINT_OPS and op.get("character") for op in ops_of(rows))

    def check_title(label: str, rows: Any, via: Any, where: str) -> None:
        stripped = APPOINT_EXEMPT.sub("", label or "")
        if not APPOINT_WORDS.search(stripped):
            return
        if has_appoint(rows):
            return
        if via:
            event = events.get(str(via))
            if event is None:
                problems.append(f"[题文] {where}「{label}」appoints_via 指向不存在的事件：{via}")
            elif not any(has_appoint(choice.get("effects")) for choice in event.get("choices") or []):
                problems.append(f"[题文] {where}「{label}」appoints_via 事件 {via} 的选项里没有任免")
            return
        problems.append(f"[题文] {where}「{label}」标题提到任免，但没有 appoint / set_army_commander")

    def check_named(text: str, cond: Any, where: str, defines: set[str] = frozenset()) -> None:
        evidence = positive_evidence(cond) | set(defines)
        for pattern, flags in NAMED_EVENTS:
            hit = re.search(pattern, text or "")
            if hit and not evidence.intersection(flags):
                problems.append(f"[史事] {where} 提到「{hit.group(0)}」，但条件里没有 {' / '.join(flags)} 之一")

    # 奏疏
    for item in memos:
        mid = item.get("id")
        cond = item.get("conditions")
        first = earliest_turn(item)
        for adv in item.get("advisors") or []:
            cid = adv.get("character")
            check_char(cid, f"奏疏 {mid} 谏言")
            check_named(adv.get("line", ""), cond, f"奏疏 {mid} 谏言（{cid}）")
            dies = MORTAL_FROM.get(cid)
            guarded = bool(adv.get("requires")) or alive_condition(cond, cid)  # requires 由引擎在列出时校验
            if dies is not None and first >= dies and not guarded:
                problems.append(f"[易逝] 奏疏 {mid} 自 T{first} 可见，谏言人 {cid} 可能已故，却无「在世」条件")
        check_named(f"{item.get('title', '')}｜{item.get('summary', '')}", cond, f"奏疏 {mid} 标题/正文")
        for opt in item.get("options") or []:
            where = f"奏疏 {mid}.{opt.get('id')}"
            for mem in memories(opt.get("memory")):
                check_char(mem.get("character"), f"{where} memory")
            for op in ops_of(opt.get("ops")):
                check_char(op.get("character"), f"{where} op {op.get('op')}")
            check_title(str(opt.get("label", "")), opt.get("ops"), opt.get("appoints_via"), where)
            sets_intel = any(op.get("op") == "set_flag" and str(op.get("key", "")).startswith("intel:") for op in ops_of(opt.get("ops")))
            if sets_intel and not INTEL_CAP.search(str(opt.get("hint", ""))):
                problems.append(f"[情报] {where} 设置情报旗标，但提示未写明叠加上限（只减半一次 / 不叠加）")

    # 事件
    for eid, ev in events.items():
        cond = ev.get("conditions")
        defines = {str(op.get("key")) for op in ops_of(ev.get("effects")) if op.get("op") == "set_flag" and op.get("value", True)}
        check_named(f"{ev.get('title', '')}｜{ev.get('text', '')}", cond, f"事件 {eid}", defines)
        for op in ops_of(ev.get("effects")):
            check_char(op.get("character"), f"事件 {eid} op {op.get('op')}")
        sets_intel = any(k.startswith("intel:") for k in defines)
        if sets_intel and not INTEL_CAP.search(str(ev.get("text", ""))):
            problems.append(f"[情报] 事件 {eid} 设置情报旗标，但正文未写明叠加上限")
        for choice in ev.get("choices") or []:
            where = f"事件 {eid}.{choice.get('id')}"
            for mem in memories(choice.get("memory")):
                check_char(mem.get("character"), f"{where} memory")
            for op in ops_of(choice.get("effects")):
                check_char(op.get("character"), f"{where} op {op.get('op')}")
            check_title(str(choice.get("text", "")), choice.get("effects"), choice.get("appoints_via"), where)
    return problems


def main() -> None:
    ap = argparse.ArgumentParser(description="《天宝》剧本内容静态检查")
    ap.add_argument("--pack", default=str(PACK))
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    problems = lint(Path(args.pack))
    for line in problems:
        print(line)
    print(f"content_lint：{len(problems)} 处问题" if problems else "content_lint：无问题")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
