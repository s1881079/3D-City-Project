#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:42:50 2019

@author: s1881079
"""

from gen_pros import *
import json

__all__ = ['semStick']

def semStick(config_dict):  
    lst_simg = urlToSimg(config_dict,outputCamloc = True,outBbxloc = True)
    detected_doors = locateDoors(lst_simg,config_dict)
    writeDoors(detected_doors,config_dict['ouput_info'])

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