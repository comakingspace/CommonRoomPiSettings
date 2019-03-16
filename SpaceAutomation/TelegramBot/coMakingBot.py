#!/usr/bin/python3 -u
#Standard library imports.
import sys
import os
import json

#Related third party imports.

#Local application/library specific imports.
import bot_config as config
from message_handling import CoMakingBot
from mqtt_handling import MqttHandler


if __name__ == "__main__":
    CoMakingBot.setup()
    CoMakingBot.run()
    MqttHandler.run()
    #updater.bot.send_message(chat_id=config.group_id, text = 'bot started')

    print('started')
