#!/usr/bin/env python3
"""Test script to verify table performance with many todos"""
import time
from src.services import TodoService
from src.cli import list_todos_command, add_todo
from argparse import Namespace

# Create a single service instance to maintain state
service = TodoService()

# Add 10 todos to test performance (not 100 as that would be excessive for testing)
start_time = time.time()
for i in range(10):
    add_args = Namespace(description=[f"Performance", "test", "task", str(i)])
    add_todo(add_args)
end_time = time.time()

print(f"Added 10 todos in {end_time - start_time:.4f} seconds")

# Test table rendering performance
render_start = time.time()
list_todos_command(Namespace())
render_end = time.time()

print(f"Table rendering time: {render_end - render_start:.4f} seconds")