# 《天宝》接口契约 v1

本文件是引擎（`engine/` 子模块，即 llm-sim-game-template）、剧本（`scenarios/tianbao_751/`）、前端（`app/`）、桌面壳（`desktop/`）、MCP 接入四部分之间的约定。改动契约须先改本文件。

通用原则：
- 引擎是唯一事实来源。LLM（包括客户端模型）只能提议 StateOp，由规则层校验后执行。
- 叙事只能使用已执行的事实。
- 所有随机都用种子 RNG。
- 所有文本文件 UTF-8（无 BOM），所有 JSON 响应 `ensure_ascii=False` 且 `Content-Type` 带 `charset=utf-8`。

## 1. 引擎扩展（写在 engine/，保持场景无关）

### 1.1 WorldState 新字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `counters` | `dict[str,int]` | 计数器 |
| `flag_turns` | `dict[str,int]` | 每个 flag 最近一次被设置的回合，用于 `flag_age` |
| `pending_choices` | `list[PendingChoice]` | `{id, event_id, title, text, options:[{id,text,effects,conditions?}], default_option, created_turn, deadline_turn}` |
| `outcome` | `Outcome \| None` | `{kind: "ending"\|"fail", id, title, text, turn}`。非空即终局：推进回合返回 409，可读不可写（rewind/fork 除外） |
| `rules` | `dict[str,Any]` | 从 scenario.settings 拷入的规则参数，例如 `max_concurrent_offices`（默认 1）。引擎另写入：`turn_unit`（剧本 turn_unit，行程文字「约 n 季」用；可用 `turn_unit_label` 覆盖）、`difficulty`（见 1.12）。可选 settings：`ruler_title`（诏书记忆里的称谓，默认「陛下」）、`bloc_names: {bloc: 显示名}`（廷议理由里的派系名，未配置时只说「本派」，不暴露 id）、`bloc_interests`（见 2 的廷议） |

### 1.2 实体新字段

| 实体 | 新字段 |
|---|---|
| `Character` | `offices: list[str]`（全部兼职）；`office` 保留为主职，二者由 apply 同步维护；`bloc: str \| None`；`title: str = ""` |
| `Army` | `commander: str \| None`、`loyal_to: str \| None`、`quality: float = 1.0` |
| `Region` | `controller: str \| None`（势力 id，默认为场景主势力） |
| `Resource` | `hidden: bool = False`、`estimate_width: float = 0`（公开视图中的区间半宽基数） |
| `Character` / `Army` | `in_transit: {to_region, eta_turn, from_region, route: [起点…终点]}`（route 为整段路径，见 1.3） |
| `PendingClause` | `label: str = ""`：来源说明（奏疏标题、「诏令」），延期执行时作为事实原因 |
| `Fact` | `cause: str \| None`：原因（op 的 `reason`，否则为来源：奏疏标题 / 事件标题 / 抉择标题 / 「X竣工」/ 「常设令：X」/ 延期包 label） |

### 1.3 新 StateOp

| op | 字段 | 校验要点 |
|---|---|---|
| `adjust_army` | `army, delta, reason` | 兵力下限为 0 |
| `set_army_faction` | `army, faction` | 势力必须存在 |
| `set_army_commander` | `army, character \| null` | 人物须在世 |
| `adjust_trait` | `character, trait, delta` | 人物须存在 |
| `adjust_counter` | `key, delta` | — |
| `set_counter` | `key, value` | — |
| `set_region_controller` | `region, faction` | — |
| `choose_event_option` | `choice_id, option_id` | 选项须存在且其 conditions 满足；执行 effects 后移除该 pending choice |

已有 op 的行为调整：
- `appoint`：当 `len(offices) >= rules.max_concurrent_offices` 时返回 `OFFICE_HELD`；任命追加到 `offices`；`office` 为空时设为主职。
- `dismiss`：从 `offices` 移除，并重设主职。
- `set_character_status`：非 alive 时清空全部官职、军队统帅身份和在途状态。
- `move_character` / `move_army`：目标可以不相邻。引擎按邻接表寻最短路（总行程回合最少；同样短时优先途经行进者本方控制的地区，再取途经最少、id 序最小者），整段作为一次行程出发，`eta_turn = 当前回合 + 各段之和`，途中不可再调动。事实文字「X自A启程赴Y（经Z，约n季）」。目标即所在地 → `INVALID_TARGET`；无路可达 → `OUT_OF_RANGE`。
- `set_army_commander` 且 `character: null`：事实与摘要写「罢X统帅」。

