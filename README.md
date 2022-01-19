# VOC_CO2_station
CO2 and volatile organic compounds measurement using IoT sensors and Raspberry Pi.

## MQTT topics:
- voc
- co2
- temp
- rh

## JSON format:
- { ‘device_name’ : (string), ‘time’: (timestamp), ‘co2’: (int), ‘voc’ : (int) }
- { ‘device_name’ : (string), ‘time’: (timestamp), ‘temp’: (float), ‘rh’ : (float) } 

## Ranges and units
- VOC:     0  - 60,000           [ppb] 
- CO2:    400 - 60,000           [ppm] 
- TEMP:   -20 – 85      (+/- 1)  [°C]
- RH:      0  - 100     (+/- 5)  [% relative humidity]  
