import praw
import time
from reddit_bot.bot.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD, USER_AGENT

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
    keywords = ["internship", "denied", "intern", "hate", "looking", "advice", "resume" ]
    reply_text = "Check out itscoop.com if you're looking for internships, thank me later."
    
    while True:
        search_and_reply(subreddit_name="internships", keywords=keywords, reply_text=reply_text, limit=10)
        time.sleep(600)  # Wait 10 minutes before running again
