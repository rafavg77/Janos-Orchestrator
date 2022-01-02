import os
from telebot import types, telebot
import pihole as ph
import ipinfo
from configparser import ConfigParser

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, os.environ.get('SNORT_CONFIG'))
config = ConfigParser()
config.read(initfile)

BOT_TOKEN = config.get('params','telegram_token')
BOT_CHAT = config.get('params','telegram_chat_id')
IPINFO_TOKEN = config.get('params','ipinfo_token')
PIHOLE_ADDRESS = config.get('params','pihole_addess')
PIHOLE_AUTH = config.get('params','pihole_auth')


access_token = IPINFO_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)
pihole = ph.PiHole(PIHOLE_ADDRESS)
pihole.authenticate(PIHOLE_AUTH)

statusBlock = '🔥 Status de bloqueo PiHole 🔥'
changeStatus = '🎮 Cambiar Status de bloqueo PiHole 🎮'
checkIP = '🕹️ Consultar Direccion IP pública 🕹️'

def keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=5)
    itembtna = types.KeyboardButton(statusBlock)
    itembtnv = types.KeyboardButton(changeStatus)
    itembtnc = types.KeyboardButton(checkIP)
    markup.row(itembtna)
    markup.row(itembtnv)
    markup.row(itembtnc)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "You can use the keyboard",reply_markup=keyboard())

@bot.message_handler(commands=['blockStatus'])
def send_block_status(message):
    pihole.refresh()
    status = pihole.status
    bot.send_message(message.chat.id, "Blocking Status is: " + status)

@bot.message_handler(commands=['changeBlockStatus'])
def send_change_block_status(message):
    pihole.refresh()
    status = pihole.status
    if status == "disabled":
        pihole.enable()
        bot.send_message(message.chat.id, "Blocking Status is: Enabled")
    elif status == "enabled":
        pihole.disable(0)
        bot.send_message(message.chat.id, "Blocking Status is: Disabled")

@bot.message_handler(commands=['getIpinfo'])
def get_ip_info(message):
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails()
    bot.send_message(message.chat.id, "Public IP: " + details.ip)

@bot.message_handler(func=lambda message:True)
def all_messages(message):
    if message.text == statusBlock:
        send_block_status(message)
    elif message.text ==  changeStatus:
        send_change_block_status(message)
    elif message.text == checkIP:
        get_ip_info(message)

bot.infinity_polling()