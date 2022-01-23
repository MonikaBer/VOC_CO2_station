#!/usr/bin/env python

import smbus
import time
import json
import struct


bus = smbus.SMBus(1)
address_scd30 = 0x61

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


def test_of_scd30(measurement):
    print("CO2 = {0} ppm".format(measurement))


def print_co2_json(measurement):
    value = {
        "device_name": "scd30",
        "co2": measurement,
    }
    print(json.dumps(value))


def main():
    bus.write_i2c_block_data(address_scd30, 0x00, [0x10])

    while True:
        # Measurement of CO2
        value = measure_co2()
        print(value)


if __name__ == "__main__":
    main()
