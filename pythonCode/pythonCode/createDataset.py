import urllib
import time
import requests
from urllib3 import encode_multipart_formdata
import base64
from PIL import Image

def compressImage(file_path):
    img = Image.open(file_path)
    w,h = img.size
    img.resize((w/2,h/2)).save(file_path,'jpg')

Key = "qxi-QhnjaQWijs4tEzstAJgVmZL1hn8X"
Secret = "8OsYOMa_c_TJhwGonBJ9TujjuzFJlE6w"
http_url = "https://api-cn.faceplusplus.com/facepp/v3/faceset/create"
data_pram = {
    "api_key":Key,
    "api_secret":Secret,
    "outer_id":"user_set1",
    "face_tokens":"1b35b9dbf1c412dec7cfc8d1cf01f698"
}

resp = requests.post(http_url, data=data_pram)#发送请求
print(resp.json())
