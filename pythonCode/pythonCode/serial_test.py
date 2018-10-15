import serial
from time import sleep
import binascii

while True:
    info = "2"
    s.write(info.encode('utf-8'));
    sleep(0.01)
    n = s.read(1000)
    data_pre = n.decode('utf-8')
    print(data_pre)