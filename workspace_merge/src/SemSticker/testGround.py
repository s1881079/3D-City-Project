#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 12:43:50 2019

@author: s1881079
"""

import ImgPro as ip
import MtchBD as mb

from bdComps import SuspObj

from simg_process import *

import os


def downloadImgOnly(url_txt,img_folder,key_txt):
    '''
    download images only and preview with online api to see how the api work on them
    
    '''
    key = ip.gen_process.getExtInfo(key_txt)
    
    if os.path.exists(img_folder,) is False:
        os.makedirs(img_folder)
        
    lst_gsv = ip.downloadGSV(url_txt,img_folder,key)
    
    img_csv = 'test_camloc'
    ip.gen_process.writeObjInfoCsv(lst_gsv,img_folder,img_csv)
    
    
if __name__ == '__main__':
    url_txt = '../../data/gge_url/test_ggeurl.txt'
    img_folder = '../../intm_output/preview_imgs/'
    key_txt = '../../../locked/GSVdl_key.txt'
    
    downloadImgOnly(url_txt,img_folder,key_txt)
    