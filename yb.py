# -*- coding: cp1251 -*-
import os,sys,unicodedata,subprocess, contextlib , datetime, platform


if (sys.version_info.major != 3 and sys.version_info.minor != 8):
    print("This script is tested on Python 3.8!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

 
def help_():
  print("use: \nyb.py files \nyb.py video \nyb.py all\nyb.py torrents")
  


cudir=(os.path.abspath(os.getcwd()))
cur_system=platform.system()
now = datetime.datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
trycount=9
downoadir=os.getcwd()+'/Video_Downloads'
downoadir2=os.getcwd()+'/Files_Downloads'


if (cur_system=='Windows'):
  wgetbin=os.getcwd()+ '/bin/wget/wget.exe'
  ytdlbin=os.getcwd()+ '/bin/youtube-dl.exe'
  ffmpegbin=os.getcwd()+ '/bin/ffmpeg/ffmpeg.exe'
  aria2c=os.getcwd()+ '/bin/aria2/aria2c.exe'
elif (cur_system=='Linux'):
      wgetbin='wget'
      ytdlbin='youtube-dl'
      ffmpegbin='ffmpeg'
      aria2c='aria2c'
  

  

if not os.path.exists(downoadir): os.mkdir(downoadir)
if not os.path.exists(downoadir2): os.mkdir(downoadir2)
    
logf = open("log.log","a")
logf.write('\n----------------------  Started at:  '+dt_string +'  ----------------------\n\n' )
 


def torrents_(): 
 torf = open("torrents.txt","w")
 for file in os.listdir(os.getcwd()+"/torrents"):
   if file.endswith(".torrent"):
     torf.write(os.getcwd()+"/torrents/"+ file+"\n")

 torf.close()

 cmd = [aria2c,"-i",  os.getcwd()+"/torrents.txt" , "-d", os.getcwd()+"/torrents"]
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
        logf.write('\nDownloading failed for: \"'+line+'\"\n' )
       cnt += 1
       os.chdir(cudir)
       line = fp.readline()
#except:
  #print("Files failed") 
 open(fl, 'w').close()

def videos_():   

 print("\n\nDownloading videos... \n\n")       
#Low quality
 lq = "lq.txt"
#try:

 with open(lq) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       if (line == "\n"):break
       os.chdir(downoadir)
       print("\n------------------\n\nDownloading LQ {}: {}".format(cnt, line.strip())+"\n\n")
       checkformat = subprocess.check_output([ytdlbin,"-F",line]).splitlines()
       i = -1
       
       while (checkformat):
           
           if ("mp4" in checkformat[i].decode() and "18 " in checkformat[i].decode()  and "360p" in checkformat[i].decode()) or ("mp4" in checkformat[i].decode() and "video only" in checkformat[i].decode()  and "480p" in checkformat[i].decode())  :
             #print (checkformat[i]+"\n")
           
           
             cmd = [ytdlbin,"--restrict-filenames", "-R", "30", "--write-auto-sub", "-f" , checkformat[i][0:3].decode() , line]
             print ("\n\nSelected video format is: \n\n"+checkformat[i].decode()+"\n\n")
             break
            
           i -= 1
        
       tr=0 
       while tr<trycount: 
        popen = subprocess.Popen(cmd, shell=False)
        popen.wait()
        rc = popen.returncode
        tr+=1
        if rc==0:break   

       
       if rc!=0:
        logf.write('\nDownloading fail: \"'+line+'\"\n' )
       else:  
        print ("\n\nDownloading soundtrack...\n\n")
        cmd = [ytdlbin,"--restrict-filenames", "--geo-bypass", "-R", "30", "--write-auto-sub", "-f", "251", line]
        tr=0 
        while tr<trycount: 
         popen = subprocess.Popen(cmd, shell=False)
         popen.wait()
         rc = popen.returncode
         tr+=1
         if rc==0:break  
       
        if rc!=0:
        #print
         logf.write('\nDownloading soundtrack failed for: \"'+line+'\"\n' )
       cnt += 1
       os.chdir(cudir)
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
       print("\n------------------\nDownloading HQ {}: {}".format(cnt, line.strip())+"\n\n")
       
       checkformat = subprocess.check_output ( [ytdlbin,"-F",str(line)]).splitlines()
       
       i = -1
       while (checkformat):
           
           if ('mp4' in checkformat[i].decode() and 'video only' in checkformat[i].decode()):
             cmd = [ytdlbin,"--restrict-filenames", "-R", "30", "--write-auto-sub", "-f", checkformat[i][0:3].decode(), line]
             print ("\n\nSelected video format is: \n\n"+checkformat[i].decode()+"\n\n")
             break
           i -= 1
       tr=0 
       while tr<trycount: 
        popen = subprocess.Popen(cmd, shell=False)
        popen.wait()
        rc = popen.returncode
        tr+=1
        if rc==0:break
       
       if rc!=0:
        logf.write('\nDownloading fail: \"'+line+'\"\n' )
       else:
        print ("\n\nDownloading soundtrack...\n\n") 
        cmd = [ytdlbin,"--restrict-filenames","--geo-bypass","-R","30","--write-auto-sub","-f","251", line]
        tr=0 
        while tr<trycount: 
         popen = subprocess.Popen(cmd, shell=False)
         popen.wait()
         rc = popen.returncode
         tr+=1
         if rc==0:break
       
        if rc!=0:
       #print
         logf.write('\nDownloading soundtrack failed for: \"'+line+'\"\n' )
       cnt += 1
       os.chdir(cudir)
       line = fp.readline()

#except:
#  print("HQ failed") 

#try:
#Merge sound and video

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
     
     if os.path.exists((os.path.splitext(filename)[0]+".webm")):
      if not os.path.exists(filenameb+".webm"):os.rename(os.path.splitext(filename)[0]+".webm",filenameb+".webm")
      cmd.insert(4,"-i")
      cmd.insert(5,filenameb+".webm")
     
     if os.path.exists((os.path.splitext(filename)[0]+".en.vtt")):
       if not os.path.exists(filenameb+".en.vtt"):os.rename(os.path.splitext(filename)[0]+".en.vtt",filenameb+".en.vtt")
       popen = subprocess.Popen([ffmpegbin,"-i",filenameb+".en.vtt",filenameb+".srt"], stdout=subprocess.PIPE)
       popen.wait()
       cmd.insert(6,"-i")
       cmd.insert(7,filenameb+".srt")
       
       
     print (os.path.abspath(os.getcwd()))  
     
     print(cmd)
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
 os.chdir(cudir)
 open(hq, 'w').close()
 open(lq, 'w').close()


#except:
 # print("Encoding failed") 
 
 
if (len(sys.argv)==1):
     help_()
     sys.exit(1)
elif (str(sys.argv[1])  == "video"):
     videos_()
elif (str(sys.argv[1])  == "files"):
     files_()
elif (str(sys.argv[1])  == "torrents"):
     torrents_()
elif (str(sys.argv[1])  == "all"):
     files_()
     videos_()
else:
     help_()
     sys.exit(1)
   
 
now = datetime.datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
logf.write('\n----------------------  Finished at:  '+dt_string +'  ----------------------\n\n' )
logf.close()




