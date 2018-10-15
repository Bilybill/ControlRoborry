from PIL import Image ,ImageDraw,ImageFont
# import ImageFont
import urllib
import time
import requests
import base64
from PIL import Image
from os.path import getsize
import os

file_path = "D:/SummerDesign/source/lsw.jpg"
Key = "qxi-QhnjaQWijs4tEzstAJgVmZL1hn8X"
Secret = "8OsYOMa_c_TJhwGonBJ9TujjuzFJlE6w"
http_url = {
    "DetectAPI":"https://api-cn.faceplusplus.com/facepp/v3/detect",
    "SetUserID":"https://api-cn.faceplusplus.com/facepp/v3/face/setuserid",
    "SearchAPI":"https://api-cn.faceplusplus.com/facepp/v3/search",
    "AddFaceAPI":"https://api-cn.faceplusplus.com/facepp/v3/faceset/addface"
}

def compressImage(file_path):
    img = Image.open(file_path)
    w,h = img.size
    img.resize((int(0.9*w),int(0.9*h))).save(file_path)

def getImgInfo(file_path):
    if(getsize(file_path) > 2097152):
        compressImage(file_path)
    f = open(file_path,'rb')
    content = base64.b64encode(f.read())
    f.close()
    data_pram = {
        "api_key":(None,Key),
        "api_secret":(None,Secret),
        "image_base64":content,
        "return_landmark":(None,1),
        "return_attributes":"gender,age,beauty,emotion,skinstatus"
    }
    resp = requests.post(http_url["DetectAPI"], data=data_pram)#发送请求
    face_info = resp.json()['faces']
    if len(face_info) == 0:
        msg = "No face detected"
        return 0
    face_info = face_info[0]
    face_token = face_info['face_token']
    corr = face_info["landmark"]
    corr = [values for values in corr.values()]
    moreInfo = [list(reversed(list(x.values()))) for x in corr]
    info = moreInfo[0]
    for i in range(1,len(moreInfo)):
        info.append(moreInfo[i][0])
        info.append(moreInfo[i][1])
    rectangle = face_info["face_rectangle"]
    attributes = face_info["attributes"]
    beauty = attributes["beauty"]
    gender = attributes["gender"]
    emotion = attributes["emotion"]
    skinstatus = attributes["skinstatus"]
    age = attributes["age"] 
    top = rectangle['top']
    left = rectangle['left']
    width = rectangle['width']
    height = rectangle['height']
    image = Image.open(file_path)
    draw = ImageDraw.Draw(image)
    draw.rectangle((left,top,left+width,top+height),outline=(0,255,0))
    draw.point(info,fill=(255,255,0))
    font1 = ImageFont.truetype("C:\Windows\Fonts\simsunb.ttf",36)
    font2 = ImageFont.truetype("C:\Windows\Fonts\simsunb.ttf",20)
    draw.text((0,0),"age:"+str(age['value'])+" gender:"+gender['value'],font=font1)
    draw.text((0,50),"beauty: " + str(beauty) + "skinstatus:" + str(skinstatus),font=font2)
    draw.text((0,100),"skinstatus:" + str(skinstatus),font=font2)
    image.save(file_path)
    data_pram = {
        "api_key":(None,Key),
        "api_secret":(None,Secret),
        "face_token":face_token,
        "outer_id":"user_set1"
    }
    resp = requests.post(http_url["SearchAPI"], data=data_pram)#发送请求
    result = resp.json()['results'][0]
    if "error_message" in result.keys():
        print(result['error_message'])
        return
    result = result['confidence']
    return result