#!/bin/bash

# EloM Nusk Setup Script
# This script helps you set up the AI Scrum Master bot

echo "=========================================="
echo "EloM Nusk - AI Scrum Master Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required"
    echo "Current version: $python_version"
    exit 1
fi

echo "Python version OK: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ""
    echo "================================================"
    echo "IMPORTANT: Please edit .env file with your credentials"
    echo "================================================"
    echo ""
    echo "You need to add:"
    echo "  1. Slack Bot Token (SLACK_BOT_TOKEN)"
    echo "  2. Slack App Token (SLACK_APP_TOKEN)"
    echo "  3. Slack Signing Secret (SLACK_SIGNING_SECRET)"
    echo "  4. Jira Server URL (JIRA_SERVER)"
    echo "  5. Jira Username (JIRA_USERNAME)"
    echo "  6. Jira API Token (JIRA_API_TOKEN)"
    echo "  7. Jira Project Key (JIRA_PROJECT_KEY)"
    echo "  8. Anthropic API Key (ANTHROPIC_API_KEY)"
    echo ""
else
    echo ".env file already exists"
    echo ""
fi

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python main.py"
echo ""
echo "For detailed instructions, see README.md"
echo ""
