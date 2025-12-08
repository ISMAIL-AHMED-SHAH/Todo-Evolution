#!/usr/bin/env python3
"""Test script to verify handling of empty todo lists"""
from src.services import TodoService
from src.cli import list_todos_command
from argparse import Namespace

# Create a fresh service instance with no todos
service = TodoService()

# List todos when there are none
list_todos_command(Namespace())