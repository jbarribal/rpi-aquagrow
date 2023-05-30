import time
import board
import random
import adafruit_dht
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


token = "n2TK4tu9UOPRHB_wKnNSXhuVlmZRCUyhnD7ZHpLDAOv1zfTHCDi8JAx474vM-zQNhcHnoLYRbbUYpEQ19Ps9LQ=="
org = "dev"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
bucket = "rpi3test"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)




def writeDataToInfluxDB(data, interval):
    try:
        point = Point("aquagrow")\
        .tag("device", "raspberrypi")\
        .field("temperature", data.temperature)\
        .field("humidity", data.humidity)\
        .field("turbidity", data.turbidity)\
        .field("ph_level", data.ph_level)\
        .field("dissolved_oxygen", data.dissolved_oxygen)\
        .field("electrical_conductivity", data.electrical_conductivity)\
        
        write_api.write(bucket=bucket, record=point)
        

    except Exception as error:
        raise error
    
    time.sleep(interval)
        