
from src.models import Todo

class TodoService:
    def __init__(self):
        self._todos: list[Todo] = []
        self._next_id: int = 1

    def add_todo(self, description: str) -> Todo:
        if not description:
            raise ValueError("Todo description cannot be empty.")
        todo = Todo(id=self._next_id, description=description)
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def mark_todo_status(self, todo_id: int, completed: bool) -> Todo:
        if not isinstance(todo_id, int) or todo_id <= 0:
            raise ValueError("Todo ID must be a positive integer.")
        for todo in self._todos:
            if todo.id == todo_id:
                todo.completed = completed
                return todo
        raise ValueError(f"Todo with ID {todo_id} not found.")

    def list_todos(self) -> list[Todo]:
        return list(self._todos)

    def update_todo(self, todo_id: int, new_description: str) -> Todo:
        if not isinstance(todo_id, int) or todo_id <= 0:
            raise ValueError("Todo ID must be a positive integer.")
        if not new_description:
            raise ValueError("Todo description cannot be empty.")
        for todo in self._todos:
            if todo.id == todo_id:
                todo.description = new_description
                return todo
        raise ValueError(f"Todo with ID {todo_id} not found.")

    def delete_todo(self, todo_id: int) -> None:
        if not isinstance(todo_id, int) or todo_id <= 0:
            raise ValueError("Todo ID must be a positive integer.")
        original_len = len(self._todos)
        self._todos = [todo for todo in self._todos if todo.id != todo_id]
        if len(self._todos) == original_len:
            raise ValueError(f"Todo with ID {todo_id} not found.")

