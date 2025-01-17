"""Task definitions."""


def scrape() -> None:
    """Scrape Reddit for new submissions and comments."""
    from holly_willoughbot.reddit import search_comments, search_submissions
    from holly_willoughbot.tables import RedditSubmissions, RedditSubreddits

    for subreddit in RedditSubreddits.objects().where(RedditSubreddits.enabled.eq(value=True)).run_sync():
        if not subreddit.first_scrape_complete:
            search_submissions(subreddit=subreddit.subreddit, limit=None)
            subreddit.first_scrape_complete = True
            subreddit.save().run_sync()
            continue
        search_submissions(subreddit=subreddit.subreddit, limit=subreddit.search_limit)
    for submission in RedditSubmissions.objects().where(RedditSubmissions.locked.eq(value=False)).run_sync():
        search_comments(submission_id=submission.submission_id)


def lock() -> None:
    """Lock submissions older than a week."""
    import datetime

    from holly_willoughbot.reddit import lock_submission
    from holly_willoughbot.tables import RedditSubmissions

    for submission in (
        RedditSubmissions.objects()
        .where(
            (RedditSubmissions.locked.eq(value=False))
            & (RedditSubmissions.created < datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=7)),
        )
        .run_sync()
    ):
        lock_submission(submission_id=submission.submission_id)


def notify() -> None:
    """Send Notifications for new submissions and comments."""
    from holly_willoughbot.tables import RedditComments, RedditSubmissions, RedditSubreddits
    from holly_willoughbot.telegram import send_message

    for subreddit in RedditSubreddits.objects().where(RedditSubreddits.muted.eq(value=False)).run_sync():
        for submission in (
            RedditSubmissions.objects()
            .where(RedditSubmissions.subreddit == subreddit.id and RedditSubmissions.notified.eq(value=False))
            .run_sync()
        ):
            send_message(
                client_id=subreddit.telegram_client,
                msg=(
                    "*New Post*:\n\n"
                    f"*Title:* {submission.title}\n"
                    f"*Subreddit:* {subreddit.subreddit}\n"
                    f"*User:* {submission.author}\n"
                    f"*Date:* {submission.created}\n"
                    f"*URL:* {submission.url}"
                ),
            )
            submission.notified = True
            submission.save().run_sync()
        for comment in (
            RedditComments.objects()
            .where(RedditComments.subreddit == subreddit.id and RedditComments.notified.eq(value=False))
            .run_sync()
        ):
            send_message(
                client_id=subreddit.telegram_client,
                msg=(
                    "*New Comment*:\n\n"
                    f"*Subreddit:* {subreddit.subreddit}\n"
                    f"*User*: {comment.author}\n"
                    f"*Date*: {comment.created}\n"
                    f"*URL*: {comment.url}\n"
                    "*Body*:\n"
                    f"{comment.body}\n\n"
                ),
            )
