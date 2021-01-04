#!/usr/bin/python3
"""A script that retrieves Poem_for_your_sprog comments."""
import json
import sys

from absl import app
from absl import flags
from absl import logging
import praw
import prawcore

USER_AGENT = 'linux:sprogapi:1.1'

FLAGS = flags.FLAGS
flags.DEFINE_string('username', None, 'The name of the user to connect as.')
flags.DEFINE_string('password', None, 'The password of the user to connect as. \
If using 2FA, this should be of the form password:2fa_token.')
flags.DEFINE_string('client_secret', None, 'The client_secret token to use. \
See OAuth2 authentication.')
flags.DEFINE_string('client_id', None, 'The client_id token to use. \
See OAuth2 authentication.')
flags.DEFINE_string('path_to_database', None, 'An optional path to a file that \
will be loaded before other poems are retrieved. The file contains \
json-encoded poems, in the format output by this same program.')

flags.mark_flag_as_required('username')
flags.mark_flag_as_required('password')
flags.mark_flag_as_required('client_id')
flags.mark_flag_as_required('client_secret')


def load_poems_from_file(path: str) -> dict:
    "Load poems from JSON-encoded file."""
    poems = {}
    with open(path, 'r') as file:
        poems = json.load(file)
    logging.info('Loaded %d poems from "%s"', len(poems), path)
    return poems


def retrieve_poems() -> dict:
    """Connects to Reddit and retrieves the last 1000 poems.

    Returns:
        A dictionary of the retrieved poems, indexed by comment id
    """
    try:
        reddit = praw.Reddit(
                client_id=FLAGS.client_id, client_secret=FLAGS.client_secret,
                user_agent=USER_AGENT, username=FLAGS.username,
                password=FLAGS.password)

        candidates = reddit.redditors.search('Poem_for_your_sprog')
        for candidate in candidates:
            if candidate.name != 'Poem_for_your_sprog':
                continue
            sprog = candidate

        if not sprog:
            logging.error('Cannot find /u/Poem_for_your_sprog, exiting.')
            sys.exit(1)

        comments = {}
        for comment in sprog.comments.new(limit=None):
            comments[comment.id] = {
                    'body': comment.body,
                    'id': comment.id,
                    'score': comment.score,
                    'permalink': comment.permalink,
            }
        logging.info('Retrieved %d poems.', len(comments))
    except prawcore.exceptions.OAuthException:
        logging.error('Invalid credentials, exiting.')
        sys.exit(2)

    return comments


def main(argv):
    """Retrieves poems from Reddit."""
    del argv
    poems = {}
    if FLAGS.path_to_database:
        poems = load_poems_from_file(FLAGS.path_to_database)
    new_poems = retrieve_poems()

    poems.update(new_poems)
    print(json.dumps(poems))
    logging.info("Written %d poems to stdout", len(poems))


if __name__ == '__main__':
    app.run(main)
