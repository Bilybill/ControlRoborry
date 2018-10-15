import socket
import threading
import time
import sys
import os
import struct

def socket_service():
    flag = 1
    while flag == 1:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('192.168.43.206', 8888))
            flag = 0
        except socket.error as msg:
            print(msg)
            flag = 1
    print("connected")
    new_filename = ""
    while 1:
        info = time.strftime("%H_%M_%S")
        new_filename ="D:\SummerDesign\source\%s.jpg"%info
        s.send(info.encode())
        fileinfo_size = struct.calcsize('128sl')
        buf = s.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl',buf)
            recvd_size = 0  # 定义已接收文件的大小
            
            fp = open(new_filename, 'wb')
            print('start receiving...')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = s.recv(1024)
                    recvd_size += len(data)
                else:
                    data = s.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print('end receive...')
        s.close()
        break
    return new_filename


if __name__ == '__main__':
    socket_service()