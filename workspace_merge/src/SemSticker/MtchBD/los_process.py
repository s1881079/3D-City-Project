#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:58:43 2019

@author: s1881079
"""

from shapely import geometry as shg
import math

__all__ = ['genLineOfSight','imgCoorToLos','findFirstHit']


def genLineOfSight(cam_pt, distance,ct_ang = 0):
    '''
    generate line of sight - only considering 2d plan at this stage, tilt of the camera is not considered
    
    Parameters
    ==========
    cam_pt : campt object
        targeted camera
        
    distance : int
        largest visible distance defined
        
    ct_angle : float
        offset angle from centre, in radiant, clock-wise as positive
        
    Returns
    =======
    shapely geom object (line)
    
    '''
    #check if centre_angle is valid
    if cam_pt['fov']/(-2) < ct_ang < cam_pt['fov']/2:
        pass
    else:
        #invalid center_angle
        return None
    edpt_x = cam_pt['x'] + distance * math.sin(math.radians(cam_pt['heading'] + ct_ang))
    edpt_y = cam_pt['y'] + distance * math.cos(math.radians(cam_pt['heading'] + ct_ang))
    endpt = shg.Point(edpt_x,edpt_y)
    stpt = shg.Point(cam_pt['x'],cam_pt['y'])
    
    #create new line in geopd
    sline = shg.LineString([stpt,endpt])
    
    #calc endpoint and input information
    #print('sline generated')
    #print(sline)
    
    return sline

def imgCoorToLos(img_fov,x,y,nor=True,img_size = 640):
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
    
    if nor:
        pass
    else:
        x = x / img_size
        y = y / img_size
        
    yaw_pre = img_fov * (x - 0.5)
    tilt_pre = img_fov * (0.5 - y)
    
    r_fov = math.radians(img_fov)
    x = x - 0.5
    y = 0.5 - y
    alfa = math.atan((img_size - 2 * x) * math.sin(r_fov / 2) / img_size * math.cos(img_fov / 2))
    beta = math.atan((img_size - 2 * y) * math.sin(r_fov / 2) / img_size * math.cos(img_fov / 2))
    
    
    print('yaw:',yaw_pre,'tilt',tilt_pre)
    print('alfa:',alfa,'beta',beta)
    return alfa,beta
    
def findFirstHit(sline,building_list):
    '''
    find the building first hitted by a line of sight and return building id and intersect point
    
    Parameters
    ==========
    sline : shapely geom object(line)
        line of sight
        
    building_lsit : list
        list of building geom objects
        
    Returns
    =======
    int
        sequence index of the target building in the inpit building list
        
    shapely point
        intersect point 
        
    shapely polygon
        taget buildig geometry
        ** CHECK : the reason for needing this
    
    '''
    
    #find all the meeting points
    l_ints = []
    lst_hitBD = []
    
    for bd in building_list:
        ints = sline.intersection(bd)
        
        if ints.length == 0:
            continue
        
        
        lst_hitBD .append(bd)
        
        if ints.geom_type == 'LineString':
            lst_mpts = list(ints.coords)
        elif ints.geom_type == 'MultiLineString':
            lst_mpts = []
            for ls in ints:
                lst_mpts += list(ls.coords)
        #find the nearest meeting point within one building
        
        nrest_coord_thisBD = min(lst_mpts, key = lambda x:abs(x[0] - sline.coords[0][0]))
        
        l_ints.append(nrest_coord_thisBD)
    
    
    try:
        nearest_coord = min(l_ints, key = lambda x:(abs(x[0] - sline.coords[0][0])))
        
        #instead of creating new point, get the oribound point would be better
        nearest_pt = shg.Point(nearest_coord[0],nearest_coord[1])
        
        #trans to using index to do this
        hitID = l_ints.index(nearest_coord)
        targetBD = lst_hitBD[hitID]
        
        return building_list.index(targetBD),nearest_pt,targetBD
    
    except:
        print('except error')
        return 2,shg.Point(1,1),None
    
#    for bd in building_list:
#        if bd.touches(nearest_pt):
#            #===========Attention: this is returning the index of another list
#            return building_list.index(bd), nearest_pt
#    else:
#        print('loop throuhg all candidate buildings, target not found ')
#        return None,None
        
    
    #return the meeting point and the building id
    
    
    #if no building hit within distance - abandon this pic or turn into another strategy

