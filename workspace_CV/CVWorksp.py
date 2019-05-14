#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 11:48:56 2019

@author: s1881079
"""
import os

def gatherInfo(txt_fname):
    basic_info = txtUrlToDict(txt_fname)

    
num_pic = 13

folder_dir = 'imgs/'
for i in range(num_pic):
    img_path = folder_dir + str(i) + '.jpg'
    resp = localize_objects(img_path)
    door_info = getDoorCt(resp)
    if len(door_info) == 1:
        
    
    