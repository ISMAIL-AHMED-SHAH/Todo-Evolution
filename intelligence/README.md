# Intelligence Layer - Spec-Kit-Plus Hackathon

**Version:** 1.0.0
**Purpose:** Reusable, modular AI agents and skills for Phase-2 and future hackathon phases

## Overview

This intelligence layer provides clean, production-ready agents and skills for building full-stack web applications following Spec-Kit-Plus methodology. The architecture supports Phase-2 implementation and is designed for future extensibility.

## Architecture

```
intelligence/
├── agents/          # Specialized agent definitions
│   ├── base.py                 # Base agent class
│   ├── rag_knowledge.py        # RAG/documentation agent
│   ├── backend_impl.py         # Backend code generation agent
│   ├── frontend_impl.py        # Frontend code generation agent
│   ├── auth_integration.py     # Authentication integration agent
│   └── database_schema.py      # Database schema agent
│
├── skills/          # Skill implementations
│   ├── rag_skills.py           # Documentation retrieval skills
│   ├── backend_skills.py       # FastAPI/SQLModel skills
│   ├── frontend_skills.py      # Next.js/React skills
│   ├── auth_skills.py          # JWT/Better Auth skills
│   └── db_skills.py            # Database/migration skills
│
├── tools/           # Shared utilities
│   ├── context7_client.py      # Context7 MCP client
│   ├── spec_loader.py          # Specification loader
│   └── jwt_utils.py            # JWT helper utilities
│
├── runners/         # Orchestration utilities
│   ├── agent_runner.py         # Single agent executor
│   └── swarm_coordinator.py    # Multi-agent coordinator
│
└── registry.py      # Central agent registration
```

## Core Agents

### 1. RAG-Knowledge-Agent
**Purpose:** Retrieve documentation and provide architecture guidance

**Skills:**
- `retrieve_docs()` - Fetch library documentation via Context7 MCP
- `summarize_spec()` - Summarize feature specifications
- `architecture_guidance()` - Provide guidance from constitution
- `resolve_api_questions()` - Answer API contract questions
- `get_database_schema()` - Retrieve database schema info

**Example:**
```python
from intelligence.agents import RAGKnowledgeAgent

agent = RAGKnowledgeAgent()

# Retrieve FastAPI documentation
docs = agent.retrieve_docs(library="fastapi", topic="authentication")

# Get architecture guidance
guidance = agent.architecture_guidance(question="What authentication method should I use?")
```

### 2. Backend-Implementation-Agent
**Purpose:** Generate FastAPI + SQLModel backend code

**Skills:**
- `generate_fastapi_routes()` - Generate API route handlers
- `generate_models_sqlmodel()` - Generate SQLModel entity definitions
- `apply_migrations()` - Create migration files
- `create_db_connection()` - Generate database connection code
- `implement_rest_endpoints()` - Implement REST endpoint logic
- `enforce_jwt_security()` - Generate JWT middleware

**Example:**
```python
from intelligence.agents import BackendImplementationAgent

agent = BackendImplementationAgent()

# Generate SQLModel entity
code = agent.generate_models_sqlmodel(
    entity_name="Task",
    fields={
        "user_id": "int",
        "title": "str",
        "description": "Optional[str]",
        "completed": "bool"
    }
)
```

### 3. Frontend-Implementation-Agent
**Purpose:** Generate Next.js + Better Auth frontend code

**Skills:**
- `generate_nextjs_routes()` - Generate Next.js page components
- `auth_ui_components()` - Generate auth UI (signup, signin, etc.)
- `create_frontend_api_client()` - Generate API client
- `connect_to_fastapi_api()` - Generate TypeScript service layer

**Example:**
```python
from intelligence.agents import FrontendImplementationAgent

agent = FrontendImplementationAgent()

# Generate auth components
components = agent.auth_ui_components()
# Returns: {"SignupForm": "...", "SigninForm": "...", ...}

# Generate API client
client_code = agent.create_frontend_api_client(base_url="http://localhost:8000")
```

### 4. Auth-Integration-Agent
**Purpose:** Configure JWT and Better Auth integration

**Skills:**
- `configure_better_auth_jwt()` - Generate Better Auth config
- `jwt_verification_middleware()` - Generate JWT verification
- `sync_frontend_backend_auth()` - Sync auth between frontend/backend
- `enforce_user_isolation()` - Generate user isolation decorator

