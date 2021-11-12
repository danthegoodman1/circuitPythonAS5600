from time import sleep
import busio
from board import *
from as5600 import AS5600

addr = 0x36

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
    i2c = busio.I2C(GP1, GP0)
    while not i2c.try_lock():
        pass
    d = i2c.scan()
    print(d)
    for i in d:
        if i == addr:
            print("yeah", i)
    i2c.unlock()
