import argparse
from mqtt import connect_mqtt


def subscribe(client, topic_base):
    def on_message(client, userdata, msg):
        print(f"Payload: {msg.payload.decode()}, topic: {msg.topic}")

    client.subscribe(topic_base + "co2")
    client.subscribe(topic_base + "voc")
    client.subscribe(topic_base + "temp")
    client.subscribe(topic_base + "rh")
    client.on_message = on_message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type = str, required = True,
                        help = 'Broker MQTT host (ip:port)')
    parser.add_argument('--client_id', type = str, required = True,
                        help = 'Client id (unique name)')
    parser.add_argument('--topic_base', type = str, required = False, default = 'svm30/',
                        help = 'Topic base')
    args = parser.parse_args()


    client = connect_mqtt(args.host, args.client_id)
    subscribe(client, args.topic_base)
    client.loop_forever()


if __name__ == '__main__':
    exit(main())
