import time
import serial
import sys,subprocess
import RPi.GPIO as GPIO
import json
import datetime

class pi_fun():
    
    def __init__(self,args):
        self.args=self.get_arg(args)
    
    def get_arg(self,a):
        tmp={'type':0,'time':0}
        try:
            for i in a.split(','):
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
            self.noise(self.args['time'])
        elif self.args['type']==3:
            self.change_date()
        
    def noise(self,tim):
        st=time.time()
        port="/dev/ttyAMA0"
        usart=serial.Serial(port,9600,timeout=None)
        usart.flushInput()
        sendbuf = bytearray.fromhex("01 03 00 00 00 01 84 0A")
        #f=open('/home/nubia/Desktop/123/123.txt','w')
        while True:
            if time.time()-st>tim:
                break
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
        
    def adb_pre(self):
        f=open('/home/nubia/Desktop/123/70-android.rules','w')
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