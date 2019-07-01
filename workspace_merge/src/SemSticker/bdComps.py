#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 15:00:37 2019

@author: s1881079
"""

import math

class SuspObj():
    def __init__(self,iter_info):
        print('calling init susobj')
        self.simgs,self.bl_bd,self.x,self.y = iter_info
        #not sure this should be used
        self._confirm = False
        
    def __str__(self):
        return('susobj-info: x:{} y:{}'.format(self.x,self.y))
        
    def setConf(self):
        self._confirm = True
    
    def calcDis(self,othobj):
        dis = (self.x - othobj.x) * (self.x  - othobj.x) + (self.y - othobj.y) * (self.y - othobj.y)
        dis = math.sqrt(dis)
        return dis
    
    def addSimg(self,lst_simgs):
        self.simgs += lst_simgs
        
        
    def mergeObj(self,otherobj):
        m_simgs = self.simgs + otherobj.simgs
        if self.bl_bd != otherobj.bl_bd:
            #this theoretically should not happen, but might happen due to error of gps, 
            #over dense buildings and large min_dis
            print('triny to merge object from different building')
        m_bl_bd = self.bl_bd
        mx,my = self.averageLoc(otherobj)
        merged_info = [m_simgs,m_bl_bd,mx,my]
        
        merged = SuspObj(merged_info)
        return merged

    def averageLoc(self,otherobj):
        nx = (self.x + otherobj.x) / 2
        ny = (self.y + otherobj.y) / 2
        return nx,ny
    
    def getMetaHead(self):
        return ['gsvids','building_id','x','y']
    
    def genSeqParaList(self):
        lst_gsvids = [i.gsvid for i in self.simgs]
        str_gsvids = '+'.join(str(i) for i in lst_gsvids)
        return [str_gsvids,self.bl_bd,str(self.x),str(self.y)]