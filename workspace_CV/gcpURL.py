#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:15:29 2019

@author: s1881079
"""

import pandas as pd
import urllib.request as re
import re
import sign_url as su

def genGsvUrl(dict_info):
    template = 'https://maps.googleapis.com/maps/api/streetview?size={insize}&location={inlat},{inlon}&fov={infov}&heading={inhead}&pitch={inpitch}&key={key}'
    return template.format(**dict_info)
    
    
    
def csvInfoToDict(dt_frame):
    '''
    read parameters of street view from csv - possible alternative way for this
    
    '''
    str_key = 'AIzaSyC8cvzlqA7P5-S12LpgECrg_0nYpmAMiTw'
    #key deleted
    rst = []
    str_size = '640x640'
    for ind,rc in dt_frame.iterrows():
        rst.append({'insize':str_size,'inlat':rc.lat,'inlon':rc.lon,'infov':rc.fov,'inhead':rc.heading,'inpitch':rc.url_pitch,'key':str_key})
        
    return rst
    
def txtUrlToDict(txt_fname):
    str_key = 'AIzaSyC8cvzlqA7P5-S12LpgECrg_0nYpmAMiTw'
    with open(txt_fname,'r') as inf:
        urls = inf.readlines()
        
    inf.close()
    rst = []
    str_size = '640x640'
    
    for url in urls:
        paras = re.search('\@(.*),',url)[1:-1].split(',')
        #heading for paras: lat lon alt unk fov heading tilt
        lat = float(paras[0])
        lon = float(paras[1])
        fov = float(paras[4][:-1])
        heading = float(paras[5][:-1])
        pitch = float(paras[6][:-1]) - 90
        rst.append({'insize':str_size,'inlat':lat,'inlon':lon,'infov':fov,'inhead':heading,'inpitch':pitch,'key':str_key})
    
    return rst    
    
def saveImgBatch(lst_url,str_id = 0):
    img_id = str_id
    for gsv_url in lst_url:
        sec = ''
        signed_url = su.sign_url(gsv_url,sec)
        
        re.urlretrieve(signed_url,'../imgs/' + str(img_id) + '.jpg')
        img_id += 1
        
def batchDownloadGSV(txt_fname):
    #txt_fn = 'gge_urls.txt'
    list_paras = txtUrlToDict(txt_fname)
    list_url = []
    
    #print url
    for para in list_paras:
        url = genGsvUrl(para)
        list_url.append(url)
        print(url)
        
    saveImgBatch(list_url)

#if __name__ == "__main__":
#    csv_fn = 'gsv_info.csv'
#    data = pd.read_csv(csv_fn)
#    list_all = csvInfoToDict(data)
#    list_url = []
#    
#    txt_fn = 'gge_urls.txt'
#    list_urls = txtUrlToDict(txt_fn)
#    
#    #print url
#    for info in list_all:
#        url = genGsvUrl(info)
#        list_url.append(url)
#        print(url)
#    
    #to save quota,only use after make sure
    #saveImgBatch(list_url)
    
    #test_url = 'https://maps.googleapis.com/maps/api/streetview?size=640x640&location=53.46799905,-2.22865136&fov=90.0&heading=77.19966767&pitch=7.16930574&key=AIzaSyC8cvzlqA7P5-S12LpgECrg_0nYpmAMiTw'
    #re.urlretrieve(test_url,'test.jpg')