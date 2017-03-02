# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import time
import random
import copy
from webcrawl import getinfo as wc
    
#class getinfo():
##    def __init__(self):
##        for x,y in zip(URL,header):
##            htmlcontent=self.htmlback(x,y,'gbk')
##            self.htmlcont=copy.copy(htmlcontent)
###            self.soupback(self.htmlcont)
##            print(self.urlgroupback(self.htmlcont,'href'))
#
#    def htmlback(self,URL,header,encode):
#        html = requests.get(URL,header,timeout=30)
#        html.encoding = encode
#        return html.text
#    
#    def findposition(self,name):
#        element=[]
#        for i in name:
#            a=i
#            b=crawlcont[i][0]
#            try:
#                c=crawlcont[i][1]
#            except:
#                c=0
#            try:
#                d=crawlcont[i][2]
#            except:
#                d=None
#            element.append((a,b,c,d))
#        print(element)
#        return element
#    
#    def soupback(self,content,name):
#        soup = BeautifulSoup(content,'lxml')
#        self.findposition(name)
#        soupinfo={}
#        #     name,x,y=findposition('qy','div.search-listbox > dl:nth-of-type(1) > dd > a',1)
#        for i in self.findposition(name):         
#            soupinfo[i[0]]=soup.select(i[1])[i[2]:i[3]]
#        return soupinfo
#       
#    def urlgroupback(self,urlcont,title,name):
#        urls=self.soupback(urlcont,name)
#        urlgroup=[]
#        for i in urls.keys():
#            for j in urls[i]:
#                urlgroup.append('http://zu.gz.fang.com'+ j.get(title))#####改url
#        return urlgroup
#    
#    def infoback(self,infocont,title):
#        infos=self.soupback(infocont)
#        infogroup=[]
#        for i in infos.keys():
#            for j in infos[i]:               
#                infogroup.append(j.get_text())
#        return infogroup
        
# 单个页面的所有房源节点

#def getInform(url, quYuNanme):
#    info = defaultdict(list)
#    print("conncecting website")
#    try:
#        html = requests.get(url,headers= header,timeout = 30)
#    except:
#        raise ValueError
#        return
#    html.encoding = 'gbk'
#    time.sleep(random.randint(2, 6))
#    print("progress webpages")
#    soup = BeautifulSoup(html.text, 'lxml')
#    zf_type = soup.select('p.font16.mt20.bold') #合租类型 整租or 合租 or 日租周租
#    title = soup.select('div.houseList > dl > dd > p:nth-of-type(1) > a') #房源描述，也是标题
#    price = soup.select('span.price')  #租房价格
#    location = soup.select('p.gray6.mt20 > a:nth-of-type(2) > span')      #只选取页面中三个信息中最后一个

    

class FTX(wc):
    def __init__(self):
        for x,y in zip(URL,header):
            print(x,y)
            htmlcontent=self.htmlback(x,y,'gbk')
#            print(htmlcontent)
            self.htmlcont=copy.copy(htmlcontent)
            urlgroup=self.urlgroupback(self.htmlcont,'href',['qy'])#细分url
            for i in urlgroup[:2]:
                print(i)
                time.sleep(random.randint(2, 6))
                xf=self.htmlback(i,header[0],'gbk')
    #            print(xf)
                self.xfcont=copy.copy(xf)
                self.soupback(self.xfcont,['zf_type','title','price','location'])
    #                soupcont=self.soupback
        print(self.soupback(self.xfcont,['zf_type','title','price','location']))
#        self.infoback()
            
    def infoback(self,name):
        info = defaultdict(list)
        for i in name:
            info[i].append()
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


##计算页面总数
#def count_Num(txt):
#    txtList =list(txt)
#    length = txtList.__len__()
#    if length == 3:
#        return int(txtList[1])
#    elif length == 4:
#        return int(txtList[1])*10+int(txtList[2])
#    else:
#        return 100
#
#pop_K = 1
#while(pop_K < 13):
#    xf_quyu.pop(0)
#    xf_quyu_name.pop(0)
#    pop_K+=1
#
#for k,j in enumerate(xf_quyu):   # k是索引值 可要可不要
##    html_q = requests.get(j,headers= header,timeout = 30)
##    html.encoding = 'gbk'
##    soup =BeautifulSoup(html_q.text, 'lxml')
#    P = soup.select('span.txt')
#    # print(len(P))
#    txt = P[0].get_text()
#    # print(P[0].get_text())
#    P_Num = count_Num(txt)
#    # print (P_Num)
#    if P_Num != 100:
#        data = []
#        for i in range(1,P_Num+1):
#            a = 'i3%s/'%i
#            url= j + a
#            print(url)
#            try:
#                info = getInform(url,xf_quyu_name[k])
#                print("info is already")
#            except ValueError:
#                print(url + '这个链接有问题')
#                f = open("log.txt", "a+")
#                f.writelines(url + "这个链接有问题")
#                f.close()
#            data.append(info)
#        result = pd.concat(data)
#        j_name = xf_quyu_name[k]
#        result.to_csv(j_name + '.csv')
#    else:
#        print (url + "需要进一步细分")
#        f= open("log.txt","a+")
#        f.writelines(url + "需要进一步细分")
#        f.close()


if __name__ == '__main__':
    f=FTX()
    



























