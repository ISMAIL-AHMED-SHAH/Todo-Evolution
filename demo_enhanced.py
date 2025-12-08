#!/usr/bin/env python3
"""Demonstration script showing the enhanced rich table output"""
from src.services import TodoService
from src.cli import add_todo, list_todos_command, complete_todo, update_todo
from argparse import Namespace

print("RICH TABULAR OUTPUT ENHANCEMENT - DEMONSTRATION")
print("="*60)
print()

# Create a service instance to maintain state during this session
service = TodoService()

print("ADDING SAMPLE TODO ITEMS...")
# Add various types of todos to showcase the enhanced features
todos_to_add = [
    ["Simple task"],
    ["Medium length task description"],
    ["Very long task description that demonstrates the excellent text wrapping and alignment capabilities of our enhanced rich table implementation"],
    ["Task with special characters: @#$%&*()"],
    ["Another regular task"]
]

for i, desc in enumerate(todos_to_add):
    add_args = Namespace(description=desc)
    add_todo(add_args)
    print(f"   - Added: {' '.join(desc)}")

print()
print("ENHANCED TABLE DISPLAY:")
print("   Here's the beautiful, enhanced table with all new features:")
print()
list_todos_command(Namespace())

print()
print("MARKING A TASK AS COMPLETE...")
# Mark the long description task as complete to show color enhancement
complete_args = Namespace(id=3)
complete_todo(complete_args)
print("   - Marked task 3 as complete")
print()
list_todos_command(Namespace())

print()
print("ENHANCED VISUAL FEATURES:")
print("   - Rounded borders for modern appearance")
print("   - Underlined headers for visual hierarchy")
print("   - Right-aligned ID column for readability")
print("   - Center-aligned status column for clarity")
print("   - Bold green 'Y' for completed tasks")
print("   - Bold red 'N' for incomplete tasks")
print("   - Proper text wrapping for long descriptions")
print("   - Accessibility-focused design")
print()
print("IMPLEMENTATION COMPLETE - VISUALLY APPEALING TABLE ACHIEVED!")