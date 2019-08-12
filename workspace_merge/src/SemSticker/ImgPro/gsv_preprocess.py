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

__all__ = ['downloadGSV','csvParaToLstGsv','urlTxtToLstGsv','genLstDlUrl','downloadImgFromLst','genImgFnList','setSeqFn']

def downloadGSV(lst_gsv,img_folder,key,fix_std = False):
    
    #lst_gsv = urlTxtToLstGsv(gge_url,fix_std)
    #num_img = len(lst_gsv)
    
#    #downloading GSV images - COMMAND THIS PART WHEN SECOND TEST
    lst_dlurl = genLstDlUrl(lst_gsv,key)
    downloadImgFromLst(lst_dlurl,img_folder)
    
    setSeqFn(lst_gsv)
    
    #return lst_gsv

def genGsvObj(gsv_folder,gsv_info_csv):
    return None

def csvParaToLstGsv(csv_fname):
    '''
    from a standart csv file specifying parameters to gsv object list
    '''
    
    inf = open(csv_fname,'r')
    head = inf.readline()[:-1]
    
    if len(head.split(',')) != 8:
        print('wrong number of colums, check the input file format')
        return None
        
    lines = inf.readlines()
    inf.close()
    
    rst = []
    
    for line in lines:
        paras = line[:-1].split(',')
        img_id = int(paras[0])
        fn = paras[1]
        lat = float(paras[2])
        lon = float(paras[3])
        alt = float(paras[4])
        fov = float(paras[5])
        heading = float(paras[6])
        pitch = float(paras[7])
        gsv = GSV([img_id,lat,lon,alt,fov,heading,pitch],inPitch = True)
        gsv.setFn(fn,withExt = True)
        rst.append(gsv)
        
    return rst
        


def urlTxtToLstGsv(txt_fname,fix_std = False):
    '''
    from a txt file containing google earth urls to list of GSVImg objects
    fix_std: fix the tilt to 0 and fov to 60
    '''
    
    with open(txt_fname,'r') as inf:
        urls = inf.readlines()
        
    inf.close()
    lst_gsv = []
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
        
        lst_gsv.append(gsv)
        img_id += 1
    
    setSeqFn(lst_gsv)
    
    return lst_gsv     
    
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


    
def setSeqFn(lst_gsv):
    for gsv in lst_gsv:
        gsv.setFn(gsv.id)
