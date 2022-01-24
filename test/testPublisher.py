import random, time, json, os, argparse
from multiprocessing import Pipe
from mqtt import connect_mqtt

def get_co2_json(co2):
    value = {
        "device_name": "scd30",
        "co2": co2
    }
    return json.dumps(value)

def get_co2eq_json(co2eq):
    value = {
        "device_name": "svm30",
        "co2eq": co2eq
    }
    return json.dumps(value)

def get_voc_json(voc):
    value = {
        "device_name": "svm30",
        "voc": voc
    }
    return json.dumps(value)

def get_temp_json(temp):
    value = {
        "device_name": "svm30",
        "temp": round(temp, 2)
    }
    return json.dumps(value)

def get_rh_json(rh):
    value = {
        "device_name": "svm30",
        "rh": round(rh, 2)
    }
    return json.dumps(value)


def measure_co2():
    co2 = random.uniform(400, 60000)
    time.sleep(.5)
    return co2

def measure_co2eq_and_voc():
    co2eq = random.randint(400, 60000)
    voc = random.randint(0, 60000)
    time.sleep(.5)
    return (co2eq, voc)

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
            topic = "scd30/co2"
        if "co2eq" in measurement:
            topic = "svm30/co2eq"
        elif "voc" in measurement:
            topic = "svm30/voc"
        elif "temp" in measurement:
            topic = "svm30/temp"
        elif "rh" in measurement:
            topic = "svm30/rh"
        else:
            pass
        client.publish(topic = topic, payload = measurement_json)

def handle_mqtt(args, conn_recv):
    client = connect_mqtt(args.host, args.client_id)
    client.loop_start()
    publish(client, conn_recv)


def measure(conn_send):
    while True:
        measurement = measure_co2()
        co2_json = get_co2_json(measurement)
        #print(co2_json)
        conn_send.send(co2_json)

        measurement = measure_co2eq_and_voc()
        co2eq_json = get_co2eq_json(measurement[0])
        voc_json = get_voc_json(measurement[1])
        #print(co2eq_json)
        #print(voc_json)
        conn_send.send(co2eq_json)
        conn_send.send(voc_json)

        measurement = measure_temp_and_rh()
        temp_json = get_temp_json(measurement[0])
        rh_json = get_rh_json(measurement[1])
        #print(temp_json)
        #print(rh_json)
        conn_send.send(temp_json)
        conn_send.send(rh_json)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type = str, required = True,
                        help = 'Broker MQTT host (ip:port)')
    parser.add_argument('--client_id', type = str, required = True,
                        help = 'Client id (unique name)')
    args = parser.parse_args()

    conn_recv, conn_send = Pipe()

    pid = os.fork()
    if pid == 0:
        handle_mqtt(args, conn_recv)
    else:
        measure(conn_send)


if __name__ == '__main__':
    exit(main())
