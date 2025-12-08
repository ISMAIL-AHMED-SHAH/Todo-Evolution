# Backup of original list_todos_command function before enhancements

def list_todos_command_original(args):
    """List all todo items."""
    todos = todo_service.list_todos()

    if not todos:
        console.print("No todo items found.")
        return

    table = Table(title="Todo List")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Completed", style="green")

    for todo in todos:
        completed_status = "[green]✓[/green]" if todo.completed else "[red]✗[/red]"
        table.add_row(str(todo.id), todo.description, completed_status)

    console.print(table)