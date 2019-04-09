#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:08:20 2019

@author: s1881079
"""

#import fiona
import geopandas as gpd
import pandas as pd

def readShp(shp_fn):
    '''
    read shapefile
    '''

    #shp = fiona.open(filename)
    #first = shp.next()
    #print first
    shp = gpd.read_file(shp_fn)
    
    return shp


def readGSVInfo(csv_fn):
    '''
    read google street view image information and turn into list of dictionary
    '''
    data = pd.read_csv(csv_fn)
    rst = []
    for ind,rc in data.iterrows():
        rst.append({'lat':rc.lat,'lon':rc.lon,'fov':rc.fov,'heading':rc.heading,'pitch':rc.url_pitch})
        
    return rst


def buildingWithinQuadBuffer(cam_pt,bds_shp,distance):
    '''
    return list of building id within buffer of the camera point
    and filter out building with no point falling in the according quad
    '''
    rst = []
    
    return rst



def genLineOfSight(cam_pt, distance,ct_ang = 0):
    '''
    generate the centre line of sight from camera point
    
    using: pt.lon, pt.lat, pt.heading, distance, centre_angle
    ct_ang: within +_ fov/2
    
    
    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\reasonable to use distance?
    '''
    #check if centre_angle is valid
    if cam_pt.fov/(-2) < ct_ang < cam_pt.fov/2:
        pass
    else:
        #invalid center_angle
        return None
    
    #create new line in geopd
    sline = 'line format'
    
    #calc endpoint and input information
    

    
    return sline
    
    
def findFirstHit(sline,building_list):
    '''
    find the first hit building id for a line of sight
    and the centre looking point
    '''
    rst_buildingID = 0
    look_centre = 'point format'
    #should be a function to calculate the meeting point of two lines - if none, type one
    #find all the meeting points
    
    #find the nearest meeting point
    
    #return the meeting point and the building id
    
    
    #if no building hit within distance - abandon this pic or turn into another strategy

    return rst_buildingID,look_centre


def findBuildingInSight(cam_pt,bds_shp,sight_distance):
    candidate_buildings = buildingWithinQuadBuffer(cam_pt,bds_shp,sight_distance)
    centre_sline = genLineOfSight(cam_pt,sight_distance,0)
    target_buildingID, look_centre = findFirstHit(centre_sline,candidate_buildings)
    
    return target_buildingID, look_centre


if __name__ == "__main__":
    shp_fn = 'SJ89_GM_buildings_districts_270315.shp'
    csv_fn = 'gsv_info.csv'
    bds_shp = readShp(shp_fn)
    cam_pts = readGSVInfo(csv_fn)
    
    sight_distance = 200
    for cam_pt in cam_pts:
        target_buildingID, look_centre = findBuildingInSight(cam_pt,bds_shp,sight_distance)
        cam_pt['t_building'] = target_buildingID
        cam_pt['eye_ct'] = look_centre
        #theoretically the look centre would be a 2d coordinate, find a properformat to store it
        
    #the result would be the updated cam_pts dictionary for later operations
    