事实文本（`apply(op, state, source=...)`）：
- 数值型事实写变化量与原因：`国库 −40（遣中使察看范阳）`、`京畿防务 +5（修城竣工）`、`李相与安节度关系 −20`；原因见 1.2 的 `Fact.cause`。`fact_line` 再附「（前→后）」。
- 隐藏资源的公开文本为「X有所变动（原因；数值不明）」。

诏书记忆：确认诏书时，`appoint` / `dismiss` / `set_character_status`（系狱、流放、致仕、赦免；赐死不写）的当事人自动得到一条记忆，如「天宝十载春，陛下任哥舒翰为河东节度使」；延期条款在下季执行成功时再写。

### 1.4 条件 DSL 扩展（`events.matches`）

所有比较都支持 `operator: eq|gt|gte|lt|lte`，未写默认 `eq`。

| kind | 字段 |
|---|---|
| `turn` | `value`（可带 operator） |
| `resource` | 已有 |
| `flag` | 已有；另支持 `operator: exists\|absent` |
| `flag_age` | `key, operator, value` |
| `counter` | `key, operator, value` |
| `region_stat` | 已有 |
| `region_controller` | `region, faction` |
| `character_status` | `character, value` |
| `character_trait` | `character, trait, operator, value` |
| `character_region` | `character, region` |
| `office_holder` | `office, character`（`character: null` 表示出缺） |
| `army_strength` | `army` 或 `faction`（取总和），`operator, value` |
| `relation` | `a, b, operator, value` |

`turn` 指正在结算进入的回合；在回合外调用时，指当前回合。

### 1.5 事件

字段：

| 字段 | 说明 |
|---|---|
| `id`, `title` | — |
| `text` | 给奏疏和弹窗用的正文 |
| `when`, `conditions`, `gravity` | 已有 |
| `effects` | 立即执行 |
| `choices` | 选项列表 |
| `default_choice` | 默认选项 id |
| `choice_deadline` | 默认 1 季 |
| `repeatable` | 默认 false |
| `cooldown` | 回合数 |
| `illustration` | 资产 id |

选项可带 `memory: {character, text}`（或其列表）：选中时追加为 `remember` op（人物须存在，validate 检查）。

- 带 `choices` 的事件触发时生成一个 PendingChoice。
- 到期仍未选择，就在下一次结算开头执行 `default_choice`，并写入 fact。

### 1.6 回合结算顺序（`resolve_turn`）

1. 到期的 PendingChoice 执行默认项。
2. 延期条款。
3. 常设命令。
4. 账目。
5. 收入：`formulas.income` 的每个键都是 `{resource, formula, per_region: true}`。
6. 工程。
7. 移动抵达。
8. 战斗（见 1.7）。
9. 漂移（乘难度 `drift_scale`）。
10. 事件（概率 = min(1, gravity × 难度 `gravity_scale`)）。
11. 计数器规则：scenario `counters: [{id, conditions, mode: streak|count}]`。`streak` 在条件不满足时归零。
12. 结局判定（见 1.8）。
13. 历法。

`TurnReport` 新增：
- `battles: list`
- `choices_opened: list`
- `outcome: Outcome | None`
- `crisis: dict`：由场景 `crisis` 定义，含各分项贡献

### 1.7 最小战斗与 AI 行军

**战斗**：同一区域内，`faction` 互为敌对（relation < 0 或场景 `wars` 列表）的军队交战。

- 战力 = `strength × quality × (1 + 守方区域 defense/100)`（仅守方享有防务加成）× RNG(0.85, 1.15)。
- 败方损失 30%，并退往相邻的己方控制区；无处可退则溃散。胜方损失 10%。
- 区域 `defense ≥ 80` 时，攻方需要 2 倍战力才能胜，否则相持一季。
- 攻方获胜且该区域无守军时，`controller` 变更。

**AI 行军**：scenario `ai_routes: [{faction, route: [region...], hold_if_outnumbered: true}]`。每季，该势力不在途的军队沿 route 前进一格。

### 1.8 结局

scenario.yaml 中声明：

```yaml
endings:
  - {id, kind: ending|fail, title, text, priority, conditions}
game_length: {last_turn: 19, overtime_flag: rebellion_started, overtime_last_turn: 23, fallback_ending: open_storm}
```

每季结算末尾，按 priority 从小到大判定，命中第一个即写入 `outcome`。到达 `last_turn` 时（若 overtime_flag 为真，则到 overtime_last_turn）仍无命中，就使用 `fallback_ending`。

### 1.9 隐藏数值与公开视图

