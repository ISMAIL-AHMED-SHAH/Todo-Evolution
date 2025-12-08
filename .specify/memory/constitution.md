<!--
Sync Impact Report
==================
Version Change: 1.1.0 → 1.2.0
Rationale: Added 'Documentation Capture' principle.

Modified Principles:
  - XIII. Documentation Capture (Added)
Added Sections: None
Removed Sections: None

Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section already exists
  ✅ spec-template.md - No changes required (technology-agnostic requirements)
  ✅ tasks-template.md - No changes required (task structure supports in-memory architecture)

Follow-up TODOs: None
-->

# In-Memory Python Todo Console App Constitution

## Core Principles

### I. Single-File In-Memory Architecture

The entire console application MUST run fully in-memory with no external persistence layer. No external database, file storage, JSON storage, or cloud API may be used for persistence. All tasks MUST be stored in Python in-memory structures such as lists, dicts, or classes.

**Rationale**: Ensures simplicity, reproducibility, and eliminates external dependencies that would complicate the development and testing workflow.

### II. Python 3.10+ Implementation

The application MUST be implemented in Python version 3.10 or higher.

**Rationale**: Ensures access to modern Python features (structural pattern matching, improved type hints, performance improvements) while maintaining reasonable compatibility across common development environments.

### III. Spec-Driven Development

The implementation MUST follow the specification file strictly. No feature may be added or removed unless updated in the spec first. Running the `specify` command on the specification must always reproduce the same structure and functions.

**Rationale**: Maintains traceability between requirements and implementation, ensures reproducibility, and prevents scope creep.

### IV. CLI-Only Interface

The application MUST run through a text-based console interface. No GUI or web interface is allowed.

**Rationale**: Keeps complexity minimal, ensures cross-platform compatibility without additional UI frameworks, and aligns with the in-memory architecture goal.

### V. Rich Library for Output Quality

The entire Command Line Interface (CLI) output MUST utilize the Python `rich` library for improved formatting, colors, and tabular presentation (e.g., for task listing).

**Rationale**: Provides professional-grade terminal output with minimal implementation effort, improving user experience while maintaining the CLI-only constraint.

### VI. Clean Architecture

Business logic and UI logic MUST be separated into functions. No business logic should be inside print/input statements.

**Rationale**: Enables independent testing of business logic, facilitates future refactoring, and improves code maintainability and clarity.

### VII. Pure Functions

All operations (add, update, delete, list) MUST be deterministic and testable with no side effects.

**Rationale**: Ensures predictable behavior, simplifies testing, and prevents hidden state mutations that could lead to bugs.

### VIII. No External Side Effects

No network calls, external imports beyond Python Standard Library (except where explicitly allowed by constitution), or system-level changes are allowed.

**Rationale**: Maintains isolation, ensures reproducibility across environments, and prevents security vulnerabilities from external dependencies.

### IX. Standard Library Preference

All non-core logic imports MUST be restricted to the Python Standard Library unless explicitly required by a Constitution rule (such as `rich`) or an approved ADR.

**Rationale**: Minimizes external dependencies, reduces security surface area, improves long-term maintainability, and ensures broad compatibility.

### X. Reproducibility

Running the `specify` command on the specification must always reproduce the same structure and functions.

**Rationale**: Ensures the specification is the single source of truth and implementation can be reliably regenerated from requirements.

### XI. Testability

All functions MUST be independently testable. State mutations MUST be explicit and traceable.

**Rationale**: Enables comprehensive test coverage, simplifies debugging, and ensures code quality can be verified objectively.

### XII. UV Environment & Dependency Management

The project MUST use `uv` as the environment and dependency manager. All dependencies MUST be listed explicitly in `pyproject.toml` or `requirements.txt` and managed by `uv`.

**Rationale**: Standardizes dependency management, ensures reproducible builds, and leverages `uv`\'s performance benefits for faster environment setup and package resolution.

### XIII. Documentation Capture

Architectural Decision Records (ADRs) and Prompt History Records (PHRs) MUST be automatically generated and maintained by the AI under the `@history` directory for every major workflow command (`/sp.plan`, `/sp.tasks`, `/sp.implement`) to ensure full project transparency and horizontal intelligence accumulation.

**Rationale**: Ensures comprehensive historical context for development decisions and interactions, facilitates knowledge transfer, and provides a traceable audit trail for all significant project changes.


## Development Workflow

### Specification-First Development

1. All features MUST be documented in the specification before implementation
2. Specification changes MUST be reviewed and approved before code changes
3. Implementation MUST reference the specific spec section being implemented

### Test-Driven Development (Recommended)

- Tests SHOULD be written before implementation when feasible
- All business logic functions MUST have corresponding unit tests
- Integration tests SHOULD cover user scenarios from the specification

### Code Review Standards

- All changes MUST reference the specification section they implement
- Reviewers MUST verify alignment with constitution principles
- Violations of constitution principles MUST be documented and justified

## Quality Standards

### Code Organization

- Business logic MUST reside in separate functions from UI code
- Functions MUST have single, clear responsibilities
- Magic values MUST be replaced with named constants

### Error Handling

- All user inputs MUST be validated
- Error messages MUST be clear and actionable
- The application MUST NOT crash from invalid user input

### Documentation

- All public functions MUST have docstrings describing purpose, parameters, and return values
- Complex algorithms MUST include inline comments explaining logic
- The README MUST provide clear usage instructions

### Performance

- Operations MUST complete in reasonable time for console interaction (< 1 second response time)
- Memory usage MUST remain reasonable for typical use (< 100MB for normal task lists)

## Governance

### Constitution Authority

This constitution supersedes all other development practices and guidelines. When conflicts arise between this constitution and other documentation, the constitution takes precedence.

### Amendment Process

1. Proposed amendments MUST be documented with rationale and impact analysis
2. Amendments MUST be approved by project stakeholders
3. Amendments MUST include a migration plan for existing code if applicable
4. All template files MUST be updated to reflect constitutional changes

### Compliance

- All pull requests MUST verify compliance with this constitution
- Complexity violations MUST be justified in the implementation plan
- Regular constitution compliance audits SHOULD be conducted

### Version Semantics

Constitution versions follow semantic versioning:
- **MAJOR**: Backward incompatible governance changes or principle removals/redefinitions
- **MINOR**: New principles added or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

**Version**: 1.2.0 | **Ratified**: 2025-12-03 | **Last Amended**: 2025-12-04
