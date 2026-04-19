# Testomat Auto Tests

UI end-to-end tests for Testomat using `pytest` and Playwright.

## Project Structure

- `src/config/`: Environment and runtime settings.
- `src/web/components/`: Reusable UI component abstractions.
- `src/web/pages/`: Page object models.
- `src/web/application.py`: App-level entry point for page/component access.
- `tests/fixtures/`: Shared pytest fixtures.
- `tests/web/`: Main web test suite.
- `tests/sandbox/`: Experimental tests (excluded by default marker config).

## Dependency Management (uv)

This project uses `uv` as the source of truth for dependencies.

- Install/sync dependencies:
  - `uv sync --all-groups`
- Run tests:
  - `uv run pytest`
- Run lint/format:
  - `uv run ruff check .`
  - `uv run ruff format .`
  - `uv run black .`

## Notes

- Main dependencies are declared in `[project.dependencies]` in `pyproject.toml`.
- Dev tooling dependencies are declared in `[dependency-groups].dev`.
- `requirements.txt` is exported from `uv` for compatibility.
