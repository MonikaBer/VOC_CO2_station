#!/usr/bin/env python

###############################################################################
#  Script for asynchronous reading from sensors and publishing data via MQTT  #
###############################################################################
import smbus, time, json, os, argparse
from multiprocessing import Pipe
from mqtt import connect_mqtt

bus = smbus.SMBus(1)

address_sgp30 = 0x58
address_shtc1 = 0x70

# Initialization control command for SGP30 (CO2 and VOC measurement)
Init_air_quality = 0x2003  # Initialization of air quality measurement

# Measurement command for SGP (CO2 and VOC measurement)
Measure_air_quality = 0x2008

# Important informations about SGP30:
# The sensor responds with 2 data bytes (MSB first) and 1
# CRC byte for each of the two preprocessed air quality signals in the order CO2eq (ppm) and TVOC (ppb).
# For the first 15s after the “Init_air_quality” command the sensor is in an
# initialization phase during which a “Measure_air_quality”
# command returns fixed values of 400 ppm CO2eq and 0 ppb TVOC.
# A new “Init_air_quality” command has to be sent after every power-up or soft reset.

Measure_raw_signals = 0x2050
Get_baseline = 0x2015
Set_baseline = 0x201e
Set_humidity = 0x2061
Measure_test = 0x2032
Get_feature_set_version = 0x202f

# Control commands for SHTC1 sensor
Read_Temp = 0x7866  # Temperature
Read_RH = 0x58E0  # Relative humidity


def init_sgp30():
    # WARNING: INITIALIZATION LASTS 15 SECONDS
    bus.write_i2c_block_data(address_sgp30, 0x20, [0x03])
    time.sleep(.5)

def measure_co2_and_voc():
    bus.write_i2c_block_data(address_sgp30, 0x20, [0x08])
    time.sleep(.6)
    value = bus.read_i2c_block_data(address_sgp30, 0)
    time.sleep(.8)
    co2 = value[0] * 256 + value[1]
    voc = value[3] * 256 + value[4]
    return (co2, voc)

def measure_temp_and_rh():
    bus.write_i2c_block_data(address_shtc1, 0x78, [0x66])
    time.sleep(.6)
    value = bus.read_i2c_block_data(address_shtc1, 0x78, 6)
    time.sleep(.8)
    temp_byte_value = value[0] * 256 + value[1]
    rh_byte_value = value[3] * 256 + value[4]
    temp = -45.68 + 175.7 * temp_byte_value / (2 ** 16)
    rh = (103.7 - 3.2 * (temp_byte_value / (2 ** 16))) * rh_byte_value / (2 ** 16)
    return (temp, rh)


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


def test_of_sgp30(measurement):
    print("CO2 = {0} ppm".format(measurement[0]))
    print("VOC = {0} ppb\n".format(measurement[1]))


def test_of_shtc1(measurement):
    print("temp = {:0.2f}°C".format(measurement[0]))
    print("RH = {:0.2f}%\n".format(measurement[1]))


def publish(client, conn_recv, topic_base):
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
        client.publish(topic = topic_base + topic, payload = measurement_json)

def handle_mqtt(args, conn_recv):
    client = connect_mqtt(args.host, args.client_id)
    client.loop_start()
    publish(client, conn_recv, args.topic_base)


def measure(conn_send):
    while True:
        # Measurement of CO2 and VOC
        measurement = measure_co2_and_voc()
        co2_json = get_co2_json(measurement[0])
        voc_json = get_voc_json(measurement[1])
        #print(co2_json)
        #print(voc_json)
        conn_send.send(co2_json)
        conn_send.send(voc_json)

        # Additional measurement of temperature and relative humidity
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
    parser.add_argument('--topic_base', type = str, required = False, default = 'svm30/',
                        help = 'Topic base')
    args = parser.parse_args()

    # Initialization of SGP30 sensor
    init_sgp30()

    conn_recv, conn_send = Pipe()

    pid = os.fork()
    if pid == 0:
        handle_mqtt(args, conn_recv)
    else:
        measure(conn_send)


if __name__ == '__main__':
    exit(main())
