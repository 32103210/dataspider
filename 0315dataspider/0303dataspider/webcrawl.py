# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 07:40:28 2017

@author: annie
"""

import requests
from bs4 import BeautifulSoup
import settingconf
import copy

class getinfo():
#    def __init__(self):
#        URL=self.initsettings('basicsettings','URL')
#        print(URL)
#        header=self.initsettings('basicsettings','header')
#        print(header)
#        encode=self.initsettings('basicsettings','encode')
#        contentname=self.initsettings('basicsettings','name')
#        contentpath=self.initsettings('basicsettings','path')
#        a=self.htmlback(URL,header,encode)
##        print(a)
#        self.soupback(a,contentname,contentpath)
        

    def initsettings(self,filename,settingname):
        """

        :param filename:
        :param settingname:
        :return: 返回URL,encode,header,name,path
        """
        return settingconf.configback(filename,settingname)
    
    def addsettings(self,sectionname,settingname,value):
        """

        :param sectionname:
        :param settingname:
        :param value:
        :return: 添加URL,encode,header,name,path
        """
        return settingconf.configadd(sectionname,settingname,value)
        

    def htmlback(self,URL,header,encode):
        """

        :param URL:
        :param header:
        :param encode:
        :return: 字典，格式为{URL1:HTML.text,URL1:HTML.text}
        """
        HTML={}
        for _URL,_header,_encode in zip(URL,header,encode):
            if _URL=='':
                break
            html = requests.get(_URL,_header,timeout=30)
            html.encoding = _encode
            HTML[_URL]=(copy.copy(html.text))#防止重复访问URL
        return HTML
    
    def soupback(self,htmlcontent,contentname,contentpath):
        """
        contentname要查找的内容，contentpath要查找的路径,均为列表
        :param htmlcontent: htmlback函数返回的html文档对象
        :param contentname: list对象包含要查询的标签信息名称
        :param contentpath: list对象包含要查寻的标签信息路径
        :return: 字典，格式为{URL1:{查找的内容：查找结果}，URL2:{查找的内容：查找结果}}
        """
        soupinfo={}
        for i in htmlcontent.keys():
            soup = BeautifulSoup(htmlcontent[i],'lxml')
            soupinfo[i]={}
            for _contentname,_contentpath in zip(contentname,contentpath):
                if _contentname=='' or _contentpath=='':
                    break
                soupinfo[i][_contentname]=soup.select(_contentpath)
        return soupinfo

#    def infoback(self,infocont,title):#这个方法暂时留着
#        infos=self.soupback(infocont)
#        infogroup=[]
#        for i in infos.keys():
#            for j in infos[i]:               
#                infogroup.append(j.get_text())
#        return infogroup
    
if __name__ == '__main__':
    f=getinfo()