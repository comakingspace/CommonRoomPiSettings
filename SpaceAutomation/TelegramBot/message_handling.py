#Standard library imports.
import sys
import os
import subprocess

#Related third party imports.
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import paho.mqtt.client as mqtt

#Local application/library specific imports.
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  
from Ringtones import RandomizeRingtone
from WikiUsers import ActiveWikiUsers
import github_updates

from mqtt_handling import MqttHandler
import bot_config as config

class CoMakingBot:
    updater = Updater(token=config.token)
    dispatcher = updater.dispatcher
    mqtt_client = mqtt.Client("Telegram_Bot")

    def start (bot, update):
        message = "Thank you for contacting me. Your Chat ID is: " + str(update.message.chat_id) + "\n Right now, I am listening to the following messages:"
        for handler in CoMakingBot.dispatcher.handlers[0]:
            if type(handler) == telegram.ext.commandhandler.CommandHandler:
                #message = message + "\n [/" + handler.command[0] + "](tg://bot_command?command=" + handler.command[0]
                message = message + "\n /" + handler.command[0]
        if update.message.chat_id in config.authorized_group1:
            message = message + "\n You are also authorized for the following commands from group 1:"
            for handler in CoMakingBot.dispatcher.handlers[1]:
                if type(handler) == telegram.ext.commandhandler.CommandHandler:
                    message = message + "\n /" + handler.command[0]
        if update.message.chat_id in config.authorized_group2:
            message = message + "\n You are also authorized for the following commands from group 2:"
            for handler in CoMakingBot.dispatcher.handlers[2]:
                if type(handler) == telegram.ext.commandhandler.CommandHandler:
                    message = message + "\n /" + handler.command[0]
        bot.send_message(chat_id=update.message.chat_id, text=message)  
    def wikiUser (bot, update):
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
    def update (bot,update):
        if update.message.chat_id in config.authorized_group2:
            bot.send_message(chat_id=update.message.chat_id, text="Starting the update...")
            output = subprocess.check_output(["git", "pull"])
            bot.send_message(chat_id=update.message.chat_id, text="The git output is: \n" + str(output))
            CoMakingBot._restart()
        else:
            bot.send_message(chat_id=update.message.chat_id, text = "not authorized")
    def new_ringtone (bot,update):
        if update.message.chat_id in config.authorized_group1:
            RandomizeRingtone.randomize_ringtone()
        else:
            bot.send_message(chat_id=update.message.chat_id, text = "not authorized")

    def fdd (bot,update,args):
        if update.message.chat_id in config.authorized_group1:
            text = ""
            for word in args:
                text = text + word + " "
            MqttHandler.send('/CommonRoom/FDD/Text',text[:-1])
        else:
            bot.send_message(chat_id=update.message.chat_id, text = "not authorized")

    def events(bot,update,args):
        import google_calendar
        if len(args) > 0:
                message = google_calendar.get_events(int(args[0]))
        else:
            message = google_calendar.get_events()
        if message == None:
            message = "Unfortunately, there is no event available in the given timeframe."
        bot.send_message(chat_id=update.message.chat_id, text = message, parse_mode=telegram.ParseMode.MARKDOWN)

    def github_events (bot,update,args):
        if update.message.chat_id in config.authorized_group2:
            if len(args) > 0:
                message = github_updates.get_updates(int(args[0]))
            else:
                message = github_updates.get_updates()
            if message == None:
                message = "Unfortunately, there is no update available in the given timeframe."
            bot.send_message(chat_id=update.message.chat_id, text = message, parse_mode=telegram.ParseMode.MARKDOWN)

    def bell_sounds (bot, update):
        #print("got the bell command")
        bot.send_message(chat_id=update.message.chat_id, text="got the bell command") 
        ringtones = RandomizeRingtone.getFiles("")
        keyboard = []
        message = "ringtones:"

        for ringtone in ringtones:
            message = message + "\n /" + ringtone
            #keyboard.append([InlineKeyboardButton(ringtone,callback_data=ringtone)])
        bot.send_message(chat_id=update.message.chat_id, text=message) 
        #reply_markup = InlineKeyboardMarkup(keyboard)
        #update.message.reply_text('Please choose:', reply_markup=reply_markup)

    def buttonReply (bot, update):
        query = update.callback_query
        message = "{'command': 'play','payload': '{}'}".format(query.data)

        query.edit_message_text(text="Selected option: {}".format(query.data))

    def _restart():
        args = sys.argv[:]
        args.insert(0, sys.executable)
        if sys.platform == 'win32':
            args = ['"%s"' % arg for arg in args]
        os.chdir(os.getcwd())
        os.execv(sys.executable, args)
    def setup():
        start_handler = CommandHandler('start', CoMakingBot.start)
        WikiUser_handler = CommandHandler('WikiUser', CoMakingBot.wikiUser)
        nerven_handler = CommandHandler('wie_kann_ich_Martin_am_besten_nerven', CoMakingBot.nerven)
        new_ringtone_handler = CommandHandler('Randomize_Ringtone',CoMakingBot.new_ringtone)
        help_handler = CommandHandler('help', CoMakingBot.help)
        update_handler = CommandHandler('update', CoMakingBot.update)
        fdd_handler = CommandHandler('FDD',CoMakingBot.fdd,pass_args=True)
        github_handler = CommandHandler('github',CoMakingBot.github_events,pass_args=True)
        google_handler = CommandHandler('events', CoMakingBot.events, pass_args=True)

        CoMakingBot.dispatcher.add_handler(start_handler)
        CoMakingBot.dispatcher.add_handler(WikiUser_handler)
        CoMakingBot.dispatcher.add_handler(nerven_handler,1)
        CoMakingBot.dispatcher.add_handler(new_ringtone_handler,1)
        CoMakingBot.dispatcher.add_handler(help_handler)
        CoMakingBot.dispatcher.add_handler(fdd_handler,1)
        CoMakingBot.dispatcher.add_handler(google_handler)
        CoMakingBot.dispatcher.add_handler(update_handler,2)
        CoMakingBot.dispatcher.add_handler(github_handler,2)

        bell_handler = CommandHandler('doorbell',CoMakingBot.bell_sounds)
        CoMakingBot.dispatcher.add_handler(bell_handler,2)
        bell_callback_handler = CallbackQueryHandler(CoMakingBot.buttonReply)
        CoMakingBot.dispatcher.add_handler(bell_callback_handler)
        #print("handlers registered")
    def run():
        CoMakingBot.updater.start_polling()
        print("bot started")

if __name__ == "__main__":
    CoMakingBot.setup()
    CoMakingBot.run()
