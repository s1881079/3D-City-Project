#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:30:27 2019

@author: s1881079
"""

class ImgBbx:
    
    metaHead = ['img_id','name','confidence','ctx','cty','height','width','right','left','bottom','top']
    
    def __init__(self,resp_obj,gsv_obj):
        self.in_img = gsv_obj
        #self.in_img = gsv_obj.id
        self.name = resp_obj.name
        self.confidence = resp_obj.score
        self.calcGeomAttr(resp_obj.bounding_poly.normalized_vertices)
        
    def calcGeomAttr(self,lst_veritces):
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
        seq_lst = [self.in_img,self.name,self.confidence,self.ctx,self.cty,self.height,self.width,self.right,self.left,self.bottom,self.top]
        img_infolst = self.in_img.genSeqParaList()
        merge_list = seq_lst + img_infolst
        return merge_list
        
    def getMetaHead(self):
        img_head = self.in_img.getMetaHead()
        merge_head = self.metaHead + img_head
        return(merge_head)
