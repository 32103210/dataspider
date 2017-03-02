# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 11:26:32 2017

@author: annie
"""

import pickle

def dumpin(name):
   f = open("%s"%name+'.txt', 'rb')
   pickle.load(f)
#   print(file)

#getelement('tmp')

def dumpout(name):
    f=open("%s"%name+'.txt', 'wb')
    pickle.dump(name, f)
    f.close()
    