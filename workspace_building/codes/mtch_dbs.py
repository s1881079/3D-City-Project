#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:08:20 2019

@author: s1881079
"""

import fiona
#import geopandas as gpd
import pandas as pd
import shapely as spl
from shapely import geometry as shg
#import numpy as np
import math
import pyproj
import os

def readShp(shp_fn):
    '''
    read shapefile and return list similar to the geojson format
    //idealy to return lis tof shapely geoms - no!! losing attributes that way
    '''

    shp = fiona.open(shp_fn,'r')
    #first = shp.next()
    #print first
    #shp = gpd.read_file(shp_fn)
    
    l_shp = list(shp)
    shp.close()
    
    return l_shp

def toSplGeom(l_shp):
    '''
    from list of information to shapely geometry
    '''
    l_geoms = []
    for shp in l_shp:
        l_geoms.append(shg.shape(shp['geometry']))
        
#    if l_shp[0]['geometry']['type'] == 'Polygon':
#        multi_polygons = shg.MultiPolygon(l_geoms)
#    else:
#        print('not polygon')
        
    return l_geoms
    


def readGSVInfo(csv_fn):
    '''
    read google street view image information and turn into list of dictionary
    ======== solve the projection problem using pyproj later
    
    //idealy to return shapely point lists
    '''
    data = pd.read_csv(csv_fn)
    rst = []
    
    osgb36 = pyproj.Proj(init = 'epsg:27700')
    wgs84 = pyproj.Proj(init='epsg:4326')
    
    for ind,rc in data.iterrows():
        #add pyproj stuff here
        mapx,mapy = pyproj.transform(wgs84,osgb36,rc.lon,rc.lat)
        
        rst.append({'lat':rc.lat,'lon':rc.lon,'x':mapx,'y':mapy,'fov':rc.fov,'heading':rc.heading,'pitch':rc.url_pitch})
        
    return rst
#
#def testFunc():
#    print('i am here')
#    
#def testCall():
#    return testFunc

#============================================================the origin qua thought - abandoned 
#def inFirQuad(cam_coord,bd_coord):
#    rst = np.array(cam_coord) - np.array(bd_coord)
#    if np.all(rst < 0):
#        return True
#    else:
#        return False
#    
#def inSecQuad(cam_coord,bd_coord):
#    rst = np.array(cam_coord) - np.array(bd_coord)
#    if (rst[0] < 0) and (rst[1] > 0):
#        return True
#    else:
#        return False
#    
#def inThrQuad(cam_coord,bd_coord):
#    rst = np.array(cam_coord) - np.array(bd_coord)
#    if np.all(rst > 0):
#        return True
#    else:
#        return False
#    
#def inFrtQuad(cam_coord,bd_coord):
#    rst = np.array(cam_coord) - np.array(bd_coord)
#    if (rst[0] > 0) and (rst[1] < 0):
#        return True
#    else:
#        return False
#
#def getQuaSplitFunc(heading):
#    if 0 <= heading <= 90:
#        return inFirQuad
#    elif 90 < heading <= 180:
#        return inSecQuad
#    elif 180 < heading <= 270:
#        return inThrQuad
#    elif 270 < heading < 360:
#        return inFrtQuad
#    else:
#        print('invalid heading')
#        return None
#=============================================================================

def buildingWithinQuadBuffer(cam_pt,bds_geom,distance):
    '''
    return list of building id within buffer of the camera point
    and filter out building with no point falling in the according quad
    //cam_pt is only one point here, and to keep the other attributes on, it is still in dictionary format
    '''
    rst = []
    ind_rst = []
    #find buildings within the distance range
    cam_geom = shg.Point(cam_pt['x'],cam_pt['y'])
    #quad_split_fun = getQuaSplitFunc(cam_pt.heading)
    cam_round = cam_geom.buffer(distance)
    #here create the lookoing fan directly and close up
    #need to further check the orientation of coordinate system here
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
    
    for bd in bds_geom:
        if bd.intersects(cam_fan):
            #check if the above format works
            #print(bds_geom.index(bd))
            rst.append(bd)
            ind_rst.append(bds_geom.index(bd))
    
    #print('candidate info upper')
    
    return rst



def genLineOfSight(cam_pt, distance,ct_ang = 0):
    '''
    generate the centre line of sight from camera point
    
    using: pt.lon, pt.lat, pt.heading, distance, centre_angle
    ct_ang: within +_ fov/2
    
    
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\reasonable to use distance?
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
    
    
def findFirstHit(sline,building_list):
    '''
    find the first hit building id for a line of sight
    and the centre looking point
    '''

    #should be a function to calculate the meeting point of two lines - if none, type one
    #find all the meeting points
    l_ints = []
    lst_hitBD = []
    #print('length of buildinglist')
    #print(len(building_list))
    
    for bd in building_list:
        #print(len(list(bd.bounds.coords)))
        ints = sline.intersection(bd)
        
        if ints.length == 0:
            #print(ints)
            continue
        
        #print('hit bd found')
        #print(ints)
        
        lst_hitBD .append(bd)
        
        if ints.geom_type == 'LineString':
            lst_mpts = list(ints.coords)
        elif ints.geom_type == 'MultiLineString':
            lst_mpts = []
            for ls in ints:
                lst_mpts += list(ls.coords)
        
        #print(lst_mpts)
        
        #find the nearest meeting point within one building
        
        nrest_coord_thisBD = min(lst_mpts, key = lambda x:abs(x[0] - sline.coords[0][0]))
        #print('nearest coord for this bd:')
        #print(nrest_coord_thisBD)
        
        l_ints.append(nrest_coord_thisBD)
    
    #print('printting information of l_ints')
    #print(len(l_ints))
    #print(l_ints)
    
    
    try:
        nearest_coord = min(l_ints, key = lambda x:(abs(x[0] - sline.coords[0][0])))
        
        #instead of creating new point, get the oribound point would be better
        nearest_pt = shg.Point(nearest_coord[0],nearest_coord[1])
        #print('nearest point found')
        #print(nearest_pt)
        
        #trans to using index to do this
        #print('nearest point index')
        #print(l_ints.index(nearest_coord))
        hitID = l_ints.index(nearest_coord)
        targetBD = lst_hitBD[hitID]
        
        return building_list.index(targetBD),nearest_pt
    
    except:
        print('except error')
        return 2,shg.Point(1,1)
    
#    for bd in building_list:
#        if bd.touches(nearest_pt):
#            #===========Attention: this is returning the index of another list
#            return building_list.index(bd), nearest_pt
#    else:
#        print('loop throuhg all candidate buildings, target not found ')
#        return None,None
        
    
    #return the meeting point and the building id
    
    
    #if no building hit within distance - abandon this pic or turn into another strategy



def findBuildingInSight(cam_pt,bds_geom,sight_distance):
    candidate_buildings = buildingWithinQuadBuffer(cam_pt,bds_geom,sight_distance)
    centre_sline = genLineOfSight(cam_pt,sight_distance,0)
    candidate_buildingIndex, look_centre = findFirstHit(centre_sline,candidate_buildings)
    target_buildingIndex = bds_geom.index(candidate_buildings[candidate_buildingIndex])
    
    return target_buildingIndex, look_centre


if __name__ == "__main__":
    #shp_fn = 'SJ89_GM_buildings_districts_270315.shp'
    #workspace = os.getcwd()
    os.chdir('../SJ89_GM_buildings_districts_270315')
    shp_fn = 'cliped_OS_building.shp'
    csv_fn = '../gsv_info.csv'
    bds_shp = readShp(shp_fn)
    bds_geom = toSplGeom(bds_shp)
    
    cam_pts = readGSVInfo(csv_fn)
    
    sight_distance = 50
    
    for cam_pt in cam_pts:
        target_buildingIndex, look_centre = findBuildingInSight(cam_pt,bds_geom,sight_distance)
        target_buildingID = bds_shp[target_buildingIndex]['properties']['ID']
        #print('looking at building')
        #print(bds_shp[target_buildingIndex]['id'])
        cam_pt['t_building'] = target_buildingID
        cam_pt['eye_ct'] = list(look_centre.coords)
        #should find a better way rather than list to do the above process
        #theoretically the look centre would be a 2d coordinate, find a properformat to store it
        
    #the result would be the updated cam_pts dictionary for later operations
    




