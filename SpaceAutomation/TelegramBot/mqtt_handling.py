#Standard library imports.
import sys
import os
import subprocess
from socket import gaierror

#Related third party imports.
import paho.mqtt.client as mqtt

#Local application/library specific imports.
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  
from message_handling import CoMakingBot
import bot_config as config

class MqttHandler:
    mqtt_client = mqtt.Client("Telegram_Bot")

    def on_doorbell_answer (client, userdata, msg):
        payload = str(msg.payload)
        if (payload.startswith("b'The ringtone")):   
            CoMakingBot.updater.bot.send_message(chat_id=config.small_group_id, text = "The new ringtone is: " + payload[31:-1])
        print(msg.topic+" "+str(msg.payload))

    def on_mqtt_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("/DoorBell/Answers")
    
    def send(topic, message):
        MqttHandler.mqtt_client.publish(topic,message)

    def run():
        try:
            MqttHandler.mqtt_client.connect(config.mqtt_host,1883,10)
            MqttHandler.mqtt_client.message_callback_add("/DoorBell/Answers", on_doorbell_answer)
            MqttHandler.mqtt_client.loop_start()
        except gaierror:
            print("Not able to connect to MQTT")
