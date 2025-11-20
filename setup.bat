@echo off
REM EloM Nusk Setup Script for Windows
REM This script helps you set up the AI Scrum Master bot

echo ==========================================
echo EloM Nusk - AI Scrum Master Setup
echo ==========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Check for .env file
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo ================================================
    echo IMPORTANT: Please edit .env file with your credentials
    echo ================================================
    echo.
    echo You need to add:
    echo   1. Slack Bot Token (SLACK_BOT_TOKEN)
    echo   2. Slack App Token (SLACK_APP_TOKEN)
    echo   3. Slack Signing Secret (SLACK_SIGNING_SECRET)
    echo   4. Jira Server URL (JIRA_SERVER)
    echo   5. Jira Username (JIRA_USERNAME)
    echo   6. Jira API Token (JIRA_API_TOKEN)
    echo   7. Jira Project Key (JIRA_PROJECT_KEY)
    echo   8. Anthropic API Key (ANTHROPIC_API_KEY)
    echo.
) else (
    echo .env file already exists
    echo.
)

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit .env file with your credentials
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: python main.py
echo.
echo For detailed instructions, see README.md
echo.
pause
