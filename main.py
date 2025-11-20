# main.py

import logging
from config import (
    SLACK_BOT_TOKEN,
    SLACK_APP_TOKEN,
    JIRA_SERVER,
    JIRA_USERNAME,
    JIRA_API_TOKEN,
    ANTHROPIC_API_KEY
)
from slack_bot import start_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_environment():
    """
    Validate that all required environment variables are set.

    Returns:
        bool: True if all required variables are set, False otherwise
    """
    required_vars = {
        'SLACK_BOT_TOKEN': SLACK_BOT_TOKEN,
        'SLACK_APP_TOKEN': SLACK_APP_TOKEN,
        'JIRA_SERVER': JIRA_SERVER,
        'JIRA_USERNAME': JIRA_USERNAME,
        'JIRA_API_TOKEN': JIRA_API_TOKEN,
        'ANTHROPIC_API_KEY': ANTHROPIC_API_KEY
    }

    missing_vars = [name for name, value in required_vars.items() if not value]

    if missing_vars:
        logger.error("Missing required environment variables:")
        for var in missing_vars:
            logger.error(f"  - {var}")
        logger.error("\nPlease set these variables in your .env file.")
        logger.error("See .env.example for the required format.")
        return False

    return True

def main():
    """
    Main entry point for EloM Nusk AI Scrum Master.
    """
    logger.info("=" * 60)
    logger.info("EloM Nusk - AI Scrum Master")
    logger.info("=" * 60)

    # Validate environment variables
    if not validate_environment():
        return

    logger.info("Environment validated successfully")
    logger.info("Starting Slack bot in Socket Mode...")
    logger.info("Bot will respond to slash commands and mentions")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 60)

    try:
        # Start the Slack bot
        start_bot()
    except KeyboardInterrupt:
        logger.info("\nShutting down EloM Nusk...")
        logger.info("Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
