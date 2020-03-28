# -*- coding: utf-8 -*-
#encoding=utf-8
import MySQLdb
import sys

import re
import urllib
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

'''
说明：从腾讯财经中提取自己感兴趣的数据
'''


#预定义常量
#数据库以及数据表等参数
C={}
C['DB_NAME']='mysite'
C['DB_HOST']='localhost'
C['DB_USER']='root'
C['DB_PASSWD']=''
C['DB_CHARSET']='utf8'
C['TABLE_NEWSSITE']='stock_newssite'
C['TABLE_NEWSNUM']='stock_newsnum'
C['TABLE_NEWS']='stock_news'
C['TABLE_STOCK']='stock_stock'
#网页网址切分等参数
C['STOCKURL']='http://stockhtm.finance.qq.com/sstock/ggcx/#STOCKID#.shtml'
C['WEBPAGECHARSET']='utf8'
C['HEADTAG']='<div class="rightcontent">'
C['FOOTTAG']='<div id="mbToolbar_mod" class="mbToolbar" style="left: 1149px; position: absolute; top: 3084px; ">'
C['SPLITTAG']='<div class="spacer"></div>'

#基本内容提取
C['BASEINFOSID']=2
C['BASEINFOREG']='<table class="data">[\s\S]+?<\/table>'
C['BASEINFO']=0

#股票医生内容提取,无法提取，估计采用JS生成的数据
C['DOCTORID']=3
C['DOCTORREG']='(<div class="left">[\s\S]+)<div class="right">'
C['DOCTOR']=1

C['DOCTORURL']='http://stockapp.finance.qq.com/doctor/#STOCKID#.html'
#注意此时stockid为短的那种
C['HOTURL']='http://stockhtm.finance.qq.com/sstock/quotpage/q/#STOCKID#.htm#yqfx'
def tenCapture(stockid):
	P={}
	P['stockid']=stockid

	#需要保存输出的数据保存
	O={}
	#常量赋值
	O['doctorurl']=C['DOCTORURL'].replace('#STOCKID#',stockid)
	O['hoturl']=C['HOTURL'].replace('#STOCKID#',stockid[2:8])

	#获取以及切分网页
	stockid=P['stockid'][2:8]
	weburl=C['STOCKURL'].replace('#STOCKID#',stockid)
	try:
		webpage=urllib.urlopen(weburl).read().decode(C['WEBPAGECHARSET'])
	except UnicodeError,e:
		print e
		return 0

	
	#print webpage

	tmp=webpage.partition(C['HEADTAG'])
	webpage=tmp[2]
	if(not webpage):
		print '头部获取错误'
		return 0
	tmp=webpage.partition(C['FOOTTAG'])
	webpage=tmp[0]
	if(not webpage):
		print '尾部信息获取错误'
		return 0
	webpage=webpage.split(C['SPLITTAG'])
	if(not webpage):
		print '信息切分错误'
		return 0
	
	#获取基本信息
	baseinfo=webpage[C['BASEINFOSID']]
	#print baseinfo
	baseinforeg=re.compile(C['BASEINFOREG'])
	info=baseinforeg.search(baseinfo)
	if(not info):
		print '基本信息获取失败'
		return 0
	O['baseinfo']=info.group(C['BASEINFO'])
	#print O['baseinfo']

	'''
	doctor=webpage[C['DOCTORID']]
	#print doctor
	doctorreg=re.compile(C['DOCTORREG'])
	info=doctorreg.search(doctor)
	if(not info):
		print '股票医生内容匹配失败'
		return 0
	O['doctor']=info.group(C['DOCTOR'])
	print O['doctor']
	'''
	return O

#连接数据库
con=MySQLdb.connect(host=C['DB_HOST'],db=C['DB_NAME'],user=C['DB_USER'],passwd=C['DB_PASSWD'] ,charset=C['DB_CHARSET'])
cur=con.cursor()

#获取数据库中所有的stockid
sql="select stockid from "+C['TABLE_STOCK']
info=cur.execute(sql)
info=cur.fetchall()
if(not info):
	print '查询为空 错误'
	sys.exit()
stocks=[]
for i in info:
	stocks.append(i[0])


#依次提取并保存到数据库中
for i in stocks:
	listt=tenCapture(i)
	sql="update "+C['TABLE_STOCK']+" set baseinfo="+"'"+listt['baseinfo']+"' where stockid='"+str(i)+"'"
	#print sql
	info=cur.execute(sql)
	if(not info):
		print '插入数据出错 关于'+str(i)
		continue
	else:
		print '插入数据成功 关于'+str(i)

cur.close()
con.commit()	
con.close()

'''
listt=tenCapture('sz000002')
import json
dump_str = json.dumps(listt, ensure_ascii=False)
print dump_str
'''