`public_view(state, seed)` 返回的状态中，`hidden` 资源替换为 `{id, name, hidden: true, estimate: [lo, hi]}`。

- 区间半宽 = `estimate_width × (1 + corruption/100)`，flag `intel:<resource>` 存在时减半。
- 区间中心带 ±半宽/2 的种子噪声，同一回合内稳定。
- API 的 `/view` 和 MCP 的所有工具只能用公开视图。完整状态只在 `/state?debug=1` 中提供，且仅当设置 `SIM_DEBUG=1` 时可用。

### 1.10 奏疏条目（memorials）

剧本文件 `memorials.yaml`：

```yaml
- id: t0_hedong
  turn: 0              # 或 conditions；可带 expires_after: n
  title: 河东节度出缺
  summary: ...
  region: hedong
  advisors: [{character: li_linfu, stance: support|oppose|neutral, line: "..."}]
  options:
    - {id: deny, label: 驳回，另择留后, ops: [...], hint: "外重内轻 −3"}
```

- 当回合可见条件：`turn` 匹配，或 `conditions` 满足，且未被处理。
- 采纳某个选项，就把它的 ops 加入诏书草案；确认诏书后写入 flag `memorial:<id>` = option_id。
- 选项可带 `memory: {character, text}`（或其列表），采纳时作为 `remember` op 随选项一同执行（同组延期）。条目可带 `keywords`，供廷议议题匹配。
- 条款事实的原因为奏疏标题（op 自带 reason 时用 reason）。
- 选项摘要（`ops_summary`、回执 `summary`）不出现 None：隐藏资源只写方向「禄山异志 ↓（风闻）」，隐藏心态写「心态有变（不明）」。

### 1.11 危机计

scenario.yaml：

```yaml
crisis: {resource: rebellion_risk, title: 渔阳鼙鼓, bands: [{max: 39, name: 承平}, ...], terms: [{id, label, expr}]}
```

`terms` 与 drift 公式中的分项一一对应。每季在报告里给出各分项的数值。

### 1.12 难度档

scenario.yaml：

```yaml
difficulties:
  - {id: normal, label: 常例, description: ...}
  - {id: hard, label: 多事之秋, description: ..., drift_scale: {rebellion_risk: 1.5}, gravity_scale: {"*": 1.2, some_event: 1}, start: {treasury: 2500}, delay_scale: 1.5}
default_difficulty: normal
```

- `drift_scale`：资源漂移量乘数（键为资源 id 或 `*`）；`gravity_scale`：事件概率乘数（事件 id 优先，其次 `*`；结果截到 1）；`start`：开局资源值（按上下限截断）；`delay_scale`：诏令延期概率乘数。缺省均为 1。
- 开局时（`new_game` / `POST /sessions` 的 `difficulty`，缺省 `default_difficulty`，再缺省第一档）写入 `WorldState.rules.difficulty = {id, label, description, drift_scale, gravity_scale, delay_scale}` 与存档头 `difficulty`；结算只读 `rules`。未知 id → `UNKNOWN_DIFFICULTY`（422）；场景没有 difficulties 却指定了难度也报此错。
- `validate_scenario` 检查：id 唯一、label 必填、资源 / 事件引用存在、系数为非负数、`default_difficulty` 在列表中。

### 1.13 存档与快照

- 存档是 JSONL（紧凑 JSON，键按写入顺序）。头部：`{type: session, scenario, scenario_folder, seed, scenario_version, scenario_hash, difficulty, initial_state, ...}`；`scenario_hash` 为剧本全部 YAML 解析内容的 sha256。
- 每个 `turn` 条目带 `snapshot`（结算后的完整 WorldState）。读档从路径上最近的快照起步，只重放其后的 op / pending 条目（这些不依赖剧本），所以剧本改动不会追溯改变已结算的回合；旧存档没有快照时从开局重放。
- 当前剧本哈希与存档头不同时，`/view` 返回 `scenario_changed: {saved_version, current_version, saved_hash, current_hash, message}` 并在 `warnings` 中列出 `{code: "scenario_changed", ...}`；MCP `briefing` 显示同样的提示。此后的回合按当前剧本结算。
- `sim replay <session>` 是校验工具：用当前剧本从开局完整重放，逐回合比对存档中的 `state_hash`，输出 `{ok, turns_checked, divergences: [{entry_id, turn, expected, actual}], final_hash, scenario_changed}`，有分歧时退出码 1；不修改存档。

## 2. REST API（engine/backend/api，前缀 /api）

