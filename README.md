# 3D Printer Simulator for MyMiniFactory Click & Print

This simulator acts as a connected 3D printer communicating with the MyMiniFactory MQTT API.

Current features:
- Connects to the MyMiniFactory's MQTT server
- Subscribe to messages
- Sends status update regularly

## How to Install

```bash
git clone 

pip install -r requirements.txt

cp .env.dist .env
```

## Run simulator

```bash
python printer_simulator.py
```

## Configure

You should set your own settings in the .env files.

Default config is:
```
host = "staging.myminifactory.com"
port = 8883
client_id = "test-manufacturer"
api_key = "1234"
status_topic = "/printers"
model = "test-model"
serial = "model-1234-5678-1234-5678"
status = "free"
temperature = 30
progress = 0
token = "abcd"
```