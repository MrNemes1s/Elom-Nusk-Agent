# claude_client.py

import os
from anthropic import Anthropic
from config import ANTHROPIC_API_KEY

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def generate_summary(issues_data, summary_type="daily"):
    """
    Generate an AI-powered summary of Jira issues using Claude.

    Args:
        issues_data: List of Jira issue objects or formatted issue data
        summary_type: Type of summary to generate (daily, sprint, standup)

    Returns:
        str: AI-generated summary
    """
    # Format issues data into a prompt
    issues_text = format_issues_for_prompt(issues_data)

    prompts = {
        "daily": f"""You are an AI Scrum Master assistant. Based on the following Jira issues and their current status,
create a concise daily summary for the team. Focus on:
- What was completed
- What's in progress
- Any blockers or issues
- Key priorities for today

Jira Issues:
{issues_text}

Provide a clear, actionable summary in a friendly but professional tone.""",

        "sprint": f"""You are an AI Scrum Master assistant. Based on the following Jira issues,
create a comprehensive sprint summary. Include:
- Sprint progress overview
- Completed stories and tasks
- In-progress work
- Blockers and risks
- Burndown insights
- Recommendations for the team

Jira Issues:
{issues_text}

Provide a detailed but well-structured summary.""",

        "standup": f"""You are an AI Scrum Master assistant. Based on the following Jira issues,
create a structured standup update format. For each team member or area:
- Yesterday's accomplishments
- Today's plan
- Any blockers

Jira Issues:
{issues_text}

Format this in a way that's easy to read during a standup meeting."""
    }

    prompt = prompts.get(summary_type, prompts["daily"])

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error generating summary with Claude: {e}")
        return None

def analyze_issue(issue_data):
    """
    Analyze a single Jira issue and provide insights.

    Args:
        issue_data: Jira issue object or formatted issue data

    Returns:
        str: AI-generated analysis and recommendations
    """
    issue_text = f"""
Issue Key: {issue_data.get('key', 'N/A')}
Summary: {issue_data.get('summary', 'N/A')}
Status: {issue_data.get('status', 'N/A')}
Assignee: {issue_data.get('assignee', 'Unassigned')}
Description: {issue_data.get('description', 'No description')}
"""

    prompt = f"""You are an AI Scrum Master assistant. Analyze the following Jira issue and provide:
- Brief assessment of the issue
- Potential blockers or risks
- Suggestions for the assignee
- Estimated complexity (if applicable)

{issue_text}

Provide concise, actionable insights."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error analyzing issue with Claude: {e}")
        return None

def generate_sprint_planning_insights(issues_data, sprint_goal=None):
    """
    Generate AI-powered sprint planning insights.

    Args:
        issues_data: List of Jira issues to consider for sprint
        sprint_goal: Optional sprint goal description

    Returns:
        str: AI-generated sprint planning recommendations
    """
    issues_text = format_issues_for_prompt(issues_data)
    goal_text = f"\nSprint Goal: {sprint_goal}" if sprint_goal else ""

    prompt = f"""You are an AI Scrum Master assistant helping with sprint planning.
Based on the following backlog items, provide recommendations for:
- Story prioritization
- Potential dependencies
- Capacity considerations
- Risk areas
- Suggested sprint scope
{goal_text}

Backlog Items:
{issues_text}

Provide strategic planning insights to help the team succeed."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error generating sprint planning insights: {e}")
        return None

def format_issues_for_prompt(issues):
    """
    Format Jira issues into a readable text format for the AI prompt.

    Args:
        issues: List of Jira issue objects

    Returns:
        str: Formatted issues text
    """
    if not issues:
        return "No issues found."

    formatted_text = ""
    for issue in issues:
        try:
            # Handle both Jira issue objects and dictionaries
            if hasattr(issue, 'key'):
                key = issue.key
                summary = issue.fields.summary
                status = issue.fields.status.name
                assignee = issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned"
                issue_type = issue.fields.issuetype.name
            else:
                key = issue.get('key', 'N/A')
                summary = issue.get('summary', 'N/A')
                status = issue.get('status', 'N/A')
                assignee = issue.get('assignee', 'Unassigned')
                issue_type = issue.get('type', 'Task')

            formatted_text += f"\n- [{key}] {summary}\n"
            formatted_text += f"  Type: {issue_type} | Status: {status} | Assignee: {assignee}\n"
        except Exception as e:
            print(f"Error formatting issue: {e}")
            continue

    return formatted_text
