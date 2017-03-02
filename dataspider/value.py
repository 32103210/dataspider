# -*- coding:utf-8 -*-
import pickle
import dump

URL=('http://zu.gz.fang.com',
     )
header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

name=('zf_type',
           'title',
            'price',
           'location',
      
      )
 
#('div.search-listbox > dl:nth-of-type(1) > dd > a'),
path=(
         ('p.font16.mt20.bold'),
         ( 'div.houseList > dl > dd > p:nth-of-type(1) > a'),
         ('span.price'),
         ('p.gray6.mt20 > a:nth-of-type(2) > span'),
         
    )

f1=open('asd.txt','wb')
pickle.dump(URL,f1,True)
pickle.dump(header,f1,True)
pickle.dump(name,f1,True)
pickle.dump(path,f1,True)
f1.close()

def initset(name):
    f2=open((name+'.txt'),'rb')
    a=pickle.load(f2)
    b=pickle.load(f2)
    c=pickle.load(f2)
    d=pickle.load(f2)
    findcont=[]
    for i,j in zip(c,d):
        findcont.append((i,j))

    return a,b,findcont
    
initset('initsettings')