#!/usr/bin/env python3
"""Test script to verify enhanced table display with various content"""
from src.services import TodoService
from src.cli import list_todos_command, add_todo
from argparse import Namespace

# Create a single service instance to maintain state
service = TodoService()

# Add todos with various description lengths
add_args = Namespace(description=["Short"])
add_todo(add_args)

add_args2 = Namespace(description=["Medium", "length", "task"])
add_todo(add_args2)

add_args3 = Namespace(description=["Very", "long", "task", "description", "that", "should", "test", "the", "table", "wrapping", "and", "alignment", "capabilities"])
add_todo(add_args3)

# List todos to see enhanced table
list_todos_command(Namespace())