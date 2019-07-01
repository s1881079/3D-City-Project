#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:20:15 2019

@author: s1881079
"""

#draft for campt class
#should import shapely

#basic informaiton
#map projecf when initiate
#create shapely point
#create vision field by distance
#create line of sight
#would be interestingto store directly using shp format - convenient to map later

import shapely as shp

class Campt:
    
    #rst.append({'lat':rc.lat,'lon':rc.lon,'x':mapx,'y':mapy,'fov':rc.fov,'heading':rc.heading,'pitch':rc.pitch,'dr_cx':rc.ctx,'dr_cy':rc.cty,'door_score':rc.confidence,'img_id':rc.id}
    
    def __init__(self,iterable):
        self.lat,self.lon,self.fov,self.heading,self.pitch,self.
        