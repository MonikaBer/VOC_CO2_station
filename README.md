# VOC_CO2_station
CO2 and volatile organic compounds measurement using IoT sensors and Raspberry Pi.

## MQTT topics:
- voc
- co2
- temp
- rh

## JSON format:
- { ‘device_name’ : (string), ‘co2’: (int) }
- { ‘device_name’ : (string), ‘voc’ : (int) }
- { ‘device_name’ : (string), ‘temp’: (float) }
- { ‘device_name’ : (string), ‘rh’ : (float) }

## Ranges and units
- VOC:     0  - 60,000           [ppb]
- CO2:    400 - 60,000           [ppm]
- TEMP:   -20 – 85      (+/- 1)  [°C]
- RH:      0  - 100     (+/- 5)  [% relative humidity]

# Configuration
MQTT broker:
```
sudo apt-get install mosquitto
systemctl status mosquitto
```

MQTT clients:
```
pip install paho-mqtt
PYTHONPATH=$PYTHONPATH:<path_to_project_workdir/.
export PYTHONPATH
```

# Usage
Start MQTT Broker:
```
mosquitto -p 1850
```

Start publisher:
```{python3.8}
python svm30Collector.py --host <ip>:1850 --client_id client_pub_1 --topic_base svm30/
```

Start subscriber:
```{python3.8}
python receiver.py --host <ip>:1850 --client_id client_sub_1 --topic_base svm30/
```
