import time
import board
import random
import adafruit_dht
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


#dhtDevice = adafruit_dht.DHT22(board.D17)
token = " "
org = "dev"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
bucket = "rpi3test"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

while True:
    try:
        # Print the values to the serial port
        #temperature_c = dhtDevice.temperature
        #temperature_f = temperature_c * (9 / 5) + 32
        #humidity = dhtDevice.humidity
        temperature_c = random.randrange(20,40,1)
        humidity = random.randrange(20,100,8)
        turbidity = random.randrange(1,20,1)
        ph_level = random.randrange(1,10,1)
        dissolved_oxygen = random.randrange(1,20,1)
        electrical_conductivity = random.randrange(1,5,1)
        point = Point("test_measure")\
        .tag("sensor", "my-sensor")\
        .field("temperature", temperature_c)\
        .field("humidity", humidity)\
        .field("turbidity", turbidity)\
        .field("ph_level", ph_level)\
        .field("dissolved_oxygen", dissolved_oxygen)\
        .field("electrical_conductivity", electrical_conductivity)\
        
        
        # Write the point to the InfluxDB database
        write_api.write(bucket=bucket, record=point)

        
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(10)
        continue
    except Exception as error:
        #dhtDevice.exit()
        raise error

    time.sleep(10)



    