**Example:**
```python
from intelligence.agents import AuthIntegrationAgent

agent = AuthIntegrationAgent()

# Generate Better Auth configuration
config_files = agent.configure_better_auth_jwt()
# Returns: {"auth.config.ts": "...", ".env.example": "..."}

# Generate JWT middleware
middleware = agent.jwt_verification_middleware()
```

### 5. Database-Schema-Agent
**Purpose:** Manage SQLModel schemas and migrations

**Skills:**
- `evolve_schema()` - Generate schema evolution migrations
- `update_tasks_table()` - Update tasks table schema
- `generate_migrations()` - Generate initial migrations
- `create_indexes()` - Generate index creation migrations
- `setup_foreign_keys()` - Generate foreign key migrations

**Example:**
```python
from intelligence.agents import DatabaseSchemaAgent

agent = DatabaseSchemaAgent()

# Generate migrations for entities
migrations = agent.generate_migrations([
    {"name": "User", "fields": {"email": "String", "password_hash": "String"}},
    {"name": "Task", "fields": {"title": "String", "completed": "Boolean"}}
])
```

## Running Agents

### Single Agent Execution

```python
from intelligence.runners import AgentRunner
from intelligence.agents import RAGKnowledgeAgent

runner = AgentRunner()
agent = RAGKnowledgeAgent()

result = runner.run(agent, {
    "skill": "retrieve_docs",
    "params": {"library": "fastapi", "topic": "authentication"}
})

print(result)
```

### Batch Execution

```python
runner = AgentRunner()
agent = BackendImplementationAgent()

tasks = [
    {"skill": "generate_models_sqlmodel", "params": {"entity_name": "User", ...}},
    {"skill": "generate_models_sqlmodel", "params": {"entity_name": "Task", ...}},
]

results = runner.run_batch(agent, tasks, verbose=True)
```

### Multi-Agent Coordination

```python
from intelligence.runners import SwarmCoordinator
from intelligence.agents import RAGKnowledgeAgent, BackendImplementationAgent

coordinator = SwarmCoordinator()
coordinator.register_agent(RAGKnowledgeAgent())
coordinator.register_agent(BackendImplementationAgent())

# Sequential workflow
workflow = [
    {
        "agent": "RAG-Knowledge-Agent",
        "skill": "get_database_schema",
        "params": {}
    },
    {
        "agent": "Backend-Implementation-Agent",
        "skill": "generate_models_sqlmodel",
        "params": {"entity_name": "Task", ...}
    }
]

results = coordinator.run_sequential(workflow, verbose=True)
```

### Parallel Execution

```python
# Run multiple agents in parallel
tasks = [
    {"agent": "Backend-Implementation-Agent", "skill": "generate_fastapi_routes", ...},
    {"agent": "Frontend-Implementation-Agent", "skill": "auth_ui_components", ...}
]

results = coordinator.run_parallel(tasks)
```

### Pipeline Execution

```python
# Data flows from one agent to the next
pipeline = [
    {
        "agent": "RAG-Knowledge-Agent",
        "skill": "get_database_schema"
    },
    {
        "agent": "Database-Schema-Agent",
        "skill": "generate_migrations",
        "params_from_previous": ["entities"]
    }
]

final_result = coordinator.run_pipeline(pipeline, verbose=True)
```

## Using the Global Registry

```python
from intelligence.registry import get_agent, list_agents

# Get specific agent
agent = get_agent("RAG-Knowledge-Agent")

# List all agents
agents = list_agents()
for agent_info in agents:
    print(f"{agent_info['name']}: {agent_info['description']}")
    print(f"  Skills: {', '.join(agent_info['skills'])}")
```

## Integration with Spec-Kit-Plus

### Load Specifications

```python
from intelligence.tools import SpecLoader

loader = SpecLoader()

# Load feature specification
spec = loader.load_spec("1-fullstack-web-app")
print(spec["content"])

# Load API contract
api_contract = loader.load_api_contract()
print(api_contract["endpoints"])

# Load constitution
constitution = loader.load_constitution()
print(constitution["principles"])
```

### Work with Context7 MCP

```python
from intelligence.tools import Context7Client

client = Context7Client()

# Resolve library ID
library_id = client.resolve_library_id("fastapi")  # "/tiangolo/fastapi"

# Get documentation
docs = client.get_library_docs(library_id, topic="authentication", mode="code")
```

