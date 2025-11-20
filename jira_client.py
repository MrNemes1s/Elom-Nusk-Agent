# jira_client.py

from jira import JIRA
from config import JIRA_SERVER, JIRA_USERNAME, JIRA_API_TOKEN, JIRA_PROJECT_KEY
from datetime import datetime, timedelta

def get_jira_client():
    """
    Create and return a JIRA client instance.

    Returns:
        JIRA: Authenticated JIRA client
    """
    options = {
        'server': JIRA_SERVER
    }
    return JIRA(options, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))

def get_project_issues(jira_client, project_key=None, max_results=50):
    """
    Get all issues for a project.

    Args:
        jira_client: JIRA client instance
        project_key: Project key (defaults to JIRA_PROJECT_KEY from config)
        max_results: Maximum number of issues to return

    Returns:
        list: List of JIRA issues
    """
    project_key = project_key or JIRA_PROJECT_KEY
    try:
        issues = jira_client.search_issues(
            f'project={project_key} ORDER BY updated DESC',
            maxResults=max_results
        )
        return issues
    except Exception as e:
        print(f"Error getting project issues: {e}")
        return []

def get_active_sprint_issues(jira_client, project_key=None):
    """
    Get issues in the current active sprint.

    Args:
        jira_client: JIRA client instance
        project_key: Project key (defaults to JIRA_PROJECT_KEY from config)

    Returns:
        list: List of issues in active sprint
    """
    project_key = project_key or JIRA_PROJECT_KEY
    try:
        jql = f'project={project_key} AND sprint in openSprints() ORDER BY status'
        issues = jira_client.search_issues(jql, maxResults=100)
        return issues
    except Exception as e:
        print(f"Error getting active sprint issues: {e}")
        return []

def get_issues_by_status(jira_client, status, project_key=None, max_results=50):
    """
    Get issues filtered by status.

    Args:
        jira_client: JIRA client instance
        status: Status to filter by (e.g., "In Progress", "Done", "To Do")
        project_key: Project key (defaults to JIRA_PROJECT_KEY from config)
        max_results: Maximum number of issues to return

    Returns:
        list: List of issues with specified status
    """
    project_key = project_key or JIRA_PROJECT_KEY
    try:
        jql = f'project={project_key} AND status="{status}" ORDER BY updated DESC'
        issues = jira_client.search_issues(jql, maxResults=max_results)
        return issues
    except Exception as e:
        print(f"Error getting issues by status: {e}")
        return []

def get_issues_updated_today(jira_client, project_key=None):
    """
    Get issues updated today.

    Args:
        jira_client: JIRA client instance
        project_key: Project key (defaults to JIRA_PROJECT_KEY from config)

    Returns:
        list: List of issues updated today
    """
    project_key = project_key or JIRA_PROJECT_KEY
    try:
        jql = f'project={project_key} AND updated >= startOfDay() ORDER BY updated DESC'
        issues = jira_client.search_issues(jql, maxResults=100)
        return issues
    except Exception as e:
        print(f"Error getting today's issues: {e}")
        return []

def get_user_issues(jira_client, user_email, project_key=None):
    """
    Get issues assigned to a specific user.

    Args:
        jira_client: JIRA client instance
        user_email: Email of the user
        project_key: Project key (defaults to JIRA_PROJECT_KEY from config)

    Returns:
        list: List of issues assigned to the user
    """
    project_key = project_key or JIRA_PROJECT_KEY
    try:
        jql = f'project={project_key} AND assignee="{user_email}" AND status != Done ORDER BY updated DESC'
        issues = jira_client.search_issues(jql, maxResults=50)
        return issues
    except Exception as e:
        print(f"Error getting user issues: {e}")
        return []

def get_issue_details(jira_client, issue_key):
    """
    Get detailed information about a specific issue.

    Args:
        jira_client: JIRA client instance
        issue_key: Issue key (e.g., "PROJ-123")

    Returns:
        Issue: JIRA issue object or None if not found
    """
    try:
        issue = jira_client.issue(issue_key)
        return issue
    except Exception as e:
        print(f"Error getting issue details: {e}")
        return None

def format_issue_for_slack(issue):
    """
    Format a JIRA issue for display in Slack.

    Args:
        issue: JIRA issue object

    Returns:
        str: Formatted issue string for Slack
    """
    try:
        assignee = issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned"
        status_emoji = {
            "To Do": ":white_circle:",
            "In Progress": ":large_blue_circle:",
            "Done": ":white_check_mark:",
            "Blocked": ":red_circle:"
        }.get(issue.fields.status.name, ":black_circle:")

        return f"{status_emoji} *{issue.key}*: {issue.fields.summary}\n   _Status:_ {issue.fields.status.name} | _Assignee:_ {assignee}"
    except Exception as e:
        print(f"Error formatting issue for Slack: {e}")
        return f"Error formatting issue {issue.key}"
