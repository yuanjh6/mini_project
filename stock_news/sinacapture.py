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
说明：从新浪财经提取出自己感兴趣的内容，并保存到对应的数据库中
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
C['STOCKURL']='http://finance.sina.com.cn/realstock/company/#STOCKID#/nc.shtml'
C['WEBPAGECHARSET']='gb2312'
C['HEADTAG']='<dl id="info">'
C['FOOTTAG']='<div id="ufo" unselectable="on"></div>'
C['SPLITTAG']='</dd>'

#地雷信息正则表达式
C['ITEMONEREG']="<a.+?href='(http:\/\/money.finance.sina.com.cn\/corp\/view\/vCB_AllMemordDetail.php[^>]+?)'[^>]*>(.+)<\/a>"
C['FUTURENEWSTITLE']=2
C['FUTURENEWSURL']=1

#获取分红信息
C['ITEMREGTWO']='<table id="bonus" cellpadding="0" class="list">[\s\S]*?<\/table>'
C['SHARE']=0

#获取研究报告
C['ITEMREGTHR']='<table cellpadding="0" class="list stocknews">[\s\S]+?<\/table>'
C['STUDYPAPER']=0

#分价表
C['PRICE']='http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_price_history.php?symbol=#STOCKID#'

'''

C['ITEMREGTHR']=
C['ITEMREGFOU']=
'''



		




#网页内容获取以及切分匹配
def sinaInfo(stockid):
	P={}
	P['stockid']=stockid
	O={}

	#网页内容
	stockurl=C['STOCKURL'].replace('#STOCKID#',P['stockid'])
	try:
		webpage=urllib.urlopen(stockurl).read().decode(C['WEBPAGECHARSET'])
	except UnicodeError,e:
		print e
		return 0

	#头尾切分
	tmp=webpage.partition(C['HEADTAG'])
	webpage=tmp[2]
	tmp=webpage.partition(C['FOOTTAG'])
	webpage=tmp[0]
	#print webpage
	webpage=webpage.split(C['SPLITTAG'])
	#for i in webpage:print i
	
	#获取地雷信息
	#print webpage[0]
	#print C['ITEMONEREG']
	itemonereg=re.compile(C['ITEMONEREG'])
	info=itemonereg.search(webpage[0])
	O['fnewstitle']=info.group(C['FUTURENEWSTITLE'])
	O['fnewsurl']=info.group(C['FUTURENEWSURL'])

	#获取分红信息
	#print webpage[3]
	itemtworeg=re.compile(C['ITEMREGTWO'])
	info=itemtworeg.search(webpage[3])
	if(not info):
		print '分红信息获取失败'
		return 0
	O['share']=info.group(C['SHARE'])
	#print O['share']

	#获取研究报告
	#print webpage[2]
	itemregthr=re.compile(C['ITEMREGTHR'])
	info=itemregthr.search(webpage[2])
	if(not info):
		print '研报信息获取失败'
		return 0
	O['studypaper']=info.group(C['STUDYPAPER'])
	#print O['studypaper']

	#生成分价表链接
	O['price']=C['PRICE'].replace('#STOCKID#',P['stockid'])
	#print O['price']
	return O

	

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

#更新数据
for i in stocks:
	listt=sinaInfo(i)
	if(not listt):
		print '获取信息失败'
		continue
	sql="update "+C['TABLE_STOCK']+" set fnewstitle='"+listt['fnewstitle']+"',fnewsurl='"+listt['fnewsurl']+"',share='"+listt['share']+"',studypaper='"+listt['studypaper']+"' where stockid='"+str(i)+"'"
	#print sql
	info=cur.execute(sql)
	if(not info):
		print '更新数据出错关于'+str(i)
		continue
	else:
		print '数据更新成功关于'+str(i)

cur.close()
con.commit()	
con.close()