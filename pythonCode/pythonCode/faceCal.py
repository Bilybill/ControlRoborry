import urllib
import time
import requests
import base64
from PIL import Image
from os.path import getsize

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

def getFace_token(file_path):
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
    face_token = resp.json()['faces'][0]['face_token']
    return face_token
def setUserID(facetoken,number):
    if(type(number) != str):
        number = str(number)
    data_pram = {
        "api_key":(None,Key),
        "api_secret":(None,Secret),
        "face_token":facetoken,
        "user_id":number
    }
    resp = requests.post(http_url["SetUserID"], data=data_pram)#发送请求
    info = resp.json()
    if "error_message" in info.keys():
        print(info['error_message'])
        return False
    return True
def addFace(file_path,ID):
    face_token = getFace_token(file_path)
    if not setUserID(face_token,ID):
        print("failed to set Uer ID")
        return False
    data_pram = {
        "api_key":(None,Key),
        "api_secret":(None,Secret),
        "outer_id":"user_set1",
        "face_tokens":face_token
    }
    resp = requests.post(http_url["AddFaceAPI"], data=data_pram)#发送请求
    info = resp.json()
    if "error_message" in info.keys():
        print("failed to addFace")
        return False
    return True
def seachFace(file_path):
    face_token = getFace_token(file_path)
    data_pram = {
        "api_key":(None,Key),
        "api_secret":(None,Secret),
        "face_token":face_token,
        "outer_id":"user_set1"
    }
    resp = requests.post(http_url["SearchAPI"], data=data_pram)#发送请求
    result = resp.json()
    if "error_message" in result.keys():
        print(result['error_message'])
        return
    result = result['results']['confidence']
    return result