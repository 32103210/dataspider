# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 17:59:24 2017

@author: annie
"""

import pickle
import dump

URL=(
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