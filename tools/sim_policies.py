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

策略：
- do_nothing：不批奏疏，事件抉择到期走默认项（默认项即史事）。目标：E4 ≥ 80%，T19 鼙鼓 75–95。
- historical：按史事批奏疏（准河东、征南诏、杨国忠拜相、遣中使……）。
- wise：按「好诏」批奏疏，量入为出。目标：E1 可达。
- half_wise：每条 wise 选择以 50% 概率采纳，用来看难度梯度。
- defender / purge / chaos：结局可达性探针，分别瞄准 E3、E2、E5。它们不是玩家画像。
- bankrupt / mawei_refuse：失败结局探针，分别瞄准「帑竭兵变」「龙驭宾天」。
- detain_early：开局禄山在京即留京夺镇（奏疏「禄山在京未归」），其余同 detain。用来确认早夺镇不比召而后夺更省事。
- first / last（round 8 压力测试）：每条奏疏、每个事件抉择都取首项 / 末项，不看局势。last 复现 self04（开局即留京夺镇、
  处处取末项）；目标：E1 < 10%、E3 < 25%，多为历史重演 / 藩镇之始 / 失败。
- passive_war：开局留京夺镇而穷治党与（酿成兵变），战时只守不攻（不进剿、不断粮、不招抚、不出关）。目标：罕得「再造唐室」。
- ops_disarm（仅 engine 后端）：不经奏疏，以通用诏令把禄山调入京畿、免其范阳 / 平卢节度、以郭子仪接范阳，
  验证事件「禄山留京解镇」把这一局面并入留京路线（gpt-07）。model 后端不模拟玩家 ops，此策略退化为 wise。

- wise_cards（round 9）：wise 之外，每季按局势颁行政令卡（policy_cards.yaml：疏浚漕渠、赈济、修城、常平仓、营田……），
  量入为出、遵守冷却。用来确认政令卡有用而不喧宾夺主：E1 类不应比 wise 高出许多，国库不应因卡片而日丰。

round 9 的朝会日程（settings.agenda：每季召对 3、廷议 1）：本脚本的策略只批奏疏、颁政令卡，不召对、不廷议，故不受其限；
若日后加入召对策略，须遵守 agenda_limits() 给出的上限。
驿传（settings.courier 与各地区 courier_days）：驿程超过阈值的地区（安西、南诏），奏疏晚一季才出现——
当季条件成立即「发出」，下季「奏到」可见（model 后端按此模拟；engine 后端若引擎已原生实现则交给引擎）。

输出另附「E1 类」合计（e1_* 结局，含按朝争分段的同名结局）。

--difficulty yanyi|shishi|diyu 选难度档（scenario.yaml 的 difficulties）；引擎未原生支持时由本脚本改写剧本。

输出：每种策略在 N 个种子上的结局分布，以及 T19（或终局）时渔阳鼙鼓的分布。
--coverage 检查每季可见奏疏的最少条数（硬性要求为 ≥ 3）。
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
    for name in ("scenario", "characters", "regions", "factions", "armies", "events", "memorials", "policy_cards"):
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
        self.wars = {frozenset(w.values() if isinstance(w, dict) else w) for w in sc.get("wars", [])}
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
        # 驿传（round 9）：驿程超过阈值的地区，其奏疏当季发出、下季奏到
        self.late_regions = late_regions(pack)
        self.late_sent: set[str] = set()
        self.card_last: dict[str, int] = {}

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
                return self.flags.get(c["key"]) not in (None, False)
            if op == "absent":
                return self.flags.get(c["key"]) in (None, False)
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

    def _travel_turns(self, src: str, dst: str) -> int | None:
        """最短路程（季数），Dijkstra；不可达为 None。"""
        import heapq
        best = {src: 0}
        heap = [(0, src)]
        while heap:
            d, r = heapq.heappop(heap)
            if r == dst:
                return d
            if d > best.get(r, 1 << 30):
                continue
            for n, w in self.regions[r]["adj"].items():
                if d + w < best.get(n, 1 << 30):
                    best[n] = d + w
                    heapq.heappush(heap, (d + w, n))
        return None

    def _op_move_character(self, op):
        ch = self.chars[op["character"]]
        if ch["status"] != "alive" or ch["transit"]:
            raise Rejected("人物不能行动")
        turns = self._travel_turns(ch["region"], op["to_region"])
        if not turns:
            raise Rejected("无路可达")
        ch["transit"] = {"to": op["to_region"], "eta": self.turn + turns}

    def _op_move_army(self, op):
        a = self.armies[op["army"]]
        if a["transit"] or a["strength"] <= 0:
            raise Rejected("军队不能行军")
        adj = self.regions[a["region"]]["adj"]
        if op["to_region"] not in adj:
            raise Rejected("不相邻")
        a["transit"] = {"to": op["to_region"], "eta": self.turn + adj[op["to_region"]]}

    def _op_detach(self, op):
        """分兵：自 army 扣出 strength 编为新军（id「原 id_d序号」），赴 to_region（相邻；同地则就地分屯）。"""
        a = self.armies[op["army"]]
        if a["transit"] or a["strength"] <= float(op["strength"]) or float(op["strength"]) <= 0:
            raise Rejected("不能分兵")
        self._seq = getattr(self, "_seq", 0) + 1
        new = {**a, "strength": float(op["strength"]), "commander": op.get("commander"), "transit": None}
        a["strength"] -= float(op["strength"])
        if op["to_region"] != a["region"]:
            turns = self._travel_turns(a["region"], op["to_region"])
            if turns is None:
                raise Rejected("无路可达")
            new["transit"] = {"to": op["to_region"], "eta": self.turn + turns}
        self.armies[f"{op['army']}_d{self._seq}"] = new

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
        """当季可见奏疏。驿程过远地区的奏疏（同引擎 domain.memorials.is_visible）：写 turn 者可见窗口后移一季；
        写 conditions 者须上季已可见（记为发出），且此刻条件仍成立。每季只调用一次。"""
        out = []
        for m in self.pack["memorials"]:
            if f"memorial:{m['id']}" in self.flags:
                continue
            far = m.get("region") in self.late_regions
            if "turn" in m and m["turn"] + (1 if far else 0) != self.turn:
                if far and m["turn"] == self.turn and self.matches(m.get("conditions")):
                    self.late_sent.add(m["id"])
                continue
            if "conditions" in m and not self.matches(m["conditions"]):
                continue
            if far and "conditions" in m and m["id"] not in self.late_sent:
                self.late_sent.add(m["id"])   # 本季发出，下季奏到
                continue
            if far and "turn" in m and "conditions" in m and m["id"] not in self.late_sent:
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
        return self.factions.get(f1, {}).get(f2, 0) < 0 or self.factions.get(f2, {}).get(f1, 0) < 0

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
        # 4b 养兵（formulas.upkeep：本方诸军按现有兵额计费）
        for row in self.sc["formulas"].get("upkeep", []) or []:
            wanted = set(row.get("armies") or [])
            factions = set(row.get("factions") or [self.main])
            strength = sum(a["strength"] for k, a in self.armies.items() if a["strength"] > 0
                           and (k in wanted if wanted else a["faction"] in factions))
            rid = row.get("resource", "treasury")
            self.res[rid]["amount"] = self._clamp(rid, self.res[rid]["amount"] - strength / float(row["per"]) * float(row["amount"]))
        # 5 收入
        for key, inc in self.sc["formulas"].get("income", {}).items():
            regions = list(self.regions.values()) if inc.get("per_region", True) else [{"stats": {}, "controller": self.main}]
            for reg in regions:
                if inc.get("controlled_only") and reg["controller"] != self.main:
                    continue
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
        for rid, expr in self.sc["formulas"].get("drift", {}).items():
            values = {"turn": T, **{k: v["amount"] for k, v in self.res.items()}}  # 与引擎一致：逐项取最新值
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
            if not self.matches(route_def.get("conditions"), self.turn + 1):
                continue
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


