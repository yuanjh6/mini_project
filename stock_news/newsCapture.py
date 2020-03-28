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
获取一只股票的各个新闻站点的新闻，保存各个新闻以及新闻总数的统计信息
'''

#连接数据库获取站点信息
C={}
C['DB_NAME']='mysite'
C['DB_HOST']='localhost'
C['DB_USER']='root'
C['DB_PASSWD']=''
C['DB_CHARSET']='utf8'
C['TABLE_NEWSSITE']='stock_newssite'
C['TABLE_NEWSNUM']='stock_newsnum'
# C['NEWSLASTDB']='stock_newslast'
C['TABLE_NEWS']='stock_news'
C['TABLE_STOCK']='stock_stock'

#连接数据库
con=MySQLdb.connect(host=C['DB_HOST'],db=C['DB_NAME'],user=C['DB_USER'],passwd=C['DB_PASSWD'] ,charset=C['DB_CHARSET'])
cur=con.cursor()


#获取一个站点关于一个股票的新闻
def getNews(siteid,stockid):
	if((not siteid) or (not stockid)):
		print '参数含有空值'
		return 0
	#传入参数存储
	P={}
	P['siteid']=siteid
	P['stockid']=stockid
	#默认参数
	P['page']=1


	#获取站点参数
	sql="select * from "+C['TABLE_NEWSSITE']+" where id='"+str(P['siteid'])+"'"
	info=cur.execute(sql)
	info=cur.fetchone()
	if(not info):
		print '站点信息获取错误'
		return 0
	
	#站点参数获取
	site={}
	site['url']=info[2]
	site['charset']=info[3]
	site['stocktype']=info[4]
	site['headtag']=info[5]
	site['foottag']=info[6]
	site['splittag']=info[7]
	site['itemregexp']=info[8]
	site['itemname']=info[9]
	site['itemurl']=info[10]
	site['itemdate']=info[11]
	site['baseurl']=info[12]

	#网页抓取
	if(site['stocktype']):
		stockid=P['stockid'][2:8]
	else:
		stockid=P['stockid']
	pageurl=site['url'].replace('#STOCKID#',str(stockid))
	pageurl=pageurl.replace('#PAGE#',str(P['page']))
	#print pageurl
	try:
		webpage=urllib.urlopen(pageurl).read().decode(site['charset'])
	except UnicodeError,e:
		print e
		return 0
	#去除头尾无用信息以及切分条目
	tmp=webpage.partition(site['headtag'])
	webpage=tmp[2]
#	print webpage

	tmp=webpage.partition(site['foottag'])
	webpage=tmp[0]
#	print webpage

	#条目信息切分匹配及提取
	webpage=webpage.split(site['splittag'])
	webpage.pop()#剔除最后一条无用信息
#	for i in webpage:print i

	itemregexp=re.compile(site['itemregexp'])
	wlength=len(webpage)
	newslist=[]
	
	i=0
	for v in webpage:
		news=[]
		#print i
		info=itemregexp.search(v)
		#print info
		if(not info):break
		news.append(info.group((int)(site['itemname'])))
		if(site['baseurl']):
			news.append(site['baseurl']+str(info.group((int)(site['itemurl']))))
		else:
			news.append(str(info.group((int)(site['itemurl']))))
		news.append(info.group((int)(site['itemdate'])))
		newslist.append(news)
		i=i+1
	#信息返回
	#得到获取的新闻在newslist中
	#return newslist
	#	print listnews
	listnews=newslist
	if(not listnews):
		print '获取的新闻列表为空'
		return 0
	#获取上次的最新新闻
	sql="select * from "+C['TABLE_NEWS']+" where stockid='"+str(P['stockid'])+"' and siteid='"+str(P['siteid'])+"' order by id desc limit 1"
#	print sql
	cur.execute(sql)
	info=cur.fetchone()

	#保存正真的最新的新闻
	newlistnews=[]
	
	#筛选出最新新闻
	if(info):
		#以前采集过
		info=info[5]
	#	print info
		for i in listnews:
			if(not cmp(i[1],info)):break
			newlistnews.append(i)
	else:
		#不存在上次采集，所有新闻都是最新新闻
	#	print listnews
	
	#	for i in listnews:
	#		newlistnews.append(i)
	
		newlistnews=listnews
	#for i in newlistnews:for j in i:print j

	if(not newlistnews):
		print '最新的新闻为空 站点'+str(P['siteid'])+' 关于 '+str(P['stockid'])
		return 0
	#保存时，越新ID越大，所以应该反转一下
	newlistnews.reverse()
	#返回正真的最新新闻，在newlistnews中
	#return (newlistnews)
	#转存获取的最新新闻,由于上面已经检测，所以此处不会为空
	newslist=newlistnews
	todaystr=str(datetime.date.today())

	for k in newslist:
		sql="insert into "+C['TABLE_NEWS']+" values('','"+todaystr+"','"+P['stockid']+"','"+str(P['siteid'])+"','"+k[0]+"','"+k[1]+"','"+k[2]+"')"
#				print sql
		cur.execute(sql)
	print 'store the newsdata from '+str(P['siteid'])+' about '+str(P['stockid'])
	return 0

#获取数据库中所有的stockid
sql="select stockid from "+C['TABLE_STOCK']
info=cur.execute(sql)
info=cur.fetchall()
if(not info):
	print 'stock查询为空 错误'
	sys.exit()
stocks=[]
for i in info:
	stocks.append(i[0])
	#print i[0]

#获取数据库中所有的site表的id
sql="select id from "+C['TABLE_NEWSSITE']
info=cur.execute(sql)
info=cur.fetchall()
if(not info):
	print 'site表查询 错误'
	sys.exit()
sites=[]
for i in info:
	sites.append(i[0])
	#print i[0]


for i in sites:
	for j in stocks:
		getNews(i,j)

'''
getNews(1,'sh600019')
'''
print 'end of file'
cur.close()
con.commit()
con.close()