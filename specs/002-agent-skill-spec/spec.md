# Feature Specification: Subagents and Skills for Hackathon Phases

**Feature Branch**: `002-agent-skill-spec`
**Created**: 2025-12-05
**Status**: Draft
**Input**: User description: "before going forwart Create a specification for Subagents and Skills to be used in this project
and all future hackathon phases.

Goal:
Design reusable intelligence modules using Claude Code Subagents + Skills
that assist with:
- Specification refinement
- Code generation
- UV environment management
- Task execution monitoring
- PHR/ADR generation assistance
- Testing and validation
- RAG integration (for future phases)
- Book/Docs generation support

Requirements:
1. Define 3–5 Subagents, each with a clear domain (e.g., Spec Agent,
   Code Agent, QA/Testing Agent, Doc Agent, RAG Agent).
2. Define Skills for each agent with:
   - Purpose
   - Inputs
   - Outputs
   - Behavior
3. All agents must be reusable and extendable in later phases (FastAPI,
   Next.js, RAG, Vector DB, K8s).
4. Subagents must strictly follow the project constitution and support
   automatic PHR/ADR workflows.
5. Output the full structured specification for these agents + skills.

Produce:
- Subagent definitions
- Skill definitions
- Usage examples
- How they integrate into the current Todo CLI project"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Specification Refinement with Spec Agent (Priority: P1)

As a developer, I want to use a dedicated Spec Agent to refine and validate feature specifications, ensuring clarity, completeness, and adherence to project constitution.

**Why this priority**: Essential for maintaining high-quality specifications, reducing ambiguity, and ensuring successful downstream development.

**Independent Test**: A new specification can be processed by the Spec Agent, and the agent's output (e.g., clarification questions, validation report) can be reviewed for accuracy and adherence to rules.

**Acceptance Scenarios**:

1. **Given** a draft `spec.md` exists, **When** I invoke the Spec Agent, **Then** the agent analyzes the spec for completeness, consistency, and constitutional compliance.
2. **Given** the Spec Agent identifies ambiguities or missing requirements, **When** it presents clarification questions, **Then** I can provide answers to update the spec.

---

### User Story 2 - Code Generation Assistance with Code Agent (Priority: P1)

As a developer, I want to leverage a Code Agent to generate boilerplate, implement basic functionalities, or refactor existing code based on a given plan or task, accelerating development.

**Why this priority**: Directly contributes to increased development velocity and consistency in code generation.

**Independent Test**: A set of tasks or a code plan can be provided to the Code Agent, and the generated code can be compiled and run (if applicable) or reviewed for correctness and adherence to coding standards.

**Acceptance Scenarios**:

1. **Given** a task defined in `tasks.md`, **When** I invoke the Code Agent, **Then** the agent generates or modifies code to fulfill the task.
2. **Given** an existing code snippet, **When** I ask the Code Agent to refactor it, **Then** the agent applies the refactoring while preserving functionality.

---

### User Story 3 - UV Environment Management with UV Agent (Priority: P2)

As a developer, I want an agent to assist with `uv` environment setup, dependency management, and script execution, simplifying project setup and ensuring reproducible environments.

**Why this priority**: Automates common development tasks, reduces setup time, and ensures compliance with the UV environment principle.

**Independent Test**: A project can be initialized with the UV Agent, and the agent's output (e.g., virtual environment creation, dependency installation) can be verified for correctness.

**Acceptance Scenarios**:

1. **Given** a new project, **When** I invoke the UV Agent with an environment setup request, **Then** `uv` is used to create a virtual environment and install specified dependencies.
2. **Given** a `pyproject.toml` file, **When** I ask the UV Agent to update dependencies, **Then** it uses `uv` to sync the environment.

---

### User Story 4 - Documentation Generation with Doc Agent (Priority: P2)

As a developer, I want a Doc Agent to help generate documentation artifacts like PHRs, ADRs, and project guides, ensuring comprehensive knowledge capture and adherence to documentation standards.

**Why this priority**: Supports the Documentation Capture principle, ensuring transparent project history and intelligent knowledge accumulation.

**Independent Test**: After a major workflow command, the Doc Agent can be invoked to generate a PHR or ADR draft, which can then be reviewed for completeness and accuracy.

**Acceptance Scenarios**:

1. **Given** a completed workflow (e.g., `/sp.plan`), **When** I invoke the Doc Agent to generate a PHR, **Then** a structured PHR file is created in the correct history path.
2. **Given** an architecturally significant decision, **When** I ask the Doc Agent to draft an ADR, **Then** a templated ADR is prepared for review.

---

### Edge Cases

