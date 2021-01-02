This repository contains a set of tools to create a fortune database out of /u/poem_for_your_sprog comments on Reddit.

Tools:

- `reddit_fetcher.py`: prints the last 1000 comments of /u/poem_for_your_sprog's to stdout, JSON-encoded. It queries Reddit API. Requires a username, password, client_id and client_token. The 2 latter can be created using by creating a "script" app on your reddit profile. See [OAuth2 documentation](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example).
- `format_for_strfile.sed`: contains a list of commands for `sed` that will modify the input into a format that is acceptable for `strfile`. `strfile` produces files that `fortune` understands.

Usage:

```
$ ./reddit_fetcher.py --username=<USERNAME> --password=<PASSWORD[:2FA_TOKEN]> --client_id=<CLIENT_ID> --client_secret=<CLIENT_SECRET> [--path_to_database=sprog.json] > sprog_new.json
$ mv sprog_new.json sprog.json
$ cat sprog.json | jq 'flatten | .[].body' | sed -f format_for_strfile.sed > sprog && strfile sprog
```

The command produces three files: `sprog.json`, `sprog` and `sprog.dat`. The two latter need to be placed in `/usr/share/fortune` to be available in `fortune`. The former is the sprog database, which can be enriched by re-running the script regularly.
