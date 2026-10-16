# 《天宝》接口契约 v1

本文件是引擎（`engine/` 子模块，即 llm-sim-game-template）、剧本（`scenarios/tianbao_751/`）、前端（`app/`）、桌面壳（`desktop/`）、MCP 接入四部分之间的约定。改动契约须先改本文件。

通用原则：
- 引擎是唯一事实来源。LLM（包括客户端模型）只能提议 StateOp，由规则层校验后执行；玩家（客户端模型、诏令文本解释）只能提议政策级操作（见 1.3.1）。
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
| `outcome` | `Outcome \| None` | `{kind: "ending"\|"fail", id, title, text, turn, satisfied: [str]}`。`satisfied` 为判定命中的条件（中文，见 1.8）。非空即终局：推进回合返回 409，可读不可写（rewind/fork 除外） |
| `rules` | `dict[str,Any]` | 从 scenario.settings 拷入的规则参数，例如 `max_concurrent_offices`（默认 1）。引擎另写入：`turn_unit`（剧本 turn_unit，行程文字「约 n 季」用；可用 `turn_unit_label` 覆盖）、`difficulty`（见 1.12）。可选 settings：`ruler_title`（诏书记忆里的称谓，默认「陛下」）、`bloc_names: {bloc: 显示名}`（廷议理由里的派系名，未配置时只说「本派」，不暴露 id）、`bloc_interests`（见 2 的廷议）、`player_ops`（见 1.3.1）、`intel_min_width`（见 1.9）、`flag_labels` / `counter_labels: {键: 显示名}`（结局条件与复盘里的旗标、计数器名，缺省用键名）、`player_project_max_gain`（默认 10）/ `player_project_cost_per_point`（默认 10）（见 1.3.1）、`capital_region`（无玩家人物时的「御前」所在，见 3 的 audience）。引擎另由剧本 offices 的 `army` / `seat` 生成 `office_postings: {office: {army?, seat?}}`（见 1.2） |

### 1.2 实体新字段

| 实体 | 新字段 |
|---|---|
| `Character` | `offices: list[str]`（全部兼职）；`office` 保留为主职，二者由 apply 同步维护；`bloc: str \| None`；`title: str = ""` |
| `Army` | `commander: str \| None`、`loyal_to: str \| None`、`quality: float = 1.0` |
| `Region` | `controller: str \| None`（势力 id，默认为场景主势力） |
| `Resource` | `hidden: bool = False`、`estimate_width: float = 0`（公开视图中的区间半宽基数） |
| `Character` / `Army` | `in_transit: {to_region, eta_turn, from_region, route: [起点…终点]}`（route 为整段路径，见 1.3） |
| `PendingClause` | `label: str = ""`：来源说明（奏疏标题、「诏令」），延期执行时作为事实原因 |
| `LedgerEntry` | `cancellable: bool = True`：false 时玩家不能 `cancel_ledger`（剧本 / 事件设的既定开支）；`add_ledger` 同名字段 |
| 剧本 `scenario.yaml` 的 `ledger` | 可选，开局即有的经常账目：`[{id?, name, category, amount, kind: recurring\|one_off = recurring, turns?, reason?, cancellable = false}]`。`build_initial_state` 写入 `WorldState.ledger`（T0 起可见于 op_reference / 前端账目，T0→T1 结算第 4 步即计入经常收支）；id 缺省按引擎序号 `ledger-xxxxxxxx`；剧本定额缺省不可撤销。`validate_scenario` 检查键、资源、数值、kind、turns、id 重复 |
| `Fact` | `cause: str \| None`：原因（op 的 `reason`，否则为来源：奏疏标题 / 事件标题 / 抉择标题 / 「X竣工」/ 「常设令：X」/ 延期包 label） |
| 剧本 `offices[]` | 可选 `army`（此职所统军队 id：任命即兼统该军，免职即罢其统帅）、`seat`（任所地区 id；未写时取所统军队的驻地）。二者都未写的为京官 / 虚衔，任命不涉行程。开局写入 `rules.office_postings`（`Office` 模型本身不变，旧存档状态哈希不变）；`validate_scenario` 检查军队与地区存在 |
| `LedgerLine` | `group: str = ""`：经常收支明细的归类名（收入公式的 label、账目名、「X施工」、「X漂移」、养兵「X（兵 N，每 P 兵 A）」） |

**地区指标量程**（第 8 轮）：剧本 `scenario.stats: [{id, name, range: [下限, 上限]}]`。开局拷入 `rules.stat_ranges`；开局值与一切 `adjust_region` 都截入范围，截到边时事实写「河北治安 +2（已至上限 100，原拟 +6）」，`before/after` 为实际值。`range` 不是两个数或下限 > 上限时 `validate_scenario` 报错。briefing 国势段末列「地区指标量程：繁荣 0–100、治安 0–100……」。旧存档（rules 无 stat_ranges）不截。

### 1.3 新 StateOp

| op | 字段 | 校验要点 |
|---|---|---|
| `adjust_army` | `army, delta, reason` | 兵力下限为 0 |
| `set_army_faction` | `army, faction` | 势力必须存在 |
| `set_character_faction` | `character, faction` | 人物、势力必须存在（剧本层；如兵变首领随叛军改属叛方）。事实 `kind: character_faction`「史思明改属大燕」 |
| `set_army_commander` | `army, character \| null` | 人物须在世 |
| `adjust_trait` | `character, trait, delta` | 人物须存在 |
| `adjust_counter` | `key, delta` | — |
| `set_counter` | `key, value` | — |
| `set_region_controller` | `region, faction` | — |
| `choose_event_option` | `choice_id, option_id` | 选项须存在且其 conditions 满足；执行 effects 后移除该 pending choice |
| `march` | `army, to_region, with_commander = true` | 同 `move_army`；军队与同驻一地的统帅作为同一行程出发（事实「X自A出征，赴B（…），统帅某某随军」） |
| `detach` | `army, strength, to_region, new_army_name?, commander?` | 分兵：0 < strength < 原军现有兵力（全军调动用 `move_army`，否则 `INVALID_TARGET`）；原军不在途；有路可达（`OUT_OF_RANGE`）；commander 须在世。新军 id `原军id_d序号`、名缺省「原军名偏师」（重名加序号），同势力 / 素质 / loyal_to；去向与原驻地不同则整段出发（同 move_army 寻路），相同则就地分屯。commander 与原军同驻者随新军同行（其原统之军按下文任命规则处置），否则启程赴任；不写则暂无主帅。事实「禁军分兵 5000（留 15000），编为禁军前锋，自京畿开拔，赴雄关（约1季），由高内侍统领随行」 |

