# Project
Camera snapshot service. Python backend that pulls camera frames and
serves snapshot frames through an image pipeline.

# Map
- src/snapshot_service/api/          public device + snapshot API handlers
- src/snapshot_service/integrations/ per-camera integration modules
- src/snapshot_service/pipeline/     frame processing (resize, encode); add format work here
- tests/                             pytest suite; the source of truth for "correct"

# Commands
- Install:    `pip install -e ".[dev]"` (inside a virtual environment)
- Run tests:  `pytest`
- Lint:       `ruff check .` and `ruff format --check .`
- Type check: `mypy`

# Code Style
- PEP 8, 4-space indentation, enforced by Ruff.
- Type hints on every function; mypy runs in strict mode.
- Absolute imports from `snapshot_service`; no wildcard imports.
- All camera/device endpoints must use TLS (https:// / rtsps://).
- Never hardcode credentials; read them from config.

# Workflow
Follow Explore -> Plan -> Code -> Commit.
- Explore & plan in Plan Mode before editing.
- State explicit success criteria in every plan.
- Validate against tests/ (and Ruff + mypy) before considering work done.
- Run the code-reviewer subagent before committing.
