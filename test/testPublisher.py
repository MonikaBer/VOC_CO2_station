import random, time, json, os
from multiprocessing import Pipe
from mqtt import connect_mqtt

def get_co2_json(co2):
    value = {
        "device_name": "sgp30",
        "co2": co2
    }
    return json.dumps(value)

def get_voc_json(voc):
    value = {
        "device_name": "sgp30",
        "voc": voc
    }
    return json.dumps(value)

def get_temp_json(temp):
    value = {
        "device_name": "sgp30",
        "temp": round(temp, 2)
    }
    return json.dumps(value)

def get_rh_json(rh):
    value = {
        "device_name": "sgp30",
        "rh": round(rh, 2)
    }
    return json.dumps(value)


def measure_co2_and_voc():
    co2 = random.randint(400, 60000)
    voc = random.randint(0, 60000)
    time.sleep(.5)
    return (co2, voc)

def measure_temp_and_rh():
    temp = random.uniform(-20.0, 85.0)
    rh = random.uniform(0.0, 100.0)
    time.sleep(.5)
    return (temp, rh)

def publish(client, conn_recv):
    while True:
        measurement_json = conn_recv.recv()
        #print(measurement_json)
        measurement = json.loads(measurement_json)
        if "co2" in measurement:
            topic = "co2"
        elif "voc" in measurement:
            topic = "voc"
        elif "temp" in measurement:
            topic = "temp"
        elif "rh" in measurement:
            topic = "rh"
        else:
            pass
        client.publish(topic = topic, payload = measurement_json)

def handle_mqtt(conn_recv):
    client = connect_mqtt("client_1")
    client.loop_start()
    publish(client, conn_recv)


def measure(conn_send):
    while True:
        measurement = measure_co2_and_voc()
        co2_json = get_co2_json(measurement[0])
        voc_json = get_voc_json(measurement[1])
        #print(co2_json)
        #print(voc_json)
        conn_send.send(co2_json)
        conn_send.send(voc_json)

        measurement = measure_temp_and_rh()
        temp_json = get_temp_json(measurement[0])
        rh_json = get_rh_json(measurement[1])
        #print(temp_json)
        #print(rh_json)
        conn_send.send(temp_json)
        conn_send.send(rh_json)


def main():
    conn_recv, conn_send = Pipe()

    pid = os.fork()
    if pid == 0:
        handle_mqtt(conn_recv)
    else:
        measure(conn_send)


if __name__ == '__main__':
    exit(main())
