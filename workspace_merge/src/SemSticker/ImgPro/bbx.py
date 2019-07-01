#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:30:27 2019

@author: s1881079
"""

class Bbx:
    
    metaHead = ['gsv_id','name','confidence','ctx','cty','height','width','right','left','bottom','top']
    
    def __init__(self,resp_obj,*,src_tag = 'Google_Cloud_Vision'):
        self.los = None
        self.susObj = None
        self.gsv_id = -1
        
        if src_tag not in ['Google_Cloud_Vision','Customeize_Model','Hardcode_Mode']:
            print('boundig box init error: undefined source. source tag should be one of .., - shouldnt happen if following the sample, check codes')
            return None
        
        if src_tag == 'Google_Cloud_Vision':
            self.name = resp_obj.name
            self.confidence = resp_obj.score
            self.calcGeomAttr(resp_obj.bounding_poly.normalized_vertices)
        elif src_tag == 'Customize_Model':
            #change this part when using cussomized models 
            self.name = resp_obj
        elif src_tag == 'Hardcode_Mode':
            self.name,self.confidnece,self.ctx,self.cty,self.width,self.height = resp_obj
            
    def __str__(self):
        return('bbxinfo - gsvid:{gsvid} type:{bxtype} x:{x} y:{y}'.format(gsvid = self.gsv_id,bxtype = self.name,x = self.ctx,y = self.cty))
        
    def setGsvID(self,int_id):
        '''
        seems like ghost function as well
        '''
        self.gsv_id = int_id
        
    def setSusObj(self,susobj):
        print('setting suspect object in box')
        self.susObj = susobj
        
    def moveBound(self,movex,movey):
        self.right += movex
        self.left += movex
        self.bottom += movey
        self.top += movey
        
    def adaptView(self,roi_info,full_size):
        orx = self.ctx
        nx = self.ctx * roi_info[3] + roi_info[1]
        self.ctx = nx / full_size[0]
        
        ory = self.cty
        ny = self.cty * roi_info[4] + roi_info[2]
        self.cty = ny / full_size[1]
        movex = self.ctx - orx
        movey = self.cty - ory
        
        self.moveBound(movex,movey)
        
    def calcGeomAttr(self,lst_veritces):
        '''
        calculate geometry attributes
        '''
        x_list = []
        y_list = []
        for coor in lst_veritces:
            x_list.append(coor.x)
            y_list.append(coor.y)
            
        self.ctx = sum(x_list) / len(x_list)
        self.cty = sum(y_list) / len(y_list)
        self.height = max(y_list) - min(x_list)
        self.width = max(x_list) - min(x_list)
        self.right = max(x_list)
        self.left = min(x_list)
        self.bottom = max(y_list)
        self.top = min(y_list)
        
    def genSeqParaList(self):
        '''
        generate sequetail parameter slist -used during writing csv files
        '''
        seq_lst = [self.gsv_id,self.name,self.confidence,self.ctx,self.cty,self.height,self.width,self.right,self.left,self.bottom,self.top]
        #img_infolst = self.in_img.genSeqParaList()
        merge_list = seq_lst
        return merge_list
        
    def getMetaHead(self):
        '''
        get metadata head line - used during writing csv files
        '''
        #img_head = self.in_img.getMetaHead()
        merge_head = self.metaHead
        return(merge_head)
        
    def setlos(self,in_los):
        if self.los is not None:
            print('warning: trying to reset the los of bbx, not expected in process, check code')
        
        self.los = in_los
        
    def imgCoorToAng(self,img_fov,img_size,nor=True):
        '''
        generate line of sight based on the coordinate specified in the image
        the output line of sight is defined by yaw and tilt value base on centre line of sight
        xy coordinate should be normalized, if nor, set nor to FALSE to perform normalization
        the dault image size is 640*640
        
        special notice:
            the default tile size for gsv is 521*521, if the coordinate is presented in pixel level,
            the tota size should be specified as 521
            
        Parameters
        ==========
        img_fov : int
            field of view of the camera
        x, y : float
            coordinate of the taget in image
        nor : bool
            whether to normalize the coordinate
        img_size : int
            total size of the image
            
        Returns
        =======
        relative yaw and tilt of the object based on the centre of image
        '''
        x = self.ctx
        y = self.cty
        
        if nor:
            pass
        else:
            x = x / img_size
            y = y / img_size
            
        yaw = img_fov * (x - 0.5)
        tilt = img_fov * (0.5 - y)
        print('yaw:',yaw,'tilt',tilt)
        return yaw,tilt