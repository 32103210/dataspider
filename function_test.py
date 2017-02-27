# -*- coding:utf-8 -*-
# import os
# import  requests
# from  bs4 import BeautifulSoup
# url ="http://zu.gz.fang.com/"
#
# header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
# html = requests.get( url,headers= header)
# soup = BeautifulSoup(html.content, 'lxml')
#
# print soup

import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import pandas as pd

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
html = requests.get( 'http://esf.sh.fang.com',headers= header) #改
soup = BeautifulSoup(html.text, 'lxml')
qx = soup.select('div.qxName > a')[1:]
URL = 'http://esf.sh.fang.com' #网址——————
quyu = []
quyu_name =[]
for i in qx:
	quyu.append(URL + i.get('href'))
	quyu_name.append(i.get_text())
# print(len(quyu_name),len(quyu))
# print(quyu[1])
def getSource(url):
	info = defaultdict(list)
	html = requests.get( url,headers= header)
	soup = BeautifulSoup(html.text, 'lxml')
	zPrice = soup.select('span.price') #获取平方价格，单位万
	dPrice = soup.select('div.moreInfo > p:nth-of-type(2)') #获取单位平方米
	jz_area = soup.select('div.houseList > dl > dd > div:nth-of-type(2) > p:nth-of-type(1)') #获取建筑面积
	adress = soup.select('p.mt10 > span') #获取具体的位置
	xiaoqu = soup.select('p.mt10 > a') #获取小区
	descript =  soup.select('p.mt12')
	# descript_new =  re.sub(r'[\n\r\t\s]',"",descript[0].get_text())  #获取描述
	title = soup.select('div.houseList > dl > dd > p.title > a') #获取标题
	for tle,des,jz_mj,zP,dP in zip(title,descript,jz_area,zPrice,dPrice):
		info['title'].append(tle.get_text())
		info['descript'].append(re.sub(r'[\n\r\t\s]',"",des.get_text()))
		info['jz_area'].append(jz_mj.get_text())
		info['zPrice'].append(zP.get_text())
		info['dPrice'].append(dP.get_text())
	for i,j in enumerate(adress):
		if i%2 == 0:
			info['adress'].append(j.get_text())
	for i,j in enumerate(xiaoqu):
		if i%2 == 0:
			info['xiaoqu'].append(j.get_text())
#     print(info)
	df = pd.DataFrame(data=info)
	return df

def choiceItem(list,list_name):
	for k, j in enumerate(list,list_name):  # k代表索引值
		html_qy = requests.get(j, headers=header)
		soup = BeautifulSoup(html_qy.text, 'lxml')
		P = soup.select('span.fy_text')
		P_new = int(P[0].get_text().split('/')[-1])
		if P_new != 100:
			# list.pop(k)
			# list_name.pop(k)
			data = []
			for i in range(1, P_new + 1):
				a = 'i3%s/' % i
				url = j + a
				print(url)
				try:
					info = getSource(url)
				except ValueError:
					print(url + '这个链接有问题')
				data.append(info)
			result = pd.concat(data)
			j_name = list_name[k]
			result.to_csv(j_name + '.csv')
		else:
			href = soup.select('p#shangQuancontain > a')
			href_name = [list_name[k]+i.get_text() for i in href][1:]
			href_new = [URL + i.get('href') for i in href][1:]
			choiceItem(href_new,href_name)
	return list,list_name


# print(quyu)
quyu.pop(-2) #删掉
# print(quyu)
fenqu_sum = []
fenqu_sum_name=[]


for k,j in enumerate(quyu): #k代表索引值
	# print(j)
	html_q = requests.get(j,headers= header)
	# print(html_q.text)
	soup = BeautifulSoup(html_q.text, 'lxml')
	href = soup.select('p#shangQuancontain > a')
	href_name = [i.get_text() for i in href][1:]
	href_new = [URL+i.get('href') for i in href][1:]
	fenqu_sum.extend(href_new)
	fenqu_sum_name.extend(href_name)

for k,j in enumerate(fenqu_sum): #k代表索引值
	html_qy = requests.get(j,headers= header)
	soup = BeautifulSoup(html_qy.text, 'lxml')
	P = soup.select('span.fy_text')
	P_new = int(P[0].get_text().split('/')[-1])
	if P_new !=100:
		fenqu_sum.pop(k)
		fenqu_sum_name.pop(k)
		data = []
		for i in range(1,P_new+1):
			a = 'i3%s/'%i
			url = j+a
			# print(a)
			# print(url)
			try:
				info = getSource(url)
			except ValueError:
				print(url+'这个链接有问题')
			data.append(info)
		result = pd.concat(data)
		j_name =  fenqu_sum_name[k]
		result.to_csv(j_name+'.csv')

a = 'd2150/'
b= 'c2150-d2200/'
c= 'c2200-d2250/'
d = 'c2250-d2300/'
e = 'c2300-d2400/'
f = 'c2400-d2500/'
g = 'c2500-d2800/'
h ='c28000-d21000/'
qy_q_price = []
for i in fenqu_sum:
	qy_q_price.append(i + a)
	qy_q_price.append(i + b)
	qy_q_price.append(i + c)
	qy_q_price.append(i + d)
	qy_q_price.append(i + e)
	qy_q_price.append(i + f)
	qy_q_price.append(i + g)
	qy_q_price.append(i + h)
qy_q_price_name = []
for i in fenqu_sum_name:
	qy_q_price_name.append(i+a)
	qy_q_price_name.append(i + b)
	qy_q_price_name.append(i + c)
	qy_q_price_name.append(i + d)
	qy_q_price_name.append(i + e)
	qy_q_price_name.append(i + f)
	qy_q_price_name.append(i + g)
	qy_q_price_name.append(i + h)


for k,j in enumerate(qy_q_price): #k代表索引值
	html_qy = requests.get(j,headers= header)
	soup = BeautifulSoup(html_qy.text, 'lxml')
	P = soup.select('span.fy_text')
	P_new = int(P[0].get_text().split('/')[-1])
	if P_new !=100:
		qy_q_price.pop(k)
		qy_q_price_name.pop(k)
		data = []
		for i in range(1,P_new+1):
			a = 'i3%s/'%i
			url = j+a
			print(url)
			try:
				info = getSource(url)
			except ValueError:
				print(url+'这个链接有问题')
			data.append(info)
		result = pd.concat(data)
		j_name =  qy_q_price_name[k]
		result.to_csv(j_name+'.csv')