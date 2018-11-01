
import paho.mqtt.client as mqtt
import time
import logging
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys
import select
import json
import datetime

from classes.printer import Printer

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


keep_looping = True

# host = "localhost"
# port = 1883
host = "mqtt.myminifactory.com"
port = 8883

client_id = "octoprint_myminifactory"
api_key = "b4943605-52b5-4d13-94ee-34eb983a813f"
# client_id = "printer-manufacturer"
# api_key = "1234"

status_topic = "/printers"

model = "biqu-printer"
serial = "simulator-123456"
status = "free"
temperature = 25
progress = 0
token = "abcd"

printer = Printer(model, serial, status, progress, temperature)

def received_action(payload):
    global printer
    logger.debug(str(payload))
    paredPayload = json.loads(payload)

    if paredPayload['action_code'] == "100":
        logger.debug("received prepare 100")
        # status = "prepare"
        printer.prepare()
    if paredPayload['action_code'] == "101":
        logger.debug("received print 101")
        printer.print()
    if paredPayload['action_code'] == "102":
        logger.debug("received pause 102")
        printer.pause()
    if paredPayload['action_code'] == "103":
        logger.debug("received cancel 103")
        printer.cancel()
    if paredPayload['action_code'] == "104":
        logger.debug("received resume 104")
        printer.resume()
    

def send_status(client):
    global printer

    client.loop_start()
    while keep_looping:
        status_dict = {
            'actionCode': '300',
            'date': datetime.datetime.utcnow().isoformat(),
            'status': printer.status,
            'serial_number': printer.serial,
            'model': printer.model,
            'temperature': printer.temperature,
            'progress' : printer.progress
        }
        status_string = json.dumps(status_dict)
        logger.debug("Sending status: " + status_dict['status'])
        client.publish(status_topic, status_string)
        time.sleep(1)

def on_connect(client, userdata, flags, rc):
    global printer


    logger.debug("Connected with result code "+str(rc))
    topic = "/printers/"+printer.model+"/"+printer.serial
    client.subscribe(topic)
    logger.debug("subscribed to topic "+ topic)


def on_disconnect(client, userdata, rc):
    logger.debug("Disconnect with result code "+str(rc))


def on_message(client, userdata, msg):
    logger.debug("Message received")
    received_action(msg.payload)

client = mqtt.Client()
client.tls_set()
client.username_pw_set(client_id, api_key)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

logger.debug("connect")
client.connect(host, port, 60)

send_status(client)