已有接口保持不变，新增或调整的如下。所有响应均为 JSON（UTF-8），错误统一为 `{"detail": {"code": "...", "message": "中文说明"}}`。

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/scenarios` | 每项另含 `difficulties: [{id, label, description, default}]`、`default_difficulty` |
| POST | `/sessions` | body `{scenario, seed, difficulty?}` → `{id, scenario, difficulty: {id,label,description} \| null, state}` |
| GET | `/sessions/{id}/view` | 前端主数据：`{state: public_view, calendar_label, objectives: [{id,title,status,detail}], crisis: {value_or_estimate, band, terms: [{label, value}]}, memorials: [...], pending_choices: [...], outcome, last_report, can_advance, difficulty: {id,label,description} \| null, scenario_changed: {...} \| null, warnings: [{code, message, ...}]}`（见 1.13） |
| POST | `/sessions/{id}/edicts/draft` | body `{sections: {category: text}, adopted: [{memorial_id, option_id}], ops: [...]}`。ops 用于客户端模型模式。回执中每一条 clause 都带 `source: memorial\|text\|client` |
| POST | `/sessions/{id}/edicts/{edict_id}/confirm` | 已有，补写 memorial flag |
| POST | `/sessions/{id}/choices/{choice_id}` | body `{option_id}` → 执行 `choose_event_option` |
| POST | `/sessions/{id}/turn` | 已有。返回 `{state: public_view, report, memorial(纪事), outcome}`；已终局时返回 409 `GAME_OVER` |
| POST | `/sessions/{id}/debate` | body `{topic, participants: [id], memorial_id?}` → `{topic, memorial: {id,title} \| null, topic_entities: [{kind, id, name}], speeches: [{character, stance, reason, text}], summary}`。立场见下；台词由 LLM 写（Mock 用模板）。给了 memorial_id 时 topic 可空（取奏疏标题）；memorial_id 不存在 → `UNKNOWN_MEMORIAL` |
| GET / POST | `/sessions/{id}/advice` | 谏言库，记入日志的 `advice` 事件，不进入状态哈希。POST body `{character, text, source}` |
| POST | `/sessions/{id}/chat/{character}` | 已有 SSE。新增的提示词装配：人设 + 事实摘要（StateDigest）+ 该人物记忆 |
| GET | `/sessions/{id}/history` | 时间线：`[{id, type, turn, label, parentId}]` |
| POST | `/sessions/{id}/rewind` | body `{entry_id}` |
| DELETE | `/sessions/{id}` | 删除存档 |
| GET | `/health` | `{ok, version, scenarios}`，给桌面壳探活用 |

廷议立场（确定性），按优先级：
1. 议题对应奏疏（`memorial_id`，或当季可见奏疏中标题互含 / `keywords` 命中 / 标题二字组被议题覆盖 ≥ 50%）：该奏疏 `advisors` 中的人用奏疏立场。
2. 场景 `debate_topics` 的人物 / 派系立场表。
3. 议题按显示名点到的实体（`topic_entities`：人物、势力、官职、地区、军队）：本人或本人官职/所统军队/驻地被点名 → 按议题褒贬（罢、削… / 授、加…）维护自身；否则累计亲疏（人物关系、同派 +50、官职在任者、军队统帅、本方势力 +40、势力关系）与派系利益 `bloc_interests: {bloc: {实体 id 或关键词: 权重}}`，|合计| ≥ 20 时定立场（议题无褒贬时按「为其请命」处理）。
4. 忠诚 ≥ 8 赞成、≤ 3 反对。
5. 其余以种子决断（同局、同季、同议题稳定；多半持中）。

`StateDigest(character_id | None)`：引擎渲染的事实摘要，固定格式的中文文本。内容是这个人能知道的资源（隐藏资源给区间）、官职、在任者、地区要点、进行中的工程和常设令、本季已发生的事实。它供 LLM 提示词和 MCP 使用。
- 非玩家势力控制的地区列在【外域】，只给控制者与驻军，不给经济指标。
- 给定人物时按相关性筛地区：所在 → 统兵所在 → `knowledge` 中写到的地区 → 行程目的地 → 相邻，这些给全部指标；其余地区压成一行【他处】名单（按控制者分组）；另附【记忆】（最近 12 条）。

## 3. MCP 服务（engine/backend/simcore/mcp/，命令 `sim mcp`，stdio）

- 用官方 Python `mcp` SDK（FastMCP）。
- 存档目录与桌面应用相同：`LLM_SIM_HOME`，桌面版默认 `%APPDATA%/tianbao`。
- 模式由环境变量 `SIM_MCP_MODE` 指定：
  - `client`（默认）：调用方模型负责扮演和解释诏令。
  - `server`：由服务端配置的 provider 负责。

| 工具 | 入参 | 返回 |
|---|---|---|
| `list_scenarios` | — | 场景列表 |
| `new_game` | `scenario, seed, difficulty?` | session_id 与开局简报（含难度行）；`list_scenarios` 列出各场景的 difficulties |
| `list_saves` / `load_game` | `session_id` | — |
| `briefing` | `session_id` | 历法、难度、`scenario_changed` 提示（若有）、三目标、公开资源、危机计及分项、奏疏条目（含选项与 ops 摘要）、待决事件、上季事实。末尾附**扮演规则**：数字只能引用简报里的值 |
| `op_reference` | `session_id` | 全部 StateOp 的 JSON Schema 与当前可用的实体 id 表 |
| `audience` | `session_id, character` | 人设卡 + 该人物可知的 StateDigest（含【记忆】）+ 口吻要求。由调用方模型扮演；死人或在押者返回拒绝 |
| `court_debate` | `session_id, participants, topic?, memorial_id?` | 对应奏疏、「议题涉及」实体、引擎给出的各人立场 + 人设，调用方据此写辩论 |
| `save_advice` | `session_id, character, text` | — |
| `draft_edict` | `session_id, sections?, adopted?, ops?` | 回执：逐条显示 applied / rejected（原因）/ delayed |
| `confirm_edict` | `session_id, edict_id` | 确认后的回执 |
| `choose` | `session_id, choice_id, option_id` | — |
| `end_turn` | `session_id` | TurnReport：事实（逐条去重，不含「终局」行）、账目合计（一次）、战斗、事件、危机分项、outcome（末尾「终局」段只出现一次）。client 模式不再附与事实重复的「纪事」 |
| `history` / `rewind` | — | — |

工具的错误一律返回中文说明和错误码，不抛出堆栈。

## 4. 前端（app/）

- React 18 + Vite + TypeScript + Framer Motion。
- 所有文字由 DOM 渲染，图片资产一律不含文字。
- 字体：打包霞鹜文楷（标题）与思源宋体（正文）子集，覆盖 GB2312 一级、二级字和剧本用到的全部字符。后备字体链为 `"Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", serif`。
- API 地址：桌面版通过 Tauri 命令 `get_api_base` 获取；开发模式从 `VITE_API_BASE` 读取，默认 `http://127.0.0.1:8765`。
- 每个可交互元素都带 `data-testid`，命名为 `<screen>.<element>`，供 E2E 测试和按钮清单使用。
- 界面清单：

  | 界面 | 内容 |
  |---|---|
  | `title` | 标题页 |
  | `newgame` | 新开局 |
  | `desk` | 主界面：A 平铺舆图 + B 势力绸带与危机计 |
  | `resources` | 资源栏悬浮明细 |
  | `map` | 舆图图层 |
  | `memorial` | 奏疏 |
  | `audience` | 召对 |
  | `debate` | 廷议 |
  | `edict` | 诏书 |
  | `result` | 推演结果卷 |
  | `choice` | 事件抉择 |
  | `ending` | 结局 |
  | `timeline` | 存档时间线 |
  | `settings` | 设置 |

