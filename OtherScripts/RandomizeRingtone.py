import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import paho.mqtt
import random

def getRingtones():
    #subscribe.callback(on_answer,"/DoorBell/Answers",hostname="comakingcontroller")
    publish.single("/DoorBell/Control", "{'command':'listsd','payload':'/Ringtones'}", hostname="comakingcontroller")
    answer = subscribe.simple("/DoorBell/Answers",msg_count=1, hostname="comakingcontroller")
    #test = "Hallo"
    listOfMusic = []
    answerAsString = answer.payload.decode("utf-8")
    if (answerAsString[:10]=='SD Content'):
        listOfFiles = answerAsString.split("\n")
        for file in listOfFiles:
            print(file)
            if (file.find(".mp3") != -1):
                listOfMusic.append(file[:file.find(".mp3")+4])
    #print("%s %s" % (answer.topic, answer.payload))
    return listOfMusic

def on_answer(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

def randomize(listOfFiles):
    newFile = listOfFiles[random.randint(0,len(listOfFiles)-1)]
    return newFile

def setNewRingtone(newFile):
    publish.single("/DoorBell/Control", "{'command':'selectringfile','payload':'{}'}".format(newFile), hostname="comakingcontroller")

if __name__ == "__main__":
    #possibleFiles = getRingtones()
    setNewRingtone(randomize(getRingtones()))