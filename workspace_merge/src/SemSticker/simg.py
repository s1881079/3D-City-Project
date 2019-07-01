#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 13:27:31 2019

@author: s1881079
"""

#from .bbx import Bbx
#from .gsv import GSV

#from MtchBD import los_process as los
#from .semPro import *

from shapely import geometry as shg
import shapely as spl
import math
import pyproj

class SemImg():
    def __init__(self,gsv,lst_bbxs,mapProj = 'epsg:27700'):
        '''
        also need input and output as csv functions to store intermediate results
        consider using getattr and setattr
        
        '''
        self._gsv = gsv
        self._doors,self._windows,self._others = lst_bbxs
        self.map_proj = mapProj
        self.addCampt(mapProj)
        
    
    def __str__(self):
        return('gsvid:{},door_count:{},window_count:{}'.format(self.gsvid,len(self._doors),len(self._windows)))
        
    
    def __getattr__(self,key):
        if key == 'alldoors':
            return self._doors
        elif key == 'allwindows':
            return self._windows
        elif key == 'allothers':
            return self._others
        elif key == 'gsvid':
            return self._gsv.id
        elif key == 'gsv_size':
            return self._gsv.size
        elif key == 'allbbxs':
            return self._doors + self._windows + self._others
    
    def addBbx(self,bbx):
        '''
        add bounding box object - used in segmentation cusomized models
        '''
        if bbx.name == 'Door':
            self._doors.append(bbx)
        elif bbx.name == 'Window':
            self._windows.append(bbx)
        else:
            self._others.append(bbx)
    
    def addCampt(self,map_proj):
        '''
        add camera point to semimg object, creat shapely point geom and add directly as campt attribute
        
        Parameters
        ==========
        map_proj : str
            epsg string specifying what map projection it is using
            
        '''
        mapproj = pyproj.Proj(init = self.map_proj)
        #osgb36
        wgs84 = pyproj.Proj(init='epsg:4326')
        
        self.cam_x,self.cam_y = pyproj.transform(wgs84,mapproj,self._gsv.lon,self._gsv.lat)
        self.campt = shg.Point(self.cam_x,self.cam_y)
        
    def genLos(self,fur_dis,ct_ang = 0):
        '''
        generate line of sight - only considering 2d plan at this stage, tilt of the camera is not considered
        
        Parameters
        ==========
        self : semimg object
            targeted sememtic image
            
        distance : int
            largest visible distance defined
            
        ct_angle : float
            offset angle from centre, in radiant, clock-wise as positive
            
        Returns
        =======
        shapely geom object (line)
        
        '''
        fov = self._gsv.fov
        heading = self._gsv.heading
        
        if fov/(-2) < ct_ang < fov/2:
            pass
        else:
            #invalid center_angle
            return None
        edpt_x = self.cam_x + fur_dis * math.sin(math.radians(heading + ct_ang))
        edpt_y = self.cam_y + fur_dis * math.cos(math.radians(heading + ct_ang))
        endpt = shg.Point(edpt_x,edpt_y)
        stpt = self.campt
        
        #create new line in geopd
        sline = shg.LineString([stpt,endpt])
        
        #calc endpoint and input information
        #print('sline generated')
        #print(sline)
        
        return sline
        
    def genVisFan(self,fur_dis):
        '''
        generate visible fan for sementic image object based on largest visible distance
        visible fan is a shapely polygon added directly as object's visFan attribute
        
        Parmeters
        =========
        fur_dis : int
            furthest  visible distance
        '''
        
        x = self.cam_x
        y = self.cam_y
        fov = self._gsv.fov
        heading = self._gsv.heading
        
        cam_round = self.campt.buffer(fur_dis)
        
        suqare_coords = [(x,y),(x + fur_dis,y),(x + fur_dis,y + fur_dis),(x,y + fur_dis)]
        cam_square = shg.Polygon(suqare_coords)
        
        if fov != 90:
            cam_square_skew = spl.affinity.skew(cam_square,xs = 90 - fov,origin = (x,y))
        else:
            cam_square_skew = cam_square
            
        rot_angle = (-1) * (heading - 90 + (fov / 2))
        cam_square_rot = spl.affinity.rotate(cam_square_skew,rot_angle,origin = (x,y))
        
        vis_fan = cam_round.intersection(cam_square_rot)
        self.visFan = vis_fan
        
        
    def genBbxCtLines(self,fur_dis = 50,obj_key = 'Door'):
        '''
        generate list of line of sights based on object keyword and furest visible distance
        line of sight would be directly add to bbx as attribute 
        
        Parameters
        ==========
        fur_dis : int
            furthest distance specified
            
        obj_key : str
            string specifying which type of object to generate lines of sight
        '''
        switcher = {
                'Door': self._doors,
                'Window': self._windows,
                'Others' : self._others
                }
        
        try:
            bbx_list = switcher[obj_key]
        except:
            print('invalid keyword')
            return None
        
        for bbx in bbx_list:
            yaw,tilt = bbx.imgCoorToAng(self._gsv.fov,self._gsv.size)
            los = self.genLos(fur_dis,yaw)
            bbx.setlos(los)
            
    def getMetaHead(self):
        '''
        function for ouput as csv
        '''
        gsv_head = self._gsv.getMetaHead()
        merge_head = gsv_head + ['mapx','mapy','num_doors','num_window','num_others']
        return merge_head
    
    def genSeqParaList(self):
        '''
        function for output as csv
        '''
        gsv_info = self._gsv.genSeqParaList()
        merge_info = gsv_info + [self.cam_x,self.cam_y,len(self._doors),len(self._windows),len(self._others)]
        return merge_info

    def linkBbxGsvID(self):
        '''
        for each bbx in semimg object, add the id of gsv as gsv_id attribute
        partly for output as csv
        
        '''
        for drbbx in self.allbbxs:
            drbbx.setGsvID(int(self.gsvid))