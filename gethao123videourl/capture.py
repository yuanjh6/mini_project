# -*- coding: utf-8 -*-
#encoding=utf-8
import MySQLdb
import sys

import re
import urllib
import datetime
import string

reload(sys)
sys.setdefaultencoding("utf-8")

'''
数据采集
说明：
'''


#连接数据库获取站点信息
C={}
C['DB_NAME']='mysite'
C['DB_HOST']='localhost'
C['DB_USER']='root'
C['DB_PASSWD']=''
C['DB_CHARSET']='utf8'
C['TABLE_CAPTURE']='com_capture'
C['TABLE_CAPTURETO']='nav_sites'

#连接数据库
con=MySQLdb.connect(host=C['DB_HOST'],db=C['DB_NAME'],user=C['DB_USER'],passwd=C['DB_PASSWD'] ,charset=C['DB_CHARSET'])
cur=con.cursor()




#采集单个URL数据
def captureone(url,charset,headtag,foottag,splitreg,itemreg,itemmap):
	#参数验证
	P={}
	if(not url):
		print '待采集URL不能为空'
		return 0
	P['url']=url
	if(not charset):
		charset='utf8'
	P['charset']=charset
	P['headtag']=headtag
	P['foottag']=foottag
	P['splitreg']=splitreg
	if(not itemreg):
		print '提取信息正则式不能为空'
		return 0
	P['itemreg']=itemreg
	if(not itemmap):
		print '提取信息映射表不能为空'
		return 0
	P['itemmap']=itemmap

	#网页抓取
	try:
		webpage=urllib.urlopen(P['url']).read().decode(P['charset'])
	except UnicodeError,e:
		print e
		return 0
	if(not webpage):
		print '网页抓取失败'
		return 0

	#网页清理及切分
	tmp=webpage.partition(P['headtag'])
	tmp=tmp[2]
	tmp=tmp.partition(P['foottag'])
	webpage=tmp[0]
	if(not webpage):
		print '网页清除头尾后为空'
		return 0
	splitreg=re.compile(P['splitreg'])
	itemlist=splitreg.findall(webpage)
	#print P['splitreg']
	#print webpage
	if(not itemlist):
		print '切分匹配失败'
		return 0
	#for i in itemlist:print i

	#信息匹配
	tmpitemmap=P['itemmap'].split(',')
	itemmap=[]
	for i in tmpitemmap:
		i=i.split(':')
		itemmap.append(i)
	#for i in itemmap:print i

	itemreg=re.compile(P['itemreg'])
	
	iteminfolist=[]
	for i in itemlist:
		iteminfo={}
		info=itemreg.search(i)
		#print i
		#print P['itemreg']
		if(not info):
			print '条目信息匹配失败'
			continue
		for j in itemmap:
			iteminfo[j[0]]=info.group((int)(j[1]))
			#print j[0]
			#print info.group((int)(j[1]))
		iteminfolist.append(iteminfo)
	#信息返回
	return iteminfolist 

#根据字典结构生成插入的sql语句
def createsql(bef,dic,end):
	P={}
	#参数检查
	P['bef']=bef
	if(not dic):
		print '需要转化为sql的字典为空'
		return 0
	P['dic']=dic
	P['end']=end

	#生成sql语句中间部分
	msqla=[]
	msqlb=[]
	for i in dic:
		msqla.append(i)
		msqlb.append("'"+str(dic[i])+"'")
	msqla=string.join(msqla,',')
	msqlb=string.join(msqlb,',')
	msqla="("+msqla+")"
	msqlb="("+msqlb+")"
	msql=msqla+" values "+msqlb
	sql=bef+msql+end
	return sql



def capture(type):
	P={}
	#参数验证
	if(not type):
		print '待采集站点类型参数为空'
		return 0
	P['type']=type

	#获取待采集URL信息
	sql="select * from "+C['TABLE_CAPTURE']+" where type='"+P['type']+"'"
	#print sql
	info=cur.execute(sql)
	if(not info):
		print 'URLS列表获取出错'
		return 0
	urllist=cur.fetchall()

	#依次采集每个URL的数据
	for i in urllist:
		url=i[3]
		charset=i[4]
		headtag=i[5]
		foottag=i[6]
		splitreg=i[7]
		itemreg=i[8]
		itemmap=i[9]
		iteminfolist=captureone(url,charset,headtag,foottag,splitreg,itemreg,itemmap)
		if(not iteminfolist):
			print '返回网页条目信息为空'
			return 0
		for j in iteminfolist:
			bef="insert into "+C['TABLE_CAPTURETO']+" "
			dic=j
			end=" "
			sql=createsql(bef,dic,end)
			print sql
			'''
			try:
			database_code()
			except Exception, e:
			'''
			info=cur.execute(sql)
			if(not info):
				print '保存过程中sql语句执行错误'
				continue



'''
url="http://www.hao123.com/video"
charset="gb2312"
headtag='id="bd"'
foottag='id="ft"'
splitreg="<li>([\s\S]+?)</li>"
itemreg='href="(.+?)".+>(.+?)</a>'
itemmap="name:2,url:1"
tmp=captureone(url,charset,headtag,foottag,splitreg,itemreg,itemmap)
'''
capture('navsites')






cur.close()
con.commit()
con.close()
