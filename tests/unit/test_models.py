
from src.models import Todo

def test_todo_initialization():
    todo = Todo(id=1, description="Test Todo")
    assert todo.id == 1
    assert todo.description == "Test Todo"
    assert todo.completed == False

def test_todo_completion():
    todo = Todo(id=2, description="Another Todo", completed=True)
    assert todo.id == 2
    assert todo.description == "Another Todo"
    assert todo.completed == True
