# slack_client.py

import slack_sdk
from config import SLACK_BOT_TOKEN

client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

def post_message(channel, text):
    try:
        response = client.chat_postMessage(channel=channel, text=text)
        return response
    except slack_sdk.errors.SlackApiError as e:
        print(f"Error posting message: {e}")
        return None

def get_channel_history(channel, limit=100):
    try:
        response = client.conversations_history(channel=channel, limit=limit)
        return response['messages']
    except slack_sdk.errors.SlackApiError as e:
        print(f"Error getting channel history: {e}")
        return None
