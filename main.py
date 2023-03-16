import os
import tweet_scrape as ts
from telegram.ext import Updater, MessageHandler, Filters
from urllib3.exceptions import ProtocolError
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = str(os.getenv("TELEGRAM_BOT"))

def run_tweet_bot():
    
    updater = Updater(API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - print chat id if
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, onjoin))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, onleft))
    
    updater.start_polling()

    try:
        print("Tweet bot started")
        Twitter_stream =  ts.TweetBot()
        Twitter_stream.fetch_tweets()
        
    except ProtocolError :
        print("Ended")
    
def onjoin(update, context):

    print("Bot join ", update.message.chat.title)
    print("Chat ID: ", update.message.chat.id)

def onleft(update, context):

    print("Bot left ", update.message.chat.title)
    print("Chat ID: ", update.message.chat.id)

if __name__ == '__main__':
    run_tweet_bot();
    exit(1)
    