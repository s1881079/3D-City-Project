#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:31:29 2019

@author: s1881079
"""

class GSV():
    
    metaHead = ['gsvid','filename','lat','lon','alt','fov','heading','pitch','size']
    
    def __init__(self,iter_info):
        self.id,self.lat,self.lon,self.altitude, self.fov, self.heading, self.tilt= iter_info
        self.pitch = self.tilt - 90
        self.size = [640,640]
        
    def __str__(self):
        return('gsv-info: gsv_id:{gsv_id} heading:{head}'.format(gsv_id = self.id,head = self.heading))
        
    def setFn(self,filename):
        self.fn = str(filename) + '.jpg'
        
    def genBaseGsvUrl(self):
        '''
        generate base url(without google key) for downloading street view
        '''
        self.size = '640x640'
        url_template = 'https://maps.googleapis.com/maps/api/streetview?size={size}&location={lat},{lon}&fov={fov}&heading={heading}&pitch={pitch}'
        return url_template.format(**vars(self))
    
    def genSeqParaList(self):
        '''
        generate seqential parameter list -  for writing csv as intermediate result
        '''
        seq_list = [self.id,self.fn,self.lat,self.lon,self.altitude,self.fov, self.heading, self.pitch,self.size]
        return(seq_list)
        
    def getMetaHead(self):
        return(self.metaHead)
    
    