## 5. 桌面壳（desktop/）

- Tauri 2。sidecar 是用 PyInstaller 打包的 `tianbao-server.exe`，入口为 `sim serve --port <空闲端口>`。
- 环境变量：
  - `SIM_SCENARIOS_DIR`：指向打包进安装包的 scenarios 目录。
  - `LLM_SIM_HOME`：`%APPDATA%/tianbao`。
- 启动后轮询 `/health`；应用退出时结束 sidecar 进程。
- 安装包用 NSIS。

## 6. 测试与门禁

| 门禁 | 内容 |
|---|---|
| G1 | Playwright 按 `data-testid` 清单逐个点击，每个按钮都要有可断言的效果；控制台 0 错误 |
| G2 | 引擎 pytest；场景测试包括不变量检查、1000 种子模拟和结局可达性 |
| G3 | API 契约测试、仿 OpenAI 服务器测试、MCP 工具测试 |
| G4 | 乱码扫描：DOM、日志、存档中不允许出现 `�`、`锟斤拷`，以及 `Ã` `å` `æ` `ç` `è` 后跟 0x80–0xBF 字节的典型 mojibake；静态文案和剧本文字必须 100% 被打包字体覆盖 |
| G5 / G6 | 自玩与 GPT 玩的日志存入 `playtests/` |
