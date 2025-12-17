"""
Intelligence Layer Examples

Demonstrates usage patterns for agents and skills.
"""

from intelligence.agents import (
    RAGKnowledgeAgent,
    BackendImplementationAgent,
    FrontendImplementationAgent,
    AuthIntegrationAgent,
    DatabaseSchemaAgent
)
from intelligence.runners import AgentRunner, SwarmCoordinator
from intelligence.registry import get_agent, list_agents
from intelligence.tools import SpecLoader, Context7Client, JWTHelper


def example_1_single_agent():
    """Example 1: Using a single agent directly."""
    print("=== Example 1: Single Agent ===\n")

    agent = RAGKnowledgeAgent()

    # Retrieve documentation
    result = agent.retrieve_docs(library="fastapi", topic="authentication")
    print(f"Retrieved docs for FastAPI authentication")
    print(f"Library ID: {result.get('library_id', 'N/A')}\n")


def example_2_agent_runner():
    """Example 2: Using AgentRunner for batch execution."""
    print("=== Example 2: Agent Runner ===\n")

    runner = AgentRunner()
    agent = BackendImplementationAgent()

    tasks = [
        {
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
            "skill": "generate_models_sqlmodel",
            "params": {
                "entity_name": "User",
                "fields": {
                    "email": "str",
                    "password_hash": "str"
                }
            }
        }
    ]

    results = runner.run_batch(agent, tasks, verbose=True)
    print(f"\nGenerated {len(results)} models")
    print(f"Statistics: {runner.get_statistics()}\n")


def example_3_swarm_sequential():
    """Example 3: Sequential workflow with SwarmCoordinator."""
    print("=== Example 3: Sequential Workflow ===\n")

    coordinator = SwarmCoordinator()

    # Register agents
    coordinator.register_agent(RAGKnowledgeAgent())
    coordinator.register_agent(BackendImplementationAgent())

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
                "fields": {
                    "user_id": "int",
                    "title": "str",
                    "completed": "bool"
                }
            }
        }
    ]

    results = coordinator.run_sequential(workflow, verbose=True)
    print(f"\nCompleted {len(results)} workflow steps\n")


def example_4_swarm_parallel():
    """Example 4: Parallel execution with SwarmCoordinator."""
    print("=== Example 4: Parallel Execution ===\n")

    coordinator = SwarmCoordinator(max_workers=3)

    # Register agents
    coordinator.register_agent(BackendImplementationAgent())
    coordinator.register_agent(FrontendImplementationAgent())
    coordinator.register_agent(AuthIntegrationAgent())

    # Define parallel tasks
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
            "agent": "Auth-Integration-Agent",
            "skill": "configure_better_auth_jwt",
            "params": {}
        }
    ]

    results = coordinator.run_parallel(tasks, verbose=True)
    print(f"\nCompleted {len(results)} parallel tasks\n")


def example_5_global_registry():
    """Example 5: Using the global registry."""
    print("=== Example 5: Global Registry ===\n")

    # List all agents
    agents = list_agents()
    print("Available agents:")
    for agent_info in agents:
        print(f"  - {agent_info['name']}")
        print(f"    {agent_info['description']}")
        print(f"    Skills: {', '.join(agent_info['skills'][:3])}...")
        print()

    # Get specific agent
    agent = get_agent("RAG-Knowledge-Agent")
    if agent:
        print(f"Retrieved agent: {agent.name}\n")


def example_6_spec_loader():
    """Example 6: Loading specifications."""
    print("=== Example 6: Specification Loader ===\n")

    loader = SpecLoader()

    try:
        # Load feature spec
        spec = loader.load_spec("1-fullstack-web-app")
        print(f"Loaded spec: {spec['feature']}")
        print(f"Status: {spec['metadata'].get('status', 'Unknown')}")

        # Load constitution
        constitution = loader.load_constitution()
        print(f"\nConstitution has {len(constitution['principles'])} principles")
        print(f"First principle: {constitution['principles'][0]['title']}")

    except FileNotFoundError as e:
        print(f"Spec not found: {e}\n")


def example_7_context7_client():
    """Example 7: Using Context7 client."""
    print("=== Example 7: Context7 Client ===\n")

    client = Context7Client()

    # Resolve library IDs
    libraries = ["fastapi", "nextjs", "sqlmodel"]

    for lib in libraries:
        library_id = client.resolve_library_id(lib)
        print(f"{lib} -> {library_id}")

    # Get documentation
    docs = client.get_library_docs("/tiangolo/fastapi", topic="routing")
    print(f"\nRetrieved docs: {docs['library_id']}\n")


def example_8_jwt_helper():
    """Example 8: Working with JWT tokens."""
    print("=== Example 8: JWT Helper ===\n")

    jwt_helper = JWTHelper(secret="test-secret-key")

    # Create token
    token = jwt_helper.create_token(user_id=123, email="user@example.com")
    print(f"Created token: {token[:50]}...")

    # Verify token
    payload = jwt_helper.verify_token(token)
    if payload:
        print(f"Verified token for user: {payload['email']}")
        print(f"User ID: {payload['user_id']}")

    # Extract user ID
    user_id = jwt_helper.extract_user_id(token)
    print(f"Extracted user_id: {user_id}\n")


def example_9_full_backend_generation():
    """Example 9: Full backend code generation workflow."""
    print("=== Example 9: Full Backend Generation ===\n")

    backend_agent = BackendImplementationAgent()
    db_agent = DatabaseSchemaAgent()

    # Generate model
    task_model = backend_agent.generate_models_sqlmodel(
        entity_name="Task",
        fields={
            "user_id": "int",
            "title": "str",
            "description": "Optional[str]",
            "completed": "bool"
        }
    )
    print("Generated Task model")

    # Generate routes
    routes = backend_agent.generate_fastapi_routes(
        resource="tasks",
        endpoints=[
            {"method": "GET", "path": "/api/{user_id}/tasks"},
            {"method": "POST", "path": "/api/{user_id}/tasks"}
        ]
    )
    print("Generated FastAPI routes")

    # Generate migrations
    migrations = db_agent.generate_migrations([
        {
            "name": "Task",
            "fields": {
                "user_id": "Integer",
                "title": "String",
                "completed": "Boolean"
            }
        }
    ])
    print(f"Generated {len(migrations)} migration(s)\n")


def example_10_full_frontend_generation():
    """Example 10: Full frontend code generation workflow."""
    print("=== Example 10: Full Frontend Generation ===\n")

    frontend_agent = FrontendImplementationAgent()

    # Generate pages
    pages = frontend_agent.generate_nextjs_routes([
        {"name": "Tasks", "route": "/tasks"},
        {"name": "Signin", "route": "/signin"},
        {"name": "Signup", "route": "/signup"}
    ])
    print(f"Generated {len(pages)} pages")

    # Generate auth components
    auth_components = frontend_agent.auth_ui_components()
    print(f"Generated {len(auth_components)} auth components")

    # Generate API client
    api_client = frontend_agent.create_frontend_api_client()
    print(f"Generated API client ({len(api_client)} characters)\n")


def run_all_examples():
    """Run all examples."""
    examples = [
        example_1_single_agent,
        example_2_agent_runner,
        example_3_swarm_sequential,
        example_4_swarm_parallel,
        example_5_global_registry,
        example_6_spec_loader,
        example_7_context7_client,
        example_8_jwt_helper,
        example_9_full_backend_generation,
        example_10_full_frontend_generation
    ]

    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"Example {i} failed: {e}\n")

        print("-" * 60)
        print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Intelligence Layer Examples")
    print("=" * 60 + "\n")

    run_all_examples()

    print("\nAll examples completed!")
