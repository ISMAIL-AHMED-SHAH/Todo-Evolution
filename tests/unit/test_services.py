
import pytest
from src.services import TodoService
from src.models import Todo

def test_add_todo():
    service = TodoService()
    todo = service.add_todo("Buy groceries")
    assert todo.id == 1
    assert todo.description == "Buy groceries"
    assert not todo.completed
    assert len(service._todos) == 1

    todo2 = service.add_todo("Walk the dog")
    assert todo2.id == 2
    assert todo2.description == "Walk the dog"
    assert not todo2.completed
    assert len(service._todos) == 2

def test_add_todo_empty_description():
    service = TodoService()
    with pytest.raises(ValueError, match="Todo description cannot be empty."):
        service.add_todo("")
    assert len(service._todos) == 0

def test_mark_todo_status_complete():
    service = TodoService()
    todo = service.add_todo("Buy groceries")
    marked_todo = service.mark_todo_status(todo.id, True)
    assert marked_todo.completed
    assert service._todos[0].completed

def test_mark_todo_status_incomplete():
    service = TodoService()
    todo = service.add_todo("Buy groceries")
    todo.completed = True
    marked_todo = service.mark_todo_status(todo.id, False)
    assert not marked_todo.completed
    assert not service._todos[0].completed

def test_mark_todo_status_non_existent_id():
    service = TodoService()
    service.add_todo("Buy groceries")
    with pytest.raises(ValueError, match="Todo with ID 999 not found."):
        service.mark_todo_status(999, True)
    assert not service._todos[0].completed

def test_list_todos_empty():
    service = TodoService()
    assert service.list_todos() == []

def test_list_todos_multiple_items():
    service = TodoService()
    todo1 = service.add_todo("Task 1")
    todo2 = service.add_todo("Task 2")
    todo3 = service.add_todo("Task 3")

    todos = service.list_todos()
    assert len(todos) == 3
    assert todos[0] == todo1
    assert todos[1] == todo2
    assert todos[2] == todo3

def test_update_todo_description():
    service = TodoService()
    todo = service.add_todo("Original description")
    updated_todo = service.update_todo(todo.id, "Updated description")
    assert updated_todo.description == "Updated description"
    assert service._todos[0].description == "Updated description"

def test_update_todo_non_existent_id():
    service = TodoService()
    service.add_todo("Original description")
    with pytest.raises(ValueError, match="Todo with ID 999 not found."):
        service.update_todo(999, "New description")
    assert service._todos[0].description == "Original description"

def test_update_todo_empty_description():
    service = TodoService()
    todo = service.add_todo("Original description")
    with pytest.raises(ValueError, match="Todo description cannot be empty."):
        service.update_todo(todo.id, "")
    assert service._todos[0].description == "Original description"

def test_delete_todo_success():
    service = TodoService()
    todo1 = service.add_todo("Task 1")
    todo2 = service.add_todo("Task 2")
    service.delete_todo(todo1.id)
    assert len(service.list_todos()) == 1
    assert service.list_todos()[0] == todo2

def test_delete_todo_non_existent_id():
    service = TodoService()
    service.add_todo("Task 1")
    with pytest.raises(ValueError, match="Todo with ID 999 not found."):
        service.delete_todo(999)
    assert len(service.list_todos()) == 1
