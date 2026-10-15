"""《天宝》剧本平衡脚本：三种脚本策略（do_nothing / historical / wise）只通过奏疏选项与事件抉择操作。

用法（在 tianbao/ 下，使用共享 venv）：

    .venv/Scripts/python tools/sim_policies.py --seeds 200
    .venv/Scripts/python tools/sim_policies.py --backend engine --seeds 200   # 引擎实现 CONTRACT §1 后
    .venv/Scripts/python tools/sim_policies.py --policy wise --seed 3 --trace  # 单局逐季轨迹

两种后端：
- model（默认）：本文件内的参考实现，按 docs/CONTRACT.md §1 的语义解释剧本 YAML
  （条件 DSL、新 op、事件抉择、计数器、战斗与 AI 行军、结局判定）。用于引擎落地前调参。
- engine：调用 engine/backend/simcore 的 resolve_turn / apply / matches。若引擎尚不支持
  pending_choices / outcome 等字段，脚本会说明缺什么并退出。

输出：每种策略在 N 个种子上的结局分布、T19（或终局）时渔阳鼙鼓的分布。
"""
from __future__ import annotations

import argparse
import copy
import random
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "scenarios" / "tianbao_751"


# ============================================================================
# 剧本加载
# ============================================================================
def load_pack(path: Path = PACK) -> dict[str, Any]:
    data: dict[str, Any] = {"root": str(path)}
    for name in ("scenario", "characters", "regions", "factions", "armies", "events", "memorials"):
        file = path / f"{name}.yaml"
        data[name] = yaml.safe_load(file.read_text(encoding="utf-8")) if file.is_file() else []
    return data


# ============================================================================
# 参考模型（CONTRACT §1 语义）
# ============================================================================
class Rejected(Exception):
    pass


def _cmp(left: float, op: str, right: float) -> bool:
    return {
        "gt": left > right, "gte": left >= right, "lt": left < right,
        "lte": left <= right, "eq": left == right,
    }[op]


