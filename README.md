# EloM Nusk - AI Scrum Master

An intelligent Slack bot powered by Anthropic Claude that helps teams manage their Scrum workflow by integrating with Jira and providing AI-powered insights, summaries, and recommendations.

## Features

- **AI-Powered Summaries**: Generate intelligent daily and sprint summaries using Claude AI
- **Smart Stand-ups**: Automated stand-up meeting summaries
- **Issue Analysis**: Get AI insights on specific Jira issues
- **Task Management**: Quick access to your assigned tasks
- **Slack Integration**: Interactive slash commands for easy access
- **Jira Integration**: Real-time data from your Jira projects

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- A Slack workspace with admin permissions
- Jira account with API access
- Anthropic API key (Claude)

## Installation

### 1. Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone the Repository

```bash
git clone <repository-url>
cd elom_nusk
```

### 3. Run Automated Setup

```bash
./setup.sh
```

This will:
- Verify uv installation
- Create a virtual environment
- Install all dependencies
- Create `.env` from template

### 4. Manual Installation (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment with uv
uv venv

# Install dependencies
uv pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### 5. Configure Slack App

1. Go to [Slack API](https://api.slack.com/apps) and create a new app
2. Choose "From scratch" and give it a name (e.g., "EloM Nusk")
3. Select your workspace

#### Bot Token Scopes

Under "OAuth & Permissions", add these Bot Token Scopes:
- `app_mentions:read`
- `channels:history`
- `chat:write`
- `commands`
- `users:read`

#### Slash Commands

Under "Slash Commands", create these commands:
- `/daily-summary` - Generate daily team summary
- `/sprint-summary` - Generate sprint summary
- `/standup` - Generate standup notes
- `/my-tasks` - View your tasks
- `/analyze-issue` - Analyze a specific issue
- `/help-scrum` - Show help

For each command, use the Request URL: `https://your-app-url/slack/events`
(Note: In Socket Mode, you can leave this blank)

#### Enable Socket Mode

1. Go to "Socket Mode" in your app settings
2. Enable Socket Mode
3. Create an App-Level Token with `connections:write` scope
4. Save the token (starts with `xapp-`)

#### Event Subscriptions

Under "Event Subscriptions", subscribe to these bot events:
- `app_mention`
- `message.channels`

### 5. Configure Jira

1. Go to [Jira API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Create an API token
3. Note your Jira server URL (e.g., `https://your-domain.atlassian.net`)
4. Note your Jira email address

### 6. Get Anthropic API Key

1. Sign up at [Anthropic](https://www.anthropic.com/)
2. Get your API key from the console

### 7. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
SLACK_SIGNING_SECRET=your-signing-secret

# Jira Configuration
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token
JIRA_PROJECT_KEY=YOUR_PROJECT_KEY

# Anthropic Claude Configuration
ANTHROPIC_API_KEY=your-anthropic-api-key

# Optional: Default Slack channels
DEFAULT_SUMMARY_CHANNEL=#scrum-updates
DEFAULT_STANDUP_CHANNEL=#daily-standup
```

## Usage

### Starting the Bot

**Using uv (recommended):**

```bash
uv run main.py
```

**Or activate the virtual environment first:**

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
Bot will respond to slash commands and mentions
Press Ctrl+C to stop
============================================================
```

### Available Commands

#### `/daily-summary [project_key]`
Generate an AI-powered daily summary of team progress based on issues updated today.

**Example:**
```
/daily-summary PROJ
```

#### `/sprint-summary [project_key]`
Get a comprehensive summary of the current sprint with AI insights.

**Example:**
```
/sprint-summary
```

#### `/standup [project_key]`
Generate standup-ready team updates organized by what's done, in progress, and blocked.

**Example:**
```
/standup PROJ
```

#### `/my-tasks`
View all your currently assigned tasks.

**Example:**
```
/my-tasks
```

#### `/analyze-issue ISSUE-KEY`
Get AI-powered analysis and recommendations for a specific issue.

**Example:**
```
/analyze-issue PROJ-123
```

#### `/help-scrum`
Display help information and available commands.

**Example:**
```
/help-scrum
```

### Mentioning the Bot

You can also mention the bot in a channel:
```
@EloM Nusk what can you do?
```

## Project Structure

```
elom_nusk/
├── main.py              # Application entry point
├── slack_bot.py         # Slack bot implementation with slash commands
├── jira_client.py       # Jira API integration
├── claude_client.py     # Anthropic Claude AI integration
├── config.py            # Configuration and environment variables
├── slack_client.py      # Legacy Slack client (deprecated)
├── agent.py             # Legacy agent functions (deprecated)
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Example environment configuration
└── README.md           # This file
```

## Development

### Adding New Commands

To add a new slash command:

1. Register the command in Slack App settings
2. Add a handler in `slack_bot.py`:

```python
@app.command("/your-command")
def handle_your_command(ack, command, respond):
    ack()
    # Your logic here
    respond("Response message")
```

### Adding New Jira Queries

Add new query functions in `jira_client.py`:

```python
def get_custom_issues(jira_client, custom_filter):
    jql = f'your JQL query here'
    return jira_client.search_issues(jql)
```

### Customizing AI Prompts

Edit the prompts in `claude_client.py` to customize AI responses:

```python
prompts = {
    "your_type": "Your custom prompt here..."
}
```

## Troubleshooting

### Bot Not Responding

1. Check that the bot is running (`python main.py`)
2. Verify all environment variables are set correctly
3. Ensure the bot is invited to the channel
4. Check Slack app permissions

### Jira Connection Issues

1. Verify your Jira credentials in `.env`
2. Check that your API token is valid
3. Ensure your Jira project key is correct
4. Test Jira API access: `https://your-domain.atlassian.net/rest/api/2/myself`

### Anthropic API Errors

1. Verify your API key is correct
2. Check your API quota/credits
3. Review error messages in console logs

### Socket Mode Issues

1. Ensure Socket Mode is enabled in your Slack app
2. Verify your App-Level Token (SLACK_APP_TOKEN)
3. Check network connectivity

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review [Slack API Documentation](https://api.slack.com/)
- Review [Jira API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v2/)
- Review [Anthropic Documentation](https://docs.anthropic.com/)

## Acknowledgments

- Built with [Slack Bolt](https://slack.dev/bolt-python/)
- Powered by [Anthropic Claude](https://www.anthropic.com/)
- Integrated with [Jira Cloud](https://www.atlassian.com/software/jira)

---

Made with AI by the EloM Nusk team
