#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:01:02 2019

@author: s1881079
"""
import shapely as spl
from shapely import geometry as shg

__all__ = ['buildingWithinQuadBuffer','bdsWithinSight']

def buildingWithinQuadBuffer(cam_pt,bds_geom,distance):
    '''
    this seem to turn into a ghost function as well
    return list of building id which intersects with the vision field of the camera
    
    ** NOTICE: the building id returned indicates the sequence position of the building in the input list,
    not necessarily identical to the id shown in shapefile
    
    Parameters
    ==========
    cam_pt :  dict/camera obj
        detection camera
        
    bds_geom : list
        list of sahpely goem object
        
    distance : int
        the largest visible distance defined
    
    '''
    rst = []
    ind_rst = []
    #find buildings within the distance range
    
    #============================================================the following part should be included in a class function after created
    cam_geom = shg.Point(cam_pt['x'],cam_pt['y'])
    #quad_split_fun = getQuaSplitFunc(cam_pt.heading)
    cam_round = cam_geom.buffer(distance)
    #here create the lookoing fan directly and close up
    #need to further check the orientation of coordinate system here - fine
    suqare_coords = [(cam_pt['x'],cam_pt['y']),(cam_pt['x'] + distance,cam_pt['y']),(cam_pt['x'] + distance,cam_pt['y'] + distance),(cam_pt['x'],cam_pt['y'] + distance)]
    
    cam_square = shg.Polygon(suqare_coords)
    
    #skew the square to fit with FOV
    if cam_pt['fov'] != 90:
        cam_square_skew = spl.affinity.skew(cam_square,xs = 90 - cam_pt['fov'],origin = (cam_pt['x'],cam_pt['y']))
    else:
        cam_square_skew = cam_square
        
    #rotate the square here
    rot_angle = (-1) * (cam_pt['heading'] - 90 + (cam_pt['fov'] / 2))
    #print('rot_angle')

    #print(rot_angle)
    cam_square_rot = spl.affinity.rotate(cam_square_skew,rot_angle,origin = (cam_pt['x'],cam_pt['y']))
    
    #print('finish quad')
    #print(cam_square_rot)
    
    cam_fan = cam_round.intersection(cam_square_rot)
    
    #=========================================================================
    
    for bd in bds_geom:
        if bd.intersects(cam_fan):
            #check if the above format works
            #print(bds_geom.index(bd))
            rst.append(bd)
            ind_rst.append(bds_geom.index(bd))
    
    #print('candidate info upper')
    
    return rst

def bdsWithinSight(vis_fan,bds_geom):
    rst = []
    ind_rst = []
    
    for bd in bds_geom:
        if bd.intersects(vis_fan):
            #check if the above format works
            #print(bds_geom.index(bd))
            rst.append(bd)
            ind_rst.append(bds_geom.index(bd))
            
    return rst
    