class Model:
    """一局游戏的完整状态与规则。仅依赖剧本 YAML。"""

    def __init__(self, pack: dict[str, Any], seed: int) -> None:
        self.pack = pack
        sc = pack["scenario"]
        self.sc = sc
        self.rng = random.Random(seed)
        self.seed = seed
        self.turn = 0
        self.res = {
            r["id"]: {"amount": float(r.get("initial", 0)), "min": r.get("min"), "max": r.get("max")}
            for r in sc["resources"]
        }
        main = sc.get("settings", {}).get("player_faction", "tang")
        self.main = main
        self.regions = {
            r["id"]: {
                "stats": dict(r.get("stats", {})),
                "controller": r.get("controller", main),
                "adj": {e["to"]: int(e.get("travel_turns", 1)) for e in r.get("adjacency", [])},
            }
            for r in pack["regions"]
        }
        self.offices = {o["id"]: {"holder": None, "requires": o.get("requires", {})} for o in sc["offices"]}
        self.chars: dict[str, dict[str, Any]] = {}
        for c in pack["characters"]:
            offices = list(c.get("offices") or ([c["office"]] if c.get("office") else []))
            self.chars[c["id"]] = {
                "region": c["region"], "status": c.get("status", "alive"), "offices": offices,
                "traits": dict(c.get("traits", {})), "transit": None,
            }
            for o in offices:
                self.offices[o]["holder"] = c["id"]
        self.armies = {
            a["id"]: {
                "faction": a.get("faction"), "region": a["region"], "strength": float(a.get("strength", 0)),
                "quality": float(a.get("quality", 1.0)), "commander": a.get("commander"), "transit": None,
            }
            for a in pack["armies"]
        }
        self.factions = {f["id"]: dict(f.get("relations", {})) for f in pack["factions"]}
        self.wars = {frozenset((w["a"], w["b"])) for w in sc.get("wars", [])}
        self.flags: dict[str, Any] = {}
        self.flag_turns: dict[str, int] = {}
        self.counters: dict[str, int] = {}
        self.ledger: list[dict[str, Any]] = []
        self.projects: list[dict[str, Any]] = []
        self.pending: list[dict[str, Any]] = []
        self.event_last: dict[str, int] = {}
        self.outcome: dict[str, Any] | None = None
        self.max_offices = int(sc.get("settings", {}).get("max_concurrent_offices", 1))
        self.log: list[str] = []
        self._now = 0  # 写 flag_turns 用的回合

    # ---------------- 条件 ----------------
    def matches(self, c: Any, turn: int | None = None) -> bool:
        t = self.turn if turn is None else turn
        if c in (None, {}, []):
            return True
        if isinstance(c, list):
            return all(self.matches(x, t) for x in c)
        if "all" in c:
            return all(self.matches(x, t) for x in c["all"])
        if "any" in c:
            return any(self.matches(x, t) for x in c["any"])
        if "not" in c:
            return not self.matches(c["not"], t)
        k = c.get("kind")
        op = c.get("operator", "eq")
        if k == "turn":
            return _cmp(t, op, int(c["value"]))
        if k == "resource":
            return _cmp(self.res[c["id"]]["amount"], c.get("operator", "gte"), float(c["value"]))
        if k == "flag":
            if op == "exists":
                return c["key"] in self.flags
            if op == "absent":
                return c["key"] not in self.flags
            return self.flags.get(c["key"]) == c.get("value", True)
        if k == "flag_age":
            if c["key"] not in self.flag_turns or not self.flags.get(c["key"]):
                return False
            return _cmp(t - self.flag_turns[c["key"]], op, int(c["value"]))
        if k == "counter":
            return _cmp(self.counters.get(c["key"], 0), op, float(c["value"]))
        if k == "region_controller":
            return self.regions[c["region"]]["controller"] == c["faction"]
        if k == "region_stat":
            return _cmp(self.regions[c["region"]]["stats"].get(c["stat"], 0), c.get("operator", "gte"), float(c["value"]))
        if k == "character_status":
            return self.chars[c["character"]]["status"] == c["value"]
        if k == "character_trait":
            return _cmp(self.chars[c["character"]]["traits"].get(c["trait"], 0), op, float(c["value"]))
        if k == "character_region":
            return self.chars[c["character"]]["region"] == c["region"]
        if k == "office_holder":
            return self.offices[c["office"]]["holder"] == c.get("character")
        if k == "army_strength":
            if "army" in c:
                total = self.armies[c["army"]]["strength"]
            else:
                total = sum(a["strength"] for a in self.armies.values() if a["faction"] == c["faction"])
            return _cmp(total, op, float(c["value"]))
        if k == "relation":
            return _cmp(self.factions[c["a"]].get(c["b"], 0), op, float(c["value"]))
        raise ValueError(f"未知条件：{k}")

    # ---------------- op ----------------
    def apply(self, op: dict[str, Any]) -> None:
        kind = op["op"]
        fn = getattr(self, f"_op_{kind}", None)
        if fn is None:
            raise Rejected(f"未知 op {kind}")
        fn(op)

    def try_apply(self, op: dict[str, Any], tag: str = "") -> bool:
        try:
            self.apply(op)
            return True
        except Rejected as exc:
            self.log.append(f"T{self.turn} 拒绝 {tag} {op.get('op')}: {exc}")
            return False

    def _clamp(self, rid: str, value: float) -> float:
        r = self.res[rid]
        if r["min"] is not None:
            value = max(r["min"], value)
        if r["max"] is not None:
            value = min(r["max"], value)
        return value

    def _op_adjust_resource(self, op):
        if op["resource"] not in self.res:
            raise Rejected("资源不存在")
        r = self.res[op["resource"]]
        r["amount"] = self._clamp(op["resource"], r["amount"] + float(op["delta"]))

    def _op_add_ledger(self, op):
        self.ledger.append(dict(op))

    def _op_appoint(self, op):
        ch, off = self.chars[op["character"]], self.offices[op["office"]]
        if ch["status"] != "alive" or ch["transit"]:
            raise Rejected("人物不能任职")
        if off["holder"] not in (None, op["character"]):
            raise Rejected("官职有人")
        if op["office"] in ch["offices"]:
            return
        if len(ch["offices"]) >= self.max_offices:
            raise Rejected("OFFICE_HELD")
        if any(ch["traits"].get(k, 0) < v for k, v in off["requires"].items()):
            raise Rejected("不满足任职条件")
        ch["offices"].append(op["office"])
        off["holder"] = op["character"]

    def _op_dismiss(self, op):
        ch = self.chars[op["character"]]
        if op["office"] not in ch["offices"]:
            raise Rejected("未任此职")
        ch["offices"].remove(op["office"])
        self.offices[op["office"]]["holder"] = None

    def _op_set_character_status(self, op):
        ch = self.chars[op["character"]]
        ch["status"] = op["status"]
        if op["status"] != "alive":
            for o in ch["offices"]:
                self.offices[o]["holder"] = None
            ch["offices"] = []
            ch["transit"] = None
            for a in self.armies.values():
                if a["commander"] == op["character"]:
                    a["commander"] = None

    def _op_move_character(self, op):
        ch = self.chars[op["character"]]
        if ch["status"] != "alive" or ch["transit"]:
            raise Rejected("人物不能行动")
        adj = self.regions[ch["region"]]["adj"]
        if op["to_region"] not in adj:
            raise Rejected("不相邻")
        ch["transit"] = {"to": op["to_region"], "eta": self.turn + adj[op["to_region"]]}

    def _op_move_army(self, op):
        a = self.armies[op["army"]]
        if a["transit"] or a["strength"] <= 0:
            raise Rejected("军队不能行军")
        adj = self.regions[a["region"]]["adj"]
        if op["to_region"] not in adj:
            raise Rejected("不相邻")
        a["transit"] = {"to": op["to_region"], "eta": self.turn + adj[op["to_region"]]}

    def _op_start_project(self, op):
        for rid, cost in op["cost_per_turn"].items():
            committed = sum(p["cost_per_turn"].get(rid, 0) for p in self.projects)
            if self.res[rid]["amount"] - committed < cost:
                raise Rejected("工程款不足")
        self.projects.append({**op, "progress": 0})

    def _op_adjust_region(self, op):
        stats = self.regions[op["region"]]["stats"]
        if op["stat"] not in stats:
            raise Rejected("地区指标不存在")
        stats[op["stat"]] += float(op["delta"])

    def _op_adjust_relation(self, op):
        rel = self.factions[op["a"]]
        rel[op["b"]] = rel.get(op["b"], 0) + float(op["delta"])

    def _op_set_flag(self, op):
        self.flags[op["key"]] = op["value"]
        self.flag_turns[op["key"]] = self._now

    def _op_remember(self, op):
        pass

    def _op_adjust_army(self, op):
        a = self.armies[op["army"]]
        a["strength"] = max(0.0, a["strength"] + float(op["delta"]))

    def _op_set_army_faction(self, op):
        if op["faction"] not in self.factions:
            raise Rejected("势力不存在")
        self.armies[op["army"]]["faction"] = op["faction"]

    def _op_set_army_commander(self, op):
        cid = op.get("character")
        if cid is not None and self.chars[cid]["status"] != "alive":
            raise Rejected("人物不在世")
        self.armies[op["army"]]["commander"] = cid

    def _op_adjust_trait(self, op):
        tr = self.chars[op["character"]]["traits"]
        tr[op["trait"]] = tr.get(op["trait"], 0) + float(op["delta"])

    def _op_adjust_counter(self, op):
        self.counters[op["key"]] = self.counters.get(op["key"], 0) + int(op["delta"])

    def _op_set_counter(self, op):
        self.counters[op["key"]] = int(op["value"])

    def _op_set_region_controller(self, op):
        self.regions[op["region"]]["controller"] = op["faction"]

    def _op_choose_event_option(self, op):
        pc = next((p for p in self.pending if p["id"] == op["choice_id"]), None)
        if pc is None:
            raise Rejected("抉择不存在")
        opt = next((o for o in pc["options"] if o["id"] == op["option_id"]), None)
        if opt is None or not self.matches(opt.get("conditions")):
            raise Rejected("选项无效")
        for e in opt.get("effects", []):
            self.try_apply(e, pc["event_id"])
        self.pending.remove(pc)
        self.log.append(f"T{self.turn} 抉择 {pc['event_id']} → {opt['id']}")

    # ---------------- 奏疏 ----------------
    def visible_memorials(self) -> list[dict[str, Any]]:
        out = []
        for m in self.pack["memorials"]:
            if f"memorial:{m['id']}" in self.flags:
                continue
            if "turn" in m and m["turn"] != self.turn:
                continue
            if "conditions" in m and not self.matches(m["conditions"]):
                continue
            out.append(m)
        return out

    def adopt(self, memorial: dict[str, Any], option_id: str) -> None:
        opt = next(o for o in memorial["options"] if o["id"] == option_id)
        self._now = self.turn
        for op in opt.get("ops", []):
            self.try_apply(op, memorial["id"])
        self.flags[f"memorial:{memorial['id']}"] = option_id
        self.log.append(f"T{self.turn} 奏疏 {memorial['id']} → {option_id}")

    # ---------------- 回合结算 ----------------
    def hostile(self, f1: str, f2: str) -> bool:
        if f1 == f2 or f1 is None or f2 is None:
            return False
        if frozenset((f1, f2)) in self.wars:
            return True
        return self.factions.get(f1, {}).get(f2, 0) < 0

    def resolve(self) -> None:
        T = self.turn + 1
        self._now = T
        # 1 到期抉择
        for pc in list(self.pending):
            if pc["deadline"] <= T:
                self._op_choose_event_option({"choice_id": pc["id"], "option_id": pc["default"]})
        # 4 账目
        for e in list(self.ledger):
            r = self.res[e["category"]]
            r["amount"] = self._clamp(e["category"], r["amount"] + e["amount"])
            if e["kind"] == "one_off":
                self.ledger.remove(e)
        # 5 收入
        for key, inc in self.sc["formulas"].get("income", {}).items():
            for reg in self.regions.values():
                val = _eval(inc["formula"], {**reg["stats"], "turn": T})
                rid = inc["resource"]
                self.res[rid]["amount"] = self._clamp(rid, self.res[rid]["amount"] + val)
        # 6 工程
        for p in list(self.projects):
            if any(self.res[k]["amount"] < v for k, v in p["cost_per_turn"].items()):
                continue
            for k, v in p["cost_per_turn"].items():
                self.res[k]["amount"] -= v
            p["progress"] += 1
            if p["progress"] >= p["turns"]:
                for op in p.get("on_complete", []):
                    self.try_apply(op, p["name"])
                self.projects.remove(p)
                self.log.append(f"T{T} 竣工 {p['name']}")
        # 7 抵达
        for ent in list(self.chars.values()) + list(self.armies.values()):
            if ent["transit"] and ent["transit"]["eta"] <= T:
                ent["region"] = ent["transit"]["to"]
                ent["transit"] = None
        # 8 战斗 + AI 行军
        self._battles(T)
        self._ai_march()
        # 9 漂移
        values = {k: v["amount"] for k, v in self.res.items()}
        for rid, expr in self.sc["formulas"].get("drift", {}).items():
            self.res[rid]["amount"] = self._clamp(rid, self.res[rid]["amount"] + _eval(expr, values))
        # 10 事件
        for ev in self.pack["events"]:
            eid = ev["id"]
            if eid in self.event_last:
                if not ev.get("repeatable"):
                    continue
                if T - self.event_last[eid] <= int(ev.get("cooldown", 0)):
                    continue
            when = ev.get("when", {})
            if when.get("turn") not in (None, T):
                continue
            if not self.matches(ev.get("conditions"), T):
                continue
            if self.rng.random() > float(ev.get("gravity", 1)):
                continue
            for op in ev.get("effects", []):
                self.try_apply(op, eid)
            self.event_last[eid] = T
            self.log.append(f"T{T} 事件 {eid}")
            if ev.get("choices"):
                self.pending.append({
                    "id": f"choice-{eid}-{T}", "event_id": eid, "options": ev["choices"],
                    "default": ev.get("default_choice", ev["choices"][0]["id"]),
                    "deadline": T + int(ev.get("choice_deadline", 1)),
                })
        # 11 计数器
        for c in self.sc.get("counters", []):
            hit = self.matches(c["conditions"], T)
            cur = self.counters.get(c["id"], 0)
            if c.get("mode", "count") == "streak":
                self.counters[c["id"]] = cur + 1 if hit else 0
            elif hit:
                self.counters[c["id"]] = cur + 1
        # 12 结局
        for e in sorted(self.sc.get("endings", []), key=lambda x: x["priority"]):
            if self.matches(e["conditions"], T):
                self.outcome = {"id": e["id"], "kind": e["kind"], "turn": T}
                break
        gl = self.sc.get("game_length", {})
        if self.outcome is None and gl:
            last = gl["last_turn"]
            if self.flags.get(gl.get("overtime_flag")):
                last = gl.get("overtime_last_turn", last)
            if T >= last:
                self.outcome = {"id": gl["fallback_ending"], "kind": "ending", "turn": T}
        self.turn = T

    def _power(self, armies: list[dict], defense: float) -> float:
        return sum(a["strength"] * a["quality"] for a in armies) * (1 + defense / 100)

    def _battles(self, T: int) -> None:
        for rid, reg in self.regions.items():
            present = [a for a in self.armies.values() if a["region"] == rid and not a["transit"] and a["strength"] > 0]
            facs = {a["faction"] for a in present}
            ctrl = reg["controller"]
            # 无守军时直接占领
            if len(facs) == 1:
                f = next(iter(facs))
                if f != ctrl and self.hostile(f, ctrl):
                    reg["controller"] = f
                    self.log.append(f"T{T} {f} 占领 {rid}")
                continue
            if len(facs) < 2:
                continue
            defender = ctrl if ctrl in facs else max(facs, key=lambda f: sum(a["strength"] for a in present if a["faction"] == f))
            attackers = [f for f in facs if f != defender and self.hostile(f, defender)]
            if not attackers:
                continue
            att_f = attackers[0]
            dfa = [a for a in present if a["faction"] == defender]
            ata = [a for a in present if a["faction"] == att_f]
            d_def = reg["stats"].get("defense", 0)
            dp = self._power(dfa, d_def) * self.rng.uniform(0.85, 1.15)
            ap = self._power(ata, 0) * self.rng.uniform(0.85, 1.15)
            if d_def >= 80 and ap < 2 * dp:
                self.log.append(f"T{T} {rid} 相持 攻{ap:.0f} 守{dp:.0f}")
                continue
            if ap > dp:
                win, lose, lose_f = ata, dfa, defender
            else:
                win, lose, lose_f = dfa, ata, att_f
            for a in win:
                a["strength"] *= 0.9
            for a in lose:
                a["strength"] *= 0.7
                back = next((n for n in reg["adj"] if self.regions[n]["controller"] == lose_f), None)
                if back:
                    a["region"] = back
                else:
                    a["strength"] = 0
            self.log.append(f"T{T} {rid} 交战 攻{ap:.0f} 守{dp:.0f} 败方 {lose_f}")
            if ap > dp:
                reg["controller"] = att_f

    def _ai_march(self) -> None:
        for route_def in self.sc.get("ai_routes", []):
            route, fac = route_def["route"], route_def["faction"]
            for a in self.armies.values():
                if a["faction"] != fac or a["transit"] or a["strength"] <= 0 or a["region"] not in route:
                    continue
                i = route.index(a["region"])
                if i + 1 >= len(route):
                    continue
                nxt = route[i + 1]
                # 本区仍有敌军则不前进
                if any(b["region"] == a["region"] and not b["transit"] and b["strength"] > 0 and self.hostile(b["faction"], fac) for b in self.armies.values()):
                    continue
                if route_def.get("hold_if_outnumbered"):
                    enemy = [b for b in self.armies.values() if b["region"] == nxt and not b["transit"] and self.hostile(b["faction"], fac)]
                    if self._power(enemy, self.regions[nxt]["stats"].get("defense", 0)) > a["strength"] * a["quality"] * 2.2:
                        continue
                if nxt in self.regions[a["region"]]["adj"]:
                    a["transit"] = {"to": nxt, "eta": self.turn + self.regions[a["region"]]["adj"][nxt]}

    # ---------------- 便捷 ----------------
    def r(self, rid: str) -> float:
        return self.res[rid]["amount"]