已有 op 的行为调整：
- `appoint`：当 `len(offices) >= rules.max_concurrent_offices` 时返回 `OFFICE_HELD`；任命追加到 `offices`；`office` 为空时设为主职。
- `dismiss`：从 `offices` 移除，并重设主职。
- `set_character_status`：非 alive 时清空全部官职、军队统帅身份和在途状态。
- `move_character` / `move_army`：目标可以不相邻。引擎按邻接表寻最短路（总行程回合最少；同样短时优先途经行进者本方控制的地区，再取途经最少、id 序最小者），整段作为一次行程出发，`eta_turn = 当前回合 + 各段之和`，途中不可再调动。事实文字「X自A启程赴Y（经Z，约n季）」。目标即所在地 → `INVALID_TARGET`；无路可达 → `OUT_OF_RANGE`。
- `set_army_commander` 且 `character: null`：事实与摘要写「罢X统帅」。
- `move_army` 新增 `with_commander = true`：统帅与军队同驻一地且不在途时随军同行（复制同一 `in_transit`，同时抵达）；`false` 则留驻。剧本 `ai_routes` 的行军同样带上同驻的统帅。
- **任命只有一条规则**（`set_army_commander` 与 `appoint` 有任所的官职）：op 带 `dispatch: bool = false`。玩家层提议（客户端 ops、诏令文本解释）未写 `dispatch` 时按 `true` 处理；剧本层（奏疏选项、事件效果、抉择）按其写明的值，缺省 `false`。判定由 `rules.posting_plan` 给出，回执摘要（`summarize_op`）、事实文本与 op_reference 的说明用同一套措辞：
  - 已在任所 / 军中：「人在军中，即日视事」（官职为「人在任所，即日视事」）；
  - 已在赴任途中：「已在赴任途中（自A赴B，约n季后到），由副将暂摄」；
  - `dispatch: true` 且有路：启程赴任，事实「X军易帅，由某某统领；已启程赴任（自A经B、C，约n季抵D），到任前由副将暂摄」；
  - **人离军而去，原统之军随之解除**（`rules.left_behind_armies`）：此人原统、与其同驻且不在途的军队，`army.commander` 真正置空，事实 / 回执附「；其原统Y军不再由其统领（暂无主帅，副将摄事）」；唯该军是他仍担任的官职所统（offices 的 `army`），官在军在，仍由其兼统，附「；仍兼统Y军（人不在军中，副将暂摄）」。此人另统而不在身边的军队（遥领）照旧兼统，回执同样写出「；仍兼领Z军（不在军中，副将暂摄）」（遥领、不赴任时亦然），回执所列即状态中此人所统的全部军队。剧本写 `appoint` + `dispatch: true`（带 army 的官职）即一条完整回执：「某某任X，兼统X军；已启程赴任（…），到任前由副将暂摄；其原统…」。回执、状态、command_table、StateDigest 一致（digest 中离军他往者写「统帅某某离军他往（自A赴B…），副将暂摄」，赴本军者才写「未到任」）；
  - 否则遥领：「遥领，不赴任（今在A），由副将暂摄」（在途他往写「正在途中：…」，无路写「无路可达D」）。
  - `appoint` 带 `army` 的官职：同时 `army.commander = 此人`（事实「某某任X节度使，兼统X军；…」）；`dismiss` 时若此人正统该军则罢其统帅（「，罢统X军」）。
  - **同组合并**（`rules.coalesce_postings`）：同一奏疏选项（`adopted_ops`、选项 `ops_summary`）、事件抉择效果、事件效果里，`appoint` 带 army 的官职（dispatch 缺省 / false）之后又有 `set_army_commander` 令同一人统该军且 `dispatch: true` → 合并为一条 `appoint` + `dispatch: true`（「某某任X，兼统X军；已启程赴任（…）」），删去多余的易帅条，不再先说「遥领，不赴任」又说「已启程赴任」。`set_army_commander` 的新统帅与原统帅为同一人且已在军中 / 赴任途中时，事实为 internal（不重复）。
- 统帅在军判定（`rules.commander_presence`）：统帅与军队同驻一地，或二者同一行程。不在军中时战斗照常结算（战力公式不变），战报 `battles[].commanders: {army: {name, present, note}}`，并追加事实 `kind: "command"`：「X军：主帅某某赴任中（自A赴B，约n季后到），由副将暂摄」。
- 在途者（人物、军队）不能再调动：`move_character` 目的地与当前行程相同 → `INVALID_TARGET`「已在途中…，无须再下令」；否则 `CHARACTER_UNAVAILABLE`，说明带行程。
- 行程显示（`rules.travel_note`）：「自A赴B，约n季后到」（到期当季写「即将抵达」）。简报「在途」段、可召对名单、StateDigest 的【本人】【军队】【在途】、op_reference 均用此格式：「高仙芝（自河西赴范阳，约2季后到）」。

#### 1.3.1 玩家操作分层（`domain/permissions.py`）

| 层 | 来源 | 可用操作 |
|---|---|---|
| 剧本层 | 奏疏选项（adopted）、事件效果、事件抉择（choose）、工程竣工、常设令执行、存档重放 | 全部 StateOp |
| 玩家层 | `draft_edict` 的 `ops`（MCP / REST / 前端客户端模型模式）与诏令文本经 LLM 解释得到的 ops | 默认白名单：`appoint`、`dismiss`、`move_character`、`move_army`、`march`、`detach`、`set_army_commander`、`start_project`、`add_standing_order`、`cancel_standing_order`、`cancel_ledger`、`remember`、`set_character_status` |

