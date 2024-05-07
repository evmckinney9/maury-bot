import asyncio

import asyncpraw


async def get_reddit_comments(thread_url, N=25):
    reddit_instance = asyncpraw.Reddit(
        client_id="8ZsTaoJGWqysfpErsxBxZg",
        client_secret="J8W2mtOg6KfLsSWP3x0RHbvLNV1R9A",
        user_agent="script:maury:v1.0 (by u/evmckinney9)"
    )
    submission = await reddit_instance.submission(url=thread_url)
    submission.comment_sort = 'new'  # Set sort before fetching comments
    await submission.load()  # Explicitly load the submission after setting the sort
    await submission.comments.replace_more(limit=0)
    top_level_comments = submission.comments[:N]

    # Creating JSON objects for each comment
    comments_json = [
        {
            "role": "user",
            "content": f"@{comment.author.name}: {comment.body}"
        } for comment in top_level_comments if comment.author is not None
    ]
    await reddit_instance.close()
    return comments_json


async def main():
    comments = await get_reddit_comments(thread_url="https://www.reddit.com/r/SquaredCircle/comments/1clwu2v/live_wwe_raw_discussion_thread_may_6th_2024/")
    print(comments)

if __name__ == "__main__":
    asyncio.run(main())
