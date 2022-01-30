# VOC_CO2_station
CO2 and volatile organic compounds measurement using IoT sensors and Raspberry Pi.

## MQTT topics:
- co2
- voc
- co2eq
- temp
- rh

## JSON format:
- { ‘device_name’ : (string), ‘co2’ : (float) }
- { ‘device_name’ : (string), ‘co2eq’: (int) }
- { ‘device_name’ : (string), ‘voc’ : (int) }
- { ‘device_name’ : (string), ‘temp’: (float) }
- { ‘device_name’ : (string), ‘rh’ : (float) }

## Ranges and units
- VOC:     0  - 60,000           [ppb]
- CO2eq:  400 - 60,000           [ppm]
- TEMP:   -20 –   85    (+/- 1)  [°C]
- RH:      0  -  100    (+/- 5)  [% relative humidity]
- CO2:     0  - 40,000  (+/- 30) [ppm]

# Configuration

1. MQTT Broker

Install Mosquitto:
```
sudo apt-get install mosquitto
```

Add configuration to the end of _**/etc/mosquitto/mosquitto.conf**_ file:
```
listener 1850 0.0.0.0
allow_anonymous true
```

2. MQTT clients

```
pip3 install paho-mqtt
PYTHONPATH=$PYTHONPATH:/path/to/project/workdir/.
export PYTHONPATH
```

# Usage
1. Start Mosquitto MQTT Broker:
```
sudo service mosquitto start
```

2. Start publisher on Raspberry Pi:
```{python3.8}
python3 svm30Collector.py --host <ip>:1850 --client_id client_pub_1 --topic_base svm30/
```

3. Start subscriber:
```{python3.8}
python test/testSubscriber.py --host <ip>:1850 --client_id client_sub_1
```
