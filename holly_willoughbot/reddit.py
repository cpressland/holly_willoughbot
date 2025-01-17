"""Reddit API functions."""

import datetime

from loguru import logger as log
from praw import Reddit

from holly_willoughbot.tables import RedditClients, RedditComments, RedditSubmissions, RedditSubreddits


def reddit_client(client_id: str) -> Reddit:
    """Return a Reddit client."""
    client = RedditClients.objects().get(RedditClients.id == client_id).run_sync()
    return Reddit(
        client_id=client.client_id,
        client_secret=client.client_secret,
        username=client.username,
        password=client.password,
        user_agent="python:holly_willoughbot:v3.0.0 (by /u/cpressland)",
    )


def search_submissions(subreddit: str, limit: None | int = 25) -> None:
    """Search a subreddit for new posts.

    Args:
        subreddit (str): The subreddit to search.
        limit (None | int): The number of posts to search.

    """
    log.info(f"Searching Subreddit: {subreddit}")
    _subreddit = RedditSubreddits.objects().get(RedditSubreddits.subreddit == subreddit).run_sync()
    client = reddit_client(_subreddit.reddit_client)
    for submission in client.subreddit(subreddit).new(limit=limit):
        if not RedditSubmissions.exists().where(RedditSubmissions.submission_id == submission.id).run_sync():
            log.info(f"Processing Submission: {submission.id}")
            RedditSubmissions.insert(
                RedditSubmissions(
                    submission_id=submission.id,
                    subreddit=_subreddit.id,
                    title=submission.title,
                    author=submission.author.name if submission.author else "[deleted]",
                    created=datetime.datetime.fromtimestamp(submission.created_utc, tz=datetime.UTC),
                    locked=submission.locked if not submission.archived else submission.archived,
                    url=f"https://reddit.com{submission.permalink}",
                    notified=False,
                ),
            ).run_sync()
            continue
        log.debug(f"Skipping Submission: {submission.id}")


def lock_submission(submission_id: str) -> None:
    """Lock a submission.

    Args:
        submission_id (str): The submission ID to lock.

    """
    log.info(f"Locking Submission: {submission_id}")
    submission = RedditSubmissions.objects().get(RedditSubmissions.submission_id == submission_id).run_sync()
    subreddit = RedditSubreddits.objects().get(RedditSubreddits.id == submission.subreddit).run_sync()
    client = reddit_client(subreddit.reddit_client)
    client.submission(id=submission_id).mod.lock()
    submission.locked = True
    submission.save().run_sync()


def search_comments(submission_id: str) -> None:
    """Search for comments on submissions.

    Args:
        submission_id (str): The submission ID to search for comments.

    """
    log.info(f"Searching Comments for Submission: {submission_id}")
    submission = RedditSubmissions.objects().get(RedditSubmissions.submission_id == submission_id).run_sync()
    subreddit = RedditSubreddits.objects().get(RedditSubreddits.id == submission.subreddit).run_sync()
    client = reddit_client(subreddit.reddit_client)
    for comment in client.submission(id=submission_id).comments.list():
        if not RedditComments.exists().where(RedditComments.comment_id == comment.id).run_sync():
            log.info(f"Processing Comment: {comment.id}")
            RedditComments.insert(
                RedditComments(
                    comment_id=comment.id,
                    submission_id=submission.id,
                    subreddit=subreddit.id,
                    author=comment.author.name if comment.author else "[deleted]",
                    created=datetime.datetime.fromtimestamp(comment.created_utc, tz=datetime.UTC),
                    body=comment.body,
                    url=f"https://reddit.com{comment.permalink}",
                    notified=False,
                ),
            ).run_sync()
            continue
        log.debug(f"Skipping Comment: {comment.id}")
