#!/usr/bin/env python3
"""Test script to verify handling of special characters in descriptions"""
from src.services import TodoService
from src.cli import list_todos_command, add_todo
from argparse import Namespace

# Create a single service instance to maintain state
service = TodoService()

# Add a todo with special characters
add_args = Namespace(description=["Test", "with", "special", "chars:", "@#$%&*()"])
add_todo(add_args)

# List todos to see how special characters are handled
list_todos_command(Namespace())