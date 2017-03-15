# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os

def httpRequest(url,header):
    try:
        html = requests.get(url, headers=header, timeout=30)
        # html.encoding = ''
        time.sleep(4)
    except:
        print("请求超时")
        html = None
    return html


def TableDataProcess(text, name):
    # 定义了一个100*100的二维数组
    rows = 100
    cols = 100
    matrix = [[None] * cols for i in range(rows)]
    title = text.select('#bttab  > tr')
    tab_tr = text.select('#maintab > tr')
    num = len(tab_tr)
    col = 0  # 列数
    for i in range(num + 3):
        if i == 0:
            matrix[i][0] = name
            continue
        if len(title) == 3 and i == 1:
            unit = BeautifulSoup(str(title[2]), 'lxml')
            unit_text = unit.select('td')[0]
            matrix[i][0] = unit_text.get_text()
            continue
        # 将表头的出来和表主体的处理合在一起了
        else:
            if i >= len(tab_tr)+2:
                break
            tr_soup = BeautifulSoup(str(tab_tr[i - 2]), 'lxml')
            tdList = tr_soup.select('td')
            # print(tdList)
            for k, j in enumerate(tdList):
                if matrix[i][k] != None:
                    continue
                if k ==4:
                    col = len(tdList)
                rowspan = 0
                colspan = 0
                # print(j.get('rowspan'))
                if j.get('rowspan') != None:
                    rowspan = int(j.get('rowspan'))
                    # print(rowspan)
                if j.get('colspan') != None:
                    colspan = int(j.get('colspan'))
                # print(j.get_text())
                for index in range(rowspan+1):
                    matrix[i + index][k] = j.get_text()
                for index in range(colspan+1):
                    matrix[i][k + index] = j.get_text()
    result = pd.DataFrame(matrix)
    return result



# 目录地址的url 包含不同年份的统计年鉴
url = "http://data.gzstats.gov.cn/gzStat1/yearqueryAction.do?method=search&title=%E7%BB%9F%E8%AE%A1%E5%B9%B4%E9%89%B4&lmId=01"

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

html = httpRequest(url, header)

# print(html.text)

soup  = BeautifulSoup(html.text,'lxml')

# nj = soup.select('form[name="yearqueryForm"] > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > a')
find = soup.select('a')
# print(len(find))
flId = []
flname = []
title = []
fbDate = []
falg = []
year = []

for i in find:
    seeReport = i.get('onclick')  # 格式为  seeReport('241','年鉴报表','2016-12-06','统计年鉴2016','1','2016');
    # print(i.get('onclick'))
    data = re.split("','|\('|'\);", seeReport)
    flId.append(data[1])
    flname.append(data[2])
    title.append(data[3])
    fbDate.append(data[4])
    falg.append(data[5])
    year.append(data[6])

    #下面筛选有效信息
    # http: // data.gzstats.gov.cn / gzStat1 / yearqueryAction.do?method = det_Title & flId = 241 & flname = % E5 % B9 % B4 % E9 % 89 % B4 % E6 % 8
    # A % A5 % E8 % A1 % A8 & title = % E7 % BB % 9
    # F % E8 % AE % A1 % E5 % B9 % B4 % E9 % 89 % B42016 & fbDate = 2016 - 12 - 06 & falg = 1 & year = 2016

for k in range(len(find)):
    #构造统计年鉴子页面url
    url_nj ="http://data.gzstats.gov.cn/gzStat1/yearqueryAction.do?method=det_Title&flId=%s&flname=%s&title=%s&fbDate=%s&falg=%s&year=%s"%(flId[k],flname[k],title[k],fbDate[k],falg[k],year[k])
    print(url_nj)
    dirpath = 'E:\oubin\GZdata\%s' % fbDate[k]
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    try:
        nj_html = httpRequest(url_nj, header)
    except:
        print(url_nj+ "页面超时")
    if nj_html == None:
        continue
    nj_text = BeautifulSoup(nj_html.text, 'lxml')
    findtitle = nj_text.select('a')
    # [<a onclick="selectDlist('64864','TJ_RPT_400165139747601058','1-1  行政区划','2016-12-06/第一篇、综合','5140');">
    FID = []
    RPTID = []
    RPTNAME = []
    FLTITLE = []


    for j in findtitle:
        selectDlist = j.get('onclick')  # 格式为 selectDlist('64864','TJ_RPT_400165139747601058','1-1  行政区划','2016-12-06/第一篇、综合','5140')
        # http: // data.gzstats.gov.cn / gzStat1 / yearqueryAction.do?method = displayRpt & ACTFLAG = 3 & FID = 59801 &
        # RPTID = TJ_RPT_400165139747601058 & RPTNAME = 1 - 1 % 20 % 20 % D0 % D0 % D5 % FE % C7 % F8 % BB % AE
        # & FLTITLE = 2015 - 12 - 23 / % B5 % DA % D2 % BB % C6 % AA % A1 % A2 % D7 % DB % BA % CF
        data = re.split("','|\('|'\);", selectDlist)
        FID.append(data[1])
        RPTID.append(data[2])
        RPTNAME.append(data[3])
        FLTITLE.append(data[4])


    for fid, rptid, rptname, fltitle in zip(FID, RPTID, RPTNAME, FLTITLE):
        url_table = "http://data.gzstats.gov.cn/gzStat1/yearqueryAction.do?method=displayRpt&ACTFLAG=3&FID=%s&RPTID=%s&RPTNAME=%s&FLTITLE=%s" % (fid, rptid, rptname, fltitle)
        try:
            csvPath = 'E:\oubin\GZdata\%s\%s.csv' % (fbDate[k], rptname)
            if os.path.exists(csvPath):
                continue
            html_table = httpRequest(url_table, header)
            table_text = BeautifulSoup(html_table.text, 'lxml')
            tableData = TableDataProcess(table_text, name=rptname)

            tableData.to_csv(path_or_buf=csvPath)
        except:
            print(url_table + "请求超时")








