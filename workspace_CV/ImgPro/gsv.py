#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:31:29 2019

@author: s1881079
"""

class GSVImg():
    
    metaHead = ['id','lat','lon','alt','fov','heading','pitch']
    
    def __init__(self,iter_info):
        self.id, self.lat,self.lon,self.altitude, self.fov, self.heading, self.tilt= iter_info
        self.pitch = self.tilt - 90
        
    def genBaseGsvUrl(self):
        self.size = '640x640'
        url_template = 'https://maps.googleapis.com/maps/api/streetview?size={size}&location={lat},{lon}&fov={fov}&heading={heading}&pitch={pitch}'
        return url_template.format(**vars(self))
    
    def genSeqParaList(self):
        seq_list = [self.id,self.lat,self.lon,self.altitude,self.fov, self.heading, self.pitch]
        return(seq_list)
        
    def getMetaHead(self):
        return(self.metaHead)
    