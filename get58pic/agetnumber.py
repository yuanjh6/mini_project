import re
import urllib

urlsource=raw_input("input the 58.com url please:")
urlpattern=re.compile(r'<a\shref="(http://sz.58.com/\S*shtml)".*?a>')
webpage=urllib.urlopen(urlsource).read().decode("utf-8")

filep=open("urllist.txt","w")
results=urlpattern.findall(webpage)
for i in results:
    print >>filep,i
filep.close()



filep=open("urllist.txt","r")
line=filep.readline()
line=line.strip()
fileto=open("pictureurllist.txt","w")

picturepattern=re.compile(r"""<span\sclass="tel"\sid="t_phone"><img\ssrc='(http://image.58.com/\S*)'\s/></span>""")

while line!="":
    wpp=urllib.urlopen(line)
    webpage=wpp.read().decode("utf-8")
    wpp.close()
    webpage=picturepattern.finditer(webpage)
    for i in webpage:
        print >>fileto,i.group(1)
    line=filep.readline()

filep.close()
fileto.close()

#raise SystemExit()
filep=open("pictureurllist.txt","r")
line=filep.readline()
line=line.strip()
i=0
while line!="":
    filename=str(i//2)+".jpg"
    urllib.urlretrieve(line,filename)
    line=filep.readline()
    i+=1
filep.close()
print "ok"