def _eval(expr: str, values: dict[str, Any]) -> float:
    return float(eval(expr, {"__builtins__": {}, "max": max, "min": min}, dict(values)))  # 剧本公式只含算术与 min/max


# ============================================================================
# 策略
# ============================================================================
Decision = tuple[list[tuple[str, str]], dict[str, str]]  # ([(memorial_id, option_id)], {choice_id: option_id})


def do_nothing(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    """不批奏疏，事件抉择一律到期走默认项。"""
    return [], {}


HISTORICAL_MEMO = {
    "t0_hedong": "grant", "t0_xier": "lavish", "t0_nanzhao": "campaign", "t0_anxi": "campaign", "t0_huaqing": "palace",
    "t1_xier_report": "conscript", "t1_khitan": "approve", "t1_grain": "extra_haul", "t1_donggong": "allow",
    "t2_west": "hold", "t2_shuofang": "sishun", "t2_census": "convert",
    "t3_an_tribute": "reward", "t3_review": "lenient", "t3_winter": "half",
    "t4_an_troops": "approve", "t4_haul": "convert", "t4_censorate": "quiet",
    "t5_tubo": "strike", "t5_jingzhao": "approve", "t5_relief": "local",
    "t6_successor": "guozhong", "t6_feast": "feast", "t6_autumn": "census",
    "t7_anxi": "feng", "t7_winter": "yang", "t7_coin": "allow",
    "t8_zhenqing": "send", "t8_an_accuse": "ignore", "t8_spring": "none",
    "t9_jinjun_command": "keep", "t9_tubo": "fight", "t9_canal": "buy",
    "t10_geshu": "grant", "t10_horses": "grant", "t10_harvest": "tax",
    "t11_yang": "indulge", "t11_border_pay": "self",
    "t12_chancellor": "refuse", "t12_an_away": "excuse", "t12_spring": "none",
    "t13_lishi_warn": "noted", "t13_summer": "build", "t13_hedong": "keep",
    "t14_rains": "silent", "t14_frontier": "reinforce",
    "t15_jiwen": "demote", "t15_winter": "grand",
    "t16_court": "delegate", "t16_luoyang_haul": "all",
    "t17_jingji": "calm", "t17_harvest": "keep",
    "p_envoy": "eunuch",
    "r_luoyang": "recruit", "r_tongguan": "jinjun", "r_trust": "supervise", "r_guo": "march",
    "r_hebei": "hebei", "r_west": "call", "r_sortie": "sortie", "r_flight": "west", "r_tax": "merchants",
}


def historical(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    picks = []
    for memo in visible:
        oid = HISTORICAL_MEMO.get(memo["id"])
        if memo["id"] == "p_envoy" and m.turn < 16:
            continue  # 辅璆琳：十四载二月
        if memo["id"] == "p_summon" and m.turn == 18:
            oid = "summon"  # 冯神威：十四载七月
        if oid:
            picks.append((memo["id"], oid))
    return picks, {}  # 事件抉择全部走默认项（默认项即史事）


WISE_MEMO = {
    "t0_hedong": "deny", "t0_xier": "modest", "t0_nanzhao": "appease", "t0_anxi": "restrain", "t0_huaqing": "train",
    "t1_nanzhao_envoy": "honor", "t1_xier_report": "peace", "t1_khitan": "approve", "t1_grain": "canal", "t1_donggong": "protect",
    "t2_west": "hold", "t2_west_calm": "farm", "t2_shuofang": "guo", "t2_census": "censors", "t2_east": "walls",
    "t3_an_tribute": "reward", "t3_review": "strict", "t3_winter": "direct",
    "p_gaoqing": "contact",
    "t4_an_troops": "half", "t4_haul": "boats", "t4_censorate": "punish",
    "t5_tubo": "garrison", "t5_jingzhao": "deny", "t5_relief": "relief",
    "t6_successor": "chen", "t6_feast": "apart", "t6_autumn": "audit",
    "t7_anxi": "feng", "t7_jinjun": "draft", "t7_winter": "troops", "t7_coin": "ban",
    "t8_zhenqing": "keep", "t8_an_accuse": "hush", "t8_spring": "loan",
    "t9_jinjun_command": "general", "t9_tubo": "soothe", "t9_canal": "haul",
    "t10_geshu": "title_only", "t10_horses": "deny", "t10_harvest": "buy",
    "t11_hebei": "militia", "t11_yang": "curb", "t11_border_pay": "central",
    "t12_chancellor": "refuse", "t12_tongguan": "fortify", "t12_spring": "relief", "t12_an_away": "excuse",
    "t13_lishi_warn": "divide", "t13_hedong": "replace", "t13_summer": "stop", "t13_drill": "drill",
    "t14_rains": "retake", "t14_frontier": "defend", "t14_shuofang_in": "move",
    "t15_jiwen": "demote", "t15_luoyang": "stock", "t15_winter": "simple",
    "t16_longyou": "li", "t16_luoyang_haul": "split", "t16_court": "attend", "t16_famine": "relief",
    "t17_fanyang": "envoy", "t17_jingji": "levy", "t17_harvest": "grain",
    "t18_hebei_watch": "permit", "t18_tongguan": "jinjun",
    "p_restrain_guozhong": "restrain", "p_abdicate": "rouse",
    "r_luoyang": "recruit", "r_trust": "trust", "r_guo": "march", "r_hebei": "hebei",
    "r_west": "part", "r_sortie": "hold", "r_flight": "west", "r_relief": "relief", "r_tax": "palace",
}
WISE_CHOICE = {
    "guozhong_coverup": "punish", "khitan_defeat": "console", "donggong_framed_1": "protect",
    "donggong_framed_2": "protect", "abusi_revolt": "to_shuofang", "linfu_posthumous": "reject",
    "an_court_visit": "honor", "fanjiang_swap": "reject", "horse_tribute": "delay", "mawei": "execute",
}


def _treasury_cost(opt: dict) -> float:
    cost = 0.0
    for op in opt.get("ops", []):
        if op.get("op") == "adjust_resource" and op.get("resource") == "treasury":
            cost -= float(op["delta"])
        if op.get("op") == "start_project":
            cost += sum(op["cost_per_turn"].values()) * op["turns"]
    return cost


def wise(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    picks = []
    for memo in visible:
        oid = WISE_MEMO.get(memo["id"])
        if memo["id"] == "p_envoy":
            oid = "eunuch" if m.r("corruption") < 50 else None
        if memo["id"] == "p_summon":
            oid = "summon" if m.r("rebellion_risk") < 52 else None
        if memo["id"] == "t18_last":
            oid = "hereditary" if m.r("rebellion_risk") >= 52 else "preempt"
        if memo["id"] == "r_tongguan":
            oid = "hedong" if m.armies["hedong_army"]["faction"] == m.main and m.armies["hedong_army"]["strength"] > 0 else "jinjun"
        if not oid:
            continue
        opt = next(o for o in memo["options"] if o["id"] == oid)
        if _treasury_cost(opt) > m.r("treasury") - 250:
            continue  # 量入为出
        picks.append((memo["id"], oid))
    choices = {p["id"]: WISE_CHOICE[p["event_id"]] for p in pending if p["event_id"] in WISE_CHOICE}
    return picks, choices


def half_wise(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    """难度梯度：每条 wise 选择以 50% 概率采纳（以回合与条目 id 定种，可复现）。"""
    picks, choices = wise(m, visible, pending)
    keep = [p for p in picks if random.Random(f"{m.seed}:{m.turn}:{p[0]}").random() < 0.5]
    return keep, {k: v for k, v in choices.items() if random.Random(f"{m.seed}:{k}").random() < 0.5}


# ---- 结局可达性探针（非玩家画像，只证明各结局有路可走） ----
DEFENDER_MEMO = {  # 不阻止起兵，专修守备：目标 E3
    **{k: v for k, v in HISTORICAL_MEMO.items() if not k.startswith("r_")},
    "t0_huaqing": "train", "t2_shuofang": "guo", "t2_east": "walls", "t7_jinjun": "draft",
    "t9_jinjun_command": "general", "t12_tongguan": "fortify", "t14_shuofang_in": "stay",
    "t15_luoyang": "troops", "t17_jingji": "levy", "t18_tongguan": "hedong", "t13_hedong": "replace",
    "p_gaoqing": "contact",
    "r_luoyang": "recruit", "r_trust": "trust", "r_guo": "march", "r_hebei": "hebei", "r_tongguan": "jinjun",
    "r_west": "part", "r_sortie": "hold", "r_relief": "enlist", "r_tax": "palace",
}


def defender(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    return [(x["id"], DEFENDER_MEMO[x["id"]]) for x in visible if x["id"] in DEFENDER_MEMO], {}


PURGE_MEMO = {  # 一味削藩、不顾边防：目标 E2
    **WISE_MEMO, "t3_winter": "half", "t5_tubo": "envoy", "t7_jinjun": "draft", "t9_tubo": "fight",
    "t10_geshu": "deny", "t11_border_pay": "central", "t13_drill": "self", "t14_frontier": "reinforce",
    "t14_shuofang_in": "move", "t16_longyou": "wait", "t8_an_accuse": "cut", "t2_west_calm": "reward",
    "t0_anxi": "campaign", "t0_nanzhao": "campaign", "t1_xier_report": "conscript", "t2_west": "avenge",
}


def purge(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    picks, choices = wise(m, visible, pending)
    picks = [(x["id"], PURGE_MEMO[x["id"]]) for x in visible if x["id"] in PURGE_MEMO]
    for p in pending:
        if p["event_id"] == "khitan_defeat":
            choices[p["id"]] = "split_pinglu"
        if p["event_id"] == "an_court_visit":
            choices[p["id"]] = "detain"
    return picks, choices


CHAOS_MEMO = {  # 羁留禄山而放任朝争、外戚：目标 E5
    **HISTORICAL_MEMO, "t0_hedong": "deny", "t3_an_tribute": "reward", "t8_an_accuse": "ignore",
    "t12_chancellor": "grant", "t17_fanyang": "envoy", "t18_last": "hereditary", "t9_jinjun_command": "eunuch",
    "t14_rains": "silent", "t16_court": "delegate", "t10_geshu": "grant", "t6_feast": "feast",
    "t11_yang": "indulge", "t3_review": "lenient", "p_summon": "soothe", "t13_lishi_warn": "noted",
    "t12_an_away": "excuse",
}


def chaos(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    picks = [(x["id"], CHAOS_MEMO[x["id"]]) for x in visible if x["id"] in CHAOS_MEMO and not x["id"].startswith("p_envoy")]
    choices = {p["id"]: {"khitan_defeat": "console", "fanjiang_swap": "approve",
                         "linfu_posthumous": "approve", "donggong_framed_1": "allow", "an_court_visit": "detain"}.get(p["event_id"], "")
               for p in pending}
    return picks, {k: v for k, v in choices.items() if v}


POLICIES: dict[str, Callable[[Model, list, list], Decision]] = {
    "do_nothing": do_nothing, "historical": historical, "wise": wise, "half_wise": half_wise,
    "defender": defender, "purge": purge, "chaos": chaos,
}


# ============================================================================
# 运行
# ============================================================================
def play_model(pack: dict, policy: Callable, seed: int, trace: bool = False) -> dict[str, Any]:
    m = Model(pack, seed)
    risk_at_19 = None
    while m.outcome is None and m.turn < 40:
        memos, choices = policy(m, m.visible_memorials(), list(m.pending))
        for mid, oid in memos:
            memo = next(x for x in m.pack["memorials"] if x["id"] == mid)
            m.adopt(memo, oid)
        for cid, oid in choices.items():
            m._now = m.turn
            m.try_apply({"op": "choose_event_option", "choice_id": cid, "option_id": oid}, "choice")
        if trace:
            print(f"T{m.turn:>2} 鼙鼓{m.r('rebellion_risk'):5.1f} 异志{m.r('an_ambition'):5.1f} 外重{m.r('fanzhen_power'):5.1f} "
                  f"朝争{m.r('court_strife'):5.1f} 君威{m.r('authority'):5.1f} 国库{m.r('treasury'):6.0f} 太仓{m.r('grain'):6.0f} "
                  f"边患{m.r('frontier_pressure'):5.1f} 民心{m.r('morale'):5.1f} 积弊{m.r('corruption'):5.1f} 奏疏{len(m.visible_memorials())}")
        m.resolve()
        if m.turn == 19:
            risk_at_19 = m.r("rebellion_risk")
    if trace:
        for line in m.log:
            print("   ", line)
        print("结局", m.outcome)
    return {"outcome": m.outcome["id"] if m.outcome else "none", "turn": m.turn,
            "risk19": risk_at_19 if risk_at_19 is not None else m.r("rebellion_risk"),
            "rebellion": bool(m.flags.get("rebellion_started")), "min_items": None}


def check_memorial_coverage(pack: dict, seeds: int = 30) -> dict[int, int]:
    """每季可见奏疏条数的最小值（跨策略、跨种子），用于验证「每季至少 3 条」。"""
    worst: dict[int, int] = {}
    for name, pol in POLICIES.items():
        for seed in range(seeds):
            m = Model(pack, seed)
            while m.outcome is None and m.turn < 40:
                vis = m.visible_memorials()
                worst[m.turn] = min(worst.get(m.turn, 99), len(vis))
                memos, choices = pol(m, vis, list(m.pending))
                for mid, oid in memos:
                    m.adopt(next(x for x in pack["memorials"] if x["id"] == mid), oid)
                for cid, oid in choices.items():
                    m.try_apply({"op": "choose_event_option", "choice_id": cid, "option_id": oid})
                m.resolve()
    return dict(sorted(worst.items()))


# ---------------- 引擎后端 ----------------
def play_engine(pack: dict, policy: Callable, seed: int, trace: bool = False) -> dict[str, Any]:
    sys.path.insert(0, str(ROOT / "engine" / "backend"))
    from simcore.domain import models as M  # noqa: E402
    missing = [f for f in ("pending_choices", "outcome", "counters", "flag_turns") if f not in M.WorldState.model_fields]
    if missing:
        raise SystemExit(f"引擎尚未实现 CONTRACT §1 字段：{', '.join(missing)}。请先用 --backend model。")
    from simcore.domain.apply import apply  # noqa: E402
    from simcore.domain.events import matches  # noqa: E402
    from simcore.domain.turn import resolve_turn  # noqa: E402
    from simcore.scenario.loader import build_initial_state, load_scenario  # noqa: E402

    scenario = load_scenario(PACK)
    state = build_initial_state(scenario)
    rng = random.Random(seed)
    memorials = pack["memorials"]
    risk19 = None

    class View:  # 让策略函数用同一接口读取引擎状态
        def __init__(self, st):
            self.st, self.turn, self.main = st, st.turn, "tang"
            self.armies = {k: {"faction": a.faction, "strength": a.strength} for k, a in st.armies.items()}

        def r(self, rid):
            return self.st.resources[rid].amount

    while state.outcome is None and state.turn < 40:
        visible = [
            mm for mm in memorials
            if f"memorial:{mm['id']}" not in state.flags
            and ("turn" not in mm or mm["turn"] == state.turn)
            and ("conditions" not in mm or matches(mm["conditions"], state))
        ]
        pending = [{"id": p.id, "event_id": p.event_id} for p in state.pending_choices]
        memos, choices = policy(View(state), visible, pending)
        for mid, oid in memos:
            opt = next(o for o in next(x for x in memorials if x["id"] == mid)["options"] if o["id"] == oid)
            for op in opt.get("ops", []):
                try:
                    state, _ = apply(op, state)
                except ValueError:
                    pass
            state, _ = apply({"op": "set_flag", "key": f"memorial:{mid}", "value": oid}, state)
        for cid, oid in choices.items():
            try:
                state, _ = apply({"op": "choose_event_option", "choice_id": cid, "option_id": oid}, state)
            except ValueError:
                pass
        state, report = resolve_turn(state, rng, scenario)
        if state.turn == 19:
            risk19 = state.resources["rebellion_risk"].amount
    return {"outcome": state.outcome.id if state.outcome else "none", "turn": state.turn,
            "risk19": risk19 if risk19 is not None else state.resources["rebellion_risk"].amount,
            "rebellion": bool(state.flags.get("rebellion_started"))}


def main() -> None:
    ap = argparse.ArgumentParser(description="《天宝》剧本策略平衡")
    ap.add_argument("--backend", choices=["model", "engine"], default="model")
    ap.add_argument("--policy", choices=[*POLICIES, "all"], default="all")
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--seed", type=int, default=None, help="只跑一个种子")
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--coverage", action="store_true", help="检查每季可见奏疏条数")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    pack = load_pack()
    if args.coverage:
        print("每季最少可见奏疏条数：", check_memorial_coverage(pack))
        return
    play = play_model if args.backend == "model" else play_engine
    names = list(POLICIES) if args.policy == "all" else [args.policy]
    seeds = [args.seed] if args.seed is not None else list(range(args.seeds))
    for name in names:
        results = [play(pack, POLICIES[name], s, args.trace) for s in seeds]
        dist = Counter(r["outcome"] for r in results)
        risks = [r["risk19"] for r in results]
        rebel = sum(r["rebellion"] for r in results)
        print(f"\n== {name}（{len(seeds)} 局，后端 {args.backend}）")
        for k, v in dist.most_common():
            print(f"   {k:<18} {v:>4}  {v / len(seeds):6.1%}")
        print(f"   起兵 {rebel / len(seeds):.0%}；T19 鼙鼓 均值 {statistics.mean(risks):.1f}，"
              f"中位 {statistics.median(risks):.1f}，范围 {min(risks):.1f}–{max(risks):.1f}")


if __name__ == "__main__":
    main()
