# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd
from collections import defaultdict

global count
count = 0

key = ["AIzaSyCNkp6KJ1Pvla6Pp0AS-OE7Uvr6fLGfzxs", "	AIzaSyBG3-oxX3G7LUnA2mQ64X2jFETFrPcqWgE","AIzaSyBKv_iI-S-y5h5z5xNxjMWkc3Xc0XigHyI","AIzaSyCb8S_NGnGppPJrbRaN-PmA67zm0c8lzrs"]

def removeBom(file):
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s == BOM else False

    f = open(file, 'rb')
    if existBom(f.read(3)):
        fbody = f.read()
        # f.close()
        with open(file, 'wb') as f:
            f.write(fbody)
            print("转化成功")

def getLocation(addre):
    global count
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

    if((count//2500) <= len(key)):
        k = count//2500
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s ' % (j, key[k])

        html = requests.get(url, headers=header)
        count += 1
        ##############################################
        re_lat = "(?<=\"lat\"\s:\s).+?(?=,)"
        re_lng = "(?<=\"lng\"\s:\s).+?(?=\s)"
        pattern1 = re.compile(re_lat)
        pattern2 = re.compile(re_lng)           # 这里其实可以优化一下
        try:
            lat = re.findall(pattern1, html.text)[0]
            lng = re.findall(pattern2, html.text)[0]
            result = [lat, lng]
        except IndexError:
            result = ['None','None']
        finally:
            print(result)
            return result

file_name_list =['白云金沙洲北', '白云罗冲围', '白云龙归', '天河天河公园', '番禺市桥北', '天河天河南', '天河体育中心','天河车陂', '天河岑村', '天河东站', '天河东圃', '天河东莞庄', '天河岗顶', '天河华景新城社区', '天河汇景新城社区', '天河黄村', '天河科韵路', '天河龙洞', '天河龙口西', '天河龙口东', '天河沙河', '天河沙太南', '天河石牌桥', '天河上社', '天河天河北', '天河体育西', '天河天润路', '天河棠下', '天河天河客运站', '天河五山', '天河五山路口', '天河员村', '天河粤垦', '天河员村四横路', '天河员村二横路', '天河燕塘', '天河珠江新城西', '天河珠江新城中', '天河珠江新城东', '海珠宝岗', '海珠滨江东', '海珠滨江西', '海珠滨江中', '海珠昌岗路', '海珠赤岗', '海珠东晓南', '海珠工业大道北', '海珠工业大道南', '海珠广州大道南', '海珠江南大道', '海珠江南西', '海珠江燕路', '海珠客村', '海珠沥滘', '海珠鹭江', '海珠南洲', '海珠琶洲', '海珠前进路', '海珠万胜围', '海珠新港西', '海珠下渡路', '海珠中大', '白云白云大道北', '白云白云大道南', '白云广花路', '白云桂花岗', '白云广园路', '白云广州大道北', '白云黄石', '白云黄边', '白云机场路', '白云梅花园', '白云南湖', '白云人和', '白云三元里', '白云石井', '白云同和', '白云同德围', '白云新市', '越秀北京路', '越秀大沙头', '越秀东川路', '越秀东风东', '越秀东山', '越秀二沙岛', '越秀共和路', '越秀环市东', '越秀海珠广场', '越秀黄花岗', '越秀建设路', '越秀解放北', '越秀解放南', '越秀麓景路', '越秀农讲所', '越秀盘福路', '越秀水荫路', '越秀淘金', '越秀五羊新城', '越秀小北', '越秀西门口', '越秀杨箕', '番禺大石', '番禺大学城', '番禺广州雅居乐', '番禺华南', '番禺华南碧桂园社区', '番禺金山谷', '番禺洛溪', '番禺南浦', '番禺祈福', '番禺祈福新区', '番禺祈福中区', '番禺沙湾',  '番禺市桥南', '番禺市桥西', '番禺顺德碧桂园社区', '番禺石楼', '番禺星河湾社区', '番禺厦滘', '番禺亚运城', '番禺钟村', '荔湾陈家祠', '荔湾东风西', '荔湾芳村', '荔湾环市西', '荔湾黄岐', '荔湾黄沙', '荔湾花地湾', '荔湾窖口', '荔湾坑口', '荔湾流花', '荔湾南岸路', '荔湾桥中', '荔湾西关', '荔湾西村', '荔湾盐步', '荔湾中山八', '花都花山', '花都花东', '花都旧区', '花都建设北', '花都镜湖大道', '花都美林湖', '花都狮岭', '花都山前大道', '花都铁路西', '花都炭步', '花都新区', '黄埔大沙地', '黄埔丰乐路', '黄埔开发东区', '黄埔开发西区', '黄埔开创大道', '黄埔萝岗', '黄埔文冲', '增城凤凰城', '增城广园东', '增城挂绿新城', '增城荔城大道北', '增城荔城大道南', '增城新塘南', '增城新塘北', '增城增江', '增城中新', '南沙大岗', '南沙旧镇', '南沙金洲', '从化从化郊区', '从化街口中心区', '从化江埔街', '从化太平镇', '从化温泉镇', '广州周边东莞', '广州周边佛山', '广州周边清远', '广州周边其他', '广州周边中山', '广州周边肇庆']

for i in file_name_list:
    if count >2500*len(key):
        break
    location_set = set()
    info = defaultdict(list)
    loc = []
    fileNameComplete = i + ".csv"
    try:
        print (fileNameComplete)
        try:
            removeBom(fileNameComplete)
            data = pd.read_csv(fileNameComplete, encoding= "utf-8")
            data = pd.DataFrame(data)
            # print (data)
            loc = data['location']
            for j in loc:
                # print(j)
                temp = getLocation(j)
                info['lat'].append(temp[0])
                info['lng'].append(temp[1])
                # print(temp)
            # print(info)
            temp_tab = pd.DataFrame(info)
            # print(temp_tab)
            result = pd.concat([data,temp_tab],axis=1)
            # print (result)
            type(result)
            result.to_csv("E:\oubin\crawler\data\%s"% fileNameComplete)
        except UnicodeDecodeError:
            print(fileNameComplete + "have unicodeDecodeError problem")
            continue
    except IOError:
        print ( fileNameComplete + "this is not utf-8 without BOM")
        f = open("log.txt", "a+")
        f.writelines(fileNameComplete + "this is not utf-8 without BOM" + "\r\n")
        f.close()