- 不在白名单的操作（`adjust_resource`、`adjust_region`、`adjust_relation`、`adjust_army`、`adjust_trait`、`set_flag`、`adjust_counter`、`set_counter`、`set_region_controller`、`set_army_faction`、`set_character_faction`、`add_ledger`、`choose_event_option`）在回执中为 `rejected`，`code: "OP_NOT_PERMITTED"`，`reason` 为中文说明（含操作名与正确途径）。
- 白名单内另有限制（同样 `OP_NOT_PERMITTED`）：
  - 人物、军队须属玩家势力（`rules.player_faction`）；不能调遣、分兵、任帅他方军队，不能以他方人物为帅（`detach` 的 commander 同）。
  - `set_character_status` 只能用 `imprisoned` / `exiled` / `retired`（赐死、赦免须经奏疏或事件），对象不能是君主本人，须为本朝臣属或身在本朝控制之地。
  - `set_character_status` 另以 `code: "HOSTILE_TARGET"` 拒绝：对象属与玩家势力敌对的势力（关系 < 0 或同在 wars 中），或统领敌对势力的军队；
    `imprisoned`（拘拿）与 `dead` 还要求对象身在玩家势力控制的地区（无主地区不限），且当地没有（不在途的）敌军——敌军在场即视为护卫。
    延期执行的处置条款在结算时按同样规则复核，不满足则不执行并记入 warnings。
  - `start_project`：地区须为本方控制；每季花费须为正；`on_complete` 只能是本地区的 `adjust_region`（每项 0 < delta ≤ `player_project_max_gain`，且 增益合计 × `player_project_cost_per_point` ≤ 总花费）或其他玩家层操作。
  - `add_standing_order` 所含 ops 同样按玩家层检查；`cancel_ledger` 不能撤销 `cancellable: false` 的账目。
- 剧本 `settings.player_ops`：列表 = 整体替换白名单；`{allow: [...], deny: [...], statuses: [...]}` = 追加 / 移除 / 指定可用处置（加 `dead` 即允许赐死）。`validate_scenario` 检查操作名与状态名。
- 确认诏书时重新校验，客户端 / 文本条款仍按玩家层。

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
| `army_commander` | `army, character \| null, operator: eq\|ne`（`null` = 无统帅；统帅已不在世视同无统帅）。用于奏疏文本防过时：如「禁军久无宿将」只在 `{kind: army_commander, army: jinjun, character: null}` 时出现 |
| `army_region` | `army, region, operator: eq\|ne`（驻地；在途军队仍算出发地，抵达那一季结算后才改，与 `character_region` 一致） |

`army_commander` / `army_region` 只接受 `eq` / `ne`；`validate_scenario` 检查缺字段（`army_commander` 必须写 `character`，无统帅写 `null`）。中文渲染：「禁军由郭子仪统领」「禁军不由郭子仪统领」「禁军无统帅」「河东军驻河北」。

`turn` 指正在结算进入的回合；在回合外调用时，指当前回合。

条件的中文渲染（`domain/describe.py`）：`describe_condition` 只写阈值（「渔阳鼙鼓 < 60」「京畿不归大燕」「「范阳起兵」未成」「回合 ≥ T20」），不写隐藏数值真值；`describe_satisfied` 把命中的条件拆成条目（all 全列，any 只列成立的分支，not 写成否定句）。

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
4. 账目。随后养兵：`formulas.upkeep: [{resource, per, amount, label, factions?, armies?}]`（剧本选用；缺省无），每项按**当前**兵力计——所列势力（缺省玩家势力；无玩家势力时为全部）或所列军队的兵力合计 N，本季开支 N / per × amount（amount 为正即支出），记 `LedgerLine(kind: "upkeep", group: "label（兵 N，每 per 兵 amount）")`，入经常收支明细（「军饷（兵 30000，每 10000 兵 5） −15」）。增兵即增此项。briefing 另列「## 养兵经常开支」逐项预计。`validate_scenario` 检查键、资源 / 势力 / 军队存在、per > 0、amount 为数。
5. 收入：`formulas.income` 的每个键都是 `{resource, formula, per_region: true}`。
6. 工程。
7. 移动抵达。
8. 战斗（见 1.7）。
9. 漂移（乘难度 `drift_scale`）。
10. 事件（概率 = min(1, gravity × 难度 `gravity_scale`)）。
11. 计数器规则：scenario `counters: [{id, conditions, mode: streak|count}]`。`streak` 在条件不满足时归零。
12. 结局判定（见 1.8）。
13. 历法。
14. 危机计：在以上全部结算（含延期条款、事件、抉择默认项）之后，按最终状态计算一次（`report.crisis`）；`SessionStore.append_turn` 同时存下公开快照 `report.crisis.public`。end_turn、季报（`last_report`）、`/view` 与 briefing 读到的是同一份数字。

`TurnReport` 新增：
- `battles: list`
- `choices_opened: list`
- `outcome: Outcome | None`
- `crisis: dict`：由场景 `crisis` 定义，含各分项贡献（最终状态，见第 14 步）
- `reconciliation: {resource: {opening, edicts, delayed, regular, events, closing}}`：分段对账。期初 = 上次结算后的值；诏令 = 两次结算之间的操作条目（`choose_event_option` 除外）；延期执行 = 第 2 步；经常收支 = 第 3–9 步（常设令、账目、收入、工程、漂移）；事件/选择 = 第 1、10、11 步与季前的 choose。各段之差逐段相加恰为期末 − 期初。公开版（`public_report`）为列表 `[{resource, name, unit, opening, edicts, delayed, regular, events, closing, shown, display, regular_detail?, regular_display?}]`，隐藏资源不列；`shown` 为各段真值各自取一位小数，**取整余差不并入任何一段**，而是单列 `shown.rounding`（display 中「取整差 +0.1」，位于期末之前），显示值之和恰等于期末（不再出现「宣告 −2、对账 −1.9」）
- `regular_detail: {resource: [{kind, label, amount}]}`：经常收支明细，kind 为 `income`（按收入公式 label 合并各地）、`upkeep`（养兵，逐项）、`ledger`（逐项账目）、`project`（「X施工」）、`standing`（常设令与竣工效果）、`drift`（「X漂移」，含难度系数）、`other`（「其他（上下限截断）」余差）；各项之和恰为 `regular`。公开版并入 `reconciliation[].regular_detail`（每项 `{kind, label, amount, shown, display}`，明细显示值与该段显示值的差另列 `{kind: "rounding", label: "取整差"}`）与 `regular_display`（「经常收支明细：诸道税入 +120；边军月饷 −12.4；…」）；顶层 `regular_detail` 不出现在公开报告中
- `crisis.change`（内部真值）与公开快照 `crisis.public_change`：本季危机值变化拆分，见 1.11；公开报告字段为 `crisis_change`

### 1.7 最小战斗与 AI 行军

**战斗**：同一区域内，`faction` 互为敌对（relation < 0 或场景 `wars` 列表）的军队交战。

