"""Frozen / dev entry point for the tianbao-server sidecar.

`tianbao-server serve --host H --port P`  -> run the FastAPI engine directly (no string import,
so PyInstaller can see every module) and make sure CORS allows the desktop webview origins.
Anything else (`mcp`, `validate`, ...) is delegated to the engine CLI (`cli.main:app`).
"""
from __future__ import annotations

import multiprocessing
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except Exception:
        pass

if not getattr(sys, "frozen", False):
    # dev mode: run straight from the repo (tianbao/desktop/sidecar/entry.py -> tianbao/engine/backend)
    _backend = Path(__file__).resolve().parents[2] / "engine" / "backend"
    if str(_backend) not in sys.path:
        sys.path.insert(0, str(_backend))

CORS_ORIGINS = [
    "http://tauri.localhost",
    "https://tauri.localhost",
    "tauri://localhost",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]


def _ensure_cors(app) -> None:
    from starlette.middleware.cors import CORSMiddleware

    if any(m.cls is CORSMiddleware for m in getattr(app, "user_middleware", [])):
        return
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_origin_regex=r"^https?://(127\.0\.0\.1|localhost)(:\d+)?$",
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _serve(argv: list[str]) -> None:
    host, port = "127.0.0.1", 8000
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--host" and i + 1 < len(argv):
            host = argv[i + 1]
            i += 2
        elif arg == "--port" and i + 1 < len(argv):
            port = int(argv[i + 1])
            i += 2
        elif arg.startswith("--host="):
            host = arg.split("=", 1)[1]
            i += 1
        elif arg.startswith("--port="):
            port = int(arg.split("=", 1)[1])
            i += 1
        else:
            i += 1

    import uvicorn

    from api.app import app

    _ensure_cors(app)
    uvicorn.run(app, host=host, port=port, log_level="info")


def main() -> None:
    multiprocessing.freeze_support()
    argv = sys.argv[1:]
    if argv and argv[0] == "serve":
        _serve(argv[1:])
        return
    from cli.main import app as cli_app

    cli_app()


if __name__ == "__main__":
    main()
