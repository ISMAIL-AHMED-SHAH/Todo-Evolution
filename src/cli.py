
import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich import box

from src.services import TodoService

console = Console()
todo_service = TodoService()  # Global instance for maintaining state during a single CLI execution

def add_todo(args):
    """Add a new todo item."""
    description_str = " ".join(args.description)
    if not args.description or not description_str.strip():
        console.print("[red]Error:[/red] Todo description cannot be empty.")
        sys.exit(1)

    try:
        new_todo = todo_service.add_todo(description_str)
        console.print(f"[green]+[/green] Todo {new_todo.id} added: {new_todo.description}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

def list_todos_command(args):
    """List all todo items."""
    todos = todo_service.list_todos()

    if not todos:
        console.print("No todo items found.")
        return

    table = Table(title="Todo List", box=box.ROUNDED, show_header=True, header_style="bold magenta underline")
    table.add_column("ID", style="cyan", justify="right", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Completed", style="bold green", justify="center")

    for todo in todos:
        completed_status = "[bold green]Y[/bold green]" if todo.completed else "[bold red]N[/bold red]"
        table.add_row(str(todo.id), todo.description, completed_status)

    console.print(table)

def complete_todo(args):
    """Mark a todo item as complete by ID."""
    try:
        if args.id <= 0:
            console.print("[red]Error:[/red] Todo ID must be a positive number.")
            sys.exit(1)
        updated_todo = todo_service.mark_todo_status(args.id, True)
        console.print(f"[green]+[/green] Todo {updated_todo.id} marked as complete: {updated_todo.description}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

def incomplete_todo(args):
    """Mark a todo item as incomplete by ID."""
    try:
        if args.id <= 0:
            console.print("[red]Error:[/red] Todo ID must be a positive number.")
            sys.exit(1)
        updated_todo = todo_service.mark_todo_status(args.id, False)
        console.print(f"[green]+[/green] Todo {updated_todo.id} marked as incomplete: {updated_todo.description}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

def update_todo(args):
    """Update a todo item's description by ID."""
    description_str = " ".join(args.description)
    try:
        if args.id <= 0:
            console.print("[red]Error:[/red] Todo ID must be a positive number.")
            sys.exit(1)
        if not args.description or not description_str.strip():
            console.print("[red]Error:[/red] Todo description cannot be empty.")
            sys.exit(1)
        updated_todo = todo_service.update_todo(args.id, description_str)
        console.print(f"[green]+[/green] Todo {updated_todo.id} updated: {updated_todo.description}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

def delete_todo(args):
    """Delete a todo item by ID."""
    try:
        if args.id <= 0:
            console.print("[red]Error:[/red] Todo ID must be a positive number.")
            sys.exit(1)
        todo_service.delete_todo(args.id)
        console.print(f"[green]+[/green] Todo {args.id} deleted successfully.")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

def main(service=None):
    """Main entry point for the CLI application.

    Args:
        service: Optional TodoService instance to use (for testing purposes)
    """
    # Use provided service or default global instance
    active_service = service if service is not None else todo_service

    parser = argparse.ArgumentParser(description="A simple in-memory todo list CLI.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new todo item")
    add_parser.add_argument("description", nargs="*", help="Description of the todo item")

    # List command
    list_parser = subparsers.add_parser("list", help="List all todo items")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo item as complete")
    complete_parser.add_argument("id", type=int, help="ID of the todo item")

    # Incomplete command
    incomplete_parser = subparsers.add_parser("incomplete", help="Mark a todo item as incomplete")
    incomplete_parser.add_argument("id", type=int, help="ID of the todo item")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a todo item's description")
    update_parser.add_argument("id", type=int, help="ID of the todo item")
    update_parser.add_argument("description", nargs="*", help="New description of the todo item")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo item")
    delete_parser.add_argument("id", type=int, help="ID of the todo item")

    args = parser.parse_args()

    # Execute the appropriate command with the active service
    if args.command == "add":
        _execute_command(add_todo, args, active_service)
    elif args.command == "list":
        _execute_command(list_todos_command, args, active_service)
    elif args.command == "complete":
        _execute_command(complete_todo, args, active_service)
    elif args.command == "incomplete":
        _execute_command(incomplete_todo, args, active_service)
    elif args.command == "update":
        _execute_command(update_todo, args, active_service)
    elif args.command == "delete":
        _execute_command(delete_todo, args, active_service)
    else:
        parser.print_help()
        sys.exit(1)

def _execute_command(func, args, service):
    """Execute a CLI function with a specific service instance."""
    # Temporarily replace the global service for this execution
    global todo_service
    original_service = todo_service
    todo_service = service
    try:
        func(args)
    finally:
        todo_service = original_service  # Restore original service after execution

if __name__ == "__main__":
    main()
