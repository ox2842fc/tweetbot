# TweetBot

A simple Telegram Bot to Stream the tweets from any account from twitter to your telegram channel.

Using Twitter API v2 and tweepy 4.13.0 .

# Requirement

* python 3.9

# Guide
1. Get Twitter API BearerToken from [here](https://developer.twitter.com/en)
2. Go to [@BotFather](https://t.me/botfather) in telegram and create a Bot
3. Create .env for your token.
4. Open `tweet_scrape.py` and add the usernames of the person's you want to Stream tweets and update channel mapping

```py
## twitter user name
followingList = []

## Get chat id / group id from telegram
grouplist = {
    "exmaple_group" : "",
    "playground" : ""
}

## tweet & telegram mapping
sublist = {
    "twitter_username1" : ["exmaple_group"],
    "twitter_username2" : ["exmaple_group","playground"]
}
```

5. Run the Bot by executing:
```
pip install -r requirements.txt
python main.py
```