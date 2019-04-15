#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:15:29 2019

@author: s1881079
"""

import pandas as pd
import urllib.request as re

def genGsvUrl(dict_info):
    template = 'https://maps.googleapis.com/maps/api/streetview?size={insize}&location={inlat},{inlon}&fov={infov}&heading={inhead}&pitch={inpitch}&key={key}'
    return template.format(**dict_info)
    
    
    
def csvInfoToDict(dt_frame):
    str_key = 'AIzaSyC8cvzlqA7P5-S12LpgECrg_0nYpmAMiTw'
    #key deleted
    rst = []
    str_size = '640x640'
    for ind,rc in dt_frame.iterrows():
        rst.append({'insize':str_size,'inlat':rc.lat,'inlon':rc.lon,'infov':rc.fov,'inhead':rc.heading,'inpitch':rc.url_pitch,'key':str_key})
        
    return rst
    
    
def saveImg(lst_url,str_id = 0):
    img_id = str_id
    for gsv_url in lst_url:
        re.urlretrieve(gsv_url,str(img_id) + '.jpg')
        img_id += 1

if __name__ == "__main__":
    filename = 'gsv_info.csv'
    data = pd.read_csv(filename)
    list_all = csvInfoToDict(data)
    list_url = []
    
    #print url
    for info in list_all:
        url = genGsvUrl(info)
        list_url.append(url)
        print(url)
    
    #to save quota,only use after make sure
    #saveImg(list_url)
    
    #test_url = 'https://maps.googleapis.com/maps/api/streetview?size=640x640&location=53.46799905,-2.22865136&fov=90.0&heading=77.19966767&pitch=7.16930574&key=AIzaSyC8cvzlqA7P5-S12LpgECrg_0nYpmAMiTw'
    #re.urlretrieve(test_url,'test.jpg')