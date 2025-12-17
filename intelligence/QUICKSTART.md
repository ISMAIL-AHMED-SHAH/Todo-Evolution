# Intelligence Layer - Quick Start Guide

Get started with the Spec-Kit-Plus Intelligence Layer in 5 minutes.

## Installation

No additional installation required - the intelligence layer uses Python standard library and integrates with existing project dependencies.

## 1. List Available Agents

```python
from intelligence.registry import list_agents

agents = list_agents()
for agent in agents:
    print(f"{agent['name']}: {agent['description']}")
```

**Output:**
```
RAG-Knowledge-Agent: Retrieves documentation and provides architecture guidance
Backend-Implementation-Agent: Generates FastAPI routes, SQLModel models, and backend infrastructure
Frontend-Implementation-Agent: Generates Next.js pages, components, and API client integration
Auth-Integration-Agent: Configures Better Auth, JWT verification, and user isolation enforcement
Database-Schema-Agent: Manages SQLModel schemas, migrations, and database operations
```

## 2. Use a Single Agent

```python
from intelligence.agents import RAGKnowledgeAgent

# Create agent
agent = RAGKnowledgeAgent()

# Retrieve documentation
docs = agent.retrieve_docs(
    library="fastapi",
    topic="authentication",
    mode="code"
)

print(docs)
```

## 3. Generate Backend Code

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

print(code)
# Save to file
with open("backend/src/models/task.py", "w") as f:
    f.write(code)
```

## 4. Generate Frontend Code

```python
from intelligence.agents import FrontendImplementationAgent

agent = FrontendImplementationAgent()

# Generate authentication components
components = agent.auth_ui_components()

# Save components
for name, code in components.items():
    filename = f"frontend/src/components/{name}.tsx"
    with open(filename, "w") as f:
        f.write(code)
    print(f"Created: {filename}")
```

## 5. Run Multiple Agents in Sequence

```python
from intelligence.runners import SwarmCoordinator
from intelligence.agents import (
    RAGKnowledgeAgent,
    BackendImplementationAgent,
    FrontendImplementationAgent
)

# Create coordinator
coordinator = SwarmCoordinator()

# Register agents
coordinator.register_agent(RAGKnowledgeAgent())
coordinator.register_agent(BackendImplementationAgent())
coordinator.register_agent(FrontendImplementationAgent())

# Define workflow
workflow = [
    {
        "agent": "RAG-Knowledge-Agent",
        "skill": "summarize_spec",
        "params": {"feature_name": "1-fullstack-web-app"}
    },
    {
        "agent": "Backend-Implementation-Agent",
        "skill": "generate_models_sqlmodel",
        "params": {
            "entity_name": "Task",
            "fields": {"user_id": "int", "title": "str", "completed": "bool"}
        }
    },
    {
        "agent": "Frontend-Implementation-Agent",
        "skill": "create_frontend_api_client",
        "params": {"base_url": "http://localhost:8000"}
        }
]

# Execute workflow
results = coordinator.run_sequential(workflow, verbose=True)
print(f"Completed {len(results)} tasks")
```

## 6. Work with Specifications

```python
from intelligence.tools import SpecLoader

loader = SpecLoader()

# Load feature specification
spec = loader.load_spec("1-fullstack-web-app")
print(f"Feature: {spec['feature']}")
print(f"Status: {spec['metadata'].get('status')}")

# Load API contract
api_contract = loader.load_api_contract()
print(f"Endpoints: {len(api_contract['endpoints'])}")

# Load constitution
constitution = loader.load_constitution()
print(f"Principles: {len(constitution['principles'])}")
```

## 7. Generate Authentication Setup

```python
from intelligence.agents import AuthIntegrationAgent

agent = AuthIntegrationAgent()

# Generate Better Auth configuration
config_files = agent.configure_better_auth_jwt()

# Save configuration files
for filename, code in config_files.items():
    print(f"Generated: {filename}")

# Generate JWT middleware for backend
middleware = agent.jwt_verification_middleware()

# Save middleware
with open("backend/src/auth/middleware.py", "w") as f:
    f.write(middleware)
```

## 8. Generate Database Migrations

```python
from intelligence.agents import DatabaseSchemaAgent

agent = DatabaseSchemaAgent()

# Generate migrations for entities
migrations = agent.generate_migrations([
    {
        "name": "User",
        "fields": {
            "email": "String",
            "password_hash": "String"
        }
    },
    {
        "name": "Task",
        "fields": {
            "user_id": "Integer",
            "title": "String",
            "description": "String",
            "completed": "Boolean"
        }
    }
])

# Save migrations
for name, code in migrations.items():
    filename = f"backend/alembic/versions/{name}.py"
    print(f"Generated: {filename}")
```

## 9. Run Agents in Parallel

```python
from intelligence.runners import SwarmCoordinator

coordinator = SwarmCoordinator(max_workers=3)

