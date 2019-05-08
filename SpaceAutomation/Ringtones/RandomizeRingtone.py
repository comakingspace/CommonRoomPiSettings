import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import paho.mqtt
import random

def getFiles(folder="/Ringtones"):
    #subscribe.callback(on_answer,"/DoorBell/Answers",hostname="comakingcontroller")
    publish.single("/DoorBell/Control", "{'command':'listsd','payload':'{}'}".format(folder), hostname="comakingcontroller")
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

def randomize_files(listOfFiles):
    newFile = listOfFiles[random.randint(0,len(listOfFiles)-1)]
    return newFile

def setNewRingtone(newFile):
    print(newFile)
    print("Setting ringtone to:{}".format(newFile))
    publish.single("/DoorBell/Control", "{{'command':'selectringfile','payload':'{}'}}".format(newFile), hostname="comakingcontroller")

def randomize_ringtone():
    setNewRingtone(randomize_files(getRingtones()))

if __name__ == "__main__":
    #possibleFiles = getRingtones()
    randomize_ringtone()