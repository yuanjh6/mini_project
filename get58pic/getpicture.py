import urllib

filep=open("pictureurllist.txt","r")
line=filep.readline()
i=0
while line.isspace()==0:
    filename=str(i)+".jpg"
    urllib.urlretrieve(line,filename)
    line=filep.readline()
    i+=1