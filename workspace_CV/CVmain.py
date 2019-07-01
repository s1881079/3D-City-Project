#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:58:43 2019

@author: s1881079
"""

import os
import ImgPro as ip

def urlToCmPt():
    '''
    attemp to get round of database and do it all in python codes
    
    '''
    url_txt = 'src/resstreet_gges.txt'
    img_folder = 'imgs_resstreet/'
    key = ip.gen_process.getExtInfo('../locked/GSVdl_key.txt')
    #sec = ip.gen_process.getExtInfo('../locked/GSVdl_sec.txt')
    
    if os.path.exists(img_folder,) is False:
        os.makedirs(img_folder)
    
    lst_gsv = ip.downloadGSV(url_txt,img_folder,key)
    
    
    fn_list = os.listdir(img_folder)
    lst_imgfn = ip.gsv_preprocess.genImgFnList(img_folder,fn_list)
    
    #testign output
    print('print gsv lantitudes')
    for gsv in lst_gsv:
        print(gsv.lat)
        
    print('print file list')
    for fn in lst_imgfn:
        print(fn)
        
    
    all_door = []
    all_window = []
    all_other  = []
    
    #create a general function - input the list of gsv,image folder name,output list of semimg object
    #lst_simgs = ip.resp_process.genSimgLst(lst_gsv,lst_imgfn)
    
    for img_fn in lst_imgfn:
        lst_doors,lst_windows,lst_others = ip.resp_process.objDetect(lst_gsv,img_fn)
        #lst_bbxs = ip.resp_process.objDetect(lst_gsv,img_fn)
        #sem_img = SemImg()
        #structure need to be changed here
        all_door += lst_doors
        all_window += lst_windows
        all_other += lst_others
    
        
    ip.gen_process.writeObjInfoCsv(all_door,img_folder,'doorBbx.csv')
    ip.gen_process.writeObjInfoCsv(all_window,img_folder,'windowBbx.csv')
    ip.gen_process.writeObjInfoCsv(all_door,img_folder,'otherBbx.csv')
    
    cam_pts = ip.gen_process.convFormat(all_door)
    
    #return lst_simgs
    
    return cam_pts

def urlToCmLoc():
    '''
    testing - from url to cmpoint(location only)
    '''
    url_txt = 'src/resstreet_gges.txt'
    csv_folder = 'rst/'
    csv_name = 'resstreet_camloc.csv'
    
    if os.path.exists(csv_folder,) is False:
        os.makedirs(csv_folder)
        
    ip.gsv_preprocess.genCamlocFromTxt(url_txt,csv_folder,csv_name)
    
if __name__ == '__main__':
    #urlToCmLoc()
    urlToCmPt()
    