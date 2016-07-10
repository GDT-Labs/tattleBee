import paho.mqtt.client as mqtt
import json

client_id = '75f55a5c2221a79'
client_secret = '7b039d13d0556893c3e5bc6461463ca5f22f3ee3'

def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    global message
    message_data = json.loads(msg.payload)
    if message_data['meaning'] == 'take_picture':
        get_image_and_post()

def on_log(mosq, obj, level, string):
    print(string)
    
def on_subscribe(client, userdata, mid, granted_qos):
    print "Subscribe: " + mid

def get_image_and_post():
    client = ImgurClient(client_id, client_secret)
    os.system('raspistill -vf -hf -o /home/pi/camera/pic.jpg')
    capture = client.upload_from_path('/home/pi/camera/pic.jpg', config=None, anon=True)
    print "Uploaded image to " + capture['link']

def publish_URL(url):
    return NotImplemented

mqttc = mqtt.Client()
mqttc.username_pw_set('9fd83945-7910-409f-ac4d-ff79128f3fec', 'sIrfSbTIfjHm')
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect

# Connect
mqttc.connect("mqtt.relayr.io", 1883)

mqttc.subscribe("/v1/9fd83945-7910-409f-ac4d-ff79128f3fec/data", qos=0)

while (True):
    mqttc.loop()
    get_image_and_post():
    time.sleep(10)