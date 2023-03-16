import os
import tweepy as tp
import re
from telegram import Bot
from telegram import InputMediaPhoto
from telegram import ParseMode
from dotenv import load_dotenv
import orjson
load_dotenv()

token = str(os.getenv("TELEGRAM_BOT"))
bearerToken = str(os.getenv("BearerToken"))

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

class TwitterStream(tp.StreamingClient):

    def on_connect(self):
        print("Connected")
        
    def on_data(self, raw_data):
        # Received as bytes
        raw_data = orjson.loads(raw_data)
        
        print("data")
        print(raw_data.get('data', None))
        
        print("media")
        print(raw_data.get('includes', None))
        
        try:

            tg_text = raw_data.get('data', None)['text']

            ## trim any url from text, will add the tweet link at the bottom to prvent unexpected telegram preview
            tg_text = re.sub(r'https?:\/\/.*[\r]*','', tg_text)

            tweet_id = raw_data.get('data', None)['id']
            author_name = raw_data.get('includes', None)['users'][0]['username']
            
            tweet_link = "https://twitter.com/"+author_name+"/status/"+tweet_id
            caption = "#" + author_name + ":\n" + tg_text + "\n\n" + tweet_link
     
            raw_media_group = raw_data.get('includes', None).get('media', None)
            media_group = []
            
            ## Get image from tweet and upload it to telegram
            if(str(raw_media_group) != 'None'):
                if len(raw_media_group) > 0:
                    # find image
                    idx = 0

                    for media in raw_media_group:
                        preview_pic = media['url']
                        media_group.append(InputMediaPhoto(media=preview_pic, caption = caption if idx == 0 else ""))
                        idx = idx + 1
                    
            bot = Bot(token=token)
            sub = sublist[author_name]
            
            for chat_name in sub:
            
                chatid = grouplist[chat_name]

                if len(media_group) > 0:
                    bot.send_media_group(chat_id = chatid
                                    , media = media_group)
                else:
                    bot.send_message(chat_id=chatid
                    , text= "#" + author_name + ":\n" + tg_text + "\n\n" + tweet_link
                    , disable_web_page_preview=False
                    , parse_mode=ParseMode.HTML
                    , timeout=20
                    )
                    
        except Exception as e:
            print("error cannot get :" + str(e))
            
    def on_error(self,status_code):
        # if 403, go to https://developer.twitter.com/en to get correct token
        print(status_code)
        if status_code == 420:
            return False



class TweetBot():

    def __init__(self):
        pass


    def fetch_tweets(self):

        client = TwitterStream(bearerToken)

        ## In case you want to remove group, remove this comment block to delete rules via delete_rules
        """
        rules = client.get_rules()
        rule_ids = []
        for rule in rules.data:
            rule_ids.append(rule.id)
			
        if(len(rule_ids) > 0):
            client.delete_rules(rule_ids)
        else:
            print("no rules to delete")
        """

        for user in followingList:
            client.add_rules(tp.StreamRule("from:" + user))
        
            
        client.filter(
            expansions="attachments.poll_ids,attachments.media_keys,author_id",
            tweet_fields="text",
            user_fields="username",
            media_fields="duration_ms,height,media_key,preview_image_url,type,url,width"
        )          