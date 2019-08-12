#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:42:50 2019

@author: s1881079
"""

from .gen_pros import *
import json
import time

__all__ = ['semStick']

def semStick(config_dict):
    '''
    main pipeline for detecting and adding doors to building footprint data
    parameters are specitied in the configuration file
    '''
    
    #generate sematic image list
    start = time.time()
    lst_simg = urlToSimg(config_dict,outputCamloc = True,outBbxloc = True)
    after_cv = time.time()
    cv_time = after_cv - start
    
    #generate building component lsit
    detected_doors = locateDoors(lst_simg,config_dict)
    after_locate = time.time()
    locate_time= after_locate - after_cv
    
    print('cv_time and locate_time',cv_time,locate_time)
    
    #output result
    writeDoors(detected_doors,config_dict['output_info'])

#
#if __name__ == "__main__":
#    with open('../config.json') as config_file:
#        config_data = json.load(config_file)
#    
##    url_txt = '../../data/gge_url/test_ggeurl.txt'
##    bd_shp = '../../data/building_footprint/resstreet_clip.shp'
##    img_folder = '../../intm_output/images/'
##    key_txt = '../../../locked/GSVdl_key.txt'
##    result_folder = '../../result/'
##    out_csv = 'testdoors.csv'
#
##if using  config file.the dict itself instead of the separated information should be passed to the functions
#    
#    
#    
#    if input_form not in input_selection:
#        print('invalid input form, quit')
#        exit(0)
#    
#    sight_dis = 50
#    min_sep = 0.8
#    
#    ## the upper parameters should be specified by either command lines or config files
#    
#    