def late_regions(pack: dict[str, Any]) -> set[str]:
    """驿程超过 settings.courier.late_threshold_days（缺省 60）的地区：奏疏晚一季奏到、诏令晚一季到达（CONTRACT §7.3）。"""
    settings = (pack.get("scenario") or {}).get("settings") or {}
    threshold = float((settings.get("courier") or {}).get("late_threshold_days", 60))
    return {str(r["id"]) for r in pack.get("regions") or [] if float(r.get("courier_days") or 0) > threshold}


def agenda_limits(pack: dict[str, Any]) -> dict[str, int | None]:
    """每季召对、廷议上限（settings.agenda；未写为不限）。召对类策略须据此限次。"""
    agenda = ((pack.get("scenario") or {}).get("settings") or {}).get("agenda") or {}
    return {"audience": agenda.get("audience_per_season"), "debate": agenda.get("debate_per_season")}


def _fill(value: Any, params: dict[str, Any]) -> Any:
    """政令卡 ops 模板的占位替换：整值 "{name}" 保留参数类型，嵌在文字中的替换为字符串。"""
    if isinstance(value, str):
        if value.startswith("{") and value.endswith("}") and value[1:-1] in params:
            return params[value[1:-1]]
        for k, v in params.items():
            value = value.replace("{" + k + "}", str(v))
        return value
    if isinstance(value, dict):
        return {k: _fill(v, params) for k, v in value.items()}
    if isinstance(value, list):
        return [_fill(v, params) for v in value]
    return value


