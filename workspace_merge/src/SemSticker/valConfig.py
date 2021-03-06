#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:44:44 2019

@author: s1881079
"""
import json

__all__ = ['readConfigToDict','valConfigInfo']

input_form_selection = ["gge_url_txt","gsv_para_csv","gsvImg_and_infoCsv"]
od_src_selection = ["Google_Cloud_Vision","Customeize_Model","Hardcode_Mode"]

def readConfigToDict(json_fn):
    '''
    read configuration data
    
    Parameters
    ==========
    json_fn : str
        file name of the input configuration json
    
    Reutrns
    =======
    dict
        dictionary containing configur information
        
    '''
    with open(json_fn) as config_file:
        config_data = json.load(config_file)
        
    return config_data

def valSrcType(src_type):
    '''
    validate detection source type 
    '''
    if src_type in od_src_selection:
        return True
    else:
        return False
    
def valInputForm(inp_form):
    '''
    validate input form
    '''
    if inp_form in input_form_selection:
        return True
    else:
        return False
    
def valConfigInfo(config_dict):
    '''
    general validation of the configuration informtion
    '''
    
    src_type = config_dict['pros_params']['object_detection_src']
    inp_form = config_dict['input_data']['input_form']
    
    if valSrcType(src_type) and valInputForm(inp_form):
        return True
    else:
        return False
    