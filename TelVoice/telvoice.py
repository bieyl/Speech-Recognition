# -*-encoding:utf-8 -*-
from __future__ import division
import sys
sys.path.append('/home/nubia/.local/lib/python3.9/site-packages/')
import ui
import wx
import time,datetime
import serial
import re
#import RPi.GPIO as GPIO
import csv
import traceback
import subprocess
import json,threading
from pubsub import pub
import xml.etree.ElementTree as ET
import re
#adb shell dumpsys telephony.registry | findstr "mCallState"
#end call 79 ; call 5
#adb shell input keyevent 

class MianWindow(ui.MyFrame1):
    global rmt_ip,local_sim1,local_sim2,remote_sim1,remote_sim2,t_time,t_long,stop_test,is_link,test_case,flag
    rmt_ip='0.0.0.0'
    local_sim1='null'
    local_sim2='null'
    remote_sim1='null'
    remote_sim2='null'
    t_time=10
    t_long=10
    stop_test=False
    is_link=0
    test_case=[]
    flag=False
    
    def init_main_window(self):
        #self.m_staticText1.SetLabelText('Remote_IP:???')
        #t=threading.Thread(target=self.remote_ip,args=())
        #t.isDaemon()
        #t.start()
        #self.m_checkBox1.Enable(False)
        self.m_button2.SetBackgroundColour('#c3c3c3')
        self.m_button21.SetBackgroundColour('#c3c3c3')
        self.m_button211.SetBackgroundColour('#c3c3c3')
        self.m_textCtrl11.Enable(False)
        self.m_textCtrl1.Enable(False)
        self.m_staticText1.SetLabelText('Remote Pi connecting...Wait please!!!')
        
        self.command('adb shell settings put global stay_on_while_plugged_in 0',10)
        self.ssh_command('adb shell settings put global stay_on_while_plugged_in 0',10,'')
        
        wx.CallLater(1000,self.remote_ip)
        
        pub.subscribe(self.show_info,'show')
        pub.subscribe(self.link_test,'link')
    
    def app_check( self, event ):
        if self.m_checkBox1.IsChecked():
            self.m_button21.Enable(False)
            self.m_button211.Enable(False)
            self.m_choice1.SetSelection(1)
            self.m_choice1.Enable(False)
            self.m_slider11.SetValue(1)
            self.m_textCtrl11.SetValue('1')
        else:
            self.m_button21.Enable(True)
            self.m_button211.Enable(True)
            self.m_choice1.Enable(True)
    
    def show_info(self,msg):
        #self.m_textCtrl3.Clear()
        self.m_textCtrl3.AppendText(msg+'\n')
        
    def link_test(self,res):
        global test_case,t_time,t_long
        
        if res and len(test_case)>0:
            print('test_case:',test_case)
            self.m_slider1.SetValue(test_case[0]['times'])
            self.m_slider11.SetValue(test_case[0]['tlong'])
            
            self.m_textCtrl1.SetValue(str(test_case[0]['times']))
            t_time=int(test_case[0]['times'])
            self.m_textCtrl11.SetValue(str(test_case[0]['tlong']))
            t_long=int(test_case[0]['tlong'])
            
            self.m_choice2.SetSelection(test_case[0]['type'])
            self.m_choice1.SetSelection(test_case[0]['location'])
            self.m_choice3.SetSelection(test_case[0]['net'])
            if test_case[0]['telchat']==0:
                t=threading.Thread(target=self.tel_1,args=())
                t.start()
            elif test_case[0]['telchat']==1:
                if self.m_choice2.GetSelection()==1:
                    t1=threading.Thread(target=self.weChatCall,kwargs={"model":1})
                else:
                    t1=threading.Thread(target=self.weChatCall,kwargs={"model":0})
                t1.start()
        elif not res:
            self.m_button211.SetBackgroundColour('#c3c3c3')
            self.m_button21.SetBackgroundColour('#c3c3c3')
            self.m_button2.SetBackgroundColour('#c3c3c3')
            #self.m_button211.SetLabel('Link +')
            
    def remote_ip(self):
        global rmt_ip
        try:
            action='ping -4 nubia.local -c 1'
            out=self.command(action,10)
            if out!='Fail':
                rmt_ip=re.findall(r'\(\d+.\d+.\d+.\d+\)',out)[0][1:-1]
                print('rmt_ip:',rmt_ip)
                dev=self.command('adb shell wm size',10)
                print(dev)
                dev_remote=self.ssh_command('adb shell wm size',10,'')
                print(dev_remote)
                if dev.find('Physical size')!=-1 and dev_remote.find('Physical size')!=-1:
                    self.get_phone_num()
                    self.change_date()
                else:
                   self.m_staticText1.SetLabelText('Check mobile or remote mobile connect !!!')
                    
            else:
                self.m_staticText1.SetLabelText('Remote PI connect error !!!')
        except Exception:
            print(traceback.print_exc())
            rmt_ip=''
            self.m_staticText1.SetLabelText('Remote PI connect error !!!')
    
    def redev( self, event ):
        self.m_staticText1.SetLabelText('connecting...Wait please!!!')
        wx.CallLater(1000,self.remote_ip)
        
    def ssh_command(self,command,timout,kvs):
        global rmt_ip
        #action='sshpass -p "nubia123" ssh nubia@169.254.220.4 -o StrictHostKeyChecking=no python /home/nubia/Desktop/test.py type:2,time:10'
        #self.ssh_command('python /home/nubia/Desktop/test.py',10,'type:2,time:10')
        if kvs:
            action='sshpass -p "nubia123" ssh nubia3@%s -o StrictHostKeyChecking=no %s %s'%(rmt_ip,command,kvs)
        else:
            action='sshpass -p "nubia123" ssh nubia3@%s -o StrictHostKeyChecking=no %s'%(rmt_ip,command)
        res=self.command(action,timout*2)
        return res
    
    def command(self,action,outime):#cmd command use action and outtime
        try:
            print(action,outime)
            pi=subprocess.Popen(action,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out,_=pi.communicate(timeout=outime)
            out=bytes.decode(out,'utf-8',errors='ignore')
            if pi.stdin:
                pi.stdin.close()
            if pi.stdout:
                pi.stdout.close()
            if pi.stderr:
                pi.stderr.close()
            pi.kill()
            return out.strip()
        except Exception:
            print(traceback.print_exc())
            return 'Fail'
    
    def command_no(self,action):#cmd command use action and outtime
        try:
            print(action)
            pi=subprocess.Popen(action,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        except Exception:
            print(traceback.print_exc())
    
    def get_Noise(self,tim):#get noise data and wirte noise.csv
        port='/dev/ttyAMA0'
        usart=serial.Serial(port,9600,timeout=None)
        usart.flushInput()
        print(usart)
        sendbuf=bytearray.fromhex('01 03 00 00 00 01 84 0A')
        print(sendbuf)
        with  open('noise.csv',mode='w',encoding='utf-8-sig',newline='') as f:
            writer=csv.writer(f)
            writer.writerows([['Time','Data']])
            st=time.time()
            while True:
                print('++++')
                if time.time()-st>tim:
                    break
                usart.write(sendbuf)
                size=usart.inWaiting()
                #print(size)
                if size!=0:
                    res=usart.read(7)
                    #print(res)
                    #print(res[3])
                    #print(res[4])
                    a1=str(hex(res[3]))
                    a2=str(hex(res[4]))
                    res=(eval('0x'+a1[2:]+a2[2:]))
                    print(res)
                    self.m_staticText1.SetLabelText(str(res))
                    nt=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerows([[nt,str(res)]])
                time.sleep(0.5)
            #GPIO.cleanup()
                
    def r_csv(self):#read csv
        with open('noise.csv',mode='r',encoding='utf-8-sig',newline='') as f:
            reader=csv.reader(f)
            next(reader)
            for row in reader:
                print(row[0],row[1])
    
    def call(self,sim,call_type,num):# sim 0--sim1  1--sim2;video 0 voicephone 1 videophone; tel phonenumber
        self.command('adb shell am startservice --ei sim %d --ei video %d --es tel %s -n cn.nubia.silence.detector/.CallService'%(sim,call_type,num),10)
        
    def get_phone_num(self):
        global rmt_ip,local_sim1,local_sim2,remote_sim1,remote_sim2
        #adb pull /sdcard/android/data/cn.nubia.silence.detector/files/info/device.json /home/nubia/Desktop/device.json
        try:
            ret=self.command('adb pull /sdcard/android/data/cn.nubia.silence.detector/files/info/device.json ./device.json',10)
            f=open('./device.json','r')
            jd=json.load(f)
            no=jd['phoneNumbers']
            if len(no)==1:
                n1=no[0]['number']
                if n1.startswith('+86'):
                    local_sim1=n1[3:]
                else:
                    local_sim1=n1
            elif len(no)==2:
                n1=no[0]['number']
                n2=no[1]['number']
                if n1.startswith('+86'):
                    local_sim1=n1[3:]
                else:
                    local_sim1=n1
                if n2.startswith('+86'):
                    local_sim2=n2[3:]
                else:
                    local_sim2=n2
    
        except Exception:
            pass
        
        try:
            ret=self.ssh_command('python /home/nubia3/Desktop/test.py',10,'type:2#time:10#data:[0,0]')
            print('remote phone:',ret)
            if ret:
                ts=ret.split('/')
                if len(ts)==1:
                    remote_sim1=ret.strip()
                elif len(ts)==2:
                    remote_sim1=ts[0]
                    remote_sim2=ts[1]
        except Exception:
            pass
            
        self.m_staticText1.SetLabelText('Remote_IP:(%s)  SIM1:%s  SIM2:%s / SIM1(R):%s  SIM2(R):%s '%(rmt_ip,local_sim1,local_sim2,remote_sim1,remote_sim2))
    
    def get_remote_ring_status(self):#0:idle 1:ringing 2:speaking 
        #self.ssh_command('adb shell dumpsys telephony.registry | grep "mCallState"',10,'')
        
        try:
            status=-1
            ret=self.ssh_command('adb shell dumpsys telephony.registry | grep "mCallState"',10,'')
            
            s1=ret.split('\n')[0].split('=')[-1]
            s2=ret.split('\n')[1].split('=')[-1]
            if s1=='0' and s2=='0':
                status=0
            elif s1=='1' or s2=='1':
                status=1
            elif s1=='2' and s2=='2':
                status=2
            return status
        except Exception:
            return -1
    
    def get_ring_status(self):#0:idle 1:ringing 2:speaking 
        #self.ssh_command('adb shell dumpsys telephony.registry | grep "mCallState"',10,'')
        
        try:
            status=-1
            ret=self.command('adb shell dumpsys telephony.registry | grep "mCallState"',10)
            
            s1=ret.split('\n')[0].split('=')[-1]
            s2=ret.split('\n')[1].split('=')[-1]
            if s1=='0' and s2=='0':
                status=0
            elif s1=='1' or s2=='1':
                status=1
            elif s1=='2' and s2=='2':
                status=2
            return status
        except Exception:
            return -1
        
    def get_remote_noise(self,tim,data):
        ret=self.ssh_command('python /home/nubia3/Desktop/test.py',tim,'type:1#time:%d#data:[%d,%d]'%(tim,data[0],data[1]))
        f=open('./noise.csv','a')
        f.write(ret+'\n')
        f.write('='*10+'\n')
        f.close()
        return ret
    
    def get_remote_word(self):
        ret=self.ssh_command('python /home/nubia3/Desktop/test.py',60,'type:5#time:60#data:[0,0]')
        return ret
    
    def get_remote_getword(self):
        ret=self.ssh_command('python /home/nubia3/Desktop/test.py',60,'type:6#time:60#data:[0,0]')
        return ret
    
    def change_date(self):
        try:
            d=self.command('adb shell date +%m/%d/%Y',10)
            t=self.command('adb shell date +%H:%M:%S',10)
            action='sudo date -s "%s %s"'%(d,t)
            
            r=self.command(action,3)
            r=self.ssh_command('python /home/nubia3/Desktop/test.py',10,'type:3#time:10#data:[0,0]')
            
        except Exception:
            print(traceback.print_exc())
    
    def is_noise(self,nis,nis2):
        err_list=[]
        
        n1=nis.split('\n')
        n2=nis2.split('\n')
        
        bn=self.time_Noise(n1)
        print('base:',bn)
        
        for i in range(0,len(n2),5):
            if i+5<len(n2):
                n=self.time_Noise(n2[i:i+5])
                print(n)
            else:
                n=self.time_Noise(n2[i:])
                print(n)
            if n and n['nis']<=(bn['nis']):
                err_list.append(n)
        return err_list
    
    def change_5G(self,sim,is_on):# sim 0--sim1  1--sim2;video 0 voicephone 1 videophone; tel phonenumber
        self.command('adb shell settings put global 5g_switch_status_new_%d %d'%(sim,is_on),10)
        self.ssh_command('adb shell settings put global 5g_switch_status_new_%d %d'%(sim,is_on),10,'')
    
    def tel_1(self):
        global rmt_ip,local_sim1,local_sim2,remote_sim1,remote_sim2,t_time,t_long,stop_test,is_link,test_case
        try:
            wx.CallLater(500,pub.sendMessage,'show',msg='Start Telephone Call')
        except:
            pass
        
        if self.m_choice3.GetSelection()==0:
            ret=self.change_5G(0,1)
        else:
            ret=self.change_5G(0,0)
        
        stop_test=False
        err_list=[]
        mt=[0,0]
        test_time=t_long*60
        if test_time==0:
            test_time=10
        if t_time==0:
            t_time=1
        self.nubia_log_start()
        self.nubia_log_start_remote()
        nis_base=self.get_remote_noise(10,mt)
        for i in range(t_time):
            try:
                wx.CallLater(500,pub.sendMessage,'show',msg='Call:%d'%(i+1))
                #pub.sendMessage('show',msg=err_txt)
            except:
                pass
            
            if self.m_choice2.GetSelection()==1:
                ret=self.call(0,1,remote_sim1)
            else:
                ret=self.call(0,0,remote_sim1)
            print(ret)
            while 1:
                ret=self.get_remote_ring_status()
                print(ret)
                if ret==1 or stop_test:
                    break
            if stop_test:
                break
            
            self.ssh_command('adb shell input keyevent 5',10,'')
            if self.m_choice1.GetSelection()==1:
                mt=self.find_by_text('免提',True)
                self.ssh_command('adb shell input tap %d %d'%(mt[0],mt[1]),10,'')
                mt=[0,0]
            elif self.m_choice1.GetSelection()==2:
                mt=self.find_by_text('免提',True)
                
            self.command_no('python ./playsound.py %d'%(test_time))
            nis=self.get_remote_noise(test_time,mt)
            el=self.is_noise(nis_base,nis)
            err_list=err_list+el
            print('err_list:',el)
            self.ssh_command('adb shell input keyevent 79',10,'')
            while 1:
                ret=self.get_ring_status()
                print('local:',ret)
                if ret==0 or stop_test:
                    break
            if stop_test:
                break
        if err_list:
            err_txt='test no sound:'
            for k,i in enumerate(err_list):
                err_txt=err_txt+'\n'+'%d--%s: %s(DB)'%(k+1,i['tim'],i['nis'])
            print(err_txt)
        else:
            err_txt='test no sound:\n None'
        
        self.nubia_log_end()
        self.nubia_log_end_remote()
        stop_test=False
        
        try:
            wx.CallLater(500,pub.sendMessage,'show',msg=err_txt)
            #pub.sendMessage('show',msg=err_txt)
        except:
            pass
        
        if (len(test_case))>1:
            test_case.pop(0)
            pub.sendMessage('link',res=True)
        elif (len(test_case)-1)==0:
            is_link=0
            test_case.pop(0)
            pub.sendMessage('link',res=False)
        else:
            pub.sendMessage('link',res=False)
    
    def tel_2(self):
        global rmt_ip,local_sim1,local_sim2,remote_sim1,remote_sim2,t_time,t_long,stop_test,is_link,test_case
        
        dy='com.ss.android.ugc.aweme/.main.MainActivity'
        ks='com.smile.gifmaker/com.yxcorp.gifshow.activity.UriRouterActivity'
        err_list=[]
        try:
            wx.CallLater(500,pub.sendMessage,'show',msg='Start Telephone Call 3rdAPP')
        except:
            pass
        
        if self.m_choice3.GetSelection()==0:
            ret=self.change_5G(0,1)
        else:
            ret=self.change_5G(0,0)
        
        stop_test=False
        err_list=[]
        mt=[0,0]
        test_time=t_long*60
        if test_time==0:
            test_time=10
        if t_time==0:
            t_time=1
        self.nubia_log_start()
        self.nubia_log_start_remote()
        for i in range(t_time):
            if(i%2==0):
                self.ssh_command('adb shell am start -n %s'%dy,10,'')
            else:
                self.ssh_command('adb shell am start -n %s'%ks,10,'')
            
            try:
                wx.CallLater(500,pub.sendMessage,'show',msg='Call:%d'%(i+1))
                #pub.sendMessage('show',msg=err_txt)
            except:
                pass
            
            if self.m_choice2.GetSelection()==1:
                ret=self.call(0,1,remote_sim1)
            else:
                ret=self.call(0,0,remote_sim1)
            print(ret)
            while 1:
                ret=self.get_remote_ring_status()
                print(ret)
                if ret==1 or stop_test:
                    break
            if stop_test:
                break
            
            self.ssh_command('adb shell input keyevent 5',10,'')
            mt=self.find_by_text('免提',True)
            self.ssh_command('adb shell input tap %d %d'%(mt[0],mt[1]),10,'')
                
            self.command_no('python ./playsound_eng.py %d'%(10))
            self.get_remote_word()
            print('getword')
            self.ssh_command('adb shell input keyevent 79',10,'')
            while 1:
                ret=self.get_ring_status()
                print('local:',ret)
                if ret==0 or stop_test:
                    break
            
            if stop_test:
                break
            
#             r1=re.compile('\d')
#             for i in r1.findall(nis):
#                 print(i)
            nis=self.get_remote_getword()
            tim=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            err_list.append(tim+'  ('+nis+')')
        self.nubia_log_end()
        self.nubia_log_end_remote()
        stop_test=False
        
        err_txt='Result:\r\n'
        for err in err_list:
            err_txt=err_txt+err+'\r\n'
        print('err_list:',err_txt)
        try:
            wx.CallLater(500,pub.sendMessage,'show',msg=err_txt)
            #pub.sendMessage('show',msg=err_txt)
        except:
            pass
        self.ssh_command('adb shell am force-stop %s'%(dy.split('/')[0]),10,'')
        self.ssh_command('adb shell am force-stop %s'%(ks.split('/')[0]),10,'')
        pub.sendMessage('link',res=False)
    
    def weChatCall( self, model ):   # 0:voice    1:video
        global t_time,t_long,stop_test,is_link,test_case
        try:
            wx.CallLater(500,pub.sendMessage,'show',msg='Start weChat Call')
        except:
            pass
        
        if self.m_choice3.GetSelection()==0:
            ret=self.change_5G(0,1)
        else:
            ret=self.change_5G(0,0)
        
        stop_test=False
        err_list=[]
        mt=[0,0]
        test_time=t_long*60
        if test_time==0:
            test_time=10
        if t_time==0:
            t_time=1
        self.nubia_log_start()
        self.nubia_log_start_remote()
        nis_base=self.get_remote_noise(10,mt)
        
        
        
        for i in range(t_time):
            self.command('adb shell am start -n com.tencent.mm/.ui.LauncherUI',10)
            self.ssh_command('adb shell am start -n com.tencent.mm/.ui.LauncherUI',10,'')
            a,b = self.find_by_text('通讯录',False)
            self.command('adb shell input tap %s %s'%(a,b),10)
            a,b = self.find_by_text('星标朋友',False)
            self.command('adb shell input tap %s %s'%(a,b),10)
            try:
                wx.CallLater(500,pub.sendMessage,'show',msg='Call:%d'%(i+1))
                #pub.sendMessage('show',msg=err_txt)
            except:
                pass
            
            a,b = self.find_by_text('音视频通话',False)
            self.command('adb shell input tap %s %s'%(a,b),10)
    
            if model == 1:
                a,b = self.find_by_text('视频通话',False)
                self.command('adb shell input tap %s %s'%(a,b),10)
                #a,b = self.find_by_image(-1,True)
                a,b =self.find_by_contentdesc('接听',True)
                self.ssh_command('adb shell input tap %d %d'%(a,b),10,'')
                
            else:
                a,b = self.find_by_text('语音通话',False)
                self.command('adb shell input tap %s %s'%(a,b),10)
                #a,b = self.find_by_image(-1,True)
                a,b =self.find_by_contentdesc('接听',True)
                self.ssh_command('adb shell input tap %d %d'%(a,b),10,'')
                if self.m_choice1.GetSelection()==1:
                    mt=self.find_by_contentdesc('扬声器已关',True)
                    self.ssh_command('adb shell input tap %d %d'%(mt[0],mt[1]),10,'')
                    mt=[0,0]
                    
            self.command_no('python ./playsound.py %d'%(test_time))
            
            nis=self.get_remote_noise(test_time,mt)
            el=self.is_noise(nis_base,nis)
            err_list=err_list+el
            print('err_list:',el)
            
            self.command('adb shell am force-stop com.tencent.mm',10)
            self.ssh_command('adb shell am force-stop com.tencent.mm',10,'')
            
            if stop_test:
                break
            
        if err_list:
            err_txt='test no sound:'
            for k,i in enumerate(err_list):
                err_txt=err_txt+'\n'+'%d--%s: %s(DB)'%(k+1,i['tim'],i['nis'])
            print(err_txt)
        else:
            err_txt='test no sound:\n None'
        
        self.nubia_log_end()
        self.nubia_log_end_remote()
        stop_test=False
        
        try:
            wx.CallLater(500,pub.sendMessage,'show',msg=err_txt)
            #pub.sendMessage('show',msg=err_txt)
        except:
            pass
        
        
        if (len(test_case))>1:
            test_case.pop(0)
            pub.sendMessage('link',res=True)
        elif (len(test_case)-1)==0:
            is_link=0
            test_case.pop(0)
            pub.sendMessage('link',res=False)
        else:
             pub.sendMessage('link',res=False)
    
    def bClick( self, event ):
        global is_link,test_case
        
        if self.m_checkBox1.IsChecked():
            self.m_button2.SetBackgroundColour('#f16f74')
            t=threading.Thread(target=self.tel_2,args=())
            #t.isDaemon()
            t.start()
        else:
            if is_link==0:
                self.m_button2.SetBackgroundColour('#f16f74')
                t=threading.Thread(target=self.tel_1,args=())
                #t.isDaemon()
                t.start()
            else:
                arg={'telchat':0,'times':self.m_slider1.GetValue(),'tlong':self.m_slider11.GetValue(),'type':self.m_choice2.GetSelection(),'location':self.m_choice1.GetSelection(),'net':self.m_choice3.GetSelection(),}
                test_case.append(arg)
                self.m_button211.SetLabel('Link +%d'%(is_link))
                is_link+=1
        
    def bClick2( self, event ):
        global rmt_ip,local_sim1,local_sim2,remote_sim1,remote_sim2,is_link,test_case
        
        if is_link==0:
            self.m_button21.SetBackgroundColour('#f16f74')
            if self.m_choice2.GetSelection()==1:
                t1=threading.Thread(target=self.weChatCall,kwargs={"model":1})
            else:
                t1=threading.Thread(target=self.weChatCall,kwargs={"model":0})
            t1.start()
        else:
            arg={'telchat':1,'times':self.m_slider1.GetValue(),'tlong':self.m_slider11.GetValue(),'type':self.m_choice2.GetSelection(),'location':self.m_choice1.GetSelection(),'net':self.m_choice3.GetSelection(),}
            test_case.append(arg)
            self.m_button211.SetLabel('Link +%d'%(is_link))
            is_link+=1
        
        
    def bClick3( self, event ):
        global is_link,test_case,t_time,t_long
        arg={'times':0,'tlong':0,'type':0,'location':0,'net':0,}
        
        if is_link==0:
            self.m_button211.SetLabel('Link +')
            self.m_button211.SetBackgroundColour('#b8cc0c')
            is_link+=1
        else:
            #self.m_button211.SetBackgroundColour('#aaf7af')
            self.m_button211.SetBackgroundColour('#f16f74')
            
            pub.sendMessage('link',res=True)
    
    
    def nubia_log_start(self,):
        self.command_no('adb shell am startservice --es command start --ei type 3 -n cn.nubia.silence.detector/cn.nubia.auto.nubialog.WoodpeckerService')
    
    def nubia_log_end(self,):
        self.command_no('adb shell am startservice --es command stop --ei type 3 -n cn.nubia.silence.detector/cn.nubia.auto.nubialog.WoodpeckerService')
        
    
    def nubia_log_start_remote(self,):
        action='adb shell am startservice --es command start --ei type 3 -n cn.nubia.silence.detector/cn.nubia.auto.nubialog.WoodpeckerService'
        self.ssh_command(action,10,'')
        
    def nubia_log_end_remote(self,):
        action='adb shell am startservice --es command stop --ei type 3 -n cn.nubia.silence.detector/cn.nubia.auto.nubialog.WoodpeckerService'
        self.ssh_command(action,10,'')
    
    def time_Noise(self,noise_list):
        try:
            tn={}
            nl=[]
            d=(noise_list[0].split(' ')[0])
            t=(noise_list[0].split(' ')[1])
            #tim=datetime.datetime.strptime('%s %s'%(d,t),'%Y-%m-%d %H:%M:%S')
            tim='%s %s'%(d,t)
            for i in noise_list:
                nis=int(i.split(' ')[-1])
                if nis<100:
                    continue
                nl.append(nis)
            nis=int(sum(nl)/len(nl))
            return {'tim':tim,'nis':nis}
        except Exception:
            return {}
        
    def bStop( self, event ):
        global stop_test
        print('13')
        stop_test=True
        
        ret=self.command('pidof python',10)
        print(ret)
        if ret:
            rl=ret.split(' ')
            for r in rl:
                self.command_no('kill -9 %s'%r)
    
    def find_by_text(self,key_word,is_remote):
        try:
            action1='adb shell uiautomator dump --compressed'
            action2='adb shell cat /sdcard/window_dump.xml'
            xml=''
            bd=[0,0]
            st=time.time()
            while bd==[0,0] and (time.time()-st)<6:
                if is_remote:
                    self.ssh_command(action1,30,'')
                    xml=self.ssh_command(action2,10,'')
                else:
                    self.command(action1,30)
                    xml=self.command(action2,10)
                if xml:
                    tree=ET.fromstring(xml)
                    for i in tree.iter(tag='node'):
                        if key_word==i.attrib['text']:
                            print(i.attrib['text'],i.attrib['bounds'],self.b2d(i.attrib['bounds']))
                            bd=self.b2d(i.attrib['bounds']) 
                            break
            return bd
        except Exception:
            return [0,0]
    
    def find_by_contentdesc(self,key_word,is_remote):
        try:
            action1='adb shell uiautomator dump --compressed'
            action2='adb shell cat /sdcard/window_dump.xml'
            xml=''
            bd=[0,0]
            st=time.time()
            while bd==[0,0] and (time.time()-st)<6:
                if is_remote:
                    self.ssh_command(action1,30,'')
                    xml=self.ssh_command(action2,10,'')         
                else:
                    self.command(action1,30)
                    xml=self.command(action2,10)
                if xml:
                    tree=ET.fromstring(xml)
                    for i in tree.iter(tag='node'):
                        if key_word==i.attrib['content-desc']:
                            print(i.attrib['content-desc'],i.attrib['bounds'],self.b2d(i.attrib['bounds']))
                            bd=self.b2d(i.attrib['bounds']) 
                            break
            return bd
        except Exception:
            return [0,0]
    
    def find_by_image(self,key_word,is_remote):
        try:
            action1='adb shell uiautomator dump --compressed'
            action2='adb shell cat /sdcard/window_dump.xml'
            xml=''
            bd=[0,0]
            img_list=[]
            st=time.time()
            while bd==[0,0] and (time.time()-st)<6:
                
                if is_remote:
                    self.ssh_command(action1,30,'')
                    xml=self.ssh_command(action2,10,'')         
                else:
                    self.command(action1,30)
                    xml=self.command(action2,10)
                if xml:
                    tree=ET.fromstring(xml)
                    for i in tree.iter(tag='node'):
                        if 'android.widget.ImageView'==i.attrib['class']:
                            print(i.attrib['content-desc'],i.attrib['bounds'],self.b2d(i.attrib['bounds']))
                            img_list.append(i.attrib['bounds'])
                    if len(img_list)>0:
                        bd=self.b2d(img_list[key_word])
            print(time.time()-st)
            return bd
        except Exception:
            print(traceback.print_exc())
            return [0,0]
    
    def b2d(self,bounds):
        dd=[]
        td=[]
        dd.append(eval(bounds[:bounds.find(']')+1]))
        dd.append(eval(bounds[bounds.find(']')+1:]))
        td.append(dd[0][0]+(dd[1][0]-dd[0][0])//2)
        td.append(dd[0][1]+(dd[1][1]-dd[0][1])//2)
        return td
    
        
        
    def timeScroll( self, event ):
        global t_time,t_long
        a=self.m_slider1.GetValue()
        self.m_textCtrl1.SetValue(str(a))
        
        t_time=int(a)

    def timeScroll2( self, event ):
        global t_time,t_long
        a=self.m_slider11.GetValue()
        self.m_textCtrl11.SetValue(str(a))
        t_long=int(a)
        
if __name__ == '__main__':
    app = wx.App()
    main_win = MianWindow(None)
    main_win.init_main_window()
    main_win.Show()

    app.MainLoop()