def expand_card(pack: dict[str, Any], card_id: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    card = next(c for c in pack.get("policy_cards") or [] if c["id"] == card_id)
    return [_fill(op, params) for op in card["ops"]]


# ============================================================================
# 策略
# ============================================================================
Decision = tuple[list[tuple[str, Any]], dict[str, str]]  # ([(memorial_id, option_id)], {choice_id: option_id})
# 特例：(OPS, [op, ...]) 表示玩家自拟的诏令 ops（只有 engine 后端执行；model 后端忽略）
OPS = "__ops__"


# 同一奏疏的状态分支（剧本按局势写的不同版本，选项 id 相同）：策略表只写主条目，分支沿用其选择。
VARIANT_BASE = {
    "t4_an_troops_calm": "t4_an_troops", "t6_jiannan_vacant": "t6_jiannan", "t10_huihe_tribute": "t10_huihe",
    "t13_lishi_warn_peace": "t13_lishi_warn", "t14_lishi": "t14_rains", "t14_frontier_peace": "t14_frontier",
    "t15_luoyang_war": "t15_luoyang", "t16_court_war": "t16_court", "t16_famine_plain": "t16_famine",
    "t18_hebei_watch_far": "t18_hebei_watch", "t18_tongguan_safe": "t18_tongguan", "r_tongguan_jinjun": "r_tongguan",
    "t7_anxi_away": "t7_anxi", "t10_geshu_title": "t10_geshu", "p_gaoqing_away": "p_gaoqing",
    "t16_court_detained": "t16_court", "t15_jiwen_court": "t15_jiwen", "t5_jingzhao_held": "t5_jingzhao",
    # gpt-10 #5 / #6：禄山已留京解镇、国忠出镇在蜀时的分支
    "t1_khitan_deputy": "t1_khitan", "t3_fanyang_tribute": "t3_an_tribute", "t4_fanyang_troops": "t4_an_troops",
    "t12_fanyang_merit": "t12_gaoshen", "t12_chancellor_far": "t12_chancellor",
}


def lookup(table: dict[str, str], memo: dict) -> str | None:
    """策略表中该奏疏（或其主条目）的选项；选项在本分支不存在时返回 None。"""
    oid = table.get(memo["id"])
    if oid is None:
        oid = table.get(VARIANT_BASE.get(memo["id"], ""))
    return oid if oid and any(o["id"] == oid for o in memo.get("options", [])) else None


def do_nothing(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    """不批奏疏，事件抉择一律到期走默认项。"""
    return [], {}


HISTORICAL_MEMO = {
    "t0_hedong": "grant", "t0_xier": "lavish", "t0_nanzhao": "campaign", "t0_anxi": "campaign", "t0_huaqing": "palace",
    "t1_xier_report": "conscript", "t1_khitan": "approve", "t1_grain": "extra_haul", "t1_donggong": "allow",
    "t2_west": "hold", "t2_shuofang": "sishun", "t2_census": "convert",
    "t3_an_tribute": "reward", "t3_review": "lenient", "t3_winter": "half",
    "t4_an_troops": "approve", "t4_haul": "convert", "t4_censorate": "quiet",
    "t5_tubo": "strike", "t5_jingzhao": "approve", "t5_wanghong": "purge",
    "t6_successor": "guozhong", "t6_feast": "feast", "t6_tianchang": "feast", "t6_abusi": "an_pursue",
    "t6_jiannan": "brief",
    "t7_anxi": "feng", "t7_winter": "yang", "t7_coin": "allow",
    "t8_zhenqing": "send", "t8_an_accuse": "ignore", "t8_neishi": "expand", "t8_yangnu": "slave_only",
    "t8_song": "allow",
    "t9_jinjun_command": "keep", "t9_jiuqu": "strike", "t9_lychee": "send",
    "t10_geshu": "grant", "t10_huihe": "reward", "t10_bolu": "reward",
    "t11_yang": "indulge", "t11_border_pay": "self",
    "t12_chancellor": "refuse", "t12_an_away": "excuse", "t12_gaoshen": "grant", "t12_horses": "grant",
    "t12_limi": "approve",
    "t13_lishi_warn": "noted", "t13_hedong": "keep",
    "t14_rains": "silent", "t14_frontier": "reinforce", "t14_zhiju": "poetry", "t14_shence": "establish",
    "t15_jiwen": "demote", "t15_winter": "grand",
    "t16_court": "delegate", "t16_supi": "receive",
    "t17_jingji": "calm", "t17_zanpu": "ignore", "t17_qingzong_far": "invite",
    "t18_huaqing": "go",
    "p_envoy": "eunuch", "p_an_capital": "release",
    "r_luoyang": "recruit", "r_tongguan": "jinjun", "r_trust": "supervise", "r_guo": "march", "r_shuofang_march": "march",
    "r_hebei": "hebei", "r_west": "call", "r_sortie": "sortie", "r_flight": "west", "r_tax": "merchants",
}


def historical(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    picks = []
    for memo in visible:
        oid = lookup(HISTORICAL_MEMO, memo)
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
    "t5_tubo": "garrison", "t5_jingzhao": "deny", "t5_wanghong": "limit",
    "t6_successor": "chen", "t6_feast": "apart", "t6_tianchang": "refuse", "t6_abusi": "shuofang",
    "t6_jiannan": "brief",
    "t7_anxi": "feng", "t7_jinjun": "draft", "t7_winter": "troops", "t7_coin": "ban",
    "t8_zhenqing": "keep", "t8_an_accuse": "hush", "t8_neishi": "cut", "t8_yangnu": "slave_only",
    "t8_song": "deny",
    "t9_jinjun_command": "general", "t9_jiuqu": "hold", "t9_lychee": "stop",
    "t10_geshu": "title_only", "t10_huihe": "trade", "t10_bolu": "reward",
    "t11_hebei": "militia", "t11_yang": "curb", "t11_border_pay": "central",
    "t12_chancellor": "refuse", "t12_tongguan": "fortify", "t12_an_away": "excuse",
    "t12_gaoshen": "court", "t12_horses": "deny", "t12_limi": "deny",
    "t13_lishi_warn": "divide", "t13_hedong": "replace", "t13_drill": "drill", "t13_shuofang_in": "move",
    "t14_rains": "retake", "t14_frontier": "defend", "t14_zhiju": "strict", "t14_shence": "capital",
    "t15_jiwen": "demote", "t15_luoyang": "stock", "t15_winter": "simple",
    "t16_longyou": "li", "t16_supi": "receive", "t16_court": "attend", "t16_famine": "relief",
    "t17_fanyang": "envoy", "t17_jingji": "levy", "t17_zanpu": "condole", "t17_qingzong_near": "plain",
    "t18_hebei_watch": "permit", "t18_tongguan": "jinjun", "t18_huaqing": "stay",
    "p_restrain_guozhong": "restrain", "p_abdicate": "rouse", "p_an_capital": "honor",
    "r_luoyang": "recruit", "r_trust": "trust", "r_guo": "march", "r_shuofang_march": "march", "r_hebei": "hebei",
    "r_west": "part", "r_sortie": "hold", "r_flight": "west", "r_relief": "relief", "r_tax": "palace",
    "r_tongguan_jinjun": "jinjun", "p_fanyang_warn": "pay_amnesty",
    "s_demobilize": "keep_best", "s_compensate": "honor", "s_canal": "repair", "s_finance": "abolish",
    "s_rewards": "honor_recall", "s_hebei": "relief", "s_frontier": "garrison", "s_collaborators": "lenient",
}
# 乱局奏疏池（round 8）：明君亦须进讨——直捣范阳、出井陉、断粮道、资义兵、招降胁从；东都暂不轻出。
WAR_POOL_WISE = {
    "wp_strike_shuofang": "march", "wp_strike_shuofang_2": "march", "wp_strike_hedong": "hebei", "wp_strike_hedong_2": "hebei",
    "wp_jinjun_east": "hold", "wp_jinjun_east_2": "hold", "wp_supply_raid": "burn", "wp_supply_raid_2": "burn",
    "wp_amnesty": "pardon", "wp_amnesty_2": "pardon", "wp_tongguan": "repair", "wp_tongguan_2": "repair",
    "wp_hebei_loyal": "arm", "wp_hebei_loyal_2": "arm", "wp_finance": "frugal", "wp_finance_2": "frugal",
    "wp_grain": "route", "wp_grain_2": "route", "wp_morale": "remit", "wp_morale_2": "relief",
    "wp_recruit": "hire", "wp_recruit_2": "hire", "wp_taiyuan": "walls", "wp_taiyuan_2": "supply",
    "wp_suiyang": "walls", "wp_suiyang_2": "supply", "wp_canal": "route", "wp_canal_2": "route",
    "wp_rewards": "reward", "wp_rewards_2": "reward", "wp_huihe": "accept", "wp_west_troops": "decline",
    "p_fanyang_kept": "disarm",
}
WISE_MEMO.update(WAR_POOL_WISE)
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
        oid = lookup(WISE_MEMO, memo)
        if memo["id"] == "p_envoy":
            oid = "eunuch" if m.r("corruption") < 50 else None
        if memo["id"] == "p_summon":
            oid = "summon" if m.r("rebellion_risk") < 52 else None
        if memo["id"] == "t18_last":
            oid = "hereditary" if m.r("rebellion_risk") >= 52 else "preempt"
        if memo["id"] == "t17_qingzong_far":
            oid = "invite" if m.r("rebellion_risk") < 52 else "hostage"
        if memo["id"] == "r_tongguan":
            oid = "hedong" if m.armies["hedong_army"]["faction"] == m.main and m.armies["hedong_army"]["strength"] > 0 else "jinjun"
        if memo["id"] in ("r_guo", "r_shuofang_march", "r_hebei") and any(x["id"].startswith("wp_strike_shuofang") for x in visible):
            continue  # 同季已议朔方直捣范阳，不再另调朔方军（免得两道军令相冲）
        if not oid:
            continue
        opt = next(o for o in memo["options"] if o["id"] == oid)
        if _treasury_cost(opt) > m.r("treasury") - 250:
            continue  # 量入为出
        picks.append((memo["id"], oid))
    choices = {p["id"]: WISE_CHOICE[p["event_id"]] for p in pending if p["event_id"] in WISE_CHOICE}
    return picks, choices


# ---- 政令卡（round 9）：wise 加按局势颁行的卡片 ----
_CARD_USE: dict[tuple[int, str], int] = {}   # (种子, 卡 id) → 最近颁行回合（策略函数无状态，故记于此）
_CARD_PACK: dict[str, Any] = {}


def _cards_pack() -> dict[str, Any]:
    if not _CARD_PACK:
        _CARD_PACK.update(load_pack())
    return _CARD_PACK


def _card_ready(m: Any, card_id: str) -> bool:
    card = next(c for c in _cards_pack().get("policy_cards") or [] if c["id"] == card_id)
    last = _CARD_USE.get((m.seed, card_id))
    if m.turn == 0:
        last = None
        _CARD_USE.pop((m.seed, card_id), None)
    return last is None or m.turn - last > int(card.get("cooldown") or 0)


def _region_stat(m: Any, rid: str, stat: str) -> float:
    st = getattr(m, "st", None)
    if st is not None:
        return float(st.regions[rid].stats.get(stat, 0))
    return float(m.regions[rid]["stats"].get(stat, 0))


def _controlled(m: Any, rid: str) -> bool:
    st = getattr(m, "st", None)
    ctrl = st.regions[rid].controller if st is not None else m.regions[rid]["controller"]
    return ctrl in (None, m.main)


def wise_cards(m: Any, visible: list[dict], pending: list[dict]) -> Decision:
    """wise 批奏疏，另每季至多颁两张政令卡（钱粮宽裕时，守冷却）：漕渠、赈济最乱之道、乱起修潼关、边地营田、常平仓。"""
    picks, choices = wise(m, visible, pending)
    spend = sum(_treasury_cost(next(o for o in x["options"] if o["id"] == oid))
                for x in visible for mid, oid in picks if mid == x["id"])
    budget = m.r("treasury") - spend - 400   # 留足一年开支，余钱才办地方之事
    plan: list[tuple[str, dict[str, Any], float]] = []
    rebellion = bool(getattr(m, "st", None).flags.get("rebellion_started") if getattr(m, "st", None) is not None
                     else m.flags.get("rebellion_started"))
    if rebellion and _controlled(m, "tongguan"):
        plan.append(("int_walls", {"region": "tongguan"}, 60))
    if 1 <= m.turn <= 12 and _controlled(m, "henan"):
        plan.append(("int_canal", {"region": "henan"}, 90))
    rows = [r for r in ("hebei", "henan", "jingji", "duji", "huainan", "jiangnan", "shannan", "jiannan") if _controlled(m, r)]
    if rows:
        worst = min(rows, key=lambda r: _region_stat(m, r, "order"))
        if _region_stat(m, worst, "order") < 65 and m.r("grain") > 900:
            plan.append(("int_relief", {"region": worst}, 10))
    if m.turn <= 14 and _controlled(m, "longyou"):
        plan.append(("fin_tuntian", {"region": "longyou"}, 90))
    used = 0
    for card_id, params, cost in plan:
        if used >= 2 or cost > budget or not _card_ready(m, card_id):
            continue
        picks.append((OPS, expand_card(_cards_pack(), card_id, params)))
        _CARD_USE[(m.seed, card_id)] = m.turn
        budget -= cost
        used += 1
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
    "t9_jinjun_command": "general", "t12_tongguan": "fortify", "t13_shuofang_in": "stay",
    "t15_luoyang": "troops", "t17_jingji": "levy", "t18_tongguan": "hedong", "t13_hedong": "replace",
    "p_gaoqing": "contact",
    "r_luoyang": "recruit", "r_trust": "trust", "r_guo": "march", "r_shuofang_march": "march", "r_hebei": "hebei", "r_tongguan": "jinjun",
    "r_west": "part", "r_sortie": "hold", "r_relief": "enlist", "r_tax": "palace",
    **{k: v for k, v in WAR_POOL_WISE.items() if k.startswith("wp_")},
}


def defender(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    return [(x["id"], oid) for x in visible if (oid := lookup(DEFENDER_MEMO, x))], {}


PURGE_MEMO = {  # 一味削藩、不顾边防：目标 E2
    **WISE_MEMO, "t3_winter": "half", "t5_tubo": "envoy", "t7_jinjun": "draft", "t9_tubo": "fight",
    "t10_geshu": "deny", "t11_border_pay": "central", "t13_drill": "self", "t14_frontier": "reinforce",
    "t13_shuofang_in": "move", "t16_longyou": "wait", "t8_an_accuse": "cut", "t2_west_calm": "reward",
    "t0_anxi": "campaign", "t0_nanzhao": "campaign", "t1_xier_report": "conscript", "t2_west": "avenge",
    "t9_jiuqu": "soothe", "t14_shence": "capital", "t17_zanpu": "ignore", "t16_supi": "return",
    "t12_gaoshen": "court", "p_an_capital": "detain", "p_fanyang_warn": "all_three",
}


def purge(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    picks, choices = wise(m, visible, pending)
    picks = [(x["id"], oid) for x in visible if (oid := lookup(PURGE_MEMO, x))]
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
    "t12_an_away": "excuse", "p_fanyang_warn": "pay_amnesty",
}


def chaos(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    picks = [(x["id"], oid) for x in visible if not x["id"].startswith("p_envoy") and (oid := lookup(CHAOS_MEMO, x))]
    choices = {p["id"]: {"khitan_defeat": "console", "fanjiang_swap": "approve",
                         "linfu_posthumous": "approve", "donggong_framed_1": "allow", "an_court_visit": "detain"}.get(p["event_id"], "")
               for p in pending}
    return picks, {k: v for k, v in choices.items() if v}


# ---- 夺镇路线（#36）：留京解兵、新帅到镇、安抚旧部；careless 版只夺镇不安抚 ----
DETAIN_PICK = "detain_guo"


def _detain(m: Model, visible: list[dict], pending: list[dict], careful: bool) -> Decision:
    picks, choices = wise(m, visible, pending)
    picks = [(mid, oid) for mid, oid in picks if mid not in ("p_summon", "p_an_capital", "p_fanyang_warn", "t17_fanyang")]
    for memo in visible:
        mid = memo["id"]
        if mid == "p_summon":
            picks.append((mid, "summon"))  # 不论风闻高低，都设法召其入朝
        elif mid == "p_an_capital":
            picks.append((mid, DETAIN_PICK))
        elif mid == "p_fanyang_warn":
            if careful:
                picks.append((mid, "all_three"))
            else:
                picks.append((mid, "purge"))
    for p in pending:
        if p["event_id"] == "an_court_visit":
            choices[p["id"]] = DETAIN_PICK
    return picks, choices


def detain_early(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    """开局即留京夺镇（奏疏「禄山在京未归」→ 郭子仪接范阳），此后三策安抚，同 detain。"""
    picks, choices = _detain(m, visible, pending, careful=True)
    for memo in visible:
        if memo["id"] == "p_an_in_capital":
            picks.append((memo["id"], DETAIN_PICK))
    return picks, choices


def ops_disarm(m: Any, visible: list[dict], pending: list[dict]) -> Decision:
    """通用诏令夺镇（engine 后端）：T10 起若禄山在范阳，诏其移驻京畿；到京后免范阳、平卢节度，以郭子仪接范阳（赴任）。
    不用「禄山在京」系列奏疏与华清宫抉择的留京选项；「范阳旧部可虑」出现后行三策。"""
    picks, choices = wise(m, visible, pending)
    picks = [(mid, oid) for mid, oid in picks if mid not in ("p_summon", "p_an_capital", "p_an_in_capital", "t17_fanyang")]
    for memo in visible:
        if memo["id"] == "p_fanyang_warn":
            picks = [(mid, oid) for mid, oid in picks if mid != "p_fanyang_warn"] + [("p_fanyang_warn", "all_three")]
    choices = {k: v for k, v in choices.items() if v not in ("detain", "detain_guo", "detain_feng")}
    st = getattr(m, "st", None)
    if st is None:
        return picks, choices
    an = st.characters["an_lushan"]
    holds = set(an.offices or [])
    if m.turn >= 10 and an.region == "fanyang" and not an.in_transit and "fanyang_jds" in holds and not st.flags.get("an_detained"):
        picks.append((OPS, [{"op": "move_character", "character": "an_lushan", "to_region": "jingji"}]))
    elif m.turn >= 10 and an.region == "jingji" and not an.in_transit and "fanyang_jds" in holds:
        ops = [{"op": "dismiss", "character": "an_lushan", "office": office} for office in ("fanyang_jds", "pinglu_jds") if office in holds]
        guo = st.characters["guo_ziyi"]
        ops += [{"op": "dismiss", "character": "guo_ziyi", "office": office} for office in (guo.offices or [])]
        ops.append({"op": "appoint", "character": "guo_ziyi", "office": "fanyang_jds", "dispatch": True})
        picks.append((OPS, ops))
    return picks, choices


def detain(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    """夺镇弭兵：召禄山入朝即留京解兵，郭子仪接范阳，三策安抚旧部。目标：E1 类结局 ≥ 60%。"""
    return _detain(m, visible, pending, careful=True)


def detain_careless(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    """只夺镇、不安抚（穷治党与）：目标：多数酿成范阳旧部兵变。"""
    return _detain(m, visible, pending, careful=False)


def _cost(opt: dict) -> float:
    """选项的钱粮花费（粮按 0.5 折钱），用于「挥霍」探针。"""
    cost = _treasury_cost(opt)
    for op in opt.get("ops", []):
        if op.get("op") == "adjust_resource" and op.get("resource") == "grain":
            cost -= 0.5 * float(op["delta"])
    return cost


def bankrupt(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    """挥霍探针：每条奏疏都挑最花钱粮的选项（不传位），目标：帑竭兵变。"""
    picks = []
    for memo in visible:
        opts = [o for o in memo["options"] if not (memo["id"] == "p_abdicate" and o["id"] == "abdicate")]
        if opts:
            picks.append((memo["id"], max(opts, key=_cost)["id"]))
    return picks, {}


def mawei_refuse(m: Model, visible: list[dict], pending: list[dict]) -> Decision:
    """史事路线，但马嵬驿拒绝诛杨：目标：龙驭宾天。"""
    picks, _ = historical(m, visible, pending)
    return picks, {p["id"]: "refuse" for p in pending if p["event_id"] == "mawei"}


# ---- 按位次选项的压力测试（round 8）：不看局势，每条奏疏、每个事件抉择都取首项 / 末项 ----
_EVENT_CHOICES: dict[str, list[dict]] = {}


def _choice_rows(event_id: str) -> list[dict]:
    if not _EVENT_CHOICES:
        for ev in load_pack()["events"] or []:
            _EVENT_CHOICES[ev["id"]] = list(ev.get("choices") or [])
    return _EVENT_CHOICES.get(event_id, [])


def _choice_ok(m: Any, row: dict) -> bool:
    cond = row.get("conditions")
    if not cond:
        return True
    st = getattr(m, "st", None)
    if st is not None:
        from simcore.domain.events import matches  # noqa: E402
        return matches(cond, st)
    return m.matches(cond)


def _positional(m: Any, visible: list[dict], pending: list[dict], index: int) -> Decision:
    picks = [(memo["id"], memo["options"][index]["id"]) for memo in visible if memo.get("options")]
    choices = {}
    for p in pending:
        rows = [row for row in _choice_rows(p["event_id"]) if _choice_ok(m, row)]
        if rows:
            choices[p["id"]] = rows[index]["id"]
    return picks, choices


def first(m: Any, visible: list[dict], pending: list[dict]) -> Decision:
    """每条奏疏、每个事件抉择都取第一项（多为奏疏所议之案 / 进取之策）。"""
    return _positional(m, visible, pending, 0)


def last(m: Any, visible: list[dict], pending: list[dict]) -> Decision:
    """每条奏疏、每个事件抉择都取最后一项（self04 压力局：多为最差或最消极之选）。目标：E1 < 10%、E3 < 25%。"""
    return _positional(m, visible, pending, -1)


# 消极应战：开局即留京夺镇而穷治党与（酿成兵变），战时只守不攻——只采纳守备、财计、民心类奏疏，
# 不进剿、不断粮、不招抚、不出关。目标：多为「藩镇之始·河北割据」、历史重演或失败，罕得「再造唐室」。
PASSIVE_WAR_MEMO = {
    "r_luoyang": "recruit", "r_tongguan": "hedong", "r_tongguan_jinjun": "jinjun", "r_trust": "trust",
    "r_guo": "defend", "r_shuofang_march": "defend", "r_hebei": "tongguan", "r_west": "part", "r_sortie": "hold",
    "r_flight": "west", "r_relief": "relief", "r_tax": "palace",
}
PASSIVE_WAR_POOL = {"finance", "grain", "morale", "recruit", "tongguan", "canal", "taiyuan", "suiyang"}  # 只守不攻的题目（war_pool）


def passive_war(m: Any, visible: list[dict], pending: list[dict]) -> Decision:
    picks, choices = wise(m, visible, pending)
    picks = [(mid, oid) for mid, oid in picks if mid not in ("p_summon", "p_an_capital", "p_fanyang_warn", "t17_fanyang")
             and not mid.startswith(("r_", "wp_"))]
    for memo in visible:
        mid = memo["id"]
        if mid == "p_an_in_capital":
            picks.append((mid, "detain_feng"))
        elif mid == "p_fanyang_warn":
            picks.append((mid, "purge"))
        elif mid in PASSIVE_WAR_MEMO and any(o["id"] == PASSIVE_WAR_MEMO[mid] for o in memo["options"]):
            picks.append((mid, PASSIVE_WAR_MEMO[mid]))
        elif memo.get("war_pool") in PASSIVE_WAR_POOL:
            picks.append((mid, memo["options"][0]["id"]))
    return picks, choices


POLICIES: dict[str, Callable[[Model, list, list], Decision]] = {
    "do_nothing": do_nothing, "historical": historical, "wise": wise, "half_wise": half_wise,
    "defender": defender, "purge": purge, "chaos": chaos, "bankrupt": bankrupt, "mawei_refuse": mawei_refuse,
    "detain": detain, "detain_careless": detain_careless, "detain_early": detain_early, "ops_disarm": ops_disarm,
    "first": first, "last": last, "passive_war": passive_war, "wise_cards": wise_cards,
}


# ============================================================================
# 难度档（scenario.yaml 的 difficulties，CONTRACT §1.12）。引擎后端交给引擎；model 后端由本脚本按同一约定改写剧本：
#   drift_scale {资源: 倍数}        → 该资源漂移公式整体乘以倍数
#   gravity_scale {事件 id 或 "*": 倍数} → 事件 gravity 乘以倍数（上限 1）；"*" 作用于全部事件，故只宜 ≥ 1
#   start {资源: 值}                → 开局初值
#   delay_scale                     → 诏令延误参数倍数（本脚本不模拟延误，忽略）
# ============================================================================
def difficulty_def(scenario_def: dict, diff_id: str | None) -> dict | None:
    rows = scenario_def.get("difficulties") or []
    diff_id = diff_id or scenario_def.get("default_difficulty")
    if not diff_id:
        return None
    row = next((r for r in rows if r.get("id") == diff_id), None)
    if row is None:
        raise SystemExit(f"难度不存在：{diff_id}（可选：{', '.join(r['id'] for r in rows)}）")
    return row


def apply_difficulty(scenario_def: dict, events: list[dict], diff: dict | None) -> None:
    """就地改写剧本定义与事件表。"""
    if not diff:
        return
    drift = scenario_def.setdefault("formulas", {}).setdefault("drift", {})
    for rid, factor in (diff.get("drift_scale") or {}).items():
        if rid in drift and float(factor) != 1.0:
            drift[rid] = f"({drift[rid]}) * {float(factor)}"
    gscale = diff.get("gravity_scale") or {}
    for ev in events:
        g = float(ev.get("gravity", 1))
        factor = gscale.get(ev["id"], gscale.get("*", 1.0))
        ev["gravity"] = min(1.0, g * float(factor))
    starts = diff.get("start") or {}
    for res in scenario_def.get("resources", []):
        if res["id"] in starts:
            res["initial"] = starts[res["id"]]


# ============================================================================
# 运行
# ============================================================================
def play_model(pack: dict, policy: Callable, seed: int, trace: bool = False, on_turn: Callable | None = None) -> dict[str, Any]:
    m = Model(pack, seed)
    risk_at_19 = None
    peak = m.r("rebellion_risk")
    while m.outcome is None and m.turn < 40:
        visible = m.visible_memorials()
        if on_turn:
            on_turn(m.turn, visible)
        memos, choices = policy(m, visible, list(m.pending))
        for mid, oid in memos:
            if mid == OPS:
                for op in oid:  # 玩家自拟 / 政令卡的 ops：参考模型只模拟工程（start_project），调兵、任免、军态从略
                    if op.get("op") == "start_project":
                        m._now = m.turn
                        m.try_apply(op, "政令卡")
                continue
            memo = next(x for x in m.pack["memorials"] if x["id"] == mid)
            m.adopt(memo, oid)
        for cid, oid in choices.items():
            m._now = m.turn
            m.try_apply({"op": "choose_event_option", "choice_id": cid, "option_id": oid}, "choice")
        if trace:
            print(f"T{m.turn:>2} 鼙鼓{m.r('rebellion_risk'):5.1f} 异志{m.r('an_ambition'):5.1f} 外重{m.r('fanzhen_power'):5.1f} "
                  f"朝争{m.r('court_strife'):5.1f} 君威{m.r('authority'):5.1f} 国库{m.r('treasury'):6.0f} 太仓{m.r('grain'):6.0f} "
                  f"边患{m.r('frontier_pressure'):5.1f} 民心{m.r('morale'):5.1f} 积弊{m.r('corruption'):5.1f} 奏疏{len(visible)}")
        m.resolve()
        if m.turn <= 18:
            peak = max(peak, m.r("rebellion_risk"))
        if m.turn == 19:
            risk_at_19 = m.r("rebellion_risk")
    if trace:
        for line in m.log:
            print("   ", line)
        print("结局", m.outcome)
    return {"outcome": m.outcome["id"] if m.outcome else "none", "turn": m.turn, "peak": peak,
            "risk19": risk_at_19 if risk_at_19 is not None else m.r("rebellion_risk"),
            "rebellion": bool(m.flags.get("rebellion_started"))}


# ---------------- 引擎后端 ----------------
class EngineView:
    """把引擎 WorldState 包成策略函数所需的最小接口（turn / seed / r() / armies / main）。"""

    def __init__(self, state: Any, seed: int, main: str) -> None:
        self.st, self.turn, self.seed, self.main = state, state.turn, seed, main
        self.armies = {k: {"faction": a.faction, "strength": a.strength} for k, a in state.armies.items()}

    def r(self, rid: str) -> float:
        return self.st.resources[rid].amount


_ENGINE: dict[str, Any] = {}


def engine_scenario(pack: dict, diff_id: str | None) -> tuple[dict, bool, str | None]:
    """载入引擎剧本（缓存），并按难度改写。引擎若原生支持难度（build_initial_state 有 difficulty 参数），交给引擎。"""
    sys.path.insert(0, str(ROOT / "engine" / "backend"))
    from simcore.domain import models as M  # noqa: E402
    missing = [f for f in ("pending_choices", "outcome", "counters", "flag_turns") if f not in M.WorldState.model_fields]
    if missing:
        raise SystemExit(f"引擎尚未实现 CONTRACT §1 字段：{', '.join(missing)}。请先用 --backend model。")
    import inspect  # noqa: E402
    from simcore.scenario.loader import build_initial_state, load_scenario  # noqa: E402
    key = f"scenario:{diff_id}"
    if key not in _ENGINE:
        scenario = load_scenario(PACK)
        scenario.setdefault("memorials", pack["memorials"])
        sdef = scenario.get("scenario", scenario)
        diff = difficulty_def(sdef, diff_id)
        native = "difficulty" in inspect.signature(build_initial_state).parameters
        if not native:
            scenario = copy.deepcopy(scenario)
            sdef = scenario.get("scenario", scenario)
            apply_difficulty(sdef, scenario.get("events", []), diff)
        _ENGINE[key] = (scenario, native, diff["id"] if diff else None)
    return _ENGINE[key]


def play_engine(pack: dict, policy: Callable, seed: int, trace: bool = False, on_turn: Callable | None = None,
                diff_id: str | None = None) -> dict[str, Any]:
    scenario, native, did = engine_scenario(pack, diff_id)
    from simcore.domain.apply import apply  # noqa: E402
    from simcore.domain.memorials import adopted_ops, is_visible, memorial_flag  # noqa: E402
    from simcore.domain.turn import resolve_turn  # noqa: E402
    from simcore.scenario.loader import build_initial_state  # noqa: E402

    state = build_initial_state(scenario, difficulty=did) if native and did else build_initial_state(scenario)
    rng = random.Random(seed)
    main = pack["scenario"].get("settings", {}).get("player_faction", "tang")
    risk19 = None
    peak = state.resources["rebellion_risk"].amount
    while state.outcome is None and state.turn < 40:
        visible = [mm for mm in scenario["memorials"] if is_visible(mm, state)]
        if on_turn:
            on_turn(state.turn, visible)
        pending = [{"id": p.id, "event_id": p.event_id} for p in state.pending_choices]
        memos, choices = policy(EngineView(state, seed, main), visible, pending)
        for mid, oid in memos:
            if mid == OPS:
                for op in oid:
                    try:
                        state, _ = apply(op, state)
                    except ValueError as exc:
                        if trace:
                            print(f"   T{state.turn} 拒绝 ops {op.get('op')}: {exc}")
                continue
            try:
                ops = adopted_ops(scenario, state, mid, oid)
            except ValueError as exc:  # 同季先批之条已改变局势（如许镇河北、调走守军），此条已不可处理
                if trace:
                    print(f"   T{state.turn} 跳过 {mid}: {exc}")
                continue
            for op in ops:
                try:
                    state, _ = apply(op, state)
                except ValueError as exc:
                    if trace:
                        print(f"   T{state.turn} 拒绝 {mid}/{oid} {op.get('op')}: {exc}")
            state, _ = apply({"op": "set_flag", "key": memorial_flag(mid), "value": oid}, state)
        for cid, oid in choices.items():
            try:
                state, _ = apply({"op": "choose_event_option", "choice_id": cid, "option_id": oid}, state)
            except ValueError as exc:
                if trace:
                    print(f"   T{state.turn} 抉择失败 {cid}: {exc}")
        if trace:
            g = lambda k: state.resources[k].amount  # noqa: E731
            print(f"T{state.turn:>2} 鼙鼓{g('rebellion_risk'):5.1f} 异志{g('an_ambition'):5.1f} 外重{g('fanzhen_power'):5.1f} "
                  f"朝争{g('court_strife'):5.1f} 君威{g('authority'):5.1f} 国库{g('treasury'):6.0f} 太仓{g('grain'):6.0f} "
                  f"边患{g('frontier_pressure'):5.1f} 奏疏{len(visible)} 禄山@{state.characters['an_lushan'].region}")
        state, report = resolve_turn(state, rng, scenario)
        if trace:
            for w in report.warnings:
                print("   !", w)
            if report.events_fired:
                print("   事件", report.events_fired)
        if state.turn <= 18:
            peak = max(peak, state.resources["rebellion_risk"].amount)
        if state.turn == 19:
            risk19 = state.resources["rebellion_risk"].amount
    if trace:
        print("结局", state.outcome)
    return {"outcome": state.outcome.id if state.outcome else "none", "turn": state.turn, "peak": peak,
            "risk19": risk19 if risk19 is not None else state.resources["rebellion_risk"].amount,
            "rebellion": bool(state.flags.get("rebellion_started"))}


def check_memorial_coverage(pack: dict, play: Callable, seeds: int = 30) -> dict[int, tuple[int, str]]:
    """每季可见奏疏条数的最小值（跨策略、跨种子），用于验证「每季至少 3 条」。返回 {季: (最少条数, 策略)}。"""
    worst: dict[int, tuple[int, str]] = {}
    for name, pol in POLICIES.items():
        def note(turn: int, visible: list, name: str = name) -> None:
            if turn not in worst or len(visible) < worst[turn][0]:
                worst[turn] = (len(visible), name)
        for seed in range(seeds):
            play(pack, pol, seed, on_turn=note)
    return dict(sorted(worst.items()))


def main() -> None:
    ap = argparse.ArgumentParser(description="《天宝》剧本策略平衡")
    ap.add_argument("--backend", choices=["model", "engine"], default="model")
    ap.add_argument("--policy", choices=[*POLICIES, "all"], default="all")
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--seed", type=int, default=None, help="只跑一个种子")
    ap.add_argument("--difficulty", default=None, help="难度档 id（缺省为剧本 default_difficulty）")
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--coverage", action="store_true", help="检查每季可见奏疏条数（种子数取 --seeds，缺省 30）")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    pack = load_pack()
    if args.backend == "model":
        pack = copy.deepcopy(pack)
        apply_difficulty(pack["scenario"], pack["events"], difficulty_def(pack["scenario"], args.difficulty))

        def play(pk, pol, seed, trace=False, on_turn=None):
            return play_model(pk, pol, seed, trace, on_turn)
    else:
        def play(pk, pol, seed, trace=False, on_turn=None):
            return play_engine(pk, pol, seed, trace, on_turn, diff_id=args.difficulty)
    if args.coverage:
        cov = check_memorial_coverage(pack, play, seeds=args.seeds if args.seeds != 200 else 30)
        print(f"每季最少可见奏疏条数（后端 {args.backend}）：", {k: v[0] for k, v in cov.items()})
        low = {k: v for k, v in cov.items() if v[0] < 3}
        print("不足 3 条：", low or "无")
        return
    names = list(POLICIES) if args.policy == "all" else [args.policy]
    seeds = [args.seed] if args.seed is not None else list(range(args.seeds))
    for name in names:
        results = [play(pack, POLICIES[name], s, args.trace) for s in seeds]
        dist = Counter(r["outcome"] for r in results)
        risks = [r["risk19"] for r in results]
        peaks = [r["peak"] for r in results]
        rebel = sum(r["rebellion"] for r in results)
        print(f"\n== {name}（{len(seeds)} 局，后端 {args.backend}，难度 {args.difficulty or '默认'}）")
        for k, v in dist.most_common():
            print(f"   {k:<18} {v:>4}  {v / len(seeds):6.1%}")
        e1 = sum(v for k, v in dist.items() if k.startswith("e1_"))
        print(f"   E1 类合计           {e1:>4}  {e1 / len(seeds):6.1%}")
        print(f"   起兵 {rebel / len(seeds):.0%}；T19 鼙鼓 均值 {statistics.mean(risks):.1f}，"
              f"中位 {statistics.median(risks):.1f}，范围 {min(risks):.1f}–{max(risks):.1f}；"
              f"T1–T18 峰值 均值 {statistics.mean(peaks):.1f}")


if __name__ == "__main__":
    main()
