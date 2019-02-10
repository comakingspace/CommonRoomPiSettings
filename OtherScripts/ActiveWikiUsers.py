#!/usr/bin/env python 
import mwapi
import json
import paho.mqtt.publish as publish
import pandas as pd
import datetime
import argparse
session = mwapi.Session(host='https://wiki.comakingspace.de', api_path='/api.php')

parser = argparse.ArgumentParser(description='Publish the most active wiki users on the FlipDotDisplay')
parser.add_argument('--Users', dest='user_count', type=int, default=3, help='How many users should get displayed?')
parser.add_argument('--Days', dest='days', type=int, default=7, help='how many days should be taken into account?')
args = parser.parse_args()
user_count = args.user_count
days = args.days

def getActiveUsers():
    recentchanges_result = session.get(action='query', 
                                        format='json', 
                                        list='recentchanges', 
                                        rcstart="{:%Y-%m-%d}T00:00:00.000Z".format(datetime.datetime.now()-datetime.timedelta(days=days)),
                                        rcend="{:%Y-%m-%d}T23:59:59.999Z".format(datetime.datetime.now()), 
                                        rcdir='newer', 
                                        rcprop='title|sizes|user', 
                                        rclimit='500', 
                                        rctype='edit|new|categorize|external|log')
    changes = pd.DataFrame(recentchanges_result['query']['recentchanges'])
    changes['changedlen'] = abs(changes['newlen'] - changes['oldlen'])
    changes.loc[(changes['type']=='log') & (changes['title'].str.startswith('File')),'changedlen']=300
    changes['count'] = 1
    sorted_users = changes.groupby('user').sum().sort_values('changedlen',ascending=False)
    return sorted_users

if __name__ == "__main__":
    sorted_users = getActiveUsers()
    top_3_users = "Most active wiki users:"
    if len(sorted_users) < user_count:
        user_count = len(sorted_users)
    for i in range(0,user_count):
        top_3_users = "%s %i.%s" % (top_3_users,i+1,sorted_users.iloc[i].name)
    try:
        publish.single("/CommonRoom/FDD/Text", top_3_users, hostname="comakingcontroller")
    except:
        print(sorted_users)
        print(top_3_users)

def activeusers():
    #getting the active users from the wiki
    global session
    activeuser_result = session.get(action='query', list='allusers', auactiveusers='1')
    users = activeuser_result['query']['allusers']
    #sorting them
    users = sorted(users, key = lambda user: user['recenteditcount'],reverse=True)
    #finding the 3 most active users. Count can be adjusted by changing the header of the for loop
    top_3_users = "Most active wiki users:"
    for i in range(0,3):
        top_3_users = "%s %i.%s:%i" % (top_3_users,i+1,users[i]['name'], users[i]['recenteditcount'])

    #Sending it via mqtt
    publish.single("/CommonRoom/FDD/Text", top_3_users, hostname="comakingcontroller")
