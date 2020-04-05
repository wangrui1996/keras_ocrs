# encoding:utf-8

import requests
import base64

'''
表格文字识别(同步接口)
'''

request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/form"
#request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"
# 二进制方式打开图片文件
f = open('/Users/wangrui/work/ocrs_recognition/test_data/image1.jpg', 'rb')
print(f.read())
img = base64.b64encode(f.read())

params = {"image":img}
access_token = '24.16a1102ce05d2839694a95ff034966ce.2592000.1588602650.282335-15078748'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())