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
说明：设置stock表的预设信息,也就是无需要更新提取的内容，都是一次设置即可完成的内容
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

C['PRE_TIMEPIC_URL']='http://image.sinajs.cn/newchart/min/n/#STOCKID#.gif'
C['PRE_TIMEINFO_URL']='http://hq.sinajs.cn/list=#STOCKID#'
C['PRE_DAYPIC_URL']='http://image.sinajs.cn/newchart/daily/n/#STOCKID#.gif'
C['PRE_WEEKPIC_URL']='http://image.sinajs.cn/newchart/weekly/n/#STOCKID#.gif'
C['PRE_MOUTHPIC_URL']='http://image.sinajs.cn/newchart/monthly/n/#STOCKID#.gif'
C['PRE_DOCTOR_URL']='http://stockapp.finance.qq.com/doctor/#STOCKID#.html'
#此为短ID
C['PRE_HOT_URL']='http://stockhtm.finance.qq.com/sstock/quotpage/q/#STOCKID#.htm#yqfx'
C['PRE_PRICE_URL']='http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_price_history.php?symbol=#STOCKID#'

def preInfo(stockid):
	#参数保存
	P={}
	P['stockid']=stockid

	#输出信息保存
	O={}
	O['timepic']=C['PRE_TIMEPIC_URL'].replace('#STOCKID#',P['stockid'])
	O['timeinfo']=C['PRE_TIMEINFO_URL'].replace('#STOCKID#',P['stockid'])
	O['daypic']=C['PRE_DAYPIC_URL'].replace('#STOCKID#',P['stockid'])
	O['weekpic']=C['PRE_WEEKPIC_URL'].replace('#STOCKID#',P['stockid'])
	O['mouthpic']=C['PRE_MOUTHPIC_URL'].replace('#STOCKID#',P['stockid'])
	O['doctorurl']=C['PRE_DOCTOR_URL'].replace('#STOCKID#',P['stockid'])
	O['hoturl']=C['PRE_HOT_URL'].replace('#STOCKID#',P['stockid'][2:8])
	O['price']=C['PRE_PRICE_URL'].replace('#STOCKID#',P['stockid'])

	#返回信息
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
#for i in stocks:print i

#对每个stockid设置基本值
for i in stocks:
	listt=preInfo(i)
	if(not listt):
		print '基本信息获取失败'
		break
	sql="update "+C['TABLE_STOCK']+" set timepic='"+listt['timepic']+"',timeinfo='"+listt['timeinfo']+"',daypic='"+listt['daypic']+"',weekpic='"+listt['weekpic']+"',mouthpic='"+listt['mouthpic']+"',doctorurl='"+listt['doctorurl']+"',hoturl='"+listt['hoturl']+"',price='"+listt['price']+"' where stockid='"+str(i)+"'"
	#print sql
	info=cur.execute(sql)
	if(not info):
		print '更新语句执行失败关于'+str(i)
		continue
	else:
		print '更新成功关于'+str(i)
cur.close()
con.commit()
con.close()