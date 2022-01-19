import random, time, json

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


def main():
    while True:
        measurement = get_co2_and_voc_value()
        print_co2_and_voc_json(measurement)

        measurement = get_temp_and_rh_value()
        print_temp_and_rh_json(measurement)


if __name__ == '__main__':
    exit(main())
