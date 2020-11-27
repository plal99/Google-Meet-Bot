import os
from dotenv import load_dotenv
import requests
from discord_webhooks import DiscordWebhooks
from twilio.rest import Client 

load_dotenv()

# discord
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

# whatsapp twilio
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_NUM = os.getenv("TWILIO_NUM")
MY_NUM = os.getenv("MY_NUM")

# client = Client(TWILIO_SID, TWILIO_TOKEN)

# telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def sendTelegram(message):
    try:
        send_text = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage?chat_id=' + TELEGRAM_CHAT_ID + '&text=' + message
        
        response = requests.get(send_text)

    except:
        pass

def sendDiscord(message):
    webhook = DiscordWebhooks(DISCORD_WEBHOOK)
    # webhook.set_content(title='Seems like no class today',
    #                     description="No join button found! Assuming no class.")
    webhook.set_content(title = message)
    webhook.send()

def sendWhatsapp(message):
    pass






# $ pip install notify-run
# $ notify-run configure https://notify.run/oduMTzm40TzRcNv4
# $ notify-run send "Hello from notify.run"
# import pause
# from pynput.mouse import Button, Controller

# This module is for notification (very hassle free - please check it out)
# from notify_run import Notify