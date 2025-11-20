# config.py

import os
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

DEFAULT_SUMMARY_CHANNEL = os.getenv("DEFAULT_SUMMARY_CHANNEL", "#scrum-updates")
DEFAULT_STANDUP_CHANNEL = os.getenv("DEFAULT_STANDUP_CHANNEL", "#daily-standup")
