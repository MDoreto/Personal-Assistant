from application import app
from flask_mqtt import Mqtt


mqtt = Mqtt()
mqtt.init_app(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('NodeMcu')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)

def send_mqtt(text,topic='NodeMcu'):
    mqtt.publish(topic, text)