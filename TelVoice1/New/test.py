import time
import serial
import sys,subprocess
import RPi.GPIO as GPIO
import json
import datetime
import traceback
import speech_recognition as sr
import base64
import hashlib
import hmac
import json
import os
import time
import requests
import urllib


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
#         print("上传部分：")
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
#         print("upload参数：", param_dict)
        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url =lfasr_host + api_upload+"?"+urllib.parse.urlencode(param_dict),
                                headers = {"Content-type":"application/json"},data=data)
#         print("upload_url:",response.request.url)
        result = json.loads(response.text)
#         print("upload resp:", result)
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
#         print("")
#         print("查询部分：")
#         print("get result参数：", param_dict)
        status = 3
        # 建议使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            response = requests.post(url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                     headers={"Content-type": "application/json"})
            # print("get_result_url:",response.request.url)
#             print("查询中······")
            result = json.loads(response.text)
            status = result['content']['orderInfo']['status']
            time.sleep(5)
        x = ("get_result resp:", result['content']['orderResult'])
        res=''
        for i in eval(x[1])['lattice']:
            a = (eval(i['json_1best'])['st']['rt'])
            for j in a[0]['ws']:
                res=res+(j['cw'][0]['w'])
        return res



class pi_fun():
    
    def __init__(self,args):
        self.args=self.get_arg(args)
    
    def get_arg(self,a):
        tmp={'type':0,'time':0,'data':[0,0]}
        try:
            for i in a.split('#'):
                t=i.split(':')
                tmp[t[0]]=eval(t[1])
            return tmp
        except Exception:
            return tmp
                
    
    def test(self):
        #self.noise(10)
        if self.args['type']==2:
            sims=self.get_phone_num()
            print (sims)
        elif self.args['type']==1:
            self.noise(self.args['time'],self.args['data'])
        elif self.args['type']==3:
            self.change_date()
        elif self.args['type']==4:
            print(self.args)
        elif self.args['type']==5:
            self.word()
        elif self.args['type']==6:
            self.get_word()
            
    def noise(self,tim,data):
        st=time.time()
        port="/dev/ttyAMA0"
        usart=serial.Serial(port,9600,timeout=None)
        usart.flushInput()
        sendbuf = bytearray.fromhex("01 03 00 00 00 01 84 0A")
        #f=open('/home/nubia/Desktop/123/123.txt','w')
        sc=0
        while True:
            if time.time()-st>tim:
                break
            if data!=[0,0] and int(time.time()-st)%5==0 and int((time.time()-st)/5)!=sc:
                self.command_no('adb shell input tap %d %d'%(data[0],data[1]))
                sc=int((time.time()-st)/5)
            usart.write(sendbuf)
            size=usart.inWaiting()
            if size!=0:
                res=usart.read(7)
                a1=str(hex(res[3]))
                a2=str(hex(res[4]))
                aa=(eval('0x'+a1[2:]+a2[2:]))
                nt=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(nt,aa)
                #f.write('%s %d \r\n'%(nt,aa))
            time.sleep(0.5)
        #f.close()
            
    def word(self):
        s='arecord -D \"plughw:1,0\" -f S32_LE -r 48000 -c 1 -d 10 /home/nubia3/Desktop/temp.wav'
        self.command(s,20)
        
    
    def get_word(self):
#         txt=''
#         st=time.time()
#         r=sr.Recognizer()
#         with sr.AudioFile('/home/nubia3/Desktop/temp.wav') as source:
#             r.adjust_for_ambient_noise(source,duration=0.5)
#             audio=r.record(source)
#             try:
#                 txt=(r.recognize_google(audio,language='zh-CN'))
#             except:
#                 print('err')
#         print(time.time()-st)
#         print(txt)
#         print(len(bytes(txt,encoding='utf-8')))
        
        #s='rm -f /home/nubia/Desktop/temp.wav'
        #r=command(s,10)
        
        
        api = RequestApi(appid="b20d4e72",
                         secret_key="8a90a17e219b52e4750037c3444a3146",
                         upload_file_path="/home/nubia3/Desktop/temp.wav")

        print(api.get_result())
        
    def adb_pre(self):
        f=open('/home/nubia3/Desktop/123/70-android.rules','w')
        f.write('SUBSYSTEM=="usb",ATTRS{idVendor}=="19d2",ATTRS{idProduct}=="ffb0",MODE="0666",GROUP="plugdev"')
        f.close()
    
    def command(self,command,tim):
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
    
    def command_no(self,command):
        pi=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
    
    def get_phone_num(self):
        try:
            sim1=''
            sim2=''
            self.command('adb pull /sdcard/android/data/cn.nubia.silence.detector/files/info/device.json ./device.json',10)
            f=open('./device.json','r')
            jd=json.load(f)
            no=jd['phoneNumbers']
            if len(no)==1:
                n1=no[0]['number']
                if n1.startswith('+86'):
                    sim1=n1[3:]
                else:
                    sim1=n1
                sim=sim1
            elif len(no)==2:
                n1=no[0]['number']
                n2=no[1]['number']
                if n1.startswith('+86'):
                    sim1=n1[3:]
                else:
                    sim1=n1
                if n2.startswith('+86'):
                    sim2=n2[3:]
                else:
                    sim2=n2
                sim='%s/%s'%(sim1,sim2)
            return sim
        except Exception:
            return ('error/error')
        
    def change_date(self):
        try:
            d=self.command('adb shell date +%m/%d/%Y',10)
            t=self.command('adb shell date +%H:%M:%S',10)
            action='sudo date -s "%s %s"'%(d,t)
            self.command(action,10)
        except:
            pass
        
if __name__=='__main__':
    f=pi_fun(sys.argv[1])
    f.test()
