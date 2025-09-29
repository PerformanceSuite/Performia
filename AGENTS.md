# Repository Guidelines

## Project Structure & Module Organization
- `src/` hosts the JUCE shell (modes, layouts, shared `core/` utilities, persistent `memory/`).
- `ingest-analyze-pipe/` holds the Python song-map pipeline; services live in `services/<domain>/` and reuse helpers in `services/common/`.
- `performia---living-chart/` is the Vite + React dashboard alongside hooks, types, and fixtures; assets sit in `resources/`.
- `tests/` mirrors runtime areas (`unit/`, `components/`, `integration/`, `ui/`); add matching folders with every new module. `docs/` centralises specs and PRDs.

## Build, Test, and Development Commands
- JUCE host: generate the project via Projucer or CMake, build, then run `./build/Performia` (debug artifacts land in `build/debug/`).
- Pipeline: `make -C ingest-analyze-pipe build` assembles Docker images; `python ingest-analyze-pipe/services/packager/main.py --id demo --raw tmp/raw/demo.wav --out tmp/final` provides a quick smoke test.
- Dashboard: `cd performia---living-chart && npm install && npm run dev` starts the Vite server; use `npm run build` for release bundles.
- Sessions: `scripts/session-manager.sh start|checkpoint|end` keeps DevAssist state aligned when swapping domains.

## Coding Style & Naming Conventions
- JUCE C++: 4-space indents, PascalCase components, camelCase methods, constants in ALL_CAPS; prefer JUCE smart pointers for ownership clarity.
- Python pipeline: follow PEP 8 with type hints, snake_case modules, and store tunables in CONFIG files instead of hardcoding.
- TypeScript/React: PascalCase files/components, descriptive prop names, colocate hooks in `hooks/`, and keep data mappers under `utils/`.
- Run formatters before committing (`clang-format`, `black` + `isort`, `npm exec prettier`).

## Testing Guidelines
- Backend: keep unit coverage in `tests/unit` and run `pytest -q tests/unit`; place end-to-end flows under `tests/integration` with sample audio staged in `tmp/`.
- UI: document or automate smoke runs for all six modes in `tests/ui`; attach screenshots when visual changes differ from baselines.
- Dashboard: add component checks in `tests/components` and prefer Vitest + React Testing Library for new automation.
- Target >80% line coverage on new backend modules and assert timing/buffer limits whenever altering real-time code.

## Commit & Pull Request Guidelines
- Follow Conventional Commits (`feat:`, `fix:`, `chore:`) with optional scopes mirroring git history.
- Summaries must describe behaviour, reference an issue, and include media for UX or audio changes; call out skipped suites.
- Request reviews from affected domain owners (UI, pipeline, dashboard) after local builds and tests succeed.

## Agent & Environment Tips
- Run `./setup-performia-agents.sh` to register Claude subagents once per machine, then use `scripts/session-manager.sh checkpoint` while context-switching.
