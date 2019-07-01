#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:41:29 2019

@author: s1881079
"""

import re
import pyproj
import urllib.request as req

from .gsv import GSV

__all__ = ['downloadGSV','csvParaToLstObj','ggeUrlToLstObj','genLstDlUrl','downloadImgFromLst','genImgFnList','genCamlocFromTxt','setSeqFn']

def downloadGSV(gge_url,img_folder,key,fix_std = False):
    
    lst_gsv = ggeUrlToLstObj(gge_url,fix_std)
    #num_img = len(lst_gsv)
    
#    #downloading GSV images - COMMAND THIS PART WHEN SECOND TEST
    lst_dlurl = genLstDlUrl(lst_gsv,key)
    downloadImgFromLst(lst_dlurl,img_folder)
    
    setSeqFn(lst_gsv)
    
    return lst_gsv

def csvParaToLstObj(csv_fname):
    '''
    from a standart csv file specifying parameters to gsv object list
    '''
    
    inf = open(csv_fname,'r')
    head = inf.readline()[:-1]
    
    if len(head.split(',')) != 7:
        print('wrong number of colums, check the input file format')
        return None
        
    lines = inf.readlines()
    inf.close()
    
    rst = []
    
    for line in lines:
        paras = line[:-1].split(',')
        img_id = int(paras[0])
        lat = float(paras[1])
        lon = float(paras[2])
        alt = float(paras[3])
        fov = float(paras[4])
        heading = float(paras[5])
        tilt = float(paras[6])
        gsv = GSV([img_id,lat,lon,alt,fov,heading,tilt])
        rst.append(gsv)
        
    return rst
        


def ggeUrlToLstObj(txt_fname,fix_std):
    '''
    from a txt file containing google earth urls to list of GSVImg objects
    fix_std: fix the tilt to 0 and fov to 60
    '''
    
    with open(txt_fname,'r') as inf:
        urls = inf.readlines()
        
    inf.close()
    rst = []
    img_id = 0
    
    for url in urls:
        #print(url)
        paras = re.search('\@(.*),',url).group()[1:-1].split(',')
        lat = float(paras[0])
        lon = float(paras[1])
        alt = float(paras[2][:-1])
        fov = float(paras[4][:-1])
        heading = float(paras[5][:-1])
        tilt = float(paras[6][:-1])
        if fix_std:
            fov = 60
            tilt = 90
        gsv = GSV([img_id,lat,lon,alt,fov,heading,tilt])
        rst.append(gsv)
        img_id += 1
    
    return rst      
    
def genLstDlUrl(lst_gsv,key,sec = ''):
    '''
    from a list of gsv objects to list of ready-to download urls
    '''
    lst_dlurl = []
    for gsv in lst_gsv:
        base_url = gsv.genBaseGsvUrl()
        config_url = base_url + '&key=' + key
        #sign_url = su.sign_url(config_url,sec)
        #if not signed
        sign_url = config_url
        lst_dlurl.append(sign_url)
    return lst_dlurl

def downloadImgFromLst(lst_dlurl,img_folder):
    '''
    download google street view images from a list of urls, storing in specified folder
    '''
    #if the process starts from downloading images, the filename would be numbers start from 0
    
    img_id = 0
    for url in lst_dlurl:
        req.urlretrieve(url,img_folder + str(img_id) + '.jpg')
        img_id += 1
    
def genImgFnList(img_folder,all_fn):
    '''
    generate image filename list in folder specified
    '''
    lst_img = []
    for fn in all_fn:
        if fn[-4:] == '.jpg':
            lst_img.append(img_folder + fn)
        
    return lst_img

def genCamlocFromTxt(txt_fn,csv_folder,csv_fn):
    '''
    generate campera location from txt of urls from gge, write as csv
    '''
    with open(txt_fn,'r') as inf:
        urls = inf.readlines()
        
    inf.close()
    loc_list = []
    loc_id = 0
    
    for url in urls:
        print(url)
        paras = re.search('\@(.*),',url).group()[1:-1].split(',')
        lat = float(paras[0])
        lon = float(paras[1])
        alt = float(paras[2][:-1])
        heading = float(paras[5][:-1])
        
        osgb36 = pyproj.Proj(init = 'epsg:27700')
        wgs84 = pyproj.Proj(init='epsg:4326')
        
        mapx,mapy = pyproj.transform(wgs84,osgb36,lon,lat)
        rec = [loc_id,lon,lat,alt,heading,mapx,mapy]
        
        if rec not in loc_list:
            loc_list.append(rec)
            loc_id += 1
        
    
    
    camloc_file = csv_folder + csv_fn
    with open(camloc_file, 'w') as wfile:
        headlist = ['camloc_id','lon','lat','alt','ori_heading','mapx','mapy']
        line = ','.join(headlist)
        wfile.write(line + '\n')
        for loc in loc_list:
            line = ','.join([str(i) for i in loc])
            wfile.write(line + '\n')
            
    wfile.close()
    
def setSeqFn(lst_gsv):
    for gsv in lst_gsv:
        gsv.setFn(gsv.id)
