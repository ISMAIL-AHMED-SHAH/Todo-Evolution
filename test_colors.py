#!/usr/bin/env python3
"""Test script to verify enhanced color contrast for status indicators"""
from src.services import TodoService
from src.cli import list_todos_command, add_todo, complete_todo
from argparse import Namespace

# Create a single service instance to maintain state
service = TodoService()

# Add todos
add_args1 = Namespace(description=["Uncompleted", "task"])
add_todo(add_args1)

add_args2 = Namespace(description=["Completed", "task"])
add_todo(add_args2)

# Mark one as complete
complete_args = Namespace(id=2)
complete_todo(complete_args)

# List todos to see enhanced color contrast
list_todos_command(Namespace())