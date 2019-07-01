#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:18:27 2019

@author: s1881079
"""

import ImgPro as ip
import MtchBD as mb

import cv2
import numpy as np

from simg import SemImg

if __name__ == '__main__':
    url_txt = '../../eval/candidate_special_building_evalution.txt'
    img_folder = '../../eval/spBD_imgs/'
    key_txt = '../../../locked/GSVdl_key.txt'
    
    key = ip.gen_process.getExtInfo(key_txt)
    
    #pure generate gsv object list
    lst_gsv = ip.ggeUrlToLstObj(url_txt,False)
    ip.setSeqFn(lst_gsv)
    
    #pure download images
    lst_dlurl = ip.genLstDlUrl(lst_gsv,key)
    ip.downloadImgFromLst(lst_dlurl,img_folder)
    