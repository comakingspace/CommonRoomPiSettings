from datetime import datetime, time, timedelta
import subprocess
import os
import sys

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import bot_config as config

try:
        from icalevents.icalevents import events
        import calendar
except ImportError:
        output = subprocess.check_output([sys.executable, "-m", 'pip', 'install', "-r", str(os.path.join(os.path.dirname(__file__), "..", "requirements.txt"))])
        #pip = subprocess.call(["pip", "install -r " + str(os.path.join(os.path.dirname(__file__), "..\\")) + "requirements.txt"])
        #output = pip.stdout
        #output = subprocess.check_output(["pip", "install -r " + str(os.path.join(os.path.dirname(__file__), "..\\")) + "requirements.txt"])
        chunk_size = 4000
        for x in range (0,len(str(output)),chunk_size):
                sent_message = updater.bot.send_message(chat_id = next(iter(config.authorized_group2)) , text = str(output)[x:x+chunk_size], parse_mode=telegram.ParseMode.MARKDOWN, disable_notification=True)
else:
        pass

calendar_url = "https://calendar.google.com/calendar/ical/4hbi6bp3lol50h2m422ljg81t0%40group.calendar.google.com/public/basic.ics"

def get_events(days_to_check = 14):
        in_two_weeks = datetime.combine(datetime.today(), time.max) + timedelta(days=days_to_check)
        es = events(calendar_url,start=datetime.now(),end=in_two_weeks)
        message = ""
        for event in (event for event in sorted(es) if not ("Lunch Break Make" in event.summary or "Making Hours" in event.summary)):
                event.start = event.start.astimezone()
                event.end = event.end.astimezone()
                if not "Special Events" in message:
                        message = f"{message}\n*Special Events:*"
                translator = {"[": r"\[", "]":r"]"} #only escape the opening [ because otherwise telegram will show \] in the message
                message = f"{message}\n*{event.start.strftime('%A')}, {event.start.day:02}.{event.start.month:02}.{event.start.year:04}*\n    {event.start.hour:02}:{event.start.minute:02} - {event.end.hour:02}:{event.end.minute:02}\n    {event.summary.translate(str.maketrans(translator))}"

        for event in (event for event in sorted(es) if ("Lunch Break Make" in event.summary or "Making Hours" in event.summary)):
                event.start = event.start.astimezone()
                event.end = event.end.astimezone()
                if not "Opening Hours" in message:
                        message = "{}\n*Opening Hours*:".format(message)
                name = event.summary[event.summary.find("("):]
                message = f"{message}\n{event.start.strftime('%A')}, {event.start.day:02}.{event.start.month:02}.{event.start.year:04}\n    {event.start.hour:02}:{event.start.minute:02} - {event.end.hour:02}:{event.end.minute:02} {name}"

        return message

if __name__ == "__main__":
        message = get_events()
        print(message)
        if not message == None:
                updater = Updater(token=config.token)
                message = f"Hey all, here are the events from our [google calendar](https://calendar.google.com/calendar/embed?src=4hbi6bp3lol50h2m422ljg81t0%40group.calendar.google.com&ctz=Europe%2FBerlin) of the next two weeks:{message}"
                if config.mode =="debug":
                        for admin in config.authorized_group2:
                                sent_message = updater.bot.send_message(chat_id = admin, text = message, parse_mode=telegram.ParseMode.MARKDOWN, disable_notification=True)
                else:
                        chat = config.large_group_id
                        #chat = config.small_group_id
                        sent_message = updater.bot.send_message(chat_id = chat, text = message, parse_mode=telegram.ParseMode.MARKDOWN, disable_notification=True)