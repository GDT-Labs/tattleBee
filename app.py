import paho.mqtt.client as mqtt
import json
from imgurpython import ImgurClient
import os
import time

client_id = '75f55a5c2221a79'
client_secret = '7b039d13d0556893c3e5bc6461463ca5f22f3ee3'

mqttc = mqtt.Client()
mqttc.username_pw_set('9fd83945-7910-409f-ac4d-ff79128f3fec', 'sIrfSbTIfjHm')

# mqtt credentials
creds = {
    'clientId': 'Tn9g5RXkQQJ+sTf95Eo8/7A',
    'user':     '9fd83945-7910-409f-ac4d-ff79128f3fec',
    'password': 'sIrfSbTIfjHm',
    'topic':    '/v1/9fd83945-7910-409f-ac4d-ff79128f3fec/',
    'server':   'mqtt.relayr.io',
    'port':     1883
}

def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    global message
    message_data = json.loads(msg.payload)
    if message_data['meaning'] == 'request_image':
        print "Image requested..."
        get_image_and_post()

def on_log(mosq, obj, level, string):
    print(string)
    
def on_subscribe(client, userdata, mid, granted_qos):
    print "Subscribe: " + mid

def delete_image():
    os.system('rm -rf pic.jpg')

def get_image_and_post():
    client = ImgurClient(client_id, client_secret)
    print "Taking image..."
    os.system('raspistill -o pic.jpg')
    print "Uploading image to Imgur."
    capture = client.upload_from_path('pic.jpg', config=None, anon=True)
    publish_URL(creds, capture['link'])
    print "Uploaded image to " + capture['link']
    delete_image()

def publish_URL(credentials, url):
    message2 = {
    'meaning': 'image',
    'value': url
    }
    mqttc.publish(credentials['topic'] +'data', json.dumps(message2))

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect

# Connect
mqttc.connect("mqtt.relayr.io", 1883)

mqttc.subscribe("/v1/9fd83945-7910-409f-ac4d-ff79128f3fec/data", qos=0)

while (True):
    mqttc.loop()
