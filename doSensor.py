
import math

class doSensor:
    vref = 5000	#mV
    res = 4096	#adc resolution
    
    DO_Table = [
    14460, 14220, 13820, 13440, 13090, 12740, 12420, 12110, 11810, 11530,
    11260, 11010, 10770, 10530, 10300, 10080, 9860, 9660, 9460, 9270,
    9080, 8900, 8730, 8570, 8410, 8250, 8110, 7960, 7820, 7690,
    7560, 7430, 7300, 7180, 7070, 6950, 6840, 6730, 6630, 6530, 6410]
    
    lowTemp = 10
    highTemp = 35
    
    lowVolt = 1150
    highVolt = 1750
    
    
    def __init__(self):
        pass
    
    def setVRef(self, value):
        self.vref = value
        
    def setRes(self, value):
        self.res = value
        
    def setLow(self, tempVal, voltVal):
        self.lowTemp = tempVal
        self.lowVolt = voltVal
        
    def setHigh(self, tempVal, voltVal):
        self.highTemp = tempVal
        self.highVolt = voltVal
        
    def readDO(self, tempVal, voltVal):
        V_saturation = (tempVal - self.highTemp) * (self.lowVolt - self.highVolt) / (self.lowTemp - self.highTemp) + self.highVolt;
        tempSet = math.floor(tempVal)
        return (voltVal * self.DO_Table[tempSet] / V_saturation) / 1000;