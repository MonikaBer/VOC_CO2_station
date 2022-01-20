from paho.mqtt.client import Client

def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker...")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = Client(client_id = client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect("localhost", port = 1850, keepalive = 60)
    return client
