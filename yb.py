# -*- coding: cp1251 -*-
import os,sys,unicodedata,subprocess, contextlib , datetime


if (sys.version_info.major != 3 and sys.version_info.minor != 8):
    print("This script is tested on Python 3.8!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)


now = datetime.datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")



downoadir=os.getcwd()+'\Video_Downloads'
try:
  os.mkdir(downoadir)
except:
  print("Folder create failed") 
  
logf = open("log.log","a")

logf.write('\n----------------------  Started at:  '+dt_string +'  ----------------------\n\n' )

       
#Low quality
lq = "lq.txt"
#try:

with open(lq) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       if (line == "\n"):break
       os.chdir(downoadir)
       print("\n\nDownloading LQ {}: {}".format(cnt, line.strip())+"\n\n")
       checkformat = subprocess.check_output("youtube-dl -F " + line).splitlines()
       i = -1
       
       while (checkformat):
           
           if ("mp4" in checkformat[i].decode() and "18 " in checkformat[i].decode()  and "360p" in checkformat[i].decode()) or ("mp4" in checkformat[i].decode() and "video only" in checkformat[i].decode()  and "480p" in checkformat[i].decode())  :
             #print (checkformat[i]+"\n")
           
           
             cmd = "youtube-dl --restrict-filenames --geo-bypass -R 30 --write-auto-sub -f " + checkformat[i][0:3].decode() + " " + line
             print ("\n\nSelected video format is: \n\n"+checkformat[i].decode()+"\n\n")
             break
            
           i -= 1
        
       
       popen = subprocess.Popen(cmd, shell=True)
       popen.wait()
       rc = popen.returncode
       
       if rc!=0:
        logf.write('\nDownloading fail: \"'+line+'\"\n' )
       print ("\n\nDownloading soundtrack...\n\n")
       cmd = "youtube-dl --restrict-filenames --geo-bypass -R 30 --write-auto-sub -f 251 "+ line
       popen = subprocess.Popen(cmd, shell=True)
       popen.wait()
       rc = popen.returncode
       
       if rc!=0:
       #print
        logf.write('\nDownloading soundtrack failed for: \"'+line+'\"\n' )
       cnt += 1
       os.chdir('..')
       line = fp.readline()
#except:
  #print("LQ failed") 




#High Quality
hq = "hq.txt"
#try:
with open(hq) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       if (line=="\n"):break
       os.chdir(downoadir)
       print("Downloading HQ {}: {}".format(cnt, line.strip())+"\n\n")
       
       checkformat = subprocess.check_output("youtube-dl -F " + str(line)).splitlines()
       
       i = -1
       while (checkformat):
           
           if ('mp4' in checkformat[i].decode() and 'video only' in checkformat[i].decode()):
             cmd = "youtube-dl --restrict-filenames --geo-bypass -R 30 --write-auto-sub -f " + checkformat[i][0:3].decode() + " " + line
             print ("\n\nSelected video format is: \n\n"+checkformat[i].decode()+"\n\n")
             break
           i -= 1
        
        
       popen = subprocess.Popen(cmd, shell=True)
       popen.wait()
       rc = popen.returncode
       
       if rc!=0:
        logf.write('\nDownloading fail: \"'+line+'\"\n' )
       print ("\n\nDownloading soundtrack...\n\n") 
       cmd = "youtube-dl --restrict-filenames --geo-bypass -R 30 --write-auto-sub -f 251 "+ line
       popen = subprocess.Popen(cmd, shell=True)
       popen.wait()
       rc = popen.returncode
       
       if rc!=0:
       #print
        logf.write('\nDownloading soundtrack failed for: \"'+line+'\"\n' )
       cnt += 1
       os.chdir('..')
       line = fp.readline()

#except:
#  print("HQ failed") 

#try:
#Merge sound and video

print("\n\nEncoding... \n\n")  
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
     filenameb=os.path.splitext(asciidata)[0].decode()
     aux=""
     if os.path.exists((os.path.splitext(filename)[0]+".webm")):
      if not os.path.exists(filenameb+".webm"):os.rename (os.path.splitext(filename)[0]+".webm",filenameb+".webm")
      aux=" -i \""+filenameb+".webm\" "
     sub=""
     if os.path.exists((os.path.splitext(filename)[0]+".en.vtt")):
       
       if not os.path.exists(filenameb+".en.vtt"):os.rename (os.path.splitext(filename)[0]+".en.vtt",filenameb+".en.vtt")
       sub="  -i \""+filenameb+".en.vtt\" "
       cmd = "ffmpeg  "+sub  + "\""+filenameb + ".srt\" "
       popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
       popen.wait()
       sub="  -i \""+filenameb+".srt\" "
     cmd = "ffmpeg -y -i \""+ filenameb +".mp4\" "+sub +aux + " -c copy  \""  + filenameb + ".mkv\" "
     popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
     popen.wait()
     #streamdata = popen.communicate()[0]
     rc = popen.returncode
     output = popen.stdout.read()
     
     if rc==0:
 
       logf.write('\nEncoding success: \"'+filenameb+'\"\n' )
       if os.path.exists(filenameb+".webm"): os.remove(filenameb+".webm")
       if os.path.exists(filenameb+".mp4"): os.remove(filenameb+".mp4")
       if os.path.exists(filenameb+".en.vtt"): os.remove(filenameb+".en.vtt")
       if os.path.exists(filenameb+".srt"): os.remove(filenameb+".srt")
       
     else:
       logf.write('\nEncoding fail: \"'+filenameb+'\"\n' )
     


#except:
 # print("Encoding failed") 
os.chdir('..')
open(hq, 'w').close()
open(lq, 'w').close()

now = datetime.datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
logf.write('\n----------------------  Finished at:  '+dt_string +'  ----------------------\n\n' )



logf.close()
