import re
import urllib


urlpattern=re.compile(r'<a\shref="(http://sz.58.com/\S*shtml)".*?a>')
webpage=urllib.urlopen("http://sz.58.com/yingyou/").read().decode("utf-8")

filep=open("urllist.txt","w")
results=urlpattern.findall(webpage)
for i in results:
    print >>filep,i
filep.close()