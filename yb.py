import os,sys,unicodedata,subprocess
 	
downoadir='./Video_Downloads'
try:
  os.mkdir(downoadir)
except:
  print("Folder create failed") 
  
logf = open("encoding.log","a")
#High Quality
hq = 'hq.txt'
with open(hq) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       os.chdir(downoadir)
       print("Line {}: {}".format(cnt, line.strip()))
       cmd = "youtube-dl  --write-auto-sub -f 137 "+ line
       popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
       popen.wait()
       rc = popen.returncode
       output = popen.stdout.read()
       print rc
       cmd = "youtube-dl  --write-auto-sub -f 251 "+ line
       popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
       popen.wait()
       rc = popen.returncode
       output = popen.stdout.read()
       print rc
       cnt += 1
       os.chdir('..')
       line = fp.readline()

       
#Low quality       
lq = 'lq.txt'
with open(lq) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       os.chdir(downoadir)
       print("Line {}: {}".format(cnt, line.strip()))
       cmd = "youtube-dl  --write-auto-sub -f 18 "+ line
       popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
       popen.wait()
       rc = popen.returncode
       output = popen.stdout.read()
       if rc==0:
       #print
       logf.write('\nDownloading success: \"'+line+'\"\n' )
       os.remove(filenameb+".webm")
       os.remove(filenameb+".mp4") 
       else:
       logf.write('\nDownloading fail: \"'+line+'\"\n' )
       cnt += 1
       os.chdir('..')
       line = fp.readline()


#Merge sound and video       
os.chdir(downoadir)
files_path = u'.'
files = [unicodedata.normalize('NFC', f) for f in os.listdir(u'.')]
for filename in files:
    if filename.endswith(".mp4"):
     fileenc=filename.encode('utf-8')
     asciidata=fileenc.decode("utf-8").encode("ascii","ignore")
     os.rename (filename,asciidata)
     filenameb=os.path.splitext(asciidata)[0]
     os.rename (os.path.splitext(filename)[0]+".webm",filenameb+".webm")
     cmd = "ffmpeg -i \""+ filenameb +".mp4\" -i \""+filenameb+".webm" + "\" -c copy \""  + filenameb + ".mkv\""
     
     popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
     popen.wait()
     #streamdata = popen.communicate()[0]
     rc = popen.returncode
     output = popen.stdout.read()
       
     if rc==0:
       #print
       logf.write('\nEncoding success: \"'+filenameb+'\"\n' )
       os.remove(filenameb+".webm")
       os.remove(filenameb+".mp4") 
     else:
       logf.write('\nEncoding fail: \"'+filenameb+'\"\n' )
     
os.chdir('..')

logf.close()
