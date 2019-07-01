#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:42:50 2019

@author: s1881079
"""

from gen_pros import *


if __name__ == "__main__":
    url_txt = '../../data/gge_url/test_ggeurl.txt'
    bd_shp = '../../data/building_footprint/resstreet_clip.shp'
    img_folder = '../../intm_output/images/'
    key_txt = '../../../locked/GSVdl_key.txt'
    result_folder = '../../result/'
    out_csv = 'testdoors.csv'
    
    sight_dis = 50
    min_sep = 0.8
    
    ## the upper parameters should be specified by either command lines or config files
    
    lst_simg = urlToSimg(url_txt,img_folder,key_txt,outputCamloc = True,outBbxloc = True,detection_src = 'Google_Cloud_Vision',segment_img = True)
    detected_doors = locateDoors(lst_simg,bd_shp,sight_dis,min_sep)
    writeDoors(detected_doors,result_folder,out_csv)