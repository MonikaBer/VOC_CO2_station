import argparse
from mqtt import connect_mqtt


def subscribe(client):
    def on_message(client, userdata, msg):
        print(f"Payload: {msg.payload.decode()}, topic: {msg.topic}")

    client.subscribe("scd30/co2")

    client.subscribe("svm30/co2eq")
    client.subscribe("svm30/voc")
    client.subscribe("svm30/temp")
    client.subscribe("svm30/rh")
    client.on_message = on_message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type = str, required = True,
                        help = 'Broker MQTT host (ip:port)')
    parser.add_argument('--client_id', type = str, required = True,
                        help = 'Client id (unique name)')
    args = parser.parse_args()


    client = connect_mqtt(args.host, args.client_id)
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    exit(main())
