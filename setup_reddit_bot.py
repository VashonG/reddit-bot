import os
import subprocess

def create_directory_structure():
    print("Creating directory structure...")
    
    # Create project root directory
    os.makedirs('reddit_bot/bot', exist_ok=True)
    os.makedirs('reddit_bot/tests', exist_ok=True)

    # Create files
    with open('reddit_bot/bot/__init__.py', 'w') as f:
        pass

    with open('reddit_bot/bot/bot.py', 'w') as f:
        f.write(bot_file_content())

    with open('reddit_bot/bot/config.py', 'w') as f:
        f.write(config_file_content())

    with open('reddit_bot/tests/test_bot.py', 'w') as f:
        f.write(test_file_content())

    with open('reddit_bot/requirements.txt', 'w') as f:
        f.write(requirements_content())

    with open('reddit_bot/README.md', 'w') as f:
        f.write(readme_content())

def bot_file_content():
    return '''\
import praw
import time
from bot.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, USER_AGENT

def create_reddit_instance():
    """Create and authenticate Reddit instance."""
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        user_agent=USER_AGENT
    )
    return reddit

def search_and_reply(subreddit_name, keywords, reply_text, limit=10):
    """Searches for posts with specific keywords and replies."""
    reddit = create_reddit_instance()
    subreddit = reddit.subreddit(subreddit_name)

    for submission in subreddit.new(limit=limit):  # Search through latest posts
        if any(keyword.lower() in submission.title.lower() or keyword.lower() in submission.selftext.lower() for keyword in keywords):
            print(f"Found a post: {submission.title}")
            submission.comments.replace_more(limit=0)
            already_replied = any(comment.author == reddit.user.me() for comment in submission.comments)
            if not already_replied:
                try:
                    submission.reply(reply_text)
                    print(f"Replied to: {submission.title}")
                except Exception as e:
                    print(f"Error replying to post: {e}")
                time.sleep(10)  # Avoid rate-limiting

if __name__ == "__main__":
    keywords = ["python", "bot", "automation"]
    reply_text = "I noticed you mentioned Python automation! Let me know if you need help!"
    
    while True:
        search_and_reply(subreddit_name="learnpython", keywords=keywords, reply_text=reply_text, limit=10)
        time.sleep(600)  # Wait 10 minutes before running again
'''

def config_file_content():
    return '''\
# config.py
# Store Reddit credentials here

REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
REDDIT_USERNAME = "your_username"
REDDIT_PASSWORD = "your_password"
USER_AGENT = "bot by /u/your_username"
'''

def test_file_content():
    return '''\
# tests/test_bot.py

import unittest
from bot.bot import search_and_reply

class TestRedditBot(unittest.TestCase):
    def test_search_and_reply(self):
        """Test search_and_reply function (mock Reddit interaction)."""
        # This should mock Reddit's API responses and test without making real requests
        self.assertTrue(True)  # Replace with actual tests

if __name__ == "__main__":
    unittest.main()
'''

def requirements_content():
    return '''\
praw==7.6.0
pytest
'''

def readme_content():
    return '''\
# Reddit Bot

## Overview
This bot searches for Reddit posts containing specific keywords and responds to those posts with a custom message.

## Setup

1. Install dependencies:
pip install -r requirements.txt


2. Set up your Reddit API credentials in `bot/config.py`.

3. Run the bot:
python bot/bot.py

arduino

## Requirements
- PRAW: Reddit API wrapper
'''

def install_dependencies():
 print("Installing dependencies...")
 subprocess.run(['pip', 'install', '-r', 'reddit_bot/requirements.txt'])

if __name__ == "__main__":
 create_directory_structure()
 print("Project structure created.")
 
 install_dependencies()
 print("Dependencies installed.")
 
 print("Setup complete. Please configure your Reddit credentials in 'reddit_bot/bot/config.py'.")
