import sys          
import time
import datetime
import board
import busio

#import adafruit_ads1x15.ads1115 as ADS
#from adafruit_ads1x15.analog_in import AnalogIn
from DFRobot_ADS1115 import ADS1115
import SDL_Pi_HDC1080
import doSensor
import ecSensor
import phSensor
from w1thermsensor import W1ThermSensor, Sensor

import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

ADS1115_REG_CONFIG_PGA_4_096V        = 0x02

#influxdb
token = "n2TK4tu9UOPRHB_wKnNSXhuVlmZRCUyhnD7ZHpLDAOv1zfTHCDi8JAx474vM-zQNhcHnoLYRbbUYpEQ19Ps9LQ=="
org = "dev"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
bucket = "rpi3test"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS) 
sensor = W1ThermSensor(Sensor.DS18B20, "3c54f6486295")

hdc1080 = SDL_Pi_HDC1080.SDL_Pi_HDC1080()
hdc1080.turnHeaterOn()
hdc1080.turnHeaterOff()

hdc1080.setTemperatureResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
hdc1080.setHumidityResolution(SDL_Pi_HDC1080.HDC1080_CONFIG_HUMIDITY_RESOLUTION_14BIT)

# Create the I2C bus
i2c = busio.I2C(board.D3, board.D2)

# Create the ADC object using the I2C bus
ads1115 = ADS1115()
ads1115.setAddr_ADS1115(0x48)
#Sets the gain and input voltage range.
ads1115.setGain(ADS1115_REG_CONFIG_PGA_4_096V)
#ads.setGain(GAIN_ONE)

# Initialize sensor objects
do = doSensor.doSensor()
ec = ecSensor.DFRobot_EC()
ph = phSensor.DFRobot_PH()

# Create single-ended input on channel 0




print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    wtp = sensor.get_temperature()
    atp = hdc1080.readTemperature()
    ahm = hdc1080.readHumidity()
    #wtp = 25.55	
    #atp = 31.26
    #ahm = 81.24
    chan1 = ads1115.readVoltage(0)	#DO sensor
    chan2 = ads1115.readVoltage(1)	#EC Sensor
    chan3 = ads1115.readVoltage(2)	#PH Sensor
    pHv = ph.readPH((chan1['r']), wtp)
    #time.sleep(1)
    dov = do.readDO(wtp, (chan2['r']))
    #time.sleep(1)
    ecv = ec.readEC((chan3['r']), wtp)
    #time.sleep(1)
    
    print ("Water Temperature = %3.1f C" % wtp)
    print ("Air Temperature = %3.1f C" % atp)
    print ("Humidity = %3.1f %%" % ahm)
    print("S1: {:>5.3f}".format(chan1['r']))
    print("S2: {:>5.3f}".format(chan2['r']))
    print("S3: {:>5.3f}".format(chan3['r']))
    print("Water pH = %3.2f " % pHv)
    print("Dissolved Oxygen = %3.2f mg/L" % dov)
    print("Electrical Conductivity = %3.2f" % ecv)
    
    point = Point("production_data")\
    .tag("sensor", "raspberrypi")\
    .field("ph_level", pHv)\
    .field("dissolved_oxygen", dov)\
    .field("electrical_conductivity", ecv)\
    .field("ambient_temperature", atp)\
    .field("humidity", ahm)\
    .field("temperature", wtp)\
    .field("ph_voltge", chan1['r'])\
    .field("do_volt", chan2['r'])\
    .field("ec_volt", chan3['r'])
    
    
    write_api.write(bucket=bucket, record=point)
    time.sleep(30)
    