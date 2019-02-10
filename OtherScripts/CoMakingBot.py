import ActiveWikiUsers
import config

from telegram.ext import Updater
updater = Updater(token=config.token)
dispatcher = updater.dispatcher

def start (bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Johannes, Luzian, nicht so ungeduldig!")
    
def wikiUser(bot, update):
    UserList = ActiveWikiUsers.getActiveUsers()
    del UserList['newlen']
    del UserList['ns']
    del UserList['oldlen']    
    bot.send_message(chat_id=update.message.chat_id, text = str(UserList))

def help (bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Ich bin nur ein armer Bot. Was weiss ich, was ich alles kann.")

def nerven (bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="Sei einfach du selbst...")
from telegram.ext import CommandHandler

start_handler = CommandHandler('start', start)
WikiUser_handler = CommandHandler('WikiUser', wikiUser)
nerven_handler = CommandHandler('wie_kann_ich_Martin_am_besten_nerven', nerven)
help_handler = CommandHandler('help', help)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(WikiUser_handler)
dispatcher.add_handler(nerven_handler)
dispatcher.add_handler(help_handler)
updater.start_polling()

#updater.bot.send_message(chat_id=config.group_id, text = 'bot started')

print('started')
