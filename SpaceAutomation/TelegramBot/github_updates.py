#!/usr/bin/python3 -u
from github import Github
from datetime import datetime, time, timedelta
from github.GithubException import RateLimitExceededException
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import bot_config as config

def get_updates(days_to_check = 1):
    g = Github()
    try:
        repo = g.get_repo('comakingspace/do-something')
        yesterday = datetime.combine(datetime.today(), time.min) - timedelta(days=days_to_check)
        issues = repo.get_issues(state='all', since=yesterday)
        message = ""
        for issue in issues:
            #print(issue)
            #get the comments
            if issue.created_at > yesterday:
                 message = f"{message}[Issue {issue.number}]({issue.html_url}) ({issue.title}) got created by {issue.user.login}\n"
            if issue.comments > 0:
                    comments = issue.get_comments(since=yesterday)
                    if comments.totalCount > 0:
                            message = f"{message}[Issue {issue.number}]({issue.html_url}) ({issue.title}) got {comments.totalCount} new comment(s)\n"
            events = issue.get_events()
            for event in (event for event in events if event.created_at > yesterday):
                if event.event == 'mentioned':
                    #do nothing
                    pass
                elif event.event == 'closed':
                    message = f"{message}[Issue {issue.number}]({issue.html_url}) ({issue.title}) got {event.event} by {event.actor.login}\n"
                elif event.event == 'subscribed':
                    #do nothing
                    pass
                elif event.event == 'assigned':
                    #message = f"{message}{event.actor.login} got {event.event} to [Issue {issue.number}]({issue.html_url}) ({issue.title})\n"
                    pass
                elif event.event == 'reopened':
                    message = f"{message}[Issue {issue.number}]({issue.html_url}) ({issue.title}) got {event.event} by {event.actor.login}\n"
                elif event.event == 'unassigned':
                    #message = f"{message}{event.actor.login} got {event.event} from [Issue {issue.number}]({issue.html_url}) ({issue.title})\n"
                    pass
                elif event.event == 'renamed':
                    message = f"{message}[Issue {issue.number}]({issue.html_url}) got {event.event} to {issue.title}\n"
                else:
                    #do nothing
                    pass
            #check the recent updates for this issue
    except RateLimitExceededException as e:
        message = "Rate limit exceeded"
    except:
        message = "Some error occurred"
    if message == "":
        return None
    return(message)

if __name__ == "__main__":
    message = get_updates()
    print(message)
    if not message == None:
        updater = Updater(token=config.token)
        message = "Hey all, here is the update of what happened since yesterday morning in our [Issue Tracker](https://github.com/comakingspace/do-something/issues):\n{message}"
        #chat = config.large_group_id
        #chat = config.small_group_id
        #updater.bot.send_message(chat_id = chat, text = message, parse_mode=telegram.ParseMode.MARKDOWN, disable_notification=True)
        for admin in config.authorized_group2:
                        sent_message = updater.bot.send_message(chat_id = admin, text = message, parse_mode=telegram.ParseMode.MARKDOWN, disable_notification=True)