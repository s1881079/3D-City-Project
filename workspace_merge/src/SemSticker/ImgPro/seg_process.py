#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 13:49:59 2019

@author: s1881079
"""

import cv2
import numpy as np
import os

from .bbx import Bbx
from .ggvision import localize_objects

#from .gsv import GSV
import sys
sys.path.append('../')
from simg import SemImg

__all__ = ['extSegSimg']

def showImg(win_name,img):
    '''
    not supported when using remote connect
    '''
    cv2.namedWindow(win_name,cv2.WINDOW_NORMAL)
    cv2.imshow(win_name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def extSegSimg(gsv,gsv_folder,detection_src = 'Google_Cloud_Vision',min_bbx_size = [50,70],max_wh_offset = 300):
    '''
    extract region of interest based on image segmentation and write to new jpg file
    the ROI image is stored within a folder on the same file level with input image - temporall for object detection
    
    Parameters
    ==========
    image_dir : str
        image directory, either absolute of relative
        
    min_bbx_size : lst / tuple / numpy array
        minimum bounding box size to be considered valid region of interest rather than noise area
        
    max_wh_offset : 
        maximum acceptable offset between width and height of ROI, used to filter out thin rectangles, set to large number if do not need to filter
    
    Returns
    =======
    SemImg object (singel)
    
    '''
    image_dir = gsv_folder + gsv.fn
    image = cv2.imread(image_dir)
    img_height, img_width = image.shape[:2]
    print(img_height,img_width)
    
    roi_folder = gsv_folder + 'ROIs/'
    
    if os.path.exists(roi_folder,) is False:
        os.makedirs(roi_folder)
    
    #turn to grey scale and blur
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray,10,150,150)
    
    #binarize
    ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    #reduce pepper noise, detect edges and join
    kernel = np.ones((3,3),np.uint8)
    closing = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel,iterations = 1)
    edged=cv2.Canny(closing,50,200)
    close  = cv2.morphologyEx(edged,cv2.MORPH_CLOSE,kernel,iterations = 1)
    
    #detect contours
    ctrs, hier = cv2.findContours(close.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    
    emp_objlist = [[],[],[]]
    simg = SemImg(gsv,emp_objlist)
    
    #extract region of interst
    for i, ctr in enumerate(sorted_ctrs):
        #get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
        roi_info = [(str(gsv.id) + '_' + str(i)),x,y,w,h]
        
        #print(x,y,w,h,abs(w-h))
        
        #extracting roid region - if not on edge, create a litle more outer space for detecting
        if (y<5 or x<5 or y>img_height - 5 - h or x > img_width - 5 - w):
            roi = image[y:y + h,x:x+w]
        else:
            roi = image[y-5:y + h+5, x-5:x + w+5]
            
        #reduce noise area and thin rectangles
        if w > min_bbx_size[0] and h > min_bbx_size[1] and abs(w-h)<max_wh_offset:
            cv2.imwrite(roi_folder + str(gsv.id) + '_{}.jpg'.format(i), roi)
            #could continue on object detection directly here
            #segObjDetect(simg,roi_info,roi_folder)
            #print(roi_info)
            
            if detection_src == 'Google_Cloud_Vision':
                segObjDetect_gcv(simg,roi_info,roi_folder)
            
    return simg

def segObjDetect_gcv(simg,roi_info,roi_folder):
    roi_dir = roi_folder + roi_info[0] + '.jpg'
    resp_objs = localize_objects(roi_dir)
    
    if len(resp_objs) == 0:
        #detect labels and if type of top labels falls in the category of tyoe of interest, add bbox base on the roi info 
        print('object detection returned null')
        
    for resp in resp_objs:
        bbx = Bbx(resp)
        #print(bbx)
        bbx.adaptView(roi_info,simg.gsv_size)
        #print('after addaptation')
        #print(bbx)
        #bbx.moveBy(roi_info[1],roi_info[2])
        simg.addBbx(bbx)
    

def segObjDetect(simg,roi_info,roi_imgfolder):
    '''
    need to put the model files under this module
    '''
    objs_list = DetectObjInROI(roi_info[0],roi_imgfolder)
    #obj_type,obj_roix,obj_roiy,obj_roiw,obj_roih = DetectObjInROI(roi_info[0],roi_imgfolder)
    
    
    for roi_obj in objs_list:
        obj_type,obj_confidence = obj_roix,obj_roiy,obj_roiw,obj_roih = roi_obj
        
        #if reutrn inforation is in pixel
        obj_gsvx = roi_info[1] + obj_roix
        obj_gsvy = roi_info[2] + obj_roiy
        obj_gsvw = obj_roiw
        obj_gsvh = obj_roih
        
        #if return inofrmation is proportional
        obj_gsvx = roi_info[1] + obj_roix * roi_info[3]
        obj_gsvy = roi_info[2] + obj_roiy * roi_info[4]
        obj_gsvw = obj_roiw * roi_info[3]
        obj_gsvh = obj_roih * roi_info[4]
        
        #createBbx
        #bbx = Bbx(obj_infos)
        #simg.addBbx(bbx)
    

def DetectObjInROI(roi_strid,roi_imgfolder):
    roi_dir = roi_imgfolder + roi_strid + '.jpg'
    
    #open the image file
    
    #process the return response -in former versio bounding box are created from google vision response object - this should change somhow
    #response = runmodel
    
    #output response 
    #bbx = Bbx(resp)
    
    return obj_type,obj_roix,obj_roiy,obj_roiw,obj_roih
    
    
