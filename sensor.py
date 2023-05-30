import time
import board
import busio
from w1thermsensor import W1ThermSensor
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from analogipins import AnalogIOPins



class Sensor:

    def __init__(self):
        self.id=''
        self.temperature = None
        self.humidity = None
        self.water_temperature = None
        self.dissolved_oxygen = None
        self.dissolved_oxygen_calibration = None
        self.raw_dissolved_oxygen = None
        self.electrical_conductivity = None
        self.turbidity = None
        self.ph_level = None
        self.ads = None
    
    
        
    def read_water_temperature(self):
        self.water_temperature =  W1ThermSensor().get_temperature()
        return self.water_temperature
        
    def calibrate_dissolved_oxygen(self, calibration_mode):
        
        DO_Table = [
            14460, 14220, 13820, 13440, 13090, 12740, 12420, 12110, 11810, 11530,
            11260, 11010, 10770, 10530, 10300, 10080, 9860, 9660, 9460, 9270,
            9080, 8900, 8730, 8570, 8410, 8250, 8110, 7960, 7820, 7690,
            7560, 7430, 7300, 7180, 7070, 6950, 6840, 6730, 6630, 6530, 6410
        ]
        
        if calibrate_mode == 0:
            V_saturation = CAL1_V + 35 * temperature_c - CAL1_T * 35
            self.dissolved_oxygen_calibration =  voltage_mv * DO_Table[temperature_c] // V_saturation
        else:
            V_saturation = (temperature_c - CAL2_T) * (CAL1_V - CAL2_V) // (CAL1_T - CAL2_T) + CAL2_V
            self.dissolved_oxygen_calibration = voltage_mv * DO_Table[temperature_c] // V_saturation
    
    
    def get_raw_dissolved_oxygen(analogIO):
        sensor = AnalogIOpins(0)
        voltage = sensor.read_voltage()
        raw_value = sensor.read_raw_value()
        print("Voltage on DO Sensor:", voltage)
        print("Raw value on DO sensor:", raw_value)
        
