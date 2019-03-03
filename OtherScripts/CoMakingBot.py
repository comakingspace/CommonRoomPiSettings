import ActiveWikiUsers
import Bot_config as config
import paho.mqtt.client as mqtt
import json
import RandomizeRingtone
import subprocess
import sys
import os

from socket import gaierror

from telegram.ext import Updater
updater = Updater(token=config.token)
dispatcher = updater.dispatcher

def start (bot, update):
    message = "(new)Thank you for contacting me. Your Chat ID is: " + str(update.message.chat_id) + "\n Right now, I am listening to the following messages:"
    for handler in dispatcher.handlers[0]:
        #message = message + "\n [/" + handler.command[0] + "](tg://bot_command?command=" + handler.command[0]
        message = message + "\n /" + handler.command[0]
    bot.send_message(chat_id=update.message.chat_id, text=message)
    
def wikiUser(bot, update):
    UserList = ActiveWikiUsers.getActiveUsers()
    del UserList['newlen']
    del UserList['ns']
    del UserList['oldlen']    
    bot.send_message(chat_id=update.message.chat_id, text = str(UserList))

def help (bot, update):
    message = "The documentation of this bot might soon be found in the CoMakingSpace Wiki. \n For the moment, please refer to /start"
    bot.send_message(chat_id=update.message.chat_id, text=message)

def nerven (bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="Sei einfach du selbst...")

def on_doorbell_answer (client, userdata, msg):
    payload = str(msg.payload)
    if (payload.startswith("b'The ringtone")):   
        updater.bot.send_message(chat_id=config.small_group_id, text = "The new ringtone is: " + payload[31:-1])
    print(msg.topic+" "+str(msg.payload))

def update (bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="Starting the update...")
    output = subprocess.check_output(["git", "pull"])
    bot.send_message(chat_id=update.message.chat_id, text="The git output is: \n" + str(output))
    _restart()

def new_ringtone(bot,update):
    RandomizeRingtone.randomize_ringtone()

def on_mqtt_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/DoorBell/Answers")

def _restart():
    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.chdir(os.getcwd())
    os.execv(sys.executable, args)

from telegram.ext import CommandHandler

start_handler = CommandHandler('start', start)
WikiUser_handler = CommandHandler('WikiUser', wikiUser)
nerven_handler = CommandHandler('wie_kann_ich_Martin_am_besten_nerven', nerven)
new_ringtone_handler = CommandHandler('Randomize_Ringtone',new_ringtone)
help_handler = CommandHandler('help', help)
update_handler = CommandHandler('update', update)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(WikiUser_handler)
dispatcher.add_handler(nerven_handler)
dispatcher.add_handler(new_ringtone_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(update_handler)
updater.start_polling()

client = mqtt.Client("Telegram_Bot")
try:
    client.connect(config.mqtt_host,1883,10)
    client.message_callback_add("/DoorBell/Answers", on_doorbell_answer)
    client.loop_start()
except gaierror:
    print("Not able to connect to MQTT")
#updater.bot.send_message(chat_id=config.group_id, text = 'bot started')

print('started')
