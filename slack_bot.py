# slack_bot.py

import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN
from jira_client import (
    get_jira_client,
    get_issues_updated_today,
    get_active_sprint_issues,
    get_user_issues,
    format_issue_for_slack
)
from claude_client import generate_summary, analyze_issue, generate_sprint_planning_insights

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize JIRA client (will be used across commands)
jira_client = None

def get_or_create_jira_client():
    """Get or create JIRA client instance."""
    global jira_client
    if jira_client is None:
        jira_client = get_jira_client()
    return jira_client

@app.command("/daily-summary")
def handle_daily_summary(ack, command, respond):
    """
    Generate an AI-powered daily summary of team progress.
    Usage: /daily-summary [project_key]
    """
    ack()
    logger.info(f"Daily summary requested by {command['user_name']}")

    try:
        # Get project key from command or use default
        project_key = command['text'].strip() if command['text'].strip() else None

        # Get JIRA issues updated today
        jira = get_or_create_jira_client()
        issues = get_issues_updated_today(jira, project_key)

        if not issues:
            respond("No issues were updated today. The team might be taking a well-deserved break!")
            return

        # Generate AI-powered summary
        respond("Generating your daily summary... :robot_face:")
        summary = generate_summary(issues, summary_type="daily")

        if summary:
            # Format the response with issue details
            response = f"*Daily Team Summary* :bar_chart:\n\n{summary}\n\n"
            response += f"_Based on {len(issues)} issue(s) updated today_"
            respond(response)
        else:
            # Fallback to basic summary if AI fails
            response = "*Daily Summary* :bar_chart:\n\n"
            for issue in issues[:10]:  # Limit to 10 issues
                response += format_issue_for_slack(issue) + "\n"
            respond(response)

    except Exception as e:
        logger.error(f"Error generating daily summary: {e}")
        respond(f":warning: Error generating daily summary: {str(e)}")

@app.command("/sprint-summary")
def handle_sprint_summary(ack, command, respond):
    """
    Generate an AI-powered summary of the current sprint.
    Usage: /sprint-summary [project_key]
    """
    ack()
    logger.info(f"Sprint summary requested by {command['user_name']}")

    try:
        # Get project key from command or use default
        project_key = command['text'].strip() if command['text'].strip() else None

        # Get active sprint issues
        jira = get_or_create_jira_client()
        issues = get_active_sprint_issues(jira, project_key)

        if not issues:
            respond("No active sprint found or no issues in the current sprint.")
            return

        # Generate AI-powered sprint summary
        respond("Analyzing sprint progress... :runner:")
        summary = generate_summary(issues, summary_type="sprint")

        if summary:
            response = f"*Sprint Summary* :rocket:\n\n{summary}\n\n"
            response += f"_Based on {len(issues)} issue(s) in active sprint_"
            respond(response)
        else:
            # Fallback to basic summary
            response = "*Sprint Summary* :rocket:\n\n"
            response += f"Total Issues: {len(issues)}\n\n"
            for issue in issues[:15]:
                response += format_issue_for_slack(issue) + "\n"
            respond(response)

    except Exception as e:
        logger.error(f"Error generating sprint summary: {e}")
        respond(f":warning: Error generating sprint summary: {str(e)}")

@app.command("/standup")
def handle_standup(ack, command, respond):
    """
    Generate a standup-ready summary of team updates.
    Usage: /standup [project_key]
    """
    ack()
    logger.info(f"Standup summary requested by {command['user_name']}")

    try:
        # Get project key from command or use default
        project_key = command['text'].strip() if command['text'].strip() else None

        # Get active sprint issues
        jira = get_or_create_jira_client()
        issues = get_active_sprint_issues(jira, project_key)

        if not issues:
            respond("No active sprint found. Start a sprint to use this command!")
            return

        # Generate AI-powered standup summary
        respond("Preparing standup notes... :microphone:")
        summary = generate_summary(issues, summary_type="standup")

        if summary:
            response = f"*Daily Standup Summary* :speaking_head_in_silhouette:\n\n{summary}"
            respond(response)
        else:
            # Fallback to status-based summary
            response = "*Daily Standup Summary* :speaking_head_in_silhouette:\n\n"

            in_progress = [i for i in issues if i.fields.status.name == "In Progress"]
            done_recently = get_issues_updated_today(jira, project_key)

            response += f"*In Progress* ({len(in_progress)}):\n"
            for issue in in_progress[:5]:
                response += format_issue_for_slack(issue) + "\n"

            response += f"\n*Completed Today* ({len(done_recently)}):\n"
            for issue in done_recently[:5]:
                if issue.fields.status.name == "Done":
                    response += format_issue_for_slack(issue) + "\n"

            respond(response)

    except Exception as e:
        logger.error(f"Error generating standup summary: {e}")
        respond(f":warning: Error generating standup summary: {str(e)}")

