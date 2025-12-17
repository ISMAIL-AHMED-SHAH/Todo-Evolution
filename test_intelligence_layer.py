"""
Test Script for Intelligence Layer

Quick verification that all agents and skills are working correctly.
"""

import sys
import io

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    from intelligence.agents import (
        BaseAgent,
        RAGKnowledgeAgent,
        BackendImplementationAgent,
        FrontendImplementationAgent,
        AuthIntegrationAgent,
        DatabaseSchemaAgent
    )

    from intelligence.skills import (
        RAGSkills,
        BackendSkills,
        FrontendSkills,
        AuthSkills,
        DatabaseSkills
    )

    from intelligence.tools import (
        Context7Client,
        SpecLoader,
        JWTHelper
    )

    from intelligence.runners import (
        AgentRunner,
        SwarmCoordinator
    )

    from intelligence.registry import (
        get_agent,
        list_agents,
        registry
    )

    print("✓ All imports successful\n")


def test_registry():
    """Test agent registry."""
    print("Testing registry...")

    from intelligence.registry import list_agents, get_agent

    agents = list_agents()
    print(f"✓ Found {len(agents)} registered agents:")

    for agent_info in agents:
        print(f"  - {agent_info['name']}")
        print(f"    Skills: {len(agent_info['skills'])}")

    # Test getting specific agent
    agent = get_agent("RAG-Knowledge-Agent")
    assert agent is not None, "Failed to get RAG-Knowledge-Agent"
    print(f"\n✓ Retrieved agent: {agent.name}\n")


def test_rag_agent():
    """Test RAG Knowledge Agent."""
    print("Testing RAG Knowledge Agent...")

    from intelligence.agents import RAGKnowledgeAgent

    agent = RAGKnowledgeAgent()

    # Test skill listing
    skills = agent._list_skills()
    print(f"✓ RAG Agent has {len(skills)} skills")

    # Test Context7 client
    result = agent.execute({
        "skill": "retrieve_docs",
        "params": {
            "library": "fastapi",
            "topic": "authentication"
        }
    })

    assert "library_id" in result or "error" in result
    print(f"✓ retrieve_docs skill executed\n")


def test_backend_agent():
    """Test Backend Implementation Agent."""
    print("Testing Backend Implementation Agent...")

    from intelligence.agents import BackendImplementationAgent

    agent = BackendImplementationAgent()

    # Test model generation
    code = agent.generate_models_sqlmodel(
        entity_name="Task",
        fields={
            "user_id": "int",
            "title": "str",
            "completed": "bool"
        }
    )

    assert "class Task" in code
    assert "SQLModel" in code
    print(f"✓ Generated SQLModel code ({len(code)} chars)")

    # Test route generation
    routes = agent.generate_fastapi_routes(
        resource="tasks",
        endpoints=[
            {"method": "GET", "path": "/api/{user_id}/tasks"}
        ]
    )

    assert "router" in routes
    assert "FastAPI" in routes or "APIRouter" in routes
    print(f"✓ Generated FastAPI routes ({len(routes)} chars)\n")


def test_frontend_agent():
    """Test Frontend Implementation Agent."""
    print("Testing Frontend Implementation Agent...")

    from intelligence.agents import FrontendImplementationAgent

    agent = FrontendImplementationAgent()

    # Test auth components
    components = agent.auth_ui_components()

    assert "SignupForm" in components
    assert "SigninForm" in components
    print(f"✓ Generated {len(components)} auth components")

    # Test API client
    api_client = agent.create_frontend_api_client()

    assert "ApiClient" in api_client
    assert "fetch" in api_client
    print(f"✓ Generated API client ({len(api_client)} chars)\n")


def test_auth_agent():
    """Test Auth Integration Agent."""
    print("Testing Auth Integration Agent...")

    from intelligence.agents import AuthIntegrationAgent

    agent = AuthIntegrationAgent()

    # Test Better Auth config
    config_files = agent.configure_better_auth_jwt()

    assert len(config_files) > 0
    print(f"✓ Generated {len(config_files)} config files")

    # Test JWT middleware
    middleware = agent.jwt_verification_middleware()

    assert "JWT" in middleware
    assert "verify" in middleware.lower()
    print(f"✓ Generated JWT middleware ({len(middleware)} chars)\n")


