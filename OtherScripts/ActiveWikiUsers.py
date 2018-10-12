#!/usr/bin/env python 
import mwapi
import json
import paho.mqtt.publish as publish

#getting the active users from the wiki
session = mwapi.Session(host='https://wiki.comakingspace.de', api_path='/api.php')
query_result = session.get(action='query', list='allusers', auactiveusers='1')
users = query_result['query']['allusers']
#sorting them
users = sorted(users, key = lambda user: user['recenteditcount'],reverse=True)
#finding the 3 most active users. Count can be adjusted by changing the header of the for loop
top_3_users = "Most active wiki users:"
for i in range(0,3):
    top_3_users = "%s %i.%s:%i" % (top_3_users,i+1,users[i]['name'], users[i]['recenteditcount'])

#Sending it via mqtt
publish.single("CommonRoom/FDD/Text", top_3_users, hostname="comakingcontroller")
