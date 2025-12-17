@echo off
REM Clear Python bytecode cache (Windows version)
REM Run this if you experience stale import issues after schema changes

echo Clearing Python bytecode cache...

REM Remove __pycache__ directories and .pyc files
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul

echo Cache cleared successfully!
echo.
echo You can now restart your FastAPI server.
pause
