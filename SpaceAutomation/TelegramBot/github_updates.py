from github import Github
from datetime import datetime, time, timedelta
from github.GithubException import RateLimitExceededException

def get_updates(days_to_check = 1):
    g = Github()
    try:
        repo = g.get_repo('comakingspace/do-something')
        yesterday = datetime.combine(datetime.today(), time.min) - timedelta(days=days_to_check)
        issues = repo.get_issues(state='all', since=yesterday)
        message = ""
        for issue in issues:
            print(issue)
            #get the comments
            if issue.comments > 0:
                    comments = issue.get_comments(since=yesterday)
                    if comments.totalCount > 0:
                            message = "{}Issue {} ({}) got {} new comment(s)\n".format(message, issue.number, issue.title, comments.totalCount)
            events = issue.get_events()
            for event in (event for event in events if event.created_at > yesterday):
                message = "{}Issue {} ({}) got {} by {}\n".format(message, issue.number,issue.title, event.event, event.actor.name)
            #check the recent updates for this issue
    except RateLimitExceededException as e:
        message = "rate limit exceeded"
    except:
        message = "some error occurred"
    if message == "":
        return("No updates available")
    return(message)

if __name__ == "__main__":
    print(get_updates(int('3')))