- 战力 = `strength × quality × (1 + 守方区域 defense/100)`（仅守方享有防务加成）× RNG(0.85, 1.15)。
- 败方损失 30%，并退往相邻的己方控制区；无处可退则溃散。胜方损失 10%。
- 统帅不在军中时由副将暂摄（见 1.3），只记入战报与事实，不改战力。
- 区域 `defense ≥ 80` 时，攻方需要 2 倍战力才能胜，否则相持一季。
- 攻方获胜且该区域无守军时，`controller` 变更。
- 战报因素（第 8 轮）：`battles[]` 另带 `factors: {luck_spread: 0.15, defense_bonus, winner_loss, loser_loss, attacker: [{army, name, strength（开战时）, quality, commander, command: present|acting|none}], defender: [...]}`、`routed: {army: 溃散兵数}`、`retreat_names: {army: 地区名}`；公开报告再给 `detail`（`visibility.battle_breakdown`）一段：「攻：禁军20000（主帅郭将军在军）；守：叛军主力3000（无主帅），城防+30%。战力=兵×素质×(1+城防%)×天时±15%。伤亡（胜方各折1成、败方各折3成）：禁军−2000；叛军主力−900，无路可退，余2100溃散。」天时只示幅度，不示掷值。end_turn 的「## 战报」与 briefing 的上季战报、export_log 的 battles 都用它；旧存档无 factors 时照旧只列损失。

**AI 行军**：scenario `ai_routes: [{faction, route: [region...], hold_if_outnumbered: true}]`。每季，该势力不在途的军队沿 route 前进一格。

### 1.8 结局

scenario.yaml 中声明：

```yaml
endings:
  - {id, kind: ending|fail, title, text, priority, conditions}
game_length: {last_turn: 19, overtime_flag: rebellion_started, overtime_last_turn: 23, fallback_ending: open_storm}
```

每季结算末尾，按 priority 从小到大判定，命中第一个即写入 `outcome`。到达 `last_turn` 时（若 overtime_flag 为真，则到 overtime_last_turn）仍无命中，就使用 `fallback_ending`。

- `outcome.satisfied`：命中结局的条件逐条渲染为中文并带回合前缀，如「T20 时京畿不归大燕」「T20 时大燕兵力 ≤ 60000」；时限兜底写「T23 时已至终局时限 T23，其他结局条件均未满足」（加时另注「…，时限由 T19 延至 T23」）。
- **终局季提示**（`turn.final_season_notice`）：当下一次结算就会到达时限（`state.turn + 1 ≥ last_turn`；加时旗标已成立时按 `overtime_last_turn`）时，`/view.final_notice` 与 end_turn 返回的 `final_notice` 为 `{next_is_final: true, last_turn, overtime_possible, text}`，text 如「下次结算即终局：本季（T18）结算后即到 T19 时限，此后不能再下诏、处置事件或推进回合；本季是最后的决策窗口。（唯若结算之中「范阳已起兵」成立，时限延至 T23。）」；MCP briefing 在开头加粗显示，end_turn 文本附「## 注意：…」。其他结局条件可能更早终局，不在此列。剧本不必再写同义的提示事件。
- **延长模式**：结局可写 `extension_hint`，`game_length` 可写 `extension_mode`；只有 `extension_mode` 属于引擎已实现的模式（`turn.SUPPORTED_EXTENSION_MODES`，目前为空）时才把 extension_hint 接在结局正文后。现阶段一律不显示，结局正文本身不要写「可进入延长模式」。
- 终局后 `/view` 的 `memorials`、`pending_choices` 为空，另给 `review: {outcome, satisfied, objectives, stats: [{id, display}], highlights: [str], omitted, turns_played}`（stats 含公开资源、隐藏资源区间、本方兵力与控制地区数；highlights 为时间线要事「T19 天宝十四载冬：范阳起兵」，按时间排列，至多 24 条，`omitted` 为略去条数，briefing 注「另有 n 条从略」）。取舍优先级：3 = 使结局条件成立之事（条件中的旗标由某事件设下；阈值条件如「禄山兵柄 ≤ 10」由不成立变为成立的最后一步，写「事件——条件（结局条件由此成立）」）、终局之季的全部可见事件、终局本身（全部保留）；2 = 剧本 `importance ≥ 2` 的事件、战事、事件抉择（含逾期默认处置）、带兵官职的任命与易帅（含延期执行）、统帅抵达所统之军驻地（「X抵达Y，到军统Z」）；其余按 importance。MCP briefing 不再列奏疏与待决事件，改为「## 终局复盘」段；end_turn 的终局段附「判定条件」。

### 1.9 隐藏数值与公开视图

`public_view(state, seed)` 返回的状态中，`hidden` 资源替换为 `{id, name, hidden: true, estimate: [lo, hi]}`。

- 基础半宽 = `estimate_width × (1 + corruption/100)`。每条情报使半宽减半：情报数 = max(为真的 flag `intel:<resource>` / `intel:<resource>:<任意>` 个数, 记下的不同来源数)。`set_flag` 设情报旗标时，引擎把来源（op 的 source：奏疏标题、事件标题……；缺省「密报」）记入内部旗标 `_internal:intel_sources:<resource>`。
- 精度上限 floor：`settings.intel_min_width`（数值，或 `{resource: 数值}`，为半宽）；未设时 floor = 基础半宽 / 2，即情报不叠加，只有第一条生效。减半后低于 floor 时收至 floor 为止，此后标 `capped`。
- 公开视图的隐藏资源另有 `precision: {half_width, base_half_width, floor, sources, narrowing, applied, capped, display: "±4.6"}`；MCP briefing 的国势行附「精度 ±4.6（基础 ±9.2）；情报：A、B；已达精度上限 ±4.6，再得情报不再收窄」。
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
  advisors: [{character: li_linfu, stance: support|oppose|neutral, line: "...", option: deny}]   # option 可选：此人所主张的选项
  proposal: approve    # 可选：「所议之案」（谏言的赞成 / 反对针对它）；不写时由引擎推定，见 2 的廷议
  options:
    - {id: deny, label: 驳回，另择留后, ops: [...], hint: "外重内轻 −3"}
