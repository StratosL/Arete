@echo off
REM Arete Setup Script for Windows
REM Sets up Supabase database and storage for development

echo.
echo 🚀 Setting up Arete development environment...
echo.

REM Check if .env exists
if not exist .env (
    echo ❌ Error: .env file not found
    echo    Please copy .env.example to .env and configure your API keys
    echo.
    goto :error
)

REM Load and check environment variables
echo 📋 Checking environment variables...
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if "%%a"=="SUPABASE_URL" set SUPABASE_URL=%%b
    if "%%a"=="SUPABASE_SERVICE_KEY" set SUPABASE_SERVICE_KEY=%%b
    if "%%a"=="CLAUDE_API_KEY" set CLAUDE_API_KEY=%%b
)

if "%SUPABASE_URL%"=="" (
    echo ❌ Error: SUPABASE_URL not found in .env
    goto :error
)
if "%SUPABASE_SERVICE_KEY%"=="" (
    echo ❌ Error: SUPABASE_SERVICE_KEY not found in .env
    goto :error
)
if "%CLAUDE_API_KEY%"=="" (
    echo ❌ Error: CLAUDE_API_KEY not found in .env
    goto :error
)

echo ✅ Environment variables configured

REM Install Python dependencies
echo.
echo 📦 Installing Python dependencies...
cd backend
python -m pip install supabase python-dotenv
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    echo    Make sure Python is installed and accessible
    cd ..
    goto :error
)
cd ..

REM Run environment validation
echo.
echo 🔍 Validating environment...
python scripts/validate_env.py
if %errorlevel% neq 0 (
    echo ❌ Environment validation failed
    goto :error
)

REM Run Supabase setup
echo.
echo 🗄️ Setting up Supabase...
python scripts/setup_supabase.py
if %errorlevel% neq 0 (
    echo ❌ Supabase setup failed
    goto :error
)

echo.
echo ✅ Setup completed successfully!
echo.
echo 🚀 You can now start the application:
echo    docker-compose up --build
echo.
echo 📝 Or run individual services:
echo    Backend:  cd backend ^&^& python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo    Frontend: cd frontend ^&^& npm run dev
echo.
echo Press any key to close...
pause >nul
exit /b 0

:error
echo.
echo ❌ Setup failed. Please check the error messages above.
echo.
echo 📝 For help, see README.md or check:
echo    - Environment variables in .env file
echo    - Python installation
echo    - Network connectivity
echo.
echo Press any key to close...
pause >nul
exit /b 1
