
import pytest
import sys
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch
from src.cli import main, todo_service
from src.services import TodoService

@pytest.fixture(autouse=True)
def reset_todos():
    # Clear todos before each test to ensure isolation
    todo_service._todos = []
    todo_service._next_id = 1

def run_cli_command(args):
    """Helper function to run CLI commands and capture output."""
    old_argv = sys.argv
    sys.argv = ['cli.py'] + args

    stdout_capture = StringIO()
    stderr_capture = StringIO()

    try:
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            main()
        stdout_output = stdout_capture.getvalue()
        stderr_output = stderr_capture.getvalue()
        exit_code = 0  # If main() runs without sys.exit(), exit code is 0
    except SystemExit as e:
        stdout_output = stdout_capture.getvalue()
        stderr_output = stderr_capture.getvalue()
        exit_code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    finally:
        sys.argv = old_argv

    return stdout_output, stderr_output, exit_code

def test_list_todos_empty():
    stdout, stderr, exit_code = run_cli_command(["list"])

    assert exit_code == 0
    assert "No todo items found." in stdout

def test_list_todos_populated():
    todo_service.add_todo("Task 1")
    todo_service.add_todo("Task 2")
    todo_service.mark_todo_status(1, True)

    stdout, stderr, exit_code = run_cli_command(["list"])

    assert exit_code == 0
    assert "Todo List" in stdout
    assert "ID" in stdout
    assert "Description" in stdout
    assert "Completed" in stdout
    assert "Task 1" in stdout
    assert "Task 2" in stdout
    assert "1" in stdout  # Check for ID
    assert "2" in stdout  # Check for ID


def test_update_todo_success():
    # Add a todo first
    todo_service.add_todo("Original description")

    stdout, stderr, exit_code = run_cli_command(["update", "1", "Updated", "description"])

    assert exit_code == 0
    assert "Todo 1 updated: Updated description" in stdout


def test_update_todo_non_existent_id():
    stdout, stderr, exit_code = run_cli_command(["update", "999", "Updated", "description"])

    assert exit_code == 1  # Command should fail with exit code 1
    assert "Error:" in stdout
    assert "not found" in stdout


def test_update_todo_empty_description():
    todo_service.add_todo("Original description")

    stdout, stderr, exit_code = run_cli_command(["update", "1"])

    assert exit_code == 1  # Command should fail with exit code 1
    assert "Error:" in stdout
    assert "empty" in stdout


def test_delete_todo_success():
    # Add a todo first
    todo_service.add_todo("Task to delete")

    stdout, stderr, exit_code = run_cli_command(["delete", "1"])

    assert exit_code == 0
    assert "Todo 1 deleted successfully" in stdout

    # Verify the todo is actually deleted
    remaining_todos = todo_service.list_todos()
    assert len(remaining_todos) == 0


def test_delete_todo_non_existent_id():
    stdout, stderr, exit_code = run_cli_command(["delete", "999"])

    assert exit_code == 1  # Command should fail with exit code 1
    assert "Error:" in stdout
    assert "not found" in stdout


def test_add_todo_success():
    stdout, stderr, exit_code = run_cli_command(["add", "New", "todo", "description"])

    assert exit_code == 0
    assert "Todo 1 added: New todo description" in stdout


def test_add_todo_empty_description():
    stdout, stderr, exit_code = run_cli_command(["add"])

    assert exit_code == 1  # Command should fail with exit code 1
    assert "Error:" in stdout
    assert "empty" in stdout


def test_complete_todo_success():
    # Add a todo first
    todo_service.add_todo("Task to complete")

    stdout, stderr, exit_code = run_cli_command(["complete", "1"])

    assert exit_code == 0
    assert "Todo 1 marked as complete" in stdout


def test_complete_todo_non_existent_id():
    stdout, stderr, exit_code = run_cli_command(["complete", "999"])

    assert exit_code == 1  # Command should fail with exit code 1
    assert "Error:" in stdout
    assert "not found" in stdout


def test_complete_todo_invalid_id():
    stdout, stderr, exit_code = run_cli_command(["complete", "0"])

    assert exit_code == 1  # Command should fail with exit code 1 for invalid ID
    assert "Error:" in stdout
    assert "positive number" in stdout


def test_incomplete_todo_success():
    # Add and complete a todo first
    todo_service.add_todo("Task to incomplete")
    todo_service.mark_todo_status(1, True)

    stdout, stderr, exit_code = run_cli_command(["incomplete", "1"])

    assert exit_code == 0
    assert "Todo 1 marked as incomplete" in stdout


def test_incomplete_todo_non_existent_id():
    stdout, stderr, exit_code = run_cli_command(["incomplete", "999"])

    assert exit_code == 1  # Command should fail with exit code 1
    assert "Error:" in stdout
    assert "not found" in stdout


def test_update_todo_invalid_id():
    stdout, stderr, exit_code = run_cli_command(["update", "0", "Updated", "description"])

    assert exit_code == 1  # Command should fail with exit code 1 for invalid ID
    assert "Error:" in stdout
    assert "positive number" in stdout


def test_delete_todo_invalid_id():
    stdout, stderr, exit_code = run_cli_command(["delete", "0"])

    assert exit_code == 1  # Command should fail with exit code 1 for invalid ID
    assert "Error:" in stdout
    assert "positive number" in stdout
