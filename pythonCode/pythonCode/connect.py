import itchat
import serial
from itchat.content import *
from time import sleep
import socket
import time
import sys
import os
import struct
from Client import socket_service
from dealWithImg import getImgInfo
import pymysql
import datetime
import faceCal
import matplotlib.pyplot as plt

s = serial.Serial(
    port = 'COM13',
    baudrate = 9600,
    bytesize = 8,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout=2
)

help_begin = "您好，欢迎使用微信家居智能小助手，请在使用前确保您的小车已经联网并且已经开启蓝牙，并且您已经得到管理员的许可，使用说明如下:"
help_1 = "1. 发送1(或“温湿度”)，即可查询居室当前温度与湿度，默认将当前数据加入数据库，如想取消，请发送cancel"
help_2 = '2. 发送2(或“测量体温”)，即可探测您当前的体温，注意确保将手至于温度探测器上方2cm处，待手势稳定后，再发送2探测，默认将当前数据加入数据库'
help_3 = '3. 发送3(或“拍照”),即可让小车拍摄当前环境照片并返回，小车可自动检测出当前环境的人脸并返回相应的信息，并与数据库中的人脸进行比对，如果找不到该人，则会向您示警'
help_4 = '4. 发送4(或“加入数据库”),即可让小车拍摄当前环境中的人脸并加入数据库，请确保该人在摄像头的范围内'
help_5 = '5. 发送5，可开启让小车自主迅游的模式(发送6，关闭该模式)'
help_6 = '发送A+微信备注名可添加用户到用户数据库中（仅数据库中用户有此权限）'
temInfo = '请将手放在温度探测器上方2cm处，待手势稳定后，再发送2开始测量'
sql = pymysql.connect(host = "localhost",user = "root",passwd = "1998527",db = "homeinfo",charset = "utf8")
cursor = sql.cursor()
def getResponse(content):
    info = ''
    if content == 1:
        info = '1'
    elif content == 2:
        info = '2'
    else :info = str(content)
    s.write(info.encode('utf-8'))
    sleep(0.01)
    n = s.read(1000)
    data_pre = n.decode('utf-8')
    data_pre = data_pre[:-1]
    return data_pre
tem_count = 1
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    if msg['ToUserName']!='filehelper':
        UserName = msg['User']['RemarkName']
        print(UserName)
        cmd = 'select * from userlist where name = "%s"'%(UserName)
        cursor.execute(cmd)
        rs = cursor.fetchall()
        if len(rs) == 0:
            return
    global tem_count
    if msg.text[0] == 'A':
        SenderName = msg.text[1:]
        SenderName = '"%s"'%SenderName
        cmd = 'insert into userlist(name)VALUES(%s);'%(SenderName)
        try:
            cursor.execute(cmd)
            sql.commit()
        except:
            sql.rollback()
        msg.user.send('添加成功')
    if msg.text == 'help':
        msg.user.send(help_1)
        msg.user.send(help_2)
        msg.user.send(help_3)
        msg.user.send(help_4)
        msg.user.send(help_5)
        msg.user.send(help_6)
    if msg.text == "温湿度" or msg.text == '1':
        data_pre = getResponse(1)
        print(data_pre)
        if data_pre == '':
            msg.user.send('系统正在初始化，请稍后再次发送...')
            return
        Tem = data_pre[0:5]
        print(Tem)
        Hum = data_pre[5:]
        Tem = float(Tem)
        Hum = float(Hum)
        NowTime = time.strftime("%H:%M:%S")
        NowTime = str(NowTime)
        NowTime = '"%s"'%(NowTime)
        cmd = 'insert into temhuminfo(Tem,Hum,Time)VALUES(%f,%f,%s);'%(Tem,Hum,NowTime)
        try:
            print(cmd)
            cursor.execute(cmd)
            sql.commit()
        except:
            sql.rollback()
        msg.user.send("您当前居室的湿温度为:%f%%,%f%%"%(Tem,Hum))
        msg.user.send("如想查询最近居室的温湿度变化情况，请发送drawTemHum")
    elif (msg.text == "测量体温" or msg.text == '2') and tem_count == 1:
        msg.user.send(temInfo)
        tem_count += 1
    elif msg.text == '2' and tem_count == 2:
        tem_count = 1
        data_pre = getResponse(2)
        if data_pre == '':
            msg.user.send('系统正在初始化，请稍后再次发送...')
            return
        print(data_pre)
        Tem = float(data_pre)
        NowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        NowTime = str(NowTime)
        NowTime = '"%s"'%(NowTime)
        cmd = 'insert into bodyteminfo(Tem,Time)VALUES(%f,%s);'%(Tem,NowTime)
        try:
            cursor.execute(cmd)
            sql.commit()
        except:
            sql.rollback()
        msg.user.send("您当前的体温为:%f℃"%(Tem))
        msg.user.send("如想查询最近体温变化情况，请发送drawTem")
    elif msg.text == '3':
        path = socket_service()
        threholds = getImgInfo(path)
        msg.user.send("@img@%s"%path)
        if threholds<50 and threholds!=0 :
            msg.user.send("注意，该人在数据库中所有人脸的匹配度小于50，属于陌生人")
        if threholds>50:
            msg.user.send("在数据库中匹配到的相似人脸的相似度为%f"%threholds)
        else:
            msg.user.send("未检测到属于数据库中的人脸")   
    elif msg.text == '4':
        ID = time.strftime("%H_%M_%S")
        path = socket_service()
        faceCal.addFace(path,ID)
        msg.user.send("该人脸加入数据库成功")
        msg.user.send("@img@%s"%path)
    elif msg.text == '5':
        getResponse('S')
    elif msg.text == '6':
        getResponse('s')
    elif msg.text == 'drawTem':
        Teminfo = []
        cmd = 'select * from bodyteminfo;'
        re = cursor.execute(cmd)
        re = cursor.fetchall()
        i = 0
        for row in re:
            Teminfo.append(row[1])
            i+=1
            if i>1000:
                break
        plt.xlabel('time')
        plt.title('BodyTempreture')
        plt.plot(Teminfo)
        save_path = 'D:/SummerDesign/temGra/Body.jpg'
        plt.savefig(save_path)# 保存图片
        msg.user.send("@img@%s"%save_path)
    elif msg.text == 'drawTemHum':
        Teminfo = []
        Huminfo = []
        cmd = 'select * from temhuminfo;'
        re = cursor.execute(cmd)
        re = cursor.fetchall()
        i = 0
        for row in re:
            Teminfo.append(row[1])
            Huminfo.append(row[2])
            i+=1
            if i>1000:
                break
        plt.xlabel('time')
        plt.title('Tempreture')
        plt.plot(Teminfo)
        save_path = 'D:/SummerDesign/temGra/Tem.jpg'
        plt.savefig(save_path)# 保存图片
        msg.user.send("@img@%s"%save_path)
        plt.xlabel('time')
        plt.title('Humidity and Tempreture')
        plt.plot(Huminfo)
        save_path = 'D:/SummerDesign/temGra/Hum.jpg'
        plt.savefig(save_path)# 保存图片
        msg.user.send("@img@%s"%save_path)
        
if __name__ == "__main__":
    itchat.auto_login(enableCmdQR=True)
    itchat.run(True)