import paho.mqtt.client as mqtt 
import services 
MQTT_SERVER = "192.168.0.173" 
MQTT_PATH = 'Desktop' 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_PATH)
def on_message(client, userdata, msg):
    action = msg.payload.decode("utf-8")
    print(action)
    getattr(services, action)()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
client.loop_forever()# use this line if you don't want to write any further code. It blocks the code forever to check for data
#client.loop_start()  #use this line if you want to write any more code here