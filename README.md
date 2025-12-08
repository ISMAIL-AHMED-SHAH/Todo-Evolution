# In-Memory Python Todo CLI App

A simple command-line interface application for managing todo items in memory. This application allows you to add, list, update, delete, and mark todos as complete or incomplete.

## Features

- Add new todo items with descriptions
- List all current todo items
- Update existing todo item descriptions
- Delete todo items
- Mark todo items as complete or incomplete
- User-friendly output formatting using `rich`
- Robust error handling and validation
- Enhanced visual styling with rounded borders and improved formatting

## Requirements

- Python 3.10+
- `rich` library
- `uv` for environment management (optional but recommended)

## Installation

1. Clone or download the project
2. Install dependencies using `uv` (recommended):
   ```bash
   uv venv
   uv pip install rich pytest
   ```

Or install dependencies manually:
```bash
pip install rich pytest
```

## Usage

The application provides several commands for managing your todos:

### Add a Todo
```bash
python -m src.cli add "Your todo description here"
```
Example:
```bash
python -m src.cli add "Buy groceries"
```

### List All Todos
```bash
python -m src.cli list
```

### Update a Todo
```bash
python -m src.cli update <id> "New description"
```
Example:
```bash
python -m src.cli update 1 "Updated todo description"
```

### Delete a Todo
```bash
python -m src.cli delete <id>
```
Example:
```bash
python -m src.cli delete 1
```

### Mark a Todo as Complete
```bash
python -m src.cli complete <id>
```
Example:
```bash
python -m src.cli complete 1
```

### Mark a Todo as Incomplete
```bash
python -m src.cli incomplete <id>
```
Example:
```bash
python -m src.cli incomplete 1
```

## Command Details

- `<id>` refers to the numeric identifier assigned to each todo item
- Todo IDs are automatically generated and start from 1
- Descriptions can contain spaces and special characters
- The application validates all inputs and provides helpful error messages

## Error Handling

The application provides user-friendly error messages for various scenarios:

- Attempting to operate on a non-existent todo ID
- Providing empty descriptions for add/update commands
- Using invalid ID formats (non-numeric or negative values)

## Enhanced Visual Features

The application includes enhanced visual styling with:

- Rounded borders for a modern, polished appearance
- Underlined headers for improved visual hierarchy
- Bold status indicators (Y/N) in green (completed) and red (incomplete)
- Right-aligned ID column for better numerical readability
- Center-aligned status column for clear indicator placement
- Proper text wrapping for long descriptions
- Accessibility-focused design with text indicators in addition to colors

## Architecture

The application follows a clean architecture pattern:

- **Models** (`src/models.py`): Defines the Todo data structure
- **Services** (`src/services.py`): Contains business logic for todo operations
- **CLI** (`src/cli.py`): Handles command-line interface and user interaction

## Testing

To run the unit and integration tests:
```bash
python -m pytest tests/
```

## Performance

The application is designed for efficiency:
- Response time: <100ms for all operations
- Memory usage: <10MB for 1000 todo items
- All operations are optimized for quick execution

## Notes

- All data is stored in-memory only and will be lost when the application exits
- Each command execution is independent, meaning todos added in one command will not persist to subsequent commands in separate executions
- The application is designed as a single-user CLI tool