# Register all agents
from intelligence.registry import registry
for agent in registry._agents.values():
    coordinator.register_agent(agent)

# Run tasks in parallel
tasks = [
    {
        "agent": "Backend-Implementation-Agent",
        "skill": "enforce_jwt_security",
        "params": {}
    },
    {
        "agent": "Frontend-Implementation-Agent",
        "skill": "auth_ui_components",
        "params": {}
    },
    {
        "agent": "Database-Schema-Agent",
        "skill": "create_indexes",
        "params": {
            "table": "tasks",
            "indexes": [{"columns": ["user_id"], "name": "idx_tasks_user_id"}]
        }
    }
]

results = coordinator.run_parallel(tasks, verbose=True)
```

## 10. Complete Phase-2 Setup Example

```python
"""
Complete Phase-2 setup workflow
"""
from intelligence.runners import SwarmCoordinator
from intelligence.registry import registry

# Initialize coordinator with all agents
coordinator = SwarmCoordinator()
for agent in registry._agents.values():
    coordinator.register_agent(agent)

# Phase 1: Setup & Configuration
phase1 = [
    {
        "agent": "Auth-Integration-Agent",
        "skill": "configure_better_auth_jwt",
        "params": {}
    },
    {
        "agent": "Backend-Implementation-Agent",
        "skill": "create_db_connection",
        "params": {}
    }
]

# Phase 2: Backend Implementation
phase2 = [
    {
        "agent": "Backend-Implementation-Agent",
        "skill": "generate_models_sqlmodel",
        "params": {
            "entity_name": "Task",
            "fields": {
                "user_id": "int",
                "title": "str",
                "description": "Optional[str]",
                "completed": "bool"
            }
        }
    },
    {
        "agent": "Backend-Implementation-Agent",
        "skill": "generate_fastapi_routes",
        "params": {
            "resource": "tasks",
            "endpoints": [
                {"method": "GET", "path": "/api/{user_id}/tasks"},
                {"method": "POST", "path": "/api/{user_id}/tasks"}
            ]
        }
    }
]

# Phase 3: Frontend Implementation
phase3 = [
    {
        "agent": "Frontend-Implementation-Agent",
        "skill": "auth_ui_components",
        "params": {}
    },
    {
        "agent": "Frontend-Implementation-Agent",
        "skill": "create_frontend_api_client",
        "params": {"base_url": "http://localhost:8000"}
    }
]

# Execute all phases
print("Phase 1: Setup & Configuration")
results1 = coordinator.run_sequential(phase1, verbose=True)

print("\nPhase 2: Backend Implementation")
results2 = coordinator.run_parallel(phase2, verbose=True)

print("\nPhase 3: Frontend Implementation")
results3 = coordinator.run_parallel(phase3, verbose=True)

print(f"\n✓ Completed {len(results1) + len(results2) + len(results3)} tasks")
```

## Next Steps

1. **Read the full README**: `intelligence/README.md`
2. **Run examples**: `python intelligence/examples.py`
3. **Customize agents**: Extend `BaseAgent` for custom needs
4. **Add new skills**: Create skill modules in `intelligence/skills/`
5. **Integrate with CI/CD**: Use agents in automated workflows

## Common Patterns

### Pattern 1: Generate and Save Code
```python
from intelligence.agents import BackendImplementationAgent

agent = BackendImplementationAgent()
code = agent.generate_models_sqlmodel(...)

with open("output.py", "w") as f:
    f.write(code)
```

### Pattern 2: Load Spec, Generate Code
```python
from intelligence.tools import SpecLoader
from intelligence.agents import BackendImplementationAgent

loader = SpecLoader()
spec = loader.load_spec("1-fullstack-web-app")

agent = BackendImplementationAgent()
# Use spec data to generate code
```

### Pattern 3: Multi-Agent Pipeline
```python
from intelligence.runners import SwarmCoordinator

coordinator = SwarmCoordinator()
# Register agents...

pipeline = [
    {"agent": "Agent-1", "skill": "task1"},
    {"agent": "Agent-2", "skill": "task2", "params_from_previous": ["data"]}
]

result = coordinator.run_pipeline(pipeline)
```

## Troubleshooting

**Problem:** Agent not found
```python
from intelligence.registry import list_agents
print([a["name"] for a in list_agents()])
```

**Problem:** Skill not working
```python
agent = RAGKnowledgeAgent()
print(agent._list_skills())  # See available skills
```

**Problem:** Can't load spec
```python
from intelligence.tools import SpecLoader
loader = SpecLoader()
try:
    spec = loader.load_spec("feature-name")
except FileNotFoundError as e:
    print(f"Spec not found: {e}")
```

## Support

For questions or issues:
1. Check the full README: `intelligence/README.md`
2. Run examples: `python intelligence/examples.py`
3. Review agent source code in `intelligence/agents/`

---

**Built with Spec-Kit-Plus methodology for Phase-2 Hackathon**
