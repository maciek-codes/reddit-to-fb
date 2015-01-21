TIWT - Today I was taught
=========================

Reddit to Facebook aggregator of top posts from /r/TodayIlearned

It runs as a WebJob on Microsoft Azure and uses Azure Table Storage as a cache.


Getting access token
---
You can use the script in access_token folder. Provide FB Client ID and secret and page Id you want to generate the access token for.


lib/post.py
---
This script is used to get posts from Reddit.com. It specifies how many posts should be fetched and from which subreddit.

Testing
----
Run: `python -m tests` and that will run all unit tests in tests/ folder.