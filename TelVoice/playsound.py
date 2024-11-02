import pyttsx3
import time,sys

engine = pyttsx3.init()
st=time.time()
set_n=int(sys.argv[1])
def onStart(name):
   print ('starting', name)
   
def onWord(name, location, length):
   print ('word', time.time()-st)
   if time.time()-st>set_n+3:
       engine.endLoop()
   engine.say('1 2 3 4 5 6 7 8 9 10 测 试 测 试 ', 'fox')
   
def onEnd(name, completed):
   pass
      
engine = pyttsx3.init()
engine.setProperty('rate',200)
engine.setProperty('voice','zh')
engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
engine.say('1 2 3 4 5 6 7 8 9 10 测 试 测 试 ', 'fox')
engine.startLoop()
