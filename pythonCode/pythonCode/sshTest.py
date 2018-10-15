from PIL import Image ,ImageDraw
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
    face_token = resp.json()['faces'][0]
    return face_token
face_info = getImgInfo(file_path)
print(type(face_info))
print([key for key in face_info.keys()])
corr = face_info["landmark"]
corr = [values for values in corr.values()]
moreInfo = [list(reversed(list(x.values()))) for x in corr]
info = moreInfo[0]
for i in range(1,len(moreInfo)):
    info.append(moreInfo[i][0])
    info.append(moreInfo[i][1])
print(info)
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
fontsize = 10
font=ImageFont.truetype（"arial.ttf",fontsize)
draw.text((0,0),"age:"+str(age)+" gender:"+gender['value']+" emotion" + str(emotion) + " beauty" + str(beauty),font=font)