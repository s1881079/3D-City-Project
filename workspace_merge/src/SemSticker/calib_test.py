#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 13:14:58 2019

@author: s1881079
"""

import ImgPro as ip
import MtchBD as mb

import cv2
import numpy as np

from simg import SemImg

#this file is only for calibration test to see how google street view datseet compatible with os buildin gfootprint

def findRedMark(img_folder,gsv):
    img_dir = img_folder+gsv.fn
    image = cv2.imread(img_dir)
    print(img_dir)
    #instead of going in range, take red out and threshold
    lower_red = np.array([0,0,200])
    higher_red = np.array([100,100,255])
#    mask = cv2.inRange(image,lower_red,higher_red)
    
#    lower_red = cv.Scalar(0,0,250)
#    higher_red = cv.Scalar(0,0,255)
    mask = cv2.inRange(image,lower_red,higher_red)
#    
#    b,g,r = cv2.split(image)
#    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#    h,s,v = cv2.split(hsv)
#    test = r - b
    #print(np.any(mask > 0))
    #result = cv2.bitwise_and(image, image, mask=mask)
    ret,thresh = cv2.threshold(mask,0,255,cv2.THRESH_BINARY)
    ctrs, hier = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #get bounding box
    print(len(ctrs))
    x, y, w, h = cv2.boundingRect(ctrs[0])
    ctx = (x+(w/2))/640
    cty = (y+(h/2))/640
    bbx_info = ['BdEdge',1,ctx,cty,w,h]
    bbx = ip.Bbx(bbx_info,src_tag = 'Hardcode_Mode')
    bbx.setGsvID(gsv.id)
    print(bbx)
    print(gsv)
    simg = SemImg(gsv,[[],[],[bbx]])
    print(simg)
    
    cv2.imwrite(img_dir[:-4] +'_red_ext.jpg',thresh)
    cv2.imwrite(img_dir[:-4] +'_reexpor.jpg',image)
    return simg
    
def wirteLosCsv(csv_dir,lst_id,lst_x,lst_y):
    with open(csv_dir,'w') as wfile:
        headline = 'id,x,y\n'
        wfile.write(headline)
        for i in range(len(lst_id)):
            line = ','.join([str(lst_id[i]),str(lst_x[i]),str(lst_y[i])])
            wfile.write(line + '\n')
            
    wfile.close()
    

if __name__ == '__main__':
    url_txt = '../../CalibTest/calib4_ggeurls.txt'
    img_folder = '../../CalibTest/calib_images/group4/'
    key_txt = '../../../locked/GSVdl_key.txt'
    
    key = ip.gen_process.getExtInfo(key_txt)
    
    #pure generate gsv object list
    lst_gsv = ip.ggeUrlToLstObj(url_txt,False)
    ip.setSeqFn(lst_gsv)
    
    #pure download images
    lst_dlurl = ip.genLstDlUrl(lst_gsv,key)
    ip.downloadImgFromLst(lst_dlurl,img_folder)
    
    
    lst_simgs = []
    list_x = []
    list_y = []
    list_id = []
    
    for gsv in lst_gsv:
        #print(gsv.fn)
        edge_simg = findRedMark(img_folder,gsv)
        edge_simg.genBbxCtLines(50,'Others')
        
        edge_bbx = edge_simg.allothers[0]
        pts = list(edge_bbx.los.coords)
        for pt in pts:
            list_id.append(gsv.id)
            list_x.append(pt[0])
            list_y.append(pt[1])
        
        lst_simgs.append(edge_simg)
        
    #instead of writing to csv, directly extract the lines and find dintersection point
    
    #prepare a csv storing the correct information for each group
    
    #calculte the centre point for all the intersections and compare it to the correct point
    
    #store paameters: error vector both adding together and separately
    csv_dir = img_folder + 'los_coords.csv'
    wirteLosCsv(csv_dir,list_id,list_x,list_y)
        

    