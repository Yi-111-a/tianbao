# 天宝

盛唐书案上的帝王模拟。你是天宝十载（751）的唐玄宗，盛世只剩最后四年——你能阻止安史之乱吗？

- LLM 扮演群臣、撰写史笔；国库、兵马、人心由确定性引擎结算，每条诏令都有执行回执。
- 本地运行的桌面应用；可接任意 OpenAI 兼容模型，也能在 Claude Code / Codex 里直接下旨游玩。
- 引擎来自 [llm-sim-game-template](https://github.com/Yi-111-a/llm-sim-game-template)（`engine/` 子模块）。

## 在 Claude Code / Codex 里玩

装好桌面版后，一条命令把游戏的 MCP 服务注册给 Codex 或 Claude Code（存档与桌面版共用）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\天宝\integrations\setup_mcp.ps1" -Codex -Claude
```

不带 `-Codex` / `-Claude` 时只打印命令、不改配置。手动命令、Claude Code 插件（「上朝」技能）和 Codex 说明见
[integrations/README.md](integrations/README.md)；桌面版「设置」里也列出本机的现成命令。

> 开发中。计划见 [docs/GAME_PLAN.md](docs/GAME_PLAN.md)，接口契约见 [docs/CONTRACT.md](docs/CONTRACT.md)，剧本大纲见 [docs/TIANBAO_751_OUTLINE.md](docs/TIANBAO_751_OUTLINE.md)。

MIT 许可。
