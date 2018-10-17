#!/usr/bin/env python 
import mwapi
import json
import paho.mqtt.publish as publish
import pandas as pd
import datetime
session = mwapi.Session(host='https://wiki.comakingspace.de', api_path='/api.php')

recentchanges_result = session.get(action='query', 
                                    format='json', 
                                    list='recentchanges', 
                                    rcstart="{:%Y-%m-%d}T00:00:00.000Z".format(datetime.datetime.now()-datetime.timedelta(days=30)),
                                    rcend="{:%Y-%m-%d}T00:00:00.000Z".format(datetime.datetime.now()), 
                                    rcdir='newer', 
                                    rcprop='title|sizes|user', 
                                    rclimit='500', 
                                    rctype='edit|new|categorize|external')
changes = pd.DataFrame(recentchanges_result['query']['recentchanges'])
changes['changedlen'] = abs(changes['newlen'] - changes['oldlen'])
changes['count'] = 1
sorted = changes.groupby('user').sum().sort_values('changedlen',ascending=False)
top_3_users = "Most active wiki users:"
for i in range(0,3):
    top_3_users = "%s %i.%s:%s" % (top_3_users,i+1,sorted.iloc[i].name, sorted.iloc[i]['count'])
try:
    publish.single("/CommonRoom/FDD/Text", top_3_users, hostname="comakingcontroller")
except:
    print(changes.groupby('user').sum().sort_values('changedlen',ascending=False))
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
    publish.single("CommonRoom/FDD/Text", top_3_users, hostname="comakingcontroller")