### JWT Utilities

```python
from intelligence.tools import JWTHelper

jwt_helper = JWTHelper(secret="your-secret")

# Create token
token = jwt_helper.create_token(user_id=1, email="user@example.com")

# Verify token
payload = jwt_helper.verify_token(token)
print(payload["user_id"])  # 1

# Extract user ID
user_id = jwt_helper.extract_user_id(token)
```

## Phase-2 Implementation Workflow

### 1. Setup Phase
```python
from intelligence.agents import BackendImplementationAgent, FrontendImplementationAgent

backend_agent = BackendImplementationAgent()
frontend_agent = FrontendImplementationAgent()

# Generate database connection
db_code = backend_agent.create_db_connection()

# Generate API client
api_client_code = frontend_agent.create_frontend_api_client()
```

### 2. Authentication Phase
```python
from intelligence.agents import AuthIntegrationAgent

auth_agent = AuthIntegrationAgent()

# Configure Better Auth
config_files = auth_agent.configure_better_auth_jwt()

# Generate JWT middleware
middleware = auth_agent.jwt_verification_middleware()

# Generate frontend auth components
auth_components = frontend_agent.auth_ui_components()
```

### 3. Backend Implementation
```python
from intelligence.tools import SpecLoader

loader = SpecLoader()
api_contract = loader.load_api_contract()

# Generate models
task_model = backend_agent.generate_models_sqlmodel(
    entity_name="Task",
    fields={"user_id": "int", "title": "str", "completed": "bool"}
)

# Generate routes
routes = backend_agent.generate_fastapi_routes(
    resource="tasks",
    endpoints=api_contract["endpoints"]
)
```

### 4. Frontend Implementation
```python
# Generate pages
pages = frontend_agent.generate_nextjs_routes([
    {"name": "Tasks", "route": "/tasks"},
    {"name": "TaskDetail", "route": "/tasks/{id}"}
])

# Generate task service
task_service = frontend_agent.connect_to_fastapi_api(
    endpoints=api_contract["endpoints"]
)
```

## Future Extensibility

### Adding New Agents

```python
from intelligence.agents.base import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="My-Custom-Agent",
            description="Custom agent for specific tasks"
        )

    def execute(self, task):
        # Implement custom logic
        pass

    def _list_skills(self):
        return ["custom_skill_1", "custom_skill_2"]

# Register with global registry
from intelligence.registry import registry
registry.register(MyCustomAgent())
```

### Adding New Skills

```python
class CustomSkills:
    def custom_operation(self, params):
        # Implement skill logic
        return {"result": "..."}

# Use in agent
class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="My-Agent", description="...")
        self.skills = CustomSkills()

    def execute(self, task):
        if task["skill"] == "custom_operation":
            return self.skills.custom_operation(task["params"])
```

## Best Practices

1. **Always use agents through the registry** - Ensures consistency
2. **Use SwarmCoordinator for multi-agent tasks** - Better orchestration
3. **Log execution for debugging** - Use `verbose=True`
4. **Follow constitution principles** - Load and validate against constitution
5. **Keep agents stateless** - All state in task params
6. **Use type hints** - All code is fully typed
7. **Document custom extensions** - Maintain this README

## Testing

```python
# Test individual agents
agent = RAGKnowledgeAgent()
result = agent.retrieve_docs(library="fastapi")
assert "error" not in result

# Test coordinated execution
coordinator = SwarmCoordinator()
coordinator.register_agent(RAGKnowledgeAgent())
coordinator.register_agent(BackendImplementationAgent())

workflow = [...]
results = coordinator.run_sequential(workflow)
assert all("error" not in r for r in results)
```

## Troubleshooting

### Agent not found
```python
from intelligence.registry import list_agents
agents = list_agents()
print([a["name"] for a in agents])
```

### Skill execution failure
```python
runner = AgentRunner()
result = runner.run(agent, task, verbose=True)
print(runner.get_statistics())
```

### Context7 MCP issues
```python
from intelligence.tools import Context7Client
client = Context7Client()
library_id = client.resolve_library_id("your-library")
print(f"Resolved to: {library_id}")
```

## License

Part of Spec-Kit-Plus Hackathon Project - Phase 2

## Contributors

Generated by Claude Code following Spec-Driven Development methodology.