- What happens if an agent is invoked with invalid inputs or insufficient context? (Agents should provide clear error messages and guidance.)
- How do agents handle conflicting instructions or ambiguous requests? (Agents should seek clarification from the user or fallback to conservative defaults.)
- How are agent failures communicated to the user? (Clear, actionable error reporting.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Each Subagent MUST have a defined purpose, inputs, outputs, and behavior.
- **FR-002**: Subagents MUST be reusable across different project phases (CLI, FastAPI, Next.js, etc.).
- **FR-003**: Subagents MUST adhere to the project constitution, especially regarding environment and documentation.
- **FR-004**: Subagents MUST support automatic generation of PHRs and suggest ADRs for significant decisions.
- **FR-005**: The Spec Agent MUST be able to analyze and refine specifications.
- **FR-006**: The Code Agent MUST be able to generate and refactor code.
- **FR-007**: The UV Agent MUST be able to manage `uv` environments and dependencies.
- **FR-008**: The Doc Agent MUST be able to assist with PHR and ADR generation.
- **FR-009**: The future RAG Agent MUST integrate with RAG systems for knowledge retrieval.

### Key Entities *(include if feature involves data)*

- **Subagent**: An autonomous AI entity with a specific domain and set of skills.
    - `name`: Unique identifier (e.g., "Spec Agent").
    - `domain`: Area of expertise (e.g., "Specification Refinement").
    - `skills`: List of callable skills.
- **Skill**: A specific capability or action an agent can perform.
    - `name`: Unique identifier (e.g., "refine_spec").
    - `purpose`: What the skill achieves.
    - `inputs`: Parameters required.
    - `outputs`: Expected results.
    - `behavior`: How the skill operates.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 3 distinct Subagents are defined with clear responsibilities and skills.
- **SC-002**: All defined Subagents and Skills are compatible with the project constitution.
- **SC-003**: Usage examples demonstrate how each agent/skill assists with its defined purpose.
- **SC-004**: The specification explicitly addresses how agents will support future project phases (FastAPI, Next.js, etc.).
- **SC-005**: All agents implicitly or explicitly support automatic PHR generation and ADR suggestion workflows.

### Assumptions

- This specification defines the *design* of subagents and skills, not their *implementation*.
- Agents will be invoked via the `Task` tool or similar mechanisms within the Claude Code environment.
- The underlying AI model supports the capabilities described for each agent and skill.

### Implementation Constraints

- **Agent Framework**: Claude Code Agent SDK.
- **Constitution Adherence**: All agents and skills MUST operate within the boundaries defined by the project constitution.
- **Modularity**: Agents and skills should be designed for independent development and easy integration into different project phases.
- **Extendability**: The design must allow for adding new agents/skills and enhancing existing ones without breaking current functionality.

### Subagent and Skill Definitions

```markdown
# Subagent: Spec Agent
## Purpose
To refine and validate feature specifications, ensuring clarity, completeness, and adherence to project constitution.

## Skills
### refine_spec
- Purpose: Analyze a given specification (spec.md) for completeness, clarity, and adherence to constitutional principles.
- Inputs: `spec_path` (str) - path to the spec file; `constitution_path` (str) - path to the constitution file.
- Outputs: `validation_report` (str) - detailed report of findings; `clarification_questions` (list of dict) - list of questions for the user if ambiguities found.
- Behavior: Reads spec and constitution, applies validation rules (e.g., no implementation details in spec, all mandatory sections present, measurable success criteria), identifies gaps/ambiguities.

### generate_acceptance_criteria
- Purpose: Generate detailed, testable acceptance criteria for user stories within a specification.
- Inputs: `spec_path` (str) - path to the spec file; `user_story_id` (str, optional) - specific user story ID to focus on.
- Outputs: `acceptance_criteria` (str) - markdown-formatted acceptance criteria.
- Behavior: Reads user stories from the spec and generates Given-When-Then scenarios.

# Subagent: Code Agent
## Purpose
To assist with code generation, boilerplate creation, and refactoring based on tasks and plans.

## Skills
### generate_code_from_task
- Purpose: Generate code snippets or full file contents based on a given task description.
- Inputs: `task_description` (str) - detailed task; `context` (str, optional) - relevant code context or file paths.
- Outputs: `generated_code` (str) - proposed code; `file_path` (str) - suggested file path.
- Behavior: Interprets task, generates code adhering to coding standards and project structure, and suggests placement.

### refactor_code
- Purpose: Refactor existing code for readability, performance, or adherence to design patterns.
- Inputs: `file_path` (str) - path to code file; `refactoring_goal` (str) - description of desired refactoring.
- Outputs: `refactored_code` (str) - proposed refactored code; `diff` (str) - diff of changes.
- Behavior: Reads code, applies refactoring logic based on goal, and generates proposed changes.

# Subagent: UV Agent
## Purpose
To manage `uv` environments and project dependencies, ensuring reproducible and efficient development setups.

## Skills
### setup_uv_environment
- Purpose: Create and configure a `uv` virtual environment for the project.
- Inputs: `project_root` (str) - path to project root; `python_version` (str, optional) - desired Python version.
- Outputs: `status` (str) - success/failure message; `venv_path` (str) - path to created environment.
- Behavior: Calls `uv venv` and activates it, configuring the environment.

### install_dependencies
- Purpose: Install project dependencies using `uv pip install`.
- Inputs: `requirements_path` (str, optional) - path to `requirements.txt`; `pyproject_path` (str, optional) - path to `pyproject.toml`.
- Outputs: `status` (str) - success/failure message; `installed_packages` (list of str) - list of installed packages.
- Behavior: Reads dependency files and executes `uv pip install`.

# Subagent: Doc Agent
## Purpose
To automate and assist with the generation of documentation artifacts (PHRs, ADRs, project guides).

## Skills
### generate_phr
- Purpose: Generate a Prompt History Record (PHR) based on a completed prompt/response interaction.
- Inputs: `prompt_text` (str); `response_text` (str); `stage` (str); `feature_name` (str, optional); `command` (str, optional).
- Outputs: `phr_path` (str) - path to the created PHR file.
- Behavior: Populates PHR template, allocates ID, computes path, writes file to `history/prompts/`.

### suggest_adr
- Purpose: Suggest the creation of an Architectural Decision Record (ADR) for significant decisions.
- Inputs: `decision_context` (str) - description of the decision; `impact` (str) - identified impact; `alternatives` (list of str, optional).
- Outputs: `adr_suggestion` (str) - formatted suggestion message for the user.
- Behavior: Evaluates decision context against ADR significance criteria and formulates a suggestion.
```