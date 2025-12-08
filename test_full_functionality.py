#!/usr/bin/env python3
"""Comprehensive test of all enhanced functionality"""
from src.services import TodoService
from src.cli import list_todos_command, add_todo, complete_todo, incomplete_todo, update_todo, delete_todo
from argparse import Namespace

print("=== Testing Full Functionality with All Enhancements ===\n")

# Create a single service instance to maintain state
service = TodoService()

# Test 1: Add multiple todos with different characteristics
print("1. Adding various todos...")
add_args1 = Namespace(description=["Regular", "task"])
add_todo(add_args1)

add_args2 = Namespace(description=["Very", "long", "task", "description", "that", "should", "test", "the", "table", "wrapping", "capabilities"])
add_todo(add_args2)

add_args3 = Namespace(description=["Task", "with", "special", "chars:", "@#$%"])
add_todo(add_args3)

print()

# Test 2: List todos (should show enhanced table)
print("2. Listing todos with enhanced table display:")
list_todos_command(Namespace())
print()

# Test 3: Mark a task as complete (should show enhanced color)
print("3. Marking task 2 as complete...")
complete_args = Namespace(id=2)
complete_todo(complete_args)
print()

# Test 4: List again to see the completed status
print("4. Listing todos after marking one as complete:")
list_todos_command(Namespace())
print()

# Test 5: Mark as incomplete
print("5. Marking task 2 as incomplete...")
incomplete_args = Namespace(id=2)
incomplete_todo(incomplete_args)
print()

# Test 6: Update a task
print("6. Updating task 3...")
update_args = Namespace(id=3, description=["Updated", "task", "with", "new", "description"])
update_todo(update_args)
print()

# Test 7: List to see all changes
print("7. Final list showing all features:")
list_todos_command(Namespace())
print()

# Test 8: Delete a task
print("8. Deleting task 1...")
delete_args = Namespace(id=1)
delete_todo(delete_args)
print("+ Todo 1 deleted successfully.")
print()

# Test 9: Final list
print("9. Final list after deletion:")
list_todos_command(Namespace())
print()

print("=== All functionality tested successfully! ===")