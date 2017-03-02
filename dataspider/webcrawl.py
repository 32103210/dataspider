# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 07:40:28 2017

@author: annie
"""

import requests
from bs4 import BeautifulSoup
import value
import copy

class getinfo():
#    def __init__(self,name='initsettings'):
#        URL,header,findcont=value.initset(name)
#        for i in URL:
#            htmlcontent=self.htmlback(i,header,'gbk')
#            self.htmlcont=copy.copy(htmlcontent)
#            self.soupback(self.htmlcont,findcont)
#        for x,y in zip(URL,header):
#            htmlcontent=self.htmlback(x,y,'gbk')
#            self.htmlcont=copy.copy(htmlcontent)
##            self.soupback(self.htmlcont)
#            print(self.urlgroupback(self.htmlcont,'href'))
    def initsettings(self,name):
        URL,header,findcont=value.initset(name)

    def htmlback(self,URL,header,encode):
        html = requests.get(URL,header,timeout=30)
        html.encoding = encode
#        print(html.text)
        return html.text
    
#    def findposition(self,*conttype):
#        element=[]
#        for i in conttype:
#            print(i)
#            a=i[0]
#            b=i[1]
#            element.append((a,b))
#        print(element)
#        return element
    
    def soupback(self,htmlcont,*conttype):#findcont传入
        soup = BeautifulSoup(htmlcont,'lxml')
#        self.findposition(name)
        soupinfo={}
        for i in range(len(conttype)):
            soupinfo[conttype[i][0]]=soup.select(conttype[i][1])
        print(soupinfo)
        return soupinfo
       
#    def urlgroupback(self,urlcont,title,name):
#        urls=self.soupback(urlcont,name)
#        urlgroup=[]
#        for i in urls.keys():
#            for j in urls[i]:
#                urlgroup.append('http://zu.gz.fang.com'+ j.get(title))#####改url
#        return urlgroup
    
    def infoback(self,infocont,title):
        infos=self.soupback(infocont)
        infogroup=[]
        for i in infos.keys():
            for j in infos[i]:               
                infogroup.append(j.get_text())
        return infogroup
    
#if __name__ == '__main__':
#    f=getinfo()