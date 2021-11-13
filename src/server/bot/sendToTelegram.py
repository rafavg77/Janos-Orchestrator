import os
import logging
import telebot
from configparser import ConfigParser

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, '/home/pi/Production/MonitorLeases/src/config/config.ini')
config = ConfigParser()
config.read(initfile)

BOT_TOKEN = config.get('params','telegram_token')
BOT_CHAT = config.get('params','telegram_chat_id')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def sendMessage(message):
    # Create bot
    bot = telebot.TeleBot(token=BOT_TOKEN)

    # Send message
    bot.send_message(BOT_CHAT, message)
