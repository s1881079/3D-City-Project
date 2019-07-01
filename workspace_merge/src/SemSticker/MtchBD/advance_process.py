#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:03:27 2019

@author: s1881079
"""
from .bd_geom import *
from .los_process import *
import numpy as np
import math

__all__ = ['findBuildingInSight','findLocDoor','fixMultiDetection']


def findBuildingInSight(cam_pt,bds_geom,sight_distance):
    '''
    find building falling in the centre of the image, detect door location
    
    Parameters
    ==========
    cam_pt : camera object
        campera focus
        
    bds_geom : lsit
        list of biudling geometries
        
    sight_distance : int
        largest visible distance defined
        
    Returns
    =======
    int
        sequence of target building in the input list
    
    shapely point
        look cetre point (intersection of the central line of sight and building boundary)
        door location point
    '''
    
    candidate_buildings = buildingWithinQuadBuffer(cam_pt,bds_geom,sight_distance)
    centre_sline = genLineOfSight(cam_pt,sight_distance,0)
    candidate_buildingIndex, look_centre, tar_bd_geom = findFirstHit(centre_sline,candidate_buildings)
    target_buildingIndex = bds_geom.index(candidate_buildings[candidate_buildingIndex])
    
    #the process for locating door - here already assum the campt has xy of dor, whihc need to be adatperd afterwards
    doorLoc = findLocDoor(tar_bd_geom,cam_pt)
    #add doorLoc to reuturn afterwards
    
    return target_buildingIndex, look_centre, doorLoc

def findLocDoor(bd_geom,cam_pt):
    '''
    find the location of door on boundary of the building
    
    Parameters
    ==========
    bd_geom : shapely geom
        the geometry of target building
        ** CHECK: whether the central strategy still siuts here
        
    cam_pt : cam_pt object
        the focus camera
        
    Returns
    =======
    shapely point
        door location
    '''
    
    print('in find door function')
    
    drcx = cam_pt['dr_cx']
    drcy = cam_pt['dr_cy']
    fov = cam_pt['fov']
    dryaw,drtilt = imgCoorToLos(fov,drcx,drcy,True)
    
    los_door = genLineOfSight(cam_pt,30,dryaw)
    bdix,coord_door,bd_geom = findFirstHit(los_door,[bd_geom])
    print('coord_door:',coord_door)
    
    return coord_door

def fixMultiDetection(cam_pts,min_dis):
    '''
    to filter out the repeated detection
    since the field of view is controled in this project, normally same entrance would be at maximum detected by 3 adjacent imgaes
    
    Parameters
    ==========
    cam_pts : lsit
        list of campt objects
        ** CHECK : why is the camera point inputted here - campt already updated with door in map before
    
    min_dis : float
        minimum tolerance to be consdered seperation - in metre
        
    Returns
    =======
    list
        list of unique doors records
    '''
    fixed_rst = []
    work_list = cam_pts[:]
    #print(work_list)
    temp_block = [cam_pts[0]]
    imgid_list = [int(i['img_id']) for i in work_list]
    #print(imgid_list)
    imgid_list = list(set(imgid_list))
    #imgid_fixlist = []
    
    #order the record by img id
    work_list.sort(key = lambda x:int(x['img_id']))
    
    #for first image id, pop in the door econized to the rst linst, store how many doors are there in image 0
    print(imgid_list)
    #print(getRctsByImgID(cam_pts,imgid_list[0]))
    #fix this line
    for i in getRctsByImgID(work_list,imgid_list[0]):
        i['all_img'] = str(i['img_id'])
        fixed_rst.append(i)
    #fixed_rst.append(i for i in getRctsByImgID(cam_pts,imgid_list[0]))
    #print(fixed_rst)
    last_block_count = len(fixed_rst)
    #get the records from second image id - if the id is not consistent, then quit the recog proceess
    #marker here
    for ilk in range(1,len(imgid_list)):
        temp_block = getRctsByImgID(work_list,imgid_list[ilk])
        print(len(temp_block))
        if (imgid_list[ilk] - imgid_list[ilk-1]) == 1:
            fixReptt(fixed_rst,temp_block,last_block_count,min_dis)
        else:
            for i in temp_block:
                i['all_img'] = str(i['img_id'])
                fixed_rst.append(i)
            #fixed_rst.append(i for i in temp_block)
        last_block_count = len(temp_block)
        
    return fixed_rst
    
    #extract x records from the rst list and calculate the cross-distance
    
    #if any of the distance is lower than the limit, update the door location in rst list
    
    #move to next img record
    


def fixReptt(fixed_rst,temp_block,last_block_count,min_dis):
    '''
    update fixed result based on the new input and min-distance
    
    Parameters
    ==========
    fixed_rst ; list
        by far the doors that are considered unique
        
    temp_block : list
        list of doors detected from the current image
        
    last_block_count : int
        numbers of records to pop from fixed_rst to check
        
    min_dis : float
        minimum tolerance to be consdered seperation - in metre
    '''
    
    posb_resptt = []
    new_uniq = temp_block[:]
    for i in new_uniq:
        i['all_img'] = str(i['img_id'])
    
    for i in range(last_block_count):
        posb_resptt.append(fixed_rst.pop())

    for i in range(len(posb_resptt)):
        for j in range(len(temp_block)):
            dis = calcDis(posb_resptt[i],temp_block[j])
            if dis <= min_dis:
                updateLoc(posb_resptt[i],temp_block[j])
                new_uniq.remove(new_uniq[j])
            else:
                pass
            
    for i in range(last_block_count):
        fixed_rst.append(posb_resptt.pop())
    
    fixed_rst += new_uniq
            
    
def getRctsByImgID(campt_list,int_id):
    '''
    getdoor records by image id
    '''
    rst = []
    stop_flg = False
    for campt in campt_list:
        if int(campt['img_id']) == int_id:
            rst.append(campt)
            stop_flg = True
        if stop_flg and int(campt['img_id']) != int_id:
            break
        
    return rst
    
def calcDis(campt1,campt2):
    '''
    calculate distance between two door detected
    '''
    #print(campt1)
    dis = (campt1['doorCtx'] - campt2['doorCtx']) * (campt1['doorCtx'] - campt2['doorCtx']) + (campt1['doorCty'] - campt2['doorCty']) * (campt1['doorCty'] - campt2['doorCty'])
    dis = math.sqrt(dis)
    return dis
    
def updateLoc(fixcamp,newin):
    '''
    update information if two doors are considered the same:
            * take adverage location as new locaiton
            * add new image id
    '''
    fixcamp['doorCtx'] = (fixcamp['doorCtx'] + newin['doorCtx']) / 2
    fixcamp['doorCty'] = (fixcamp['doorCty'] + newin['doorCty']) / 2
    fixcamp['all_img'] = str(fixcamp['all_img']) + '&' + str(newin['all_img'])
    