@app.command("/my-tasks")
def handle_my_tasks(ack, command, respond):
    """
    Show your assigned tasks with AI insights.
    Usage: /my-tasks
    """
    ack()
    user_name = command['user_name']
    logger.info(f"My tasks requested by {user_name}")

    try:
        # Get user's email (you might need to fetch this from Slack API)
        # For now, we'll use a placeholder
        user_email = f"{user_name}@example.com"  # Replace with actual email lookup

        jira = get_or_create_jira_client()
        issues = get_user_issues(jira, user_email)

        if not issues:
            respond(f"You have no open tasks assigned. Great job, {user_name}! :tada:")
            return

        response = f"*Your Tasks* :clipboard: ({len(issues)} open)\n\n"
        for issue in issues[:10]:  # Limit to 10 issues
            response += format_issue_for_slack(issue) + "\n"

        respond(response)

    except Exception as e:
        logger.error(f"Error getting user tasks: {e}")
        respond(f":warning: Error retrieving your tasks: {str(e)}")

@app.command("/analyze-issue")
def handle_analyze_issue(ack, command, respond):
    """
    Get AI-powered analysis of a specific issue.
    Usage: /analyze-issue ISSUE-KEY
    """
    ack()
    logger.info(f"Issue analysis requested by {command['user_name']}")

    try:
        issue_key = command['text'].strip().upper()

        if not issue_key:
            respond("Please provide an issue key. Usage: `/analyze-issue PROJ-123`")
            return

        jira = get_or_create_jira_client()
        issue = jira.issue(issue_key)

        if not issue:
            respond(f"Issue {issue_key} not found.")
            return

        # Prepare issue data for analysis
        issue_data = {
            'key': issue.key,
            'summary': issue.fields.summary,
            'status': issue.fields.status.name,
            'assignee': issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned',
            'description': issue.fields.description or 'No description'
        }

        respond(f"Analyzing {issue_key}... :mag:")
        analysis = analyze_issue(issue_data)

        if analysis:
            response = f"*Analysis for {issue_key}* :bulb:\n\n{analysis}"
            respond(response)
        else:
            respond(f"Could not generate analysis for {issue_key}")

    except Exception as e:
        logger.error(f"Error analyzing issue: {e}")
        respond(f":warning: Error analyzing issue: {str(e)}")

@app.command("/help-scrum")
def handle_help(ack, respond):
    """Show available commands and usage."""
    ack()

    help_text = """
*EloM Nusk - AI Scrum Master Commands* :robot_face:

*Available Commands:*

`/daily-summary [project_key]`
Generate an AI-powered daily summary of team progress

`/sprint-summary [project_key]`
Get a comprehensive summary of the current sprint

`/standup [project_key]`
Generate standup-ready team updates

`/my-tasks`
View your assigned tasks

`/analyze-issue ISSUE-KEY`
Get AI insights about a specific issue

`/help-scrum`
Show this help message

*Tips:*
- Most commands use your default project if you don't specify one
- Issue keys should be in format: PROJ-123
- All summaries are powered by Claude AI :sparkles:
"""

    respond(help_text)

@app.event("app_mention")
def handle_mention(event, say):
    """Handle when the bot is mentioned."""
    user = event['user']
    text = event['text']

    logger.info(f"Bot mentioned by {user}: {text}")

    say(f"Hi <@{user}>! I'm EloM Nusk, your AI Scrum Master. Use `/help-scrum` to see what I can do!")

def start_bot():
    """Start the Slack bot in Socket Mode."""
    try:
        logger.info("Starting EloM Nusk Slack Bot...")
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        handler.start()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    start_bot()
