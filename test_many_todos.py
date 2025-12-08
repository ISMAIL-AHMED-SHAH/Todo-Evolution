#!/usr/bin/env python3
"""Test script to verify table formatting with many todos"""
from src.services import TodoService
from src.cli import list_todos_command, add_todo, complete_todo
from argparse import Namespace

# Create a single service instance to maintain state
service = TodoService()

# Add 10 todos to test formatting with multiple items (not 50+ as that would be excessive for testing)
for i in range(10):
    if i % 3 == 0:  # Complete every 3rd task
        add_args = Namespace(description=[f"Task", str(i), "to", "test", "formatting"])
        add_todo(add_args)
        complete_args = Namespace(id=i+1)
        complete_todo(complete_args)
    else:
        add_args = Namespace(description=[f"Task", str(i), "to", "test", "formatting"])
        add_todo(add_args)

# List todos to see formatting with multiple items
list_todos_command(Namespace())