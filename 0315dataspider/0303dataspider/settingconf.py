# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 10:20:52 2017

@author: annie
"""

import configparser
import re


def configback(sectionname,settingname):
    """
    读取配置文件
    :param sectionname: 字符串
    :param settingname:字符串
    :return:
    """
    f=configparser.ConfigParser()
    f.read('settings.conf')
    _setting=f.get(sectionname,settingname)
    setting=re.split(',',_setting.replace('\n', ''))
    return setting


def configadd(sectionname,settingname,value):
    """
    增加配置文件
    :param sectionname: 字符串
    :param settingname: 字符串
    :param value: 列表
    :return:
    """
    f=configparser.ConfigParser()
    f.read('settings.conf')
    if sectionname in f.sections():#如果配置项已存在，则删除重写，避免重复
        if settingname in f.items(sectionname):
            f.remove_option(sectionname,settingname)
        f.set(sectionname,settingname,value)
    else:        
        f.add_section(sectionname)
        f.set(sectionname,settingname,value)
    f.write(open('settings.conf','w'))


#configadd('xfsettings','URL',"new-$r")
    

