#!/usr/bin/env python

###############################################################################
#  Script for asynchronous reading from sensors and publishing data via MQTT  #
###############################################################################
import smbus, time, json, os, argparse, struct
from multiprocessing import Pipe
from mqtt import connect_mqtt

bus = smbus.SMBus(1)

bus = smbus.SMBus(1)
address_scd30 = 0x61

# Initialization control command for SGP30 (CO2 and VOC measurement)
Init_air_quality = 0x2003  # Initialization of air quality measurement

# Measurement command for SGP (CO2 and VOC measurement)
Measure_air_quality = 0x2008

COMMAND_CONTINUOUS_MEASUREMENT = 0x0010
COMMAND_SET_MEASUREMENT_INTERVAL = 0x4600
COMMAND_GET_DATA_READY = 0x0202
COMMAND_READ_MEASUREMENT = 0x0300
COMMAND_AUTOMATIC_SELF_CALIBRATION = 0x5306
COMMAND_SET_FORCED_RECALIBRATION_FACTOR = 0x5204
COMMAND_SET_TEMPERATURE_OFFSET = 0x5403
COMMAND_SET_ALTITUDE_COMPENSATION = 0x5102


def measure_co2():
    bus.write_i2c_block_data(address_scd30, 0x03, [0x00])
    data = bus.read_i2c_block_data(address_scd30, 0)
    time.sleep(2.)
    buffer = [data[0], data[1], data[3], data[4]]
    buffer_byte_array = bytearray(buffer)
    measurement = struct.unpack('>f', buffer_byte_array)
    return measurement


def get_co2_json(co2):
    value = {
        "device_name": "scd30",
        "co2": co2
    }
    return json.dumps(value)


def test_of_scd30(measurement):
    print("CO2 = {0} ppm".format(measurement))


def publish(client, conn_recv, topic_base):
    while True:
        measurement_json = conn_recv.recv()
        measurement = json.loads(measurement_json)
        if "co2" in measurement:
            topic = "co2"
        else:
            pass
        client.publish(topic=topic_base + topic, payload=measurement_json)


def handle_mqtt(args, conn_recv):
    client = connect_mqtt(args.host, args.client_id)
    client.loop_start()
    publish(client, conn_recv, args.topic_base)


def measure(conn_send):
    while True:
        # Measurement of CO2 and VOC
        measurement = measure_co2()
        if 0 < measurement == measurement:
            co2_json = get_co2_json(measurement)
            conn_send.send(co2_json)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True,
                        help='Broker MQTT host (ip:port)')
    parser.add_argument('--client_id', type=str, required=True,
                        help='Client id (unique name)')
    parser.add_argument('--topic_base', type=str, required=False, default='svm30/',
                        help='Topic base')
    args = parser.parse_args()

    conn_recv, conn_send = Pipe()

    pid = os.fork()
    if pid == 0:
        handle_mqtt(args, conn_recv)
    else:
        measure(conn_send)


if __name__ == '__main__':
    exit(main())
