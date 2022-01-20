import random, time, json, os
from multiprocessing import Pipe

def get_co2_and_voc_json(measurement):
    value = {
        "device_name": "sgp30",
        "co2": measurement[0],
        "voc": measurement[1]
    }
    return json.dumps(value)

def get_temp_and_rh_json(measurement):
    value = {
        "device_name": "sgp30",
        "temp": round(measurement[0], 2),
        "rh": round(measurement[1], 2)
    }
    return json.dumps(value)


def get_co2_and_voc_value():
    co2 = random.randint(400, 60000)
    voc = random.randint(0, 60000)
    time.sleep(.5)
    return (co2, voc)

def get_temp_and_rh_value():
    temp = random.uniform(-20.0, 85.0)
    rh = random.uniform(0.0, 100.0)
    time.sleep(.5)
    return (temp, rh)


def handleMqtt(conn_recv):
    while True:
        measurement_json = conn_recv.recv()
        print(measurement_json)

def measure(conn_send):
    while True:
        measurement = get_co2_and_voc_value()
        measurement_json = get_co2_and_voc_json(measurement)
        #print(measurement_json)
        conn_send.send(measurement_json)

        measurement = get_temp_and_rh_value()
        measurement_json = get_temp_and_rh_json(measurement)
        #print(measurement_json)
        conn_send.send(measurement_json)


def main():
    conn_recv, conn_send = Pipe()

    pid = os.fork()
    if pid == 0:
        handleMqtt(conn_recv)
    else:
        measure(conn_send)


if __name__ == '__main__':
    exit(main())
