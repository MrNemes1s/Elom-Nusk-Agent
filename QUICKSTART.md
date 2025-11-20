# Quick Start Guide - EloM Nusk

Get up and running with EloM Nusk in 5 minutes!

## Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- Slack workspace admin access
- Jira account
- Anthropic API key

## Installation (Automated)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run setup
./setup.sh
```

## Installation (Manual)

### 1. Install uv and Dependencies

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Set Up Slack App

**Quick Setup:**

1. Go to https://api.slack.com/apps → Create New App → From scratch
2. Name: `EloM Nusk` → Select your workspace
3. **OAuth & Permissions** → Add Bot Token Scopes:
   - `app_mentions:read`
   - `channels:history`
   - `chat:write`
   - `commands`
   - `users:read`
4. **Socket Mode** → Enable → Create App Token with `connections:write`
5. **Slash Commands** → Create:
   - `/daily-summary`
   - `/sprint-summary`
   - `/standup`
   - `/my-tasks`
   - `/analyze-issue`
   - `/help-scrum`
6. **Event Subscriptions** → Subscribe to:
   - `app_mention`
7. **Install App** → Install to Workspace → Copy tokens

### 4. Get API Keys

**Jira:**
- Go to https://id.atlassian.com/manage-profile/security/api-tokens
- Create API token

**Anthropic:**
- Sign up at https://www.anthropic.com
- Get API key from console

### 5. Update .env

```env
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_SIGNING_SECRET=...

JIRA_SERVER=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_API_TOKEN=...
JIRA_PROJECT_KEY=PROJ

ANTHROPIC_API_KEY=sk-ant-...
```

## Running the Bot

**Using uv (recommended):**

```bash
uv run main.py
```

**Or activate virtual environment:**

```bash
source .venv/bin/activate
python main.py
```

You should see:
```
============================================================
EloM Nusk - AI Scrum Master
============================================================
Environment validated successfully
Starting Slack bot in Socket Mode...
```

## First Commands

### In Slack:

1. Invite the bot to a channel:
   ```
   /invite @EloM Nusk
   ```

2. Try your first command:
   ```
   /help-scrum
   ```

3. Generate a daily summary:
   ```
   /daily-summary
   ```

4. Get sprint overview:
   ```
   /sprint-summary
   ```

## Common Issues

### Bot not responding?
- Ensure bot is invited to the channel
- Check that main.py is running
- Verify Socket Mode is enabled

### Jira errors?
- Verify JIRA_PROJECT_KEY is correct
- Check API token is valid
- Ensure your Jira user has project access

### Anthropic API errors?
- Verify API key is correct
- Check you have available credits

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Customize AI prompts in `claude_client.py`
- Add custom Jira queries in `jira_client.py`
- Create additional slash commands in `slack_bot.py`

## Need Help?

Check the main README or create an issue in the repository.

---

Happy Scrum-ing! 🚀
