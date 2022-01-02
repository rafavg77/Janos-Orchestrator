import os,sys
from telebot import types, telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import pihole as ph
import ipinfo
from configparser import ConfigParser

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from server.db import databaseHelper


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
getHosts = '💻 Consultar todos los Hosts 💻'

def keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=5)
    itembtna = types.KeyboardButton(statusBlock)
    itembtnv = types.KeyboardButton(changeStatus)
    itembtnc = types.KeyboardButton(checkIP)
    itembtnd = types.KeyboardButton(getHosts)
    markup.row(itembtna)
    markup.row(itembtnv)
    markup.row(itembtnc)
    markup.row(itembtnd)
    return markup

def gen_host_markup():
    hosts = databaseHelper.selectUniqueHosts()
    markup = InlineKeyboardMarkup()
    markup.row_width = len(hosts)
    for host in hosts:
            markup.add(InlineKeyboardButton("💻 " + host[2] + " - Notificar : "+  host[3], callback_data='{}'.format(host[0])+","+'{}'.format(host[3])+","+'{}'.format(host[2])))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call.data)
    id = call.data.split(',')[0]
    if call.data.split(',')[1] == 'Y':
        notify = 'N'
    elif call.data.split(',')[1] == 'N':
        notify = 'Y'
    databaseHelper.updateUniqueHosts(id,notify)
    gen_host_markup()
    
    bot.answer_callback_query(call.id, "Modificando el host: " + call.data.split(',')[2])

@bot.message_handler(commands=['getHosts'])
def get_hosts(message):
    bot.send_message(message.chat.id, "Selecciona un Host: ", reply_markup=gen_host_markup())

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Puedes utilizar el teclado",reply_markup=keyboard())

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
    elif message.text == getHosts:
        get_hosts(message)

bot.send_message(BOT_CHAT, "🐧Bot is Running 🐧")
bot.infinity_polling()