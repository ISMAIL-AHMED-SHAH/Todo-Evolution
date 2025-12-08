<!--
Sync Impact Report
==================
Version Change: N/A → 1.0.0
Rationale: Initial implementation plan creation.

Modified Principles: None
Added Sections: None
Removed Sections: None

Templates Requiring Updates: None

Follow-up TODOs: None
-->

# Implementation Plan: In-Memory Python Todo CLI App

**Branch**: `001-in-memory-todo` | **Date**: 2025-12-05 | **Spec**: [specs/001-in-memory-todo/spec.md](specs/001-in-memory-todo/spec.md)
**Input**: Feature specification from `/specs/001-in-memory-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation of an In-Memory Python Todo CLI application that supports adding, listing, updating, deleting, and marking todo items. The technical approach adheres to a clean architecture, utilizing pure Python data structures for in-memory storage and the `rich` library for enhanced CLI output.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `rich` (for CLI formatting), `uv` (for environment/dependency management), `pytest` (for testing)
**Storage**: In-memory Python data structures (e.g., list of dictionaries or custom objects)
**Testing**: `pytest` for unit and integration tests
**Target Platform**: Cross-platform CLI
**Project Type**: Single project
**Performance Goals**: < 100ms response time for all CLI commands, < 10MB memory usage for 1000 todo items.
**Constraints**: In-memory only, CLI only, Python 3.10+, UV environment, Rich library for output, Pure functions for business logic, Standard Library preference.
**Scale/Scope**: Single-user application, capable of managing up to 1000 todo items efficiently.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Single-File In-Memory Architecture**: The plan explicitly uses in-memory Python data structures for all todo storage.
- [x] **II. Python 3.10+ Implementation**: Specifies Python 3.10+ as the development language.
- [x] **III. Spec-Driven Development**: This plan is derived directly from the `specs/001-in-memory-todo/spec.md`.
- [x] **IV. CLI-Only Interface**: The plan focuses solely on command-line interactions.
- [x] **V. Rich Library for Output Quality**: The plan incorporates `rich` for CLI output.
- [x] **VI. Clean Architecture**: Business logic will be separated from UI logic.
- [x] **VII. Pure Functions**: Core operations will be implemented as pure functions.
- [x] **VIII. No External Side Effects**: No external network calls or system changes are planned.
- [x] **IX. Standard Library Preference**: External dependencies are limited to `rich` and `pytest`, managed by `uv`.
- [x] **X. Reproducibility**: The spec-driven approach ensures reproducibility.
- [x] **XI. Testability**: The plan includes unit and integration testing.
- [x] **XII. UV Environment & Dependency Management**: `uv` is specified for environment and dependency management.
- [x] **XIII. Documentation Capture**: This plan will be captured as a PHR.

## Project Structure

### Documentation (this feature)

```text
specs/001-in-memory-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # (N/A for this feature - no complex research needed)
├── data-model.md        # (N/A - data model embedded in spec.md)
├── quickstart.md        # (N/A for this phase)
├── contracts/           # (N/A for this feature - no external contracts)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
. # Project Root
├── src/
│   ├── cli.py        # Main CLI application logic, argument parsing, and output display.
│   ├── models.py     # Defines the `Todo` data structure.
│   └── services.py   # Contains business logic for Todo operations (add, list, update, delete, mark).
├── tests/
│   ├── unit/
│   │   ├── test_models.py    # Unit tests for the `Todo` model.
│   │   └── test_services.py  # Unit tests for the `TodoService` logic.
│   └── integration/
│       └── test_cli.py       # Integration tests for CLI command interactions.
├── pyproject.toml    # Project metadata and dependency management (for uv).
├── requirements.txt  # Explicit list of project dependencies (for uv).
└── README.md         # Project overview and usage instructions.
```

**Structure Decision**: A single-project structure with `src/` for application logic and `tests/` for unit and integration tests. This aligns with the CLI-only and in-memory constraints, promoting modularity and testability. `pyproject.toml` and `requirements.txt` will manage dependencies via `uv`.

## Implementation Milestones & Sequence

### Phase 0: Project Initialization & Environment Setup (Foundational)

1.  **Initialize Project**: Ensure `pyproject.toml` exists with basic project metadata.
2.  **UV Environment Setup**: Create a virtual environment using `uv venv`.
3.  **Install Dependencies**: Install `rich` and `pytest` using `uv pip install` into the virtual environment.
4.  **Directory Structure**: Create `src/`, `tests/unit/`, and `tests/integration/` directories.
5.  **Initial Files**: Create empty `src/cli.py`, `src/models.py`, `src/services.py`, `tests/unit/test_models.py`, `tests/unit/test_services.py`, and `tests/integration/test_cli.py`.

### Phase 1: Core Data Model & Services (User Story 1 & 5 - Dependencies)

1.  **Implement Todo Model (`src/models.py`)**: Define the `Todo` class with `id`, `description`, and `completed` attributes.
2.  **Implement TodoService (Add & Mark) (`src/services.py`)**: Create `TodoService` to manage the in-memory list of todos. Implement `add_todo(description)` and `mark_todo_status(todo_id, completed)`.
3.  **Unit Tests (Models & Services)**: Write unit tests for `Todo` model (`tests/unit/test_models.py`) and `TodoService`'s `add_todo` and `mark_todo_status` methods (`tests/unit/test_services.py`).

### Phase 2: List Todos (User Story 2 - P1)

1.  **Implement List Functionality (`src/services.py`)**: Add `list_todos()` method to `TodoService` to return all current todos.
2.  **CLI Integration (List) (`src/cli.py`)**: Implement the CLI command to display todos, utilizing `rich` for tabular output.
3.  **Unit Tests (List)**: Write unit tests for `list_todos` method (`tests/unit/test_services.py`).
4.  **Integration Tests (List)**: Write integration tests for the `list` CLI command (`tests/integration/test_cli.py`) to verify correct output formatting.

### Phase 3: Update and Delete Todos (User Story 3 & 4 - P2)

1.  **Implement Update/Delete Functionality (`src/services.py`)**: Add `update_todo(todo_id, new_description)` and `delete_todo(todo_id)` methods to `TodoService`.
2.  **CLI Integration (Update/Delete) (`src/cli.py`)**: Implement CLI commands for updating and deleting todos by ID.
3.  **Unit Tests (Update/Delete)**: Write unit tests for `update_todo` and `delete_todo` methods (`tests/unit/test_services.py`).
4.  **Integration Tests (Update/Delete)**: Write integration tests for the `update` and `delete` CLI commands (`tests/integration/test_cli.py`).

### Phase 4: CLI Argument Parsing & Robust Error Handling (Cross-Cutting)

1.  **Argument Parsing (`src/cli.py`)**: Implement robust argument parsing for all commands (add, list, update, delete, complete, incomplete) using Python's `argparse` or similar.
2.  **Input Validation**: Add comprehensive input validation to `src/cli.py` and `src/services.py` to handle invalid IDs, empty descriptions, etc.
3.  **Error Messages (`src/cli.py`)**: Ensure user-friendly and informative error messages are displayed using `rich` for all validation failures and non-existent IDs.

### Phase 5: Final Review & Validation

1.  **Code Review & Refactoring**: Ensure adherence to clean architecture, pure functions, and Python best practices. Optimize for clarity and maintainability.
2.  **Run All Tests**: Execute all unit and integration tests to confirm full functionality and catch regressions.
3.  **Performance & Memory Check**: Manually or with simple scripts verify the performance goals (response time, memory usage) are met, especially for large todo lists.
4.  **Documentation Update**: Ensure `README.md` provides clear usage instructions for all commands.
5.  **Modularity Check**: Confirm the design allows for easy extension (e.g., adding a persistence layer later) without re-architecting core logic.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
