import paho.mqtt.client as mqtt
from mqtt import connect_mqtt


def subscribe(client):
    def on_message(client, userdata, msg):
        print(f"Payload: {msg.payload.decode()}, topic: {msg.topic}")

    client.subscribe("co2")
    client.subscribe("voc")
    client.subscribe("temp")
    client.subscribe("rh")
    client.on_message = on_message


def main():
    client = connect_mqtt("client_3")
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    exit(main())