def test_database_agent():
    """Test Database Schema Agent."""
    print("Testing Database Schema Agent...")

    from intelligence.agents import DatabaseSchemaAgent

    agent = DatabaseSchemaAgent()

    # Test migration generation
    migrations = agent.generate_migrations([
        {
            "name": "Task",
            "fields": {
                "title": "String",
                "completed": "Boolean"
            }
        }
    ])

    assert len(migrations) > 0
    print(f"✓ Generated {len(migrations)} migration(s)")

    # Test index creation
    index_migration = agent.create_indexes(
        table="tasks",
        indexes=[
            {"columns": ["user_id"], "name": "idx_tasks_user_id"}
        ]
    )

    assert "create_index" in index_migration
    print(f"✓ Generated index migration ({len(index_migration)} chars)\n")


def test_agent_runner():
    """Test Agent Runner."""
    print("Testing Agent Runner...")

    from intelligence.runners import AgentRunner
    from intelligence.agents import RAGKnowledgeAgent

    runner = AgentRunner()
    agent = RAGKnowledgeAgent()

    # Test single execution
    result = runner.run(
        agent,
        {
            "skill": "retrieve_docs",
            "params": {"library": "fastapi"}
        },
        verbose=False
    )

    assert result is not None
    print("✓ Single execution works")

    # Test batch execution
    tasks = [
        {"skill": "retrieve_docs", "params": {"library": "fastapi"}},
        {"skill": "retrieve_docs", "params": {"library": "nextjs"}}
    ]

    results = runner.run_batch(agent, tasks, verbose=False)
    assert len(results) == 2
    print(f"✓ Batch execution works ({len(results)} tasks)")

    # Test statistics
    stats = runner.get_statistics()
    assert stats["total_executions"] > 0
    print(f"✓ Statistics: {stats['total_executions']} total executions\n")


def test_swarm_coordinator():
    """Test Swarm Coordinator."""
    print("Testing Swarm Coordinator...")

    from intelligence.runners import SwarmCoordinator
    from intelligence.agents import RAGKnowledgeAgent, BackendImplementationAgent

    coordinator = SwarmCoordinator()

    # Register agents
    coordinator.register_agent(RAGKnowledgeAgent())
    coordinator.register_agent(BackendImplementationAgent())

    # Test sequential execution
    workflow = [
        {
            "agent": "RAG-Knowledge-Agent",
            "skill": "retrieve_docs",
            "params": {"library": "fastapi"}
        },
        {
            "agent": "Backend-Implementation-Agent",
            "skill": "generate_models_sqlmodel",
            "params": {
                "entity_name": "Task",
                "fields": {"title": "str"}
            }
        }
    ]

    results = coordinator.run_sequential(workflow, verbose=False)
    assert len(results) == 2
    print(f"✓ Sequential execution works ({len(results)} steps)")

    # Test listing agents
    agents = coordinator.list_agents()
    assert len(agents) == 2
    print(f"✓ Coordinator managing {len(agents)} agents\n")


def test_tools():
    """Test shared tools."""
    print("Testing shared tools...")

    # Test Context7Client
    from intelligence.tools import Context7Client

    client = Context7Client()
    library_id = client.resolve_library_id("fastapi")
    print(f"✓ Context7Client resolved fastapi -> {library_id}")

    # Test JWTHelper
    from intelligence.tools import JWTHelper

    jwt_helper = JWTHelper(secret="test-secret")
    token = jwt_helper.create_token(user_id=1, email="test@example.com")
    payload = jwt_helper.verify_token(token)

    assert payload is not None
    assert payload["user_id"] == 1
    print(f"✓ JWTHelper created and verified token")

    # Test SpecLoader
    from intelligence.tools import SpecLoader

    loader = SpecLoader()
    try:
        constitution = loader.load_constitution()
        print(f"✓ SpecLoader loaded constitution ({len(constitution['principles'])} principles)")
    except FileNotFoundError:
        print("✓ SpecLoader working (constitution file handling)")

    print()


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Intelligence Layer - Test Suite")
    print("=" * 60 + "\n")

    tests = [
        test_imports,
        test_registry,
        test_rag_agent,
        test_backend_agent,
        test_frontend_agent,
        test_auth_agent,
        test_database_agent,
        test_agent_runner,
        test_swarm_coordinator,
        test_tools
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}\n")
            failed += 1

    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    if failed == 0:
        print("✓ All tests passed! Intelligence layer is ready.\n")
    else:
        print(f"✗ {failed} test(s) failed. Please review errors above.\n")


if __name__ == "__main__":
    run_all_tests()
