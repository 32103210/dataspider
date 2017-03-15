# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import time
import random
import copy
from webcrawl import getinfo as wc#父类

class FTX(wc):
    def __init__(self):
        # rootURL = self.initsettings('basicsettings','rootURL')
        URL=self.initsettings('basicsettings','URL')
        header=self.initsettings('basicsettings','header')
        encode=self.initsettings('basicsettings','encode')
        contentname=self.initsettings('basicsettings','name')
        contentpath=self.initsettings('basicsettings','path')
        a=self.htmlback(URL,header,encode)
        qy=self.soupback(a,contentname,contentpath)#返回细分URL
        urlgroup=[]
        for i in qy.keys():#返回细分url
            for j in qy[i].keys():
                for m in qy[i][j]:
                    xf_url=m.get('href')
                    xf_name=m.get_text()
                    urlgroup.append((i+xf_url,xf_name))#urlgroup格式为[(区域url，区域名字)，(区域url，区域名字)]
        #重新开始爬细分URL，重新赋值        
        URL_xf=''
        header_xf=''
        encode_xf=''
        xfquyucontentname = ['xfname']
        xfquyucontenturl = ['div.quYu > a']

        for m,n in urlgroup[1:]:
            urltemp = [m]
            a=self.htmlback(urltemp, header, encode)
            realXF = self.soupback(a,xfquyucontentname,xfquyucontenturl)
            xfsouplist = realXF[m]['xfname']
            xfsouplist.pop(0)
            for index in xfsouplist:
                # URL_xf+=(m+',')
                URL_xf += (URL[0]+ index.get('href')+',')
                header_xf += (header[0] + ',')
                encode_xf += (encode[0] + ',')

        #把新配置加入settings.conf，细分区域section名字为‘xfsettings’，下面分别有‘URL’,‘header’，‘encode’，‘name’,'path'五个option
        self.addsettings('xfsettings','URL',URL_xf)
        self.addsettings('xfsettings','header',header_xf)
        self.addsettings('xfsettings','encode',encode_xf)
        self.addsettings('xfsettings','name','zf_type,title,price,location')
        self.addsettings('xfsettings','path','p.font16.mt20.bold,div.houseList > dl > dd > p:nth-of-type(1) > a,span.price,p.gray6.mt20 > a:nth-of-type(2) > span')
        #从settings.conf读取细分区域的配置
        URL=self.initsettings('xfsettings','URL')
        header=self.initsettings('xfsettings','header')        
        encode=self.initsettings('xfsettings','encode')
        contentname=self.initsettings('xfsettings','name')
        contentpath=self.initsettings('xfsettings','path')

        #开始实现翻页功能，发现一个问题 ，如果中断发生依旧没有办法实现断点开始查询
        page = ['pagenum']
        pagepath = ['span.txt']
        all_URL = []
        header_all = ''
        encode_all = ''
        for url in URL:
            urltemp = [url]
            a = self.htmlback(urltemp, header, encode)
            addPageURL = self.soupback(a, page, pagepath)
            print(addPageURL)
            txt = addPageURL[url]['pagenum'].get_text()
            pagenum = self.count_Num(txt)
            if pagenum != 100:
                for k in range(1,pagenum+1):
                    temp = 'i3%s/'% k
                    all_URL.append(url+ temp)  # 这里就得到了所有的查询URL
                    header_all += (header[0] + ',')
                    encode_all += (encode[0] + ',')

        # 把新配置加入settings.conf，细分区域section名字为‘xfsettings’，下面分别有‘URL’,‘header’，‘encode’，‘name’,'path'五个option
        self.addsettings('xfsettings', 'URL', all_URL)
        self.addsettings('xfsettings', 'header', header_all)
        self.addsettings('xfsettings', 'encode', encode_all)
        self.addsettings('xfsettings', 'name', 'zf_type,title,price,location')
        self.addsettings('xfsettings', 'path',
                         'p.font16.mt20.bold,div.houseList > dl > dd > p:nth-of-type(1) > a,span.price,p.gray6.mt20 > a:nth-of-type(2) > span')
        # 从settings.conf读取细分区域的配置
        URL = self.initsettings('xfsettings', 'URL')
        header = self.initsettings('xfsettings', 'header')
        encode = self.initsettings('xfsettings', 'encode')
        contentname = self.initsettings('xfsettings', 'name')
        contentpath = self.initsettings('xfsettings', 'path')

        #通过一个包含整个网络的url列表来爬取整个网站
        a=self.htmlback(URL,header,encode)
        info=self.soupback(a,contentname,contentpath)#返回结果格式{网址1：{查询名称1：[查询结果a1,查询结果b1],查询名称2：[查询结果a2,查询结果b2]}}
        crawlinfo={}
        #写正则，提取信息
        print(info.keys())
        for xf_name in info.keys():#细分url匹配地名
            print(xf_name)
            for m,n in urlgroup[1:]:
                if xf_name==m:
                    crawlinfo[n]={}
                    crawlinfo[n]['zf_type']=[]
                    crawlinfo[n]['title']=[]
                    crawlinfo[n]['fy_type']=[]
                    crawlinfo[n]['jz_area']=[]
                    crawlinfo[n]['fy_height']=[]
                    crawlinfo[n]['price']=[]
                    crawlinfo[n]['location']=[]
#                print(crawlinfo)
                    for zfType,tle, Price,Loc  in  zip(info[xf_name]['zf_type'], info[xf_name]['title'], info[xf_name]['price'], info[xf_name]['location']):
                        print(zfType,tle, Price,Loc)
                        crawlinfo[n]['zf_type'].append(zfType.get_text().split('|')[0])
                        crawlinfo[n]['title'].append(tle.get_text())
                        crawlinfo[n]['fy_type'].append(zfType.get_text().split('|')[1])
                        crawlinfo[n]['jz_area'].append(zfType.get_text().split('|')[2])
                        crawlinfo[n]['fy_height'].append(zfType.get_text().split('|')[3])
                        crawlinfo[n]['price'].append(Price.get_text())
                        crawlinfo[n]['location'].append(n+Loc.get_text())
                    break
                break
            
        print(crawlinfo)
        df=pd.DataFrame(info)

    # 计算页面总数
    def count_Num(txt):
        txtList = list(txt)
        length = txtList.__len__()
        if length == 3:
            return int(txtList[1])
        elif length == 4:
            return int(txtList[1]) * 10 + int(txtList[2])
        else:
            return 100

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
    



























