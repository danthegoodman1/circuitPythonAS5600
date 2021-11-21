from time import sleep
import busio
from board import *
from as5600 import AS5600

addr = 0x36
AS5600_id = 0x36

def main():
    print("running main")
    i2c = busio.I2C(GP1, GP0)
    z = AS5600(i2c, addr)
    z.scan()
    print('finished scan')
    while True:
        print("MD reg:", z.MD)
        sleep(1)


def test():
    i2c = busio.I2C(GP1, GP0, frequency = 400000)
    while not i2c.try_lock():
        pass
    d = i2c.scan()
    print(d)
    for i in d:
        if i == addr:
            print("yeah", i)
    i2c.unlock()
    print("reading registers:")
    while True:
        while not i2c.try_lock():
            pass
        # Write first
        i2c.writeto(AS5600_id, bytearray([0x0b]))
        # TODO: Try with I2CDevice too?
        # Then read
        buffer = bytearray(1)
        i2c.readfrom_into(AS5600_id, buffer)
        # i2c.readfrom_into(AS5600_id, buffer, start = 0x0b, end = 0x0c)
        print("buffer:", buffer[0])
        print("Magnet detected:", buffer[0]&32 != 0)
        print("Magnet too weak:", buffer[0]&16 != 0)
        print("Magnet too strong:", buffer[0]&8 != 0)
        # Get angle
        i2c.writeto(AS5600_id, bytearray([0x0c]))
        buffer = bytearray(1)
        i2c.readfrom_into(AS5600_id, buffer)
        angHi = buffer[0]
        i2c.writeto(AS5600_id, bytearray([0x0d]))
        buffer = bytearray(1)
        i2c.readfrom_into(AS5600_id, buffer)
        angLow = buffer[0]
        print("Magnitude:", (angHi<<8)|angLow)
        i2c.unlock()
        sleep(0.5)

def ttt():
    #The class AS5600 is pretty low level.
    # This inherits adds some higher level functions

    class AS5600_high(AS5600):

        def __init__(self,i2c,device):
            super().__init__( i2c,device)

        def scan(self):
            "Debug utility function to check your i2c bus"
            while not self.i2c.try_lock():
                pass
            devices = self.i2c.scan()
            self.i2c.unlock()
            print(devices)
            if AS5600_id in devices:
                print('Found AS5600 (id =',hex(AS5600_id),')')
            print(self.CONF)

        def burn_angle(self):
            "Burn ZPOS and MPOS -(can only do this 3 times)"
            #uncomment if you need it
            #self.BURN = 0x80

        def burn_setting(self):
            "Burn config and mang- (can only do this once)"
            #uncomment if you need it
            #self.BURN = 0x40

        def magnet_status(self):
            "Magnet status - this does not seem to make sense ? why"
            s = "Magnet "

            if self.MD == 1:
                s += " detected"
            else:
                s += " not detected"

            if self.ML == 1:
                s+ " (magnet too weak)"

            if self.MH == 1:
                s+ " (magnet too strong)"
            return s


    i2c = busio.I2C(GP1, GP0)
    z = AS5600_high(i2c,AS5600_id)
    z.scan()
    #read write
    #This will probably make your device crazy.  Just poweron/poweroff
    z.CONF = 0x38
    sleep(2)
    print ("should be 0x38", hex(z.CONF))
    sleep(5)
    z.CONF = 0x64
    print ("should be 0x64", hex(z.CONF)    )


    for i in range(10):
        #print(z.magnet_status())
        print ('ZANGLE',z.RAWANGLE)
        print ('ANGLE', z.ANGLE)
        print ('Magnet detected',z.MD)
        sleep(1)
