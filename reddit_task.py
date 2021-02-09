"""Reddit task process"""
from config import SUB_REDDITS
from reddit_utils.reddit_rss import RedditRss
from utils.log_utils import error_log, info_log
from utils.bot_utils import send_message


class RedditTask:
    """Reddit task"""

    def __init__(self):
        self.tasks = {}
        for subreddit in SUB_REDDITS.split(','):
            subreddit = subreddit.strip()
            self.tasks[subreddit] = RedditRss(subreddit)

    def handle_feed(self, entry):
        """After receiving rss entries, send it back to user."""
        info_log("sending message", True)
        try:
            msg = '\n=============================='
            msg += '\n【REDDIT】{}\'s new post'.format(entry.author)
            msg += '\n' + entry.title + '\n' + entry.link
            msg += '\n============================\n\n'
            send_message(msg)
        except Exception as e:
            error_log(e)

    def execute(self):
        """
            Main reddit task process.
        """
        try:
            info_log("Execute reddit task", True)
            print("Execute reddit task")
            while(True):
                for sub in SUB_REDDITS.split(','):
                    sub = sub.strip()
                    self.tasks[sub].read_rss(sub, self.handle_feed)
            info_log("Execute reddit task", False)
        except Exception as e:
            error_log(e)
            print('Error occurs while executing reddit task.')
            return
