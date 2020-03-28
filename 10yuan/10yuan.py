# -*- coding: utf-8 -*-
#encoding=utf-8
#导入类库
import sys
import re
import urllib

reload(sys)
sys.setdefaultencoding("utf-8")
#系统预定义常量
C={}
C['urlfile']='url.txt'
C['charset']='gbk'
C['headtag']='<div class="tb-detail-hd">'
C['foottag']='<ul id="J_UlThumb" class="tb-thumb tb-clearfix">'
C['itemreg']=r'<h3>(<[^>]+>)?([^<]+)(<\/a>)?<\/h3>[\s\S]*<img id="J_ImgBooth" src="(\S+)"  data-hasZoom="700" \/>'
C['itemname']='2'
C['itempic']='4'

#文件读取网址列表,保存到列表
def readurl():
	#打开温条件
	urlfile=C['urlfile']
	filep=open(urlfile,'r')
	#读取文件
	urllist=[]
	urltmp=filep.readline()
	while urltmp:
		urllist.append(urltmp.strip())
		urltmp=filep.readline()
	return urllist


#对单个URL进行网页内容获取，清理，匹配
def getcotent(weburl):
	#网页抓取
	webpage=urllib.urlopen(weburl).read().decode(C['charset'])
	if(not webpage):return 0

	#网页头尾信息清除
	tmp=webpage.partition(C['headtag'])
	webpage=tmp[2]
	tmp=webpage.partition(C['foottag'])
	webpage=tmp[0]
	#print 'this is webpage without head and foot'
	#print webpage

	#内容匹配
	itemreg=re.compile(C['itemreg'])
	info=itemreg.search(webpage)
	if(not info):
		print 'info is none'
		return 0
	#print 'item infomation '+info.group(int(C['itemname']))+weburl+info.group(int(C['itempic']))
	if(not info):
		print 'can not match the content'
		return 0
	item=[info.group(int(C['itemname'])).strip(),weburl,info.group(int(C['itempic']))]

	#内容返回
	return item


#依次对每个网址进行内容获取，结果按照特定格式打印
def endpage():
	urllist=readurl()
	if (not urllist):
		print 'urllist is none'
		return 0
	for i in urllist:
		#print i
		if(not i):
			print 'i in urlist is none'
			continue
		item=getcotent(i)
		if(not item):
			print 'itme is none,can not match'
			continue
		newitem='<h3><a href="'+str(item[1])+'">'+str(item[0])+r'</a></h3><img src="'+str(item[2])+r'"/>'
		print newitem
	return 0

'''
listt=readurl()
for i in listt:print i

listt=getcotent('http://detail.tmall.com/item.htm?id=14820627330')
for i in listt:print i
'''
endpage()