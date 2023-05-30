import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class AnalogIOPins:
    def __init__(self, channel, analogpin):
        self.channel = channel
        self.ads = ADS.ADS1115(busio.I2C(board.SCL, board.SDA))
        self.channel_obj = AnalogIn(self.ads, getattr(analogpin, f'P{self.channel}'))

    def read_voltage(self):
        return self.channel_obj.voltage

    def read_raw_value(self):
        return self.channel_obj.value
