"""Main process"""
from reddit_task import RedditTask
from concurrent.futures import ThreadPoolExecutor
import time


# Create reddit task
reddit_task = RedditTask()

print("Starting script....")
executor = ThreadPoolExecutor(max_workers=3)
time.sleep(5)
executor.submit(reddit_task.execute)
