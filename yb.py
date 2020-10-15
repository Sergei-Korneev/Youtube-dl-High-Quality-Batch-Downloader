# -*- coding: cp1251 -*-
import os,sys,unicodedata,subprocess, contextlib , datetime, platform, re
from pathlib import Path

if (sys.version_info.major != 3 and sys.version_info.minor != 8):
    print("This script is tested on Python 3.8!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

 
def help_():
  print("use: \nyb.py files \nyb.py videos \nyb.py all\nyb.py torrents")
  


cudir=(os.path.abspath(os.getcwd()))
cur_system=platform.system()
now = datetime.datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
trycount=9


if (cur_system=='Windows'):
  wgetbin=cudir+ '\\bin\\wget\\wget.exe'
  ytdlbin=cudir+ '\\bin\\youtube-dl.exe'
  ffmpegbin=cudir+ '\\bin\\ffmpeg\\ffmpeg.exe'
  aria2c=cudir+ '\\bin\\aria2\\aria2c.exe'
  pthsl='\\'
elif (cur_system=='Linux'):
      wgetbin='wget'
      ytdlbin='youtube-dl'
      ffmpegbin='ffmpeg'
      aria2c='aria2c'
      pthsl='//'

downoadir=cudir+pthsl+'Downloads'+pthsl+'Videos'
downoadir2=cudir+pthsl+'Downloads'+pthsl+'Files'
downoadir3=cudir+pthsl+'Downloads'+pthsl+'Torrents'



  

for dc in [downoadir,downoadir2,downoadir3]: 
   path = Path(dc)
   path.mkdir(parents=True, exist_ok=True)
  
logf = open("log.log","a")
logf.write('\nStarted at:  '+dt_string)
 


def torrents_(): 
 fl="torrents.txt"
 torf = open(fl,"w")
 symbols = (u"àáâãäåžæçèéêëìíîïðñòóôõö÷øùúûüýþÿÀÁÂÃÄÅšÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß",u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
 tr = {ord(a):ord(b) for a, b in zip(*symbols)}
 files = [unicodedata.normalize('NFC', f) for f in os.listdir(downoadir3)]
 for filename in files:
    if filename.endswith(".torrent"):
     filename1=filename.translate(tr)
     os.rename(downoadir3+pthsl+filename,downoadir3+pthsl+filename1)

 for file in os.listdir(downoadir3):
    print (file) 
    if file.endswith(".torrent"):
     torf.write(downoadir3+pthsl+file+"\n")
 torf.close()
 
 cmd = [aria2c,"-i",  cudir+pthsl+fl , "-d", downoadir3]
 tr=0 
 popen = subprocess.Popen(cmd, shell=False)
 popen.wait()
 rc = popen.returncode
 print (rc)
 
 
 

def files_(): 

 print("\n\nDownloading files... \n\n")       
#Files
 fl = "files.txt"
#try:

 with open(fl) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       if (line == "\n"):break
       os.chdir(downoadir2)
       print("\n------------------\n\nDownloading file {}: {}".format(cnt, line.strip())+"\n\n")
       cmd = [wgetbin,"--continue",  "--tries=15", "--show-progress", "--progress=bar:force",    line.strip() ]
       tr=0 
       while tr<trycount: 
        popen = subprocess.Popen(cmd, shell=False)
        popen.wait()
        rc = popen.returncode
        tr+=1
        if rc==0:break   

       if rc!=0:
       #print
        logf.write('\nDownloading failed for: \"'+line+'\"' )
       cnt += 1
       os.chdir(cudir)
       line = fp.readline()
#except:
  #print("Files failed") 
 open(fl, 'w').close()




#Merge sound and video

def encode():
 print("\n\nEncoding... \n\n")  
 os.chdir(downoadir)

 symbols = (u"àáâãäåžæçèéêëìíîïðñòóôõö÷øùúûüýþÿÀÁÂÃÄÅšÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß",
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
     
     cmd = [ffmpegbin,"-y", "-i",filenameb+".mp4","-c","copy",filenameb+".mkv"]
     
     for ext in [".webm",".m4a"]:
          if os.path.exists((os.path.splitext(filename)[0]+ext)):
           if not os.path.exists(filenameb+ext):os.rename(os.path.splitext(filename)[0]+ext,filenameb+ext)
           cmd.insert(4,"-i")
           cmd.insert(5,filenameb+ext)
      
     if os.path.exists((os.path.splitext(filename)[0]+".en.vtt")):
       if not os.path.exists(filenameb+".en.vtt"):os.rename(os.path.splitext(filename)[0]+".en.vtt",filenameb+".en.vtt")
       popen = subprocess.Popen([ffmpegbin,"-i",filenameb+".en.vtt",filenameb+".srt"], stdout=subprocess.PIPE)
       popen.wait()
       cmd.insert(6,"-i")
       cmd.insert(7,filenameb+".srt")
       
       
     print(cmd)
     popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
     popen.wait()
     #streamdata = popen.communicate()[0]
     rc = popen.returncode
     output = popen.stdout.read()
     
     if rc==0:
 
       logf.write('\nEncoding success: \"'+filenameb+'\"\n' )
       for ext in [".webm",".mp4",".en.vtt",".srt",".m4a"]:
          if os.path.exists(filenameb+ext): os.remove(filenameb+ext)
    
     else:
       logf.write('\nEncoding fail: \"'+filenameb+'\"' )
 os.chdir(cudir)






def videos_():   



 print("\n\nDownloading videos... \n\n")       
 
 video = "video.txt"
 
#try:

 with open(video) as fp:
   line = fp.readline()
   
   
   
   
   while line:
       if (line == "\n"):break
       
       #Parsing command line 
       commlen=len(line.split())
       url=""
       form=1
       if (commlen==1):
           if (len(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line.split()[0]))!=1):
              print("Wrong URL format: " + line.split()[0] +  "\n")
              continue 
           print("No second parameter specified. Low quality selected.\n")
           url=line.split()[0]
       elif (commlen==2):
           if (len(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line.split()[0]))!=1) or (len(re.findall(r"lq\b|hq\b|LQ\b|HQ\b", line.split()[1]))!=1):
              print("Wrong URL or quality format : " + line +  "\n")
              continue 
           url=line.split()[0]
           if (len(re.findall(r"hq\b|HQ\b", line.split()[1]))==1): form=2
           
       else:
         print("Wrong URL or quality format : " + line +  "\n")
         continue 

       
       os.chdir(downoadir)
       print("\n------------------\n\nDownloading: "+line+"\n\n")
       checkformat = subprocess.check_output([ytdlbin,"-F",url]).splitlines()
       i = -1
       
       
       if (form==1):
        while (checkformat):
        #Low quality
           #240p 144p 480p 360p
           #print (checkformat[i].decode() +"\n")
           optionalf=checkformat[i].decode() 
           #print(optionalf)
           if (
           #   "mp4" in optionalf and "480p" in optionalf and "video only" in optionalf 
              "mp4" in optionalf  and "360p" in optionalf 
              or "mp4" in optionalf  and "240p" in optionalf and "video only" in optionalf 
              or "mp4" in optionalf  and "144p" in optionalf and "video only" in optionalf 
              
           ) :
             #print (checkformat[i]+"\n")
           
           
             cmd = [ytdlbin,"--restrict-filenames", "-R", "30", "--write-auto-sub", "-f" , checkformat[i][0:3].decode() , url]
             print ("\n\nSelected video format is: \n\n"+optionalf+"\n\n")
             break
            
           i -= 1
           
       else: 
       #High quality   
        while (checkformat):
           optionalf=checkformat[i].decode() 
           if ('mp4' in optionalf and 'video only' in optionalf):
             cmd = [ytdlbin,"--restrict-filenames", "-R", "30", "--write-auto-sub", "-f", checkformat[i][0:3].decode(), url]
             print ("\n\nSelected video format is: \n\n"+optionalf+"\n\n")
             break
           i -= 1
           
           
       tr=0 
       logf.write('\nTrying cmd:  '+ url )
       while tr<trycount: 
        popen = subprocess.Popen(cmd, shell=False)
        popen.wait()
        rc = popen.returncode
        tr+=1
        if rc==0:
         logf.write(' Success!\n' )
         break   
       if rc!=0:
        logf.write(' Fail!\n' )
        
       else:  
        print ("\n\nDownloading soundtrack...\n\n")
        
        
        
        if (form==1):
         while (checkformat):
         #Low audio quality
           
           optionalf=checkformat[i].decode() 
           if (
           
              "audio only" in optionalf
           ) :
             #print (checkformat[i]+"\n")
           
           
             cmd = [ytdlbin,"--restrict-filenames", "-R", "30", "--geo-bypass", "-f" , checkformat[i][0:3].decode() , url]
             print ("\n\nSelected audio format is: \n\n"+optionalf+"\n\n")
             break
            
           i += 1
           
        else: 
        #High audio quality   
         while (checkformat):
           optionalf=checkformat[i].decode() 
           if ("audio only" in optionalf):
             cmd = [ytdlbin,"--restrict-filenames", "-R", "30", "--geo-bypass", "-f", checkformat[i][0:3].decode(), url]
             print ("\n\nSelected audio format is: \n\n"+optionalf+"\n\n")
             break
           i -= 1
        
        
        
        tr=0 
        while tr<trycount: 
         popen = subprocess.Popen(cmd, shell=False)
         popen.wait()
         rc = popen.returncode
         tr+=1
         if rc==0:
           encode() 
           break
            
       
        if rc!=0:
        #print
         logf.write('\nDownloading soundtrack failed for: \"'+url+'\"' )
       
       os.chdir(cudir)
       line = fp.readline()
   

#except:
  #print("failed") 




 open(video, 'w').close()
 

if (len(sys.argv)==1):
     help_()
     sys.exit(1)
elif (str(sys.argv[1])  == "videos"):
     videos_()
elif (str(sys.argv[1])  == "files"):
     files_()
elif (str(sys.argv[1])  == "torrents"):
     torrents_()

     
else:
     help_()
     sys.exit(1)
   
 
now = datetime.datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
logf.write('\nFinished at:  '+dt_string)
logf.close()




