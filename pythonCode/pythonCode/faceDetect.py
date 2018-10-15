import urllib
import time
import requests
from urllib3 import encode_multipart_formdata
import base64
from PIL import Image
from os.path import join,getsize

Key = "qxi-QhnjaQWijs4tEzstAJgVmZL1hn8X"
Secret = "8OsYOMa_c_TJhwGonBJ9TujjuzFJlE6w"
filepath = "D:/SummerDesign/source/lsw.jpg"
newfile = "D:/SummerDesign/source/lsw1.jpg"
boundary = '----------%s' % hex(int(time.time() * 1000))
http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
def compressImage(file_path):
    img = Image.open(file_path)
    w,h = img.size
    img.resize((int(0.9*w),int(0.9*h))).save(file_path)
# compressImage(filepath)
# f = open(filepath,'rb')
# content = base64.b64encode(f.read())
# f.close()

# data_pram = {
#     "api_key":(None,Key),
#     "api_secret":(None,Secret),
#     "image_base64":content,
#     "return landmark":(None,1),
# }

# resp = requests.post(http_url, data=data_pram)#发送请求

# face_token = resp.json()['faces'][0]['face_token']
# print(face_token)
print(getsize(filepath))