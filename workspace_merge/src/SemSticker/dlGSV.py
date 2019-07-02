#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:00:45 2019

@author: s1881079
"""

import os
import json
import ImgPro as ip

#for download image to a folder only if the folder odes not contain any images previously

def dlGSVandWriteCSV(gsv_url,gsv_folder,csv_folder,out_csv):
    if checkImgExist(gsv_folder):
        print('already image existed in img folder')
        return None
    
    lst_gsv = ip.downloadGSV(gsv_url,gsv_folder)
    ip.writeObjInfoCsv(lst_gsv,csv_folder,out_csv)

def checkImgExist(img_folder):
    lst_fn = os.listdir(img_folder)
    lst_ext = map(lambda x:x[:-4],lst_fn)
    if '.jpg' in lst_ext:
        return True
    else:
        return False
    

if __name__ == '__main__':
    with open('config.json') as config_file:
    data = json.load(config_file)
    
    gsv_url = '../data/puredl.txt'
    gsv_folder = '../data/puredl/'
    csv_folder = '../data/'
    out_csv = 'puredl.csv'
    
    dlGSVandWriteCSV(gsv_url,gsv_folder,csv_folder,out_csv)
    

