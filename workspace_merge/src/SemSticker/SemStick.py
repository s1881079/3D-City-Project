#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:42:50 2019

@author: s1881079
"""

from gen_pros import *
import json


if __name__ == "__main__":
    with open('config.json') as config_file:
        config_data = json.load(config_file)
    
#    url_txt = '../../data/gge_url/test_ggeurl.txt'
#    bd_shp = '../../data/building_footprint/resstreet_clip.shp'
#    img_folder = '../../intm_output/images/'
#    key_txt = '../../../locked/GSVdl_key.txt'
#    result_folder = '../../result/'
#    out_csv = 'testdoors.csv'

#if using  config file.the dict itself instead of the separated information should be passed to the functions
    
    input_form = config_dict['input_data']['input_form']
    input_selection = config_dict['input_data']['input_form_selection']
    
    if input_form not in input_selection:
        print('invalid input form, quit')
        exit(0)
    
    sight_dis = 50
    min_sep = 0.8
    
    ## the upper parameters should be specified by either command lines or config files
    
    lst_simg = urlToSimg(config_data,outputCamloc = True,outBbxloc = True)
    detected_doors = locateDoors(lst_simg,bd_shp,sight_dis,min_sep)
    writeDoors(detected_doors,result_folder,out_csv)