# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import time
import random

x =0
URL = 'http://zu.gz.fang.com'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
print ("connectiong website>>>>>>>>>>>")
html = requests.get(URL,headers = header,timeout = 30)
html.encoding = 'gbk'
print ("received web pages %s/" % x)
x +=1
soup = BeautifulSoup(html.text,'lxml')
html.encoding = 'gbk'
qx = soup.select('div.search-listbox > dl:nth-of-type(1) > dd > a')[1:]
quyu = []
quyu_name =[]
for i in qx:
    quyu.append(URL + i.get('href'))
    quyu_name.append(i.get_text())

count = 0
xf_quyu = []
xf_quyu_name = []
for i in quyu:
    print ("connectiong website  xf_quyu>>>>>>>>>>>")
    html = requests.get(i,headers = header,timeout = 30)
    html.encoding = 'gbk'
    time.sleep(random.randint(2,6))
    x += 1
    print ("received web pages %s/" % x)
    soup = BeautifulSoup(html.text,'lxml')
    xf = soup.select("div.quYu > a")[1:]
    for j in xf:
        xf_quyu.append(URL+j.get('href'))
        xf_quyu_name.append(quyu_name[count] + j.get_text())
    count+=1
# print(xf_quyu)   #细分过后的区域链接
# print(xf_quyu_name)   #细分后区域的名称

# 单个页面的所有房源节点
def getInform(url, quYuNanme):
    info = defaultdict(list)
    print("conncecting website")
    try:
        html = requests.get(url,headers= header,timeout = 30)
    except:
        raise ValueError
        return
    html.encoding = 'gbk'
    time.sleep(random.randint(2, 6))
    print("progress webpages")
    soup = BeautifulSoup(html.text, 'lxml')
    zf_type = soup.select('p.font16.mt20.bold') #合租类型 整租or 合租 or 日租周租
    title = soup.select('div.houseList > dl > dd > p:nth-of-type(1) > a') #房源描述，也是标题
    price = soup.select('span.price')  #租房价格
    location = soup.select('p.gray6.mt20 > a:nth-of-type(2) > span')      #只选取页面中三个信息中最后一个

    for zfType,tle, Price,Loc  in  zip(zf_type, title, price, location):
        info['zf_type'].append(zfType.get_text().split('|')[0])
        info['title'].append(tle.get_text())
        info['fy_type'].append(zfType.get_text().split('|')[1])
        info['jz_area'].append(zfType.get_text().split('|')[2])
        info['fy_height'].append(zfType.get_text().split('|')[3])
        info['price'].append(Price.get_text())
        info['location'].append(quYuNanme +Loc.get_text())
    df = pd.DataFrame(data=info)
    return df

#计算页面总数
def count_Num(txt):
    txtList =list(txt)
    length = txtList.__len__()
    if length == 3:
        return int(txtList[1])
    elif length == 4:
        return int(txtList[1])*10+int(txtList[2])
    else:
        return 100

pop_K = 1
while(pop_K < 13):
    xf_quyu.pop(0)
    xf_quyu_name.pop(0)
    pop_K+=1

for k,j in enumerate(xf_quyu):   # k是索引值 可要可不要
    html_q = requests.get(j,headers= header,timeout = 30)
    html.encoding = 'gbk'
    soup =BeautifulSoup(html_q.text, 'lxml')
    P = soup.select('span.txt')
    # print(len(P))
    txt = P[0].get_text()
    # print(P[0].get_text())
    P_Num = count_Num(txt)
    # print (P_Num)
    if P_Num != 100:
        data = []
        for i in range(1,P_Num+1):
            a = 'i3%s/'%i
            url= j + a
            print(url)
            try:
                info = getInform(url,xf_quyu_name[k])
                print("info is already")
            except ValueError:
                print(url + '这个链接有问题')
                f = open("log.txt", "a+")
                f.writelines(url + "这个链接有问题")
                f.close()
            data.append(info)
        result = pd.concat(data)
        j_name = xf_quyu_name[k]
        result.to_csv(j_name + '.csv')
    else:
        print (url + "需要进一步细分")
        f= open("log.txt","a+")
        f.writelines(url + "需要进一步细分")
        f.close()




























