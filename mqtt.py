from paho.mqtt.client import Client

def connect_mqtt(host, client_id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker...")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client = Client(client_id = client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect

    try:
        (address, port) = host.split(':')
        port = int(port)
    except:
        raise RuntimeError('\nWrong host format!\n')

    try:
        client.connect(address, port = port, keepalive = 60)
    except:
        raise RuntimeError('\nConnection error! Check address and port.\n')

    return client
