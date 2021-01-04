#!/bin/bash

ONE_DAY=$((24*60*60))

while /bin/true; do
    tmp_sprog=$(mktemp)
    ./reddit_fetcher.py \
        --username="$REDDITOR" --password="$PASSWORD" --client_id="$CLIENT_ID" \
        --client_secret="$CLIENT_SECRET" --path_to_database=sprog.json > $tmp_sprog
    [[ -s $tmp_sprog ]] && mv $tmp_sprog sprog.json
    sleep $ONE_DAY
done

