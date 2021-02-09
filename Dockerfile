FROM arm32v7/python:3

COPY reddit_fetcher.py .
COPY requirements.txt .
COPY sprog.json .

RUN apt-get update
RUN apt-get install --yes python3-pip
RUN /usr/bin/python3 -m pip install --no-cache-dir -r requirements.txt

ENTRYPOINT /reddit_fetcher.py --username=$REDDITOR --password=$PASSWORD --client_id=$CLIENT_ID --client_secret=$CLIENT_SECRET --path_to_database=sprog.json

