"""Reddit rss process"""
import feedparser
import pytz
import redis
import re
from datetime import datetime
from dateutil import parser
from config import REDIS_URL
from utils.log_utils import error_log, info_log

REDDIT_URL_REGEX = '.*reddit.com/r/{}/.*'


class RedditRss:
    """
        REDDIT RSS
    """
    def __init__(self, subreddit):
        self.redis = redis.from_url(REDIS_URL)
        self.regex = re.compile(REDDIT_URL_REGEX.format(subreddit))

    def read_rss(self, subreddit, process):
        """
            READ RSS
        """
        # Example: https://www.reddit.com/r/memes/hot/.rss
        try:
            info_log("reading rss", True)
            rss_path = "http://www.reddit.com/r/{}/new/.rss".format(subreddit)
            rss = feedparser.parse(rss_path)
            lastReadData = self.redis.get('lastRead_{}'.format(subreddit))
            # If this is the first fetch
            if lastReadData is None:
                print("Create first read for sub-reddit ' {}'.".format(
                    subreddit))
                lastRead = str(datetime.now(pytz.utc))
                self.redis.set('lastRead_{}'.format(subreddit), lastRead)
            else:
                lastRead = parser.parse(lastReadData)
            print('Last read: {}'.format(lastRead))
            for entry in rss.entries:
                entryDate = parser.parse(entry.date)
                print('RSS entry date: {}'.format(entryDate))
                # If posts is old, then break
                # TODO conditions for sending message
                if (entryDate < lastRead
                        or self.regex.search(entry.link) is None):
                    break
                rss_entry = RssEntry(entry.title, entry.author, entry.link)
                # Send message
                print('Telegram bot\'s sending message...')
                process(rss_entry)
                # Create new last read milestone
                key = 'lastRead_{}'.format(subreddit)
                value = datetime.now(pytz.utc)
                self.redis.set("{}".format(key), "{}".format(value))
        except Exception as e:
            error_log(e)
        except TimeoutError as timeout:
            error_log(timeout)

class RssEntry:
    """Define rss entry"""
    def __init__(self, title, link, author):
        self.title = title
        self.link = link
        self.author = author
