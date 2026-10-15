"""Let an external agent CLI play a full game of 天宝 through the MCP server.

    python tools/agent_play.py codex  --run gpt-01  [--model gpt-6.1-sol] [--seed 7]
    python tools/agent_play.py claude --run claude-01 [--seed 7]

Each run gets its own LLM_SIM_HOME under playtests/<agent>/<run>/home, a
transcript (events.jsonl) and the agent's own report.md written in that folder.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"

PROMPT = """你要完整地玩一局桌面策略游戏《天宝》：你扮演天宝十载（751 年）的唐玄宗。游戏通过名为 tianbao 的 MCP 服务提供工具。

规则：
1. 先调用 list_scenarios，再用 new_game 开局（scenario=tianbao_751，seed={seed}）。记下 session_id。
2. 每一季：调用 briefing 阅读局势；至少召见一位大臣（audience，你根据返回的人设和事实摘要自行扮演他回话，数字只能引用工具给出的值）；需要时开 court_debate；
   然后用 draft_edict 下诏（可以 adopted 采纳奏疏选项，也可以 ops 直接提出操作，op 格式见 op_reference），读回执后 confirm_edict；有待决事件就用 choose 选择；最后 end_turn。
3. 一直玩到游戏给出 outcome（结局或失败）为止，不要中途停下，也不要提前问我。你的目标是取得最好的结局（阻止安史之乱、财政不枯竭、君威 ≥ 50）。
4. 工具报错时，读懂错误说明，修正参数再试；同一个错误连续出现 3 次就换一种做法，并把它记进报告。
5. 结束后，把一份中文试玩报告写到文件 {report}：结局、每季一行的大事记、你遇到的所有问题（工具报错、看不懂的说明、前后矛盾的数字、卡住的地方、认为不合理的机制），以及改进建议。问题请尽量具体（哪一季、哪个工具、什么参数、返回了什么）。
"""


def mcp_env(home: Path) -> dict[str, str]:
    return {
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "SIM_GAME_ROOT": str(ROOT),
        "SIM_SCENARIOS_DIR": str(ROOT / "scenarios"),
        "LLM_SIM_HOME": str(home),
        "SIM_MCP_MODE": "client",
    }


def run_codex(run_dir: Path, prompt: str, model: str) -> list[str]:
    env = mcp_env(run_dir / "home")
    server = f"mcp_servers.tianbao"
    cmd = [
        shutil.which("codex") or "codex", "exec", "--skip-git-repo-check", "--json",
        "-m", model, "-C", str(run_dir),
        "-s", "workspace-write", "-c", 'windows.sandbox="unelevated"',
        "-c", f'{server}.command={json.dumps(str(PYTHON))}',
        "-c", f'{server}.args=["-m","cli.main","mcp"]',
        "-c", f'{server}.cwd={json.dumps(str(ROOT / "engine" / "backend"))}',
        "-c", f"{server}.env={{{', '.join(f'{k}={json.dumps(v)}' for k, v in env.items())}}}",
        "-c", f"{server}.tool_timeout_sec=120",
        prompt,
    ]
    return cmd


def run_claude(run_dir: Path, prompt: str) -> list[str]:
    config = {
        "mcpServers": {
            "tianbao": {
                "command": str(PYTHON),
                "args": ["-m", "cli.main", "mcp"],
                "cwd": str(ROOT / "engine" / "backend"),
                "env": mcp_env(run_dir / "home"),
            }
        }
    }
    config_path = run_dir / "mcp.json"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    claude = os.environ.get("CLAUDE_CLI") or shutil.which("claude") or "claude"
    return [
        claude, "-p", prompt, "--output-format", "stream-json", "--verbose",
        "--mcp-config", str(config_path), "--strict-mcp-config",
        "--allowedTools", "mcp__tianbao__*", "Write",
        "--max-turns", "400",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("agent", choices=["codex", "claude"])
    parser.add_argument("--run", required=True)
    parser.add_argument("--model", default="gpt-6.1-sol")
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    run_dir = ROOT / "playtests" / args.agent / args.run
    (run_dir / "home").mkdir(parents=True, exist_ok=True)
    report = run_dir / "report.md"
    prompt = PROMPT.format(seed=args.seed, report=report)
    cmd = run_codex(run_dir, prompt, args.model) if args.agent == "codex" else run_claude(run_dir, prompt)

    started = time.time()
    with open(run_dir / "events.jsonl", "w", encoding="utf-8") as out, open(run_dir / "stderr.txt", "w", encoding="utf-8") as err:
        proc = subprocess.run(cmd, cwd=run_dir, stdout=out, stderr=err, encoding="utf-8", errors="replace")
    elapsed = time.time() - started
    summary = {"agent": args.agent, "run": args.run, "exit": proc.returncode, "seconds": round(elapsed), "report": report.exists()}
    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return proc.returncode


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    raise SystemExit(main())
