# -*- coding: cp1251 -*-
import os,sys,unicodedata,subprocess, contextlib
 	
downoadir='./Video_Downloads'
try:
  os.mkdir(downoadir)
except:
  print("Folder create failed") 
  
logf = open("log.log","a")



         
#Low quality
lq = "lq.txt"
try:
 with open(lq) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       os.chdir(downoadir)
       print("Downloading LQ {}: {}".format(cnt, line.strip()))
       cmd = "youtube-dl  --write-auto-sub -f 18 "+ line
       popen = subprocess.Popen(cmd, shell=True)
       popen.wait()
       rc = popen.returncode
       
       if rc!=0:
        logf.write('\nDownloading fail: \"'+line+'\"\n' )
       cnt += 1
       os.chdir('..')
       line = fp.readline()
except:
  print("LQ failed") 





#High Quality
hq = "hq.txt"
try:
 with open(hq) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       os.chdir(downoadir)
       print("Downloading HQ {}: {}".format(cnt, line.strip()))
       cmd = "youtube-dl  --write-auto-sub -f 137 "+ line
       popen = subprocess.Popen(cmd, shell=True)
       popen.wait()
       rc = popen.returncode
       
       if rc!=0:
        logf.write('\nDownloading fail: \"'+line+'\"\n' )
       cmd = "youtube-dl  --write-auto-sub -f 251 "+ line
       popen = subprocess.Popen(cmd, shell=True)
       popen.wait()
       rc = popen.returncode
       print rc
       if rc!=0:
       #print
        logf.write('\nDownloading soundtrack failed for: \"'+line+'\"\n' )
       cnt += 1
       os.chdir('..')
       line = fp.readline()

except:
  print("HQ failed") 

#try:
#Merge sound and video       
os.chdir(downoadir)
symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
tr = {ord(a):ord(b) for a, b in zip(*symbols)}
files_path = u'.'
files = [unicodedata.normalize('NFC', f) for f in os.listdir(u'.')]
for filename in files:
    if filename.endswith(".mp4"):
     filename1=filename.translate(tr)
     fileenc=filename1.encode('utf-8')
     asciidata=fileenc.decode("utf-8").encode("ascii","ignore")
     os.rename (filename,asciidata)
     filenameb=os.path.splitext(asciidata)[0]
     aux=""
     if os.path.exists((os.path.splitext(filename)[0]+".webm")):
      os.rename (os.path.splitext(filename)[0]+".webm",filenameb+".webm")
      aux=" -i \""+filenameb+".webm\" "
     sub=""
     if os.path.exists((os.path.splitext(filename)[0]+".en.vtt")):
       
       os.rename (os.path.splitext(filename)[0]+".en.vtt",filenameb+".vtt")
       sub="  -i \""+filenameb+".vtt\" "
     cmd = "ffmpeg -i \""+ filenameb +".mp4\" "+sub +aux + " -c copy  \""  + filenameb + ".mkv\" "
     
     popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
     popen.wait()
     #streamdata = popen.communicate()[0]
     rc = popen.returncode
     output = popen.stdout.read()
     
     if rc==0:
       #print
       logf.write('\nEncoding success: \"'+filenameb+'\"\n' )
       if os.path.exists(filenameb+".webm"): os.remove(filenameb+".webm")
       if os.path.exists(filenameb+".mp4"): os.remove(filenameb+".mp4")
       if os.path.exists(filenameb+".vtt"): os.remove(filenameb+".vtt")
       
     else:
       logf.write('\nEncoding fail: \"'+filenameb+'\"\n' )
     


#except:
 # print("Encoding failed") 
os.chdir('..')
open(hq, 'w').close()
open(lq, 'w').close()
logf.close()
