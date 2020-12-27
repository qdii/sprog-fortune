This repository contains a set of tools to create a fortune database out of /u/poem_for_your_sprog comments on Reddit.

Tools:

- `reddit_fetcher.py`: prints the last 1000 comments of /u/poem_for_your_sprog's to stdout, JSON-encoded. It queries Reddit API. Requires a username, password, client_id and client_token. The 2 latter can be created using by creating a "script" app on your reddit profile. See [OAuth2 documentation](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example).
- `format_for_strfile.sed`: contains a list of commands for `sed` that will modify the input into a format that is acceptable for `strfile`. `strfile` produces files that `fortune` understands.

Usage:

```
$ ./reddit_fetcher.py <USERNAME> <PASSWORD[:2FA_TOKEN]> <CLIENT_ID> <CLIENT_SECRET> | jq 'flatten | .[].body' | sed -f format_for_strfile.sed > sprog && strfile sprog
```

The command produces two files: `sprog` and `sprog.dat`, both of them need to be placed in `/usr/share/fortune` to be available in `fortune`.
