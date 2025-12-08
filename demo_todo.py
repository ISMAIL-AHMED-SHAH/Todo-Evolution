#!/usr/bin/env python3
"""
Simple demonstration of the visually appealing todo application.
"""

def main():
    print("## Visually Appealing Todo Application")
    print("=" * 50)

    print("\nThis application already features:")
    print("- Interactive CLI interface")
    print("- Tabular data display using rich")
    print("- Colorful visual indicators")
    print("- Interactive operations")
    print("- Visually appealing output")

    print("\n" + "=" * 50)
    print("## HOW TO RUN THE TODO APPLICATION:")
    print("\n### Method 1: Direct Python execution")
    print("  $ python -m src.cli add 'My first task'")
    print("  $ python -m src.cli list")
    print("  $ python -m src.cli complete 1")

    print("\n### Method 2: Install and use as CLI tool")
    print("  $ pip install -e .  # Install in development mode")
    print("  $ todo add 'My first task'")
    print("  $ todo list")
    print("  $ todo complete 1")

    print("\n### Available Commands:")
    print("  • add <description>        - Add a new todo")
    print("  • list                     - Show all todos in table format")
    print("  • complete <id>            - Mark todo as complete")
    print("  • incomplete <id>          - Mark todo as incomplete")
    print("  • update <id> <new_desc>   - Update todo description")
    print("  • delete <id>              - Delete a todo")

    print("\n### Visual Features:")
    print("  • Tabular display with rich formatting")
    print("  • Color-coded status indicators (green for complete, red for incomplete)")
    print("  • Interactive feedback for all operations")
    print("  • Clean, readable table output")

    print("\n### Example Output Format:")
    print("  +-----+-----------------------------+-----------+")
    print("  |  ID | Description                 | Completed |")
    print("  +-----+-----------------------------+-----------+")
    print("  |   1 | Learn Python                | [X]       |")
    print("  |   2 | Build a CLI app             | [V]       |")
    print("  |   3 | Use rich library            | [X]       |")
    print("  +-----+-----------------------------+-----------+")

    print("\nThe application is already visually appealing with rich tabular data!")
    print("\nTo try it yourself, run the commands above in your terminal.")

if __name__ == "__main__":
    main()