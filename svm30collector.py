#!/usr/bin/env python

import smbus
import time
import json

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
    return [co2, voc]


def measure_temp_and_rh():
    bus.write_i2c_block_data(address_shtc1, 0x78, [0x66])
    time.sleep(.6)
    value = bus.read_i2c_block_data(address_shtc1, 0x78, 6)
    time.sleep(.8)
    temp_byte_value = value[0] * 256 + value[1]
    rh_byte_value = value[3] * 256 + value[4]
    temp = -45.68 + 175.7 * temp_byte_value / (2 ** 16)
    rh = (103.7 - 3.2 * (temp_byte_value / (2 ** 16))) * rh_byte_value / (2 ** 16)
    return [temp, rh]


def test_of_sgp30(measurement):
    print("CO2 = {0} ppm".format(measurement[0]))
    print("VOC = {0} ppb\n".format(measurement[1]))


def test_of_shtc1(measurement):
    print("temp = {:0.2f}°C".format(measurement[0]))
    print("RH = {:0.2f}%\n".format(measurement[1]))


def print_co2_and_voc_json(measurement):
    value = {
        "device_name": "sgp30",
        "co2": measurement[0],
        "voc": measurement[1]
    }
    print(json.dumps(value))


def print_temp_and_rh_json(measurement):
    value = {
        "device_name": "sgp30",
        "temp": round(measurement[0], 2),
        "rh": round(measurement[1], 2)
    }
    print(json.dumps(value))


def main():
    # Initialization of SGP30 sensor
    init_sgp30()

    while True:
        # Measurement of CO2 and VOC
        value = measure_co2_and_voc()
        print_co2_and_voc_json(value)
        # Additional measurement of temperature and relative humidity
        value = measure_temp_and_rh()
        print_temp_and_rh_json(value)


if __name__ == "__main__":
    main()
