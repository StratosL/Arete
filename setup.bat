@echo off
REM Arete Setup Script for Windows - Improved Version
REM This script uses Python to handle environment validation and setup

echo.
echo 🚀 Setting up Arete development environment...
echo.

REM Check if .env exists
if not exist .env (
    echo ❌ Error: .env file not found
    echo    Please copy .env.example to .env and configure your API keys
    echo.
    echo 📝 Quick setup:
    echo    1. Copy .env.example to .env
    echo    2. Edit .env with your Supabase and Claude API keys
    echo    3. Run this script again
    echo.
    goto :error
)

echo ✅ Found .env file

REM Check if Python is available (try python3 first for WSL2, then python)
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    echo ✅ Python3 is available
) else (
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Error: Python not found
        echo    Please install Python from https://python.org
        echo    Make sure to check "Add Python to PATH" during installation
        echo.
        goto :error
    )
    set PYTHON_CMD=python
    echo ✅ Python is available
)

REM Install dependencies and run setup using Python
echo.
echo 📦 Installing dependencies and running setup...
echo.

REM Use Python to handle everything (more reliable than batch parsing)
%PYTHON_CMD% -c "
import subprocess
import sys
import os

def run_command(cmd, description):
    print(f'🔄 {description}...')
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f'✅ {description} completed')
        return True
    except subprocess.CalledProcessError as e:
        print(f'❌ {description} failed: {e.stderr}')
        return False

# Get Python command from environment
python_cmd = os.environ.get('PYTHON_CMD', 'python3')

# Install Python dependencies
if not run_command(f'{python_cmd} -m pip install --break-system-packages supabase python-dotenv litellm', 'Installing Python dependencies'):
    sys.exit(1)

# Run environment validation
if not run_command(f'{python_cmd} scripts/setup/validate_env.py', 'Validating environment'):
    sys.exit(1)

# Run Supabase setup
if not run_command(f'{python_cmd} scripts/setup/setup_supabase.py', 'Setting up Supabase'):
    sys.exit(1)

print()
print('✅ Setup completed successfully!')
print()
print('🚀 You can now start the application:')
print('   docker-compose up --build')
print()
print('📝 Or run individual services:')
print(f'   Backend:  cd backend && {python_cmd} -m uvicorn main:app --reload --host 0.0.0.0 --port 8000')
print('   Frontend: cd frontend && npm run dev')
"

if %errorlevel% neq 0 (
    goto :error
)

echo.
echo Press any key to close...
pause >nul
exit /b 0

:error
echo.
echo ❌ Setup failed. Please check the error messages above.
echo.
echo 📝 For help, see README.md or check:
echo    - .env file configuration
echo    - Python installation
echo    - Network connectivity
echo    - API key validity
echo.
echo Press any key to close...
pause >nul
exit /b 1
