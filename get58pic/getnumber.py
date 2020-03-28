import re
import urllib

filep=open("urllist.txt","r")
line=filep.readline()
line=line.strip()

fileto=open("pictureurllist.txt","w")


picturepattern=re.compile(r"""<span\sclass="tel"\sid="t_phone"><img\ssrc='(http://image.58.com/\S*)'\s*/></span>""")

while line.isspace()==0:
    webpage=urllib.urlopen(line).read().decode("utf-8")
    webpage=picturepattern.findall(webpage)
    print >>fileto,webpage[0]
    line=filep.readline()

filep.close()
fileto.close()



