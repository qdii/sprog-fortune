#!/usr/bin/python3
"""A script that retrieves Poem_for_your_sprog comments."""
import json
import sys
import praw

if len(sys.argv) < 5:
    print(f'Usage: {sys.argv[0]} <USERNAME> <PASSWORD[:2FA_TOKEN]> \
<CLIENT_ID> <CLIENT_SECRET>')
    sys.exit(1)

USER_AGENT = 'linux:sprogapi:1.0'
CLIENT_ID = sys.argv[3]
CLIENT_SECRET = sys.argv[4]
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT,
                     username=USERNAME,
                     password=PASSWORD)

candidates = reddit.redditors.search('Poem_for_your_sprog')
for c in candidates:
    if c.name != 'Poem_for_your_sprog':
        continue
    sprog = c

if not sprog:
    print('Cannot find /u/Poem_for_your_sprog')
    sys.exit(1)

comments = {}
for comment in sprog.comments.new(limit=None):
    comments[comment.id] = {
            'body': comment.body,
            'id': comment.id,
            'score': comment.score,
            'permalink': comment.permalink,
    }

print(json.dumps(comments))