```

- 当回合可见条件：`turn` 匹配，或 `conditions` 满足，且未被处理。
- 谏言人校验：列出奏疏时剔除已故、系狱、流放的谏言人（致仕者仍可进言），绝不显示不在场者的台词。谏言人可带 `requires: {office: id|[id], region: id|[id], alive: bool}`：office 须任其一；region 须身在其一且不在途；`alive: false` 允许引用已不在者的旧议，显示名后缀「（旧议）」并带 `old: true`。`validate_scenario` 检查未知键与地区 id。
- 采纳某个选项，就把它的 ops 加入诏书草案；确认诏书后写入 flag `memorial:<id>` = option_id。
- `advisors[].option` / `proposal` 须为本条选项 id（`validate_scenario` 检查）。多个并列方案（非一准一驳）的奏疏建议写明，否则廷议只能「诸案并陈」。
- 选项可带 `memory: {character, text}`（或其列表），采纳时作为 `remember` op 随选项一同执行（同组延期）。条目可带 `keywords`，供廷议议题匹配。
- 条款事实的原因为奏疏标题（op 自带 reason 时用 reason）。
- 选项摘要（`ops_summary`、回执 `summary`）不出现 None：隐藏资源只写方向「禄山异志 ↓（风闻）」，隐藏心态写「心态有变（不明）」。对称的关系变化（A→B 与 B→A 同幅）只写一次「A↔B 关系 −10」；季报事实同样只留一条（同幅、同因）。
- `move_army` / `march` 摘要写明整军兵力并带「，某某随军」：「京师禁军（全军 66000） 移驻 潼关，高仙芝随军」；只调一部用 `detach`，摘要「禁军 分兵 5000，留 15000，编为「禁军前锋」赴 雄关，高内侍统领」。
- 调动（move_army / march / move_character / detach）预计抵达回合晚于终局时限（`game_length.last_turn`，加时旗标成立时按 overtime）时，回执摘要与 briefing 选项附「（预计第 n 回合抵达，晚于终局时限 T19，本局内到不了）」。

### 1.11 危机计

scenario.yaml：

```yaml
crisis: {resource: rebellion_risk, title: 渔阳鼙鼓, bands: [{max: 39, name: 承平}, ...], terms: [{id, label, expr}]}
```

`terms` 与 drift 公式中的分项一一对应。每季在报告里给出各分项的数值。

- `crisis.terms`（及 `/view.crisis`、briefing「危机计」段）按**结算后的状态**计算，即下一次结算的预计漂移；文本中注明。
- **本季变化拆分**（`visibility.public_crisis_change`，报告字段 `crisis_change`）：`{title, hidden, total, total_display, items: [{kind, kind_label, label, value, display}], drift: {terms, base, base_display, factor, difficulty_label, difficulty, difficulty_display, clamp}, other, lines: [中文行]}`。
  - `drift`：结算第 9 步当时的各分项（与 terms 同法，引用隐藏变量的分项以区间代入）、漂移基数、难度系数 `factor`（`drift_scale`）与难度加成 = 基数 ×（factor − 1）、上下限截断；
  - `items`：诏令（两次结算之间的 op，标签为奏疏标题 / 「诏令」）、抉择（季前 choose 与逾期默认处置，标签为事件标题）、延期执行、常设令 / 账目 / 工程、事件冲击（标签为**事件标题**）；`other` 为未归类的余差；
  - 危机资源隐藏时，`total`、各 item、截断与余差只给**档位区间**（`delta_range`：0.5 / 1 / 2 / 3 / 5 / 8 / 12 / 20 / 30 / 50 / 100 为界，如「+5～+8」），漂移分项给区间，不外露真值；危机资源公开时给确数。
  - end_turn 文本「## 本季危机变化（结算当时的实际贡献）」、briefing「## 上季危机变化」、`/view.last_report.crisis_change` 与 export_log 用同一份快照（结算时存入 `report.crisis.public_change`）。

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
| GET | `/sessions/{id}/view` | 前端主数据：`{state: public_view, calendar_label, objectives: [{id,title,status,detail}], crisis: {value_or_estimate, band, terms: [{label, value}]}, memorials: [...], pending_choices: [...], outcome, review, last_report, can_advance, difficulty: {id,label,description} \| null, scenario_changed: {...} \| null, warnings: [{code, message, ...}], command_table, final_notice}`（见 1.13）。`command_table`（`domain/command.py`）：玩家势力的「官职—所在—所统—指挥状态」总表 `{columns, rows: [{character, name, offices: [{id, name, station?, station_name?, status?}], location: {region, name, in_transit, display}, commands: [{army, name, strength, station, station_name, region, region_name, in_transit, whereabouts, status: present\|en_route\|remote, label}]}], vacancies: {offices: [{id, name, army?}], armies: [{army, name, strength, station, station_name, region, region_name, in_transit, whereabouts, status: "acting", label: "无统帅（副将暂摄）"}]}, alerts: [中文]}`（玩家本人不列；alerts 列遥领、兼统数军、出缺、无统帅）。`station` 是落脚地（在途时为目的地，用于判断统帅是否到任），**不是现驻地**：现驻地看 `region`（在途时为出发地），`in_transit` 为「在途：A→B，约n季后到」或 null，`whereabouts` 为显示用的「驻A」或在途说明——界面与简报一律显示 `whereabouts`，不得把在途军队写成「驻目的地」。`final_notice` 见 1.8。终局后 `memorials` / `pending_choices` 为空、`review` 为终局复盘（见 1.8），否则 `review: null`。`last_report.reconciliation` 为分段对账（见 1.6），`last_report.crisis` 与 `crisis` 在结算后未再下诏时完全相同 |
| GET | `/sessions/{id}/op_reference` | query `op?`、`entity_kind?`、`ids?`（逗号分隔），同 MCP `op_reference`（见 3） |
| POST | `/sessions/{id}/edicts/draft` | body `{sections: {category: text}, adopted: [{memorial_id, option_id}], ops: [...]}`。ops 用于客户端模型模式。回执中每一条 clause 都带 `source: memorial\|text\|client`；client / text 条款按玩家层校验（1.3.1），越权为 `rejected` + `code: OP_NOT_PERMITTED`。`delayed` 条款另带 `delay_reason`（由 `formulas.execution` 各项推出，如「吏治积弊高（55），有司稽迟；君威（68）尚能督责（本季延期概率约 2%）」）与 `due_turn`（执行回合） |
| POST | `/sessions/{id}/edicts/{edict_id}/confirm` | 已有，补写 memorial flag。回执另带 `new_memorials: [{id, title}]`（因本次确认而新出现的本季奏疏）。草案不存在 → 404 `EDICT_NOT_FOUND`，message 列出本季可确认的草案编号（「本季待确认的草案：edict-…」）；已在结算时放弃的草案 → 409 `EDICT_STALE` |
| POST | `/sessions/{id}/choices/{choice_id}` | body `{option_id}` → 执行 `choose_event_option`；返回另带 `new_memorials` |
| POST | `/sessions/{id}/turn` | 已有。返回 `{state: public_view, report, memorial(纪事), outcome, final_notice, discarded_drafts}`；已终局时返回 409 `GAME_OVER`。**本季有拟而未确认的草案时返回 409 `DRAFT_UNCONFIRMED`**（message 列出编号与摘要）——草案：本季（`base_turn` = 当前回合）拟下、未确认、未放弃、仍有 applied / delayed 条款；全被拒 / 仅记录的、只含已另行处理之奏疏的、以及其后又有本季草案被确认（「已被取代」）的不算。body `{discard_drafts: true}`（或 query `?discard_drafts=true`）则把这些草案标为已放弃（`discarded`，不能再确认）后结算，`discarded_drafts` 列出编号 |
| POST | `/sessions/{id}/debate` | body `{topic, participants: [id], memorial_id?, option_id?}` → `{topic, memorial: {id,title,options: [{id,label}]} \| null, proposition, proposal: {id, label, basis} \| null, topic_entities: [{kind, id, name}], speeches: [{character, stance, reason, text, target_option_id, target_option_label, against_option_id?, against_option_label?, proposition, position}], summary}`。立场见下；台词由 LLM 写（Mock 用模板）。给了 memorial_id 时 topic 可空（取奏疏标题）；memorial_id 不存在 → `UNKNOWN_MEMORIAL`；`option_id` 指定所议之案（须同时给 memorial_id，否则 `INVALID_REQUEST`；不是该奏疏的选项 → `UNKNOWN_OPTION`，message 列出可选 id） |
| GET / POST | `/sessions/{id}/advice` | 谏言库，记入日志的 `advice` 事件，不进入状态哈希。POST body `{character, text, source}` |
| POST | `/sessions/{id}/chat/{character}` | 已有 SSE。新增的提示词装配：人设 + 事实摘要（StateDigest）+ 该人物记忆 + 召对方式。`status` 事件带 `{status, mode: in_person\|written\|envoy, mode_label: 面见\|书面奏对\|遣使问对, mode_note}`；召对消息的 metadata 记 `mode` |
| GET | `/sessions/{id}/history` | 时间线：`[{id, type, turn, label, parentId}]`。`type` 新增 `edict`（确认诏书的回执摘要，label「确认诏书 edict-…」，不改状态） |
| GET | `/sessions/{id}/export` | query `from_turn?`、`to_turn?`（按下诏所在季，含两端；from > to → 422）。结构化复盘日志，同 MCP `export_log`（见 3） |
| POST | `/sessions/{id}/rewind` | body `{entry_id}` |
| DELETE | `/sessions/{id}` | 删除存档 |
| GET | `/health` | `{ok, version, scenarios}`，给桌面壳探活用 |
| GET | `/integration` | 只读。本机让 Codex / Claude Code 经 MCP 玩同一份存档的现成命令，设置页照原样展示（每段可复制）。见下 |

`GET /api/integration` 返回：

```jsonc
{
  "name": "tianbao",                    // MCP 服务名（桌面版 / dev_backend 为 tianbao；裸引擎为 llm-sim）
  "mode": "installed" | "source",       // 安装版：tianbao-server.exe mcp；源码：venv python -m cli.main mcp
  "server": {"command": "C:\\...\\tianbao-server.exe", "args": ["mcp"], "env": {}, "cwd": null},
  "home": "C:\\Users\\<you>\\AppData\\Roaming\\tianbao",   // 存档目录（LLM_SIM_HOME），与应用共用
  "scenarios_dir": "...",
  "codex": {
    "add": "codex mcp add tianbao -- \"C:\\...\\tianbao-server.exe\" mcp",
    "toml": "[mcp_servers.tianbao]\ncommand = '...'\nargs = [\"mcp\"]\nstartup_timeout_sec = 60\ntool_timeout_sec = 120\ndefault_tools_approval_mode = \"approve\"\n",
    "exec_flags": ["mcp_servers.tianbao.command=\"...\"", "mcp_servers.tianbao.args=[\"mcp\"]", "mcp_servers.tianbao.startup_timeout_sec=60", "mcp_servers.tianbao.tool_timeout_sec=120", "mcp_servers.tianbao.default_tools_approval_mode=\"approve\""],
    "note": "codex mcp add 不写 default_tools_approval_mode；codex exec 需要它……"
  },
  "claude": {
    "add": "claude mcp add tianbao -- \"C:\\...\\tianbao-server.exe\" mcp",
    "add_user": "claude mcp add tianbao --scope user -- \"C:\\...\\tianbao-server.exe\" mcp",
    "mcp_json": "{\n  \"mcpServers\": {\n    \"tianbao\": {\"type\": \"stdio\", \"command\": \"...\", \"args\": [\"mcp\"]}\n  }\n}\n"
  },
  "setup": {                            // 安装目录（或源码）里有 integrations/setup_mcp.ps1 时给出，否则 null
    "script": "C:\\...\\integrations\\setup_mcp.ps1",
    "codex": "powershell -NoProfile -ExecutionPolicy Bypass -File \"...setup_mcp.ps1\" -ServerExe \"...\" -Codex",
    "claude": "powershell ... -Claude"
  }
}
```

- 安装版里 `server.env` 通常为空：`tianbao-server.exe mcp` 自带与应用相同的默认值（`LLM_SIM_HOME=%APPDATA%/tianbao`、安装目录下的 `scenarios`）。应用以非默认的 `LLM_SIM_HOME` / `SIM_SCENARIOS_DIR` 启动时，差异会写进 `env`，命令里相应出现 `--env K=V`（codex）/ `-e K=V`（claude）。
- 源码模式（`mode: "source"`）：`command` 是当前 venv 的 python，`args = ["-m","cli.main","mcp"]`，`cwd` 为 `engine/backend`，`env` 含 `LLM_SIM_HOME`、`SIM_SCENARIOS_DIR`（及 `SIM_GAME_ROOT`、`PYTHONUTF8`）。`cwd` 只出现在 `toml`/`exec_flags` 里（`mcp add` 与 `.mcp.json` 无此项，venv 中已安装引擎，不依赖 cwd）。
- 所有字符串都是可直接粘贴的成品；命令行里含空格或非 ASCII 的参数用双引号括起（PowerShell / cmd / bash 通用）。
- 桌面壳经环境变量 `SIM_MCP_LAUNCH`（JSON `{name, mode, command, args, env, cwd}`）告诉引擎精确的启动方式；`SIM_MCP_NAME` 改服务名。

廷议立场（确定性），按优先级：
1. 议题对应奏疏（`memorial_id`，或当季可见奏疏中标题互含 / `keywords` 命中 / 标题二字组被议题覆盖 ≥ 50%）：该奏疏 `advisors` 中的人用奏疏立场。
2. 场景 `debate_topics` 的人物 / 派系立场表。
3. 议题按显示名点到的实体（`topic_entities`：人物、势力、官职、地区、军队）：本人或本人官职/所统军队/驻地被点名 → 按议题褒贬（罢、削… / 授、加…）维护自身；否则累计亲疏（人物关系、同派 +50、官职在任者、军队统帅、本方势力 +40、势力关系）与派系利益 `bloc_interests: {bloc: {实体 id 或关键词: 权重}}`，|合计| ≥ 20 时定立场（议题无褒贬时按「为其请命」处理）。
4. 忠诚 ≥ 8 赞成、≤ 3 反对。
5. 其余以种子决断（同局、同季、同议题稳定；多半持中）。

**立场指向的选项**（`debate.assign_option_targets`）：议题对应奏疏时，每个立场带 `target_option_id` / `target_option_label`（所主张的选项，可为 null）、`target_reason`、`position`（「主张「驳回」（deny），反对「准减赋」（approve）」或「未主一议，候圣裁」）、`proposition`（「就「X」诸选项择一」）与 `proposal_id` / `proposal_label` / `proposal_basis`（所议之案）：
- **所议之案**（`debate.infer_proposal`，谏言的赞成 / 反对针对它）：① 调用方 `option_id`；② 奏疏 `proposal`；③ 在世赞成者写明的 `option`（唯一时）；④ 奏疏 `summary` 与在世赞成者谏言中、各选项**独有**的二字组（按标点分句；去掉别的选项也有的、奏疏标题里的）命中 ≥ 2 且唯一最多者（「请加黜陟」→「严加黜陟」）；⑤ 准驳二议（恰有一个选项标题首句不带驳斥 / 罢免之意）取那一个；否则**无定案**——不以首个选项为案，`proposition` 写「诸案并陈，未有定案（可用 option_id 指定所议之案）」。
- 每人对每个选项打分：本人利害（被任命 / 统兵 / 被选中 / 恩宠升 +，免职 / 处置 / 夺兵 / 记忆写着「不用」「驳」 −，选项标题点名本人或本人官职按标题褒贬）、对选项点名人物的亲疏、派系利益 `bloc_interests`、谏言与该选项独有措辞的相合（赞成者计入全部选项；反对者只计入所议之案以外的选项——其话或复述所驳之案「恐骤加黜陟」、或道出所主之案「减其半亦足」；持中者不计）。
- 谏言人写明 `option` 即主张该选项（「所上之言即主此案」）；否则赞成者主张所议之案（或同一方中得分更高者）；反对者主张另一方得分最高者，`against_option_*` = 所议之案；持中者与其余人取得分最高者，全无利害时以种子择一（「无所偏倚，姑从此议」）。
- 无定案时：各人取得分最高者，全无利害者 `target_option_id: null`（「未主一议，候圣裁」）；非谏言人的泛泛立场（忠诚「唯上意是从」、种子决断）改为持中「议无定案，候上裁决」。
- 自由议题（无对应奏疏）：`target_option_id: null`，`proposition` 即议题原文，`position` 为「赞成 / 反对 / 持中「议题」」。`summary` 附「主张：「X」n 人（…）」。

`StateDigest(character_id | None)`：引擎渲染的事实摘要，固定格式的中文文本。内容是这个人能知道的资源（隐藏资源给区间）、官职、在任者、地区要点、进行中的工程和常设令、本季已发生的事实。它供 LLM 提示词和 MCP 使用。
- 非玩家势力控制的地区列在【外域】，只给控制者与驻军，不给经济指标。
- 给定人物时按相关性筛地区：所在 → 统兵所在 → `knowledge` 中写到的地区 → 行程目的地 → 相邻，这些给全部指标；其余地区压成一行【他处】名单（按控制者分组）；另附【记忆】（最近 12 条）。
- 在途人物列于【在途】「某某（自A赴B，约n季后到）」；【军队】行写「在途（…）」，统帅不在军中时写「统帅某某未到任（…），副将暂摄」（赴本军）/「统帅某某离军他往（…），副将暂摄」（赴他处）/「统帅某某不在军中，副将暂摄」。【本人】名后的头衔：官职与开局不同时写「（旧衔：X）」。离线召对（mock）把军队、地区、外域行改写成口语（「河东之兵五万余，皆在禄山麾下」「河东防务颇佳」），同一句不说两遍。

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
| `briefing` | `session_id` | 历法、难度、`scenario_changed` 提示（若有）、**终局季提示**（见 1.8，加粗）、三目标、公开资源（隐藏资源附情报精度，见 1.9）、危机计及分项（注明为下次结算的预计漂移）、「## 上季危机变化」（见 1.11）、「## 官职与兵权」Markdown 表（官职 | 人物 | 所在 | 所统 | 指挥状态，遥领 / 出缺 / 无统帅加粗，末附「提醒：」，终局后不列）、「## 待办与在途」（引擎已知的排期，每条带到期回合：延期条款「延至下季结算时执行（第 n 回合）」、在途人物与军队及预计抵达回合、工程进度与预计竣工回合、常设令截止、定期账目余期、待决事件期限）、奏疏条目（含选项与 ops 摘要）、待决事件、上季事实；可召对名单中的在途者附行程。终局后以「终局复盘」段代替奏疏与待决事件。末尾附**扮演规则**：数字只能引用简报里的值 |
| `op_reference` | `session_id, op?, entity_kind?, ids?` | 缺省紧凑：`permitted_ops`（玩家可用操作，每个一行字段说明 `fields` + 用本局实体写成的 `example`）、`scenario_only_ops`（只能经奏疏 / 事件产生的操作及显示名）、`usage`（奏疏、抉择的用法）、`entities`（每类 `{count, rows: ["id 名（要点）"…至多 12 行], more}`）、`rules`。`op=<名>`：该操作的完整 JSON Schema、示例、`permitted` 与说明（未知名 → `UNKNOWN_OP`）；`entity_kind=<类别>`：该类完整表（resources、characters、offices、regions、armies、factions、ledger、standing_orders、pending_choices）；`ids=[...]`：只给这些 id（附 `missing`） |
| `audience` | `session_id, character` | 首行「# 召对方式：面见 / 书面奏对 / 遣使问对——说明」，再接人设卡 + 该人物可知的 StateDigest（含【记忆】）+ 口吻要求。人设卡头衔（`persona_card.title`）在官职与开局不同时取现任官职名，静态 title 作 `former_title`（卡上「头衔：安西四镇节度使（旧衔：安西节度判官，已非现职）」）；开场白里的旧衔（静态 title 的缩写、或开局所任而今已不任的官职名）改为现任官职（无官职则删去该句），离线召对同。client 模式每次调用记一条轻量记录（见 export_log）。由调用方模型扮演；死人或在押者返回拒绝。召对方式（`rules.audience_mode`）：与君主（玩家人物）同地且不在途 → 面见；远在他处 → 书面奏对（驿递往还，不令其入京）；在途 → 遣使问对。口吻要求、服务端提示词（minister_chat 末尾追加）与离线答话（前缀「〔书面奏对·自X驿递〕」「〔遣使问对·途中回奏〕」）随之变化；server 模式返回「某某（书面奏对）：…」 |
| `court_debate` | `session_id, participants, topic?, memorial_id?, option_id?` | 「议题命题」（对应奏疏时列出全部选项，并写明所议之案及其来历，或「诸案并陈，未有定案」）、对应奏疏、「议题涉及」实体、引擎给出的各人立场与所主张 / 反对的选项（见 2 的廷议）+ 人设，调用方据此写辩论。client 模式每次调用记一条轻量记录（见 export_log） |
| `save_advice` | `session_id, character, text` | — |
| `draft_edict` | `session_id, sections?, adopted?, ops?` | 首行「诏书草案 edict_id=edict-…」单独成行（次行说明须 confirm_edict）；回执逐条（草案，未确认）：`[applied 可行（确认后本季即行）]` / `[rejected 被拒] [CODE]` / `[delayed 确认后延至下季结算时执行（第 n 回合）]`（附「延期原因：…」）/ `[narrative_only 仅记录]`；`confirm_edict` 的回执改记 `[applied 已行]` / `[delayed 已延至下季结算时执行（第 n 回合）]`。延期说法全局统一为「延至下季结算时执行（第 n 回合）」（简报、复盘日志 `delayed[].timing` 与条款 `timing`、时间线同）。玩家可见文本不出现回合代号 `T\d+`：一律写历法标签「天宝十四载冬（第 19 回合）」，十万以上的数写作「54.79万」 |
| `confirm_edict` | `session_id, edict_id` | 确认后的回执；有新出奏疏时末行「本季新出奏疏：[id] 标题、…（可在 end_turn 前继续 draft_edict 采纳）」。编号不存在时错误列出本季可确认的草案编号 |
| `choose` | `session_id, choice_id, option_id` | 事实；有新出奏疏时同上附「本季新出奏疏：…」 |
| `end_turn` | `session_id, discard_drafts?` | 本季有未确认草案时报 `错误 [DRAFT_UNCONFIRMED]：本季尚有未确认的诏书草案：edict-…（摘要）…`（规则同 REST `/turn`）；`discard_drafts: true` 放弃后结算，文本附「## 已放弃的草案（未施行）：…」。TurnReport：事实（逐条去重，不含「终局」行）、「## 对账（期初 → 诏令 → 延期执行 → 经常收支 → 事件/选择 → 期末）」（公开资源每项一行，代替旧的「账目合计」；有取整余差时行内另列「取整差」；每行下附「  - 经常收支明细：…」；隐藏资源只注「数值不明」）、战斗、事件、危机分项（与随后的 briefing 相同，注明为下次结算的预计漂移）、「## 本季危机变化（结算当时的实际贡献）」、下次结算即终局时「## 注意：…」、outcome（末尾「终局」段只出现一次，附「判定条件」）。client 模式不再附与事实重复的「纪事」 |
| `history` / `rewind` | — | — |
| `export_log` | `session_id, from_turn?, to_turn?` | 结构化复盘日志（JSON，只读，公开视图）：`{session_id, scenario, scenario_version, seed, difficulty, turn, calendar_label, outcome, note, seasons: [...]}`。每季（按下诏所在季 T）：`adopted: [{memorial_id, option_id, title, label}]`（由 `memorial:<id>` 旗标还原，旧存档亦可）、`client_ops: [{op, status, summary, code?}]`、`drafts` / `confirms: [{edict_id, adopted, clauses: [{index, status, source, summary, code?, reason?, delay_reason?, due_turn?, memorial_id?, option_id?, op?（仅玩家自拟条款）}], changed_clauses?, execution_rate?}]`、`delayed: [{label, due_turn, summary}]`、`choices: [{choice_id, option_id, title, option}]`、`audiences: [{character, mode, name?, mode_label?, via?}]`、`debates: [{topic, memorial_id?, option_id?, participants?, via?}]`（server 模式取自日志中的召对 / 廷议消息；client 模式取自旁路文件 `<session>.calls.jsonl` 的轻量记录，`via: "client"`，只记谁、方式、议题、参与者与回合，不含台词；按分支路径筛选）、`advice`、`end_turn: {resolved_to, calendar_label, facts, events, battles, choices_opened, reconciliation, crisis, crisis_change, warnings, outcome, resources}`。拟诏回执写在旁路文件 `<session>.receipts.jsonl`（拟诏不改日志、不移动 head；只导出拟于当前分支路径上的草案），确认回执写进日志的 `edict` 条目。隐藏数值只有风闻区间 / 档位区间 |

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
- 同一个 `tianbao-server.exe` 也是 MCP 服务：`tianbao-server.exe mcp`（stdio，UTF-8），默认值与应用相同，所以外部模型与应用共用存档。安装目录另带 `integrations/`（`setup_mcp.ps1`、Claude Code 插件、Codex 的 `AGENTS.md`），见 `integrations/README.md`；本机的现成命令由 `GET /api/integration` 给出（见 2）。

## 6. 测试与门禁

| 门禁 | 内容 |
|---|---|
| G1 | Playwright 按 `data-testid` 清单逐个点击，每个按钮都要有可断言的效果；控制台 0 错误 |
| G2 | 引擎 pytest；场景测试包括不变量检查、1000 种子模拟和结局可达性 |
| G3 | API 契约测试、仿 OpenAI 服务器测试、MCP 工具测试 |
| G4 | 乱码扫描：DOM、日志、存档中不允许出现 `�`、`锟斤拷`，以及 `Ã` `å` `æ` `ç` `è` 后跟 0x80–0xBF 字节的典型 mojibake；静态文案和剧本文字必须 100% 被打包字体覆盖 |
| G5 / G6 | 自玩与 GPT 玩的日志存入 `playtests/` |
