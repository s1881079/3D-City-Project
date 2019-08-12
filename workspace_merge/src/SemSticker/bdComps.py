#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 15:00:37 2019

@author: s1881079
"""

import math

class SuspObj():
    def __init__(self,iter_info):
        self.simgs,self.comp_id, self.bdc_type, self.bl_bd,self.x,self.y,self.z = iter_info
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
        mx,my,mz = self.averageLoc(otherobj)
        m_compid = str(self.comp_id) + '_' + str(otherobj.comp_id)
        m_bdc_type = self.bdc_type
        merged_info = [m_simgs,m_compid,m_bdc_type,m_bl_bd,mx,my,mz]
        
        merged = SuspObj(merged_info)
        return merged

    def averageLoc(self,otherobj):
        nx = (self.x + otherobj.x) / 2
        ny = (self.y + otherobj.y) / 2
        nz = (self.z + otherobj.z) / 2
        return nx,ny,nz
    
    def getMetaHead(self):
        return ['gsvids','object_type','building_id','x','y','z']
    
    def genSeqParaList(self):
        lst_gsvids = [i.gsvid for i in self.simgs]
        str_gsvids = '+'.join(str(i) for i in lst_gsvids)
        return [str_gsvids,self.bdc_type,self.bl_bd,str(self.x),str(self.y),str(self.z)]
    
    def outCityGML(self):
        cgml_template = '''
        <bldg:{comp_type} gml:id="{gml_id}">
        <gml:name>{gml_name}</gml:name>					
        <multiPoint>
        <gml:MultiPoint>
        <gml:pointMember>
        <gml:Point>
        <gml:pos srsDimension="3">{x_coor} {y_coor} {z_coor} </gml:pos>
        </gml:Point>
        </gml:pointMember>
        </gml:MultiPoint>
        </multiPoint>
        </bldg:Door>
        '''
        
        gmlid = self.bl_bd + '_' + self.bdc_type + '_' + str(self.comp_id)
        gmlname = self.bdc_type + '_' + str(self.comp_id)
        
        target_GML = cgml_template.format(comp_type = self.bdc_type, gml_id = gmlid,gml_name = gmlname,x_coor = str(self.x),y_coor = str(self.y),z_coor = str(self.z))
        return target_GML