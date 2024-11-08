import subprocess
import time
import serial
import sys
import RPi.GPIO as GPIO
import speech_recognition as sr
import base64
import hashlib
import hmac
import json
import os
import time
import requests
import urllib

def command(command,tim):
    pi=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,_=pi.communicate(timeout=tim)
    out=bytes.decode(out,'utf-8',errors='ignore')
    if pi.stdin:
        pi.stdin.close()
    if pi.stdout:
        pi.stdout.close()
    if pi.stderr:
        pi.stderr.close()
    pi.kill()
    return out.strip()

# s='arecord -D \"plughw:1,0\" -f S16_LE -r 48000 -c 1 -d 10 /home/nubia/Desktop/temp.wav'
# r=command(s,11)
#s='rm -f /home/nubia/Desktop/temp.wav'
#r=command(s,10)
print(sr.__version__)
# 
r=sr.Recognizer()
st=time.time()
with sr.AudioFile('/home/nubia3/Desktop/temp.wav') as source:
#     r.adjust_for_ambient_noise(source,duration=0.5)
#     audio=r.record(source,offset=0,duration=5)
    audio=r.record(source)
    txt=(r.recognize_sphinx(audio,language='zh-CN')) 
#     txt=(r.recognize_google(audio,language='zh-CN',show_all=True))
print(time.time()-st)
print(txt)
print(len(bytes(txt,encoding='utf-8')))


lfasr_host = 'https://raasr.xfyun.cn/v2/api'
# 请求的接口名
api_upload = '/upload'
api_get_result = '/getResult'


class RequestApi(object):
    def __init__(self, appid, secret_key, upload_file_path):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa


    def upload(self):
        print("上传部分：")
        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["sysDicts"] = "advertisement"#"political"#"violentTerrorism"# "uncivilizedLanguage"#
        param_dict["duration"] = "200"
        print("upload参数：", param_dict)
        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url =lfasr_host + api_upload+"?"+urllib.parse.urlencode(param_dict),
                                headers = {"Content-type":"application/json"},data=data)
        print("upload_url:",response.request.url)
        result = json.loads(response.text)
        print("upload resp:", result)
        return result


    def get_result(self):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"
        print("")
        print("查询部分：")
        print("get result参数：", param_dict)
        status = 3
        # 建议使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            response = requests.post(url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                     headers={"Content-type": "application/json"})
            # print("get_result_url:",response.request.url)
            print("查询中······")
            result = json.loads(response.text)
            status = result['content']['orderInfo']['status']
            time.sleep(5)
        x = ("get_result resp:", result['content']['orderResult'])
        for i in eval(x[1])['lattice']:
            a = (eval(i['json_1best'])['st']['rt'])
            for j in a[0]['ws']:
                print(j['cw'][0]['w'])
        return result




# api = RequestApi(appid="b20d4e72",
#                  secret_key="8a90a17e219b52e4750037c3444a3146",
#                  upload_file_path="./temp.wav")
# 
# api.get_result()
