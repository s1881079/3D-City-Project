#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:12:18 2019

@author: s1881079
"""

import MtchBD as mb
import os

if __name__ == "__main__":
    #shp_fn = 'SJ89_GM_buildings_districts_270315.shp'
    #workspace = os.getcwd()
    os.chdir('../SJ89_GM_buildings_districts_270315')
    shp_fn = 'resstreet_clip.shp'
    #csv_fn = '../gsv_info.csv'
    
    bds_shp = mb.readShp(shp_fn)
    bds_geom = mb.toSplGeom(bds_shp)
    
    #=======================================about way to capture camera points
    
    #origin way: read from manual format csv
    #csv_fn = '../gsv_info_single_test.csv'
    #cam_pts = mb.readGSVInfo(csv_fn)
    
    #half-auto: read from rst_csv from CVmain
    #current testing methods
    csv_fn = '../../workspace_CV/imgs_resstreet/doorBbx.csv'
    cam_pts = mb.gen_io.readCVMainRst(csv_fn)
    # fintest - change this part to read assemimg object - either from csv or geneated from other process
    
    
    
    #fully-auto: read directly from CVmain -function need further defined 
    #use this after the whole pipeline is finished
    #cam_pt = workCV.CVmain()
    
    sight_distance = 50
    
    for cam_pt in cam_pts:
    #simg_with_door = filtWithDoors(lst_simg)
    #for simg in simg_with_door:
        ##fin test - change this part - for each semiimg in thelist
        ##the folloing step could be organized as - findDoor()
        ##generate visible fan
        #simg.genVisFan(sight_distance)
        ##overlap with the total map and return candidate buildings
        #candi_bds = mb.bd_geom.bdsWithinSight(simg.visFan,bds_geom)
        ##generage line of sight for particular object - semimg.genBbxCtLines()
        #simg.genBbxCtLines(sight_distance,'Door')
        ##for bbx in semimg(simg.getDoors()),dlos = bbx.los
        #for drbbx in simg.alldoors:
        #   dlos = drbbx.los
        ##find first hit and door loc using candidate building as input
        #   candi_bd_id,door_ct,tar_bd_geom = mb.los_process.findFirstHit(dlos,candi_bds)
        #   tar_bd_id = bds_geom.index(candi_bds[candi_bd_id])
        #   target_biuldingID = bds_shp[tar_bd_id]['properties']['ID']
        #   door_coord = list(door_ct.coords)[0]
        #   sobj_info = [[simg],target_buildingID,door_coord[0],door_coord[1]]
        #   drbbx.setSusObj(SusObj(sobj_info))
        #
        ##after this process, all bbx would contain the suspect object information
        #new function for reducing repetition in simgs - foo(simg)
        #uniq_objs = findUniqueDetection(lst_simg,0.6)
        #write output 
        
        
        target_buildingIndex, look_centre, doorLoc = mb.findBuildingInSight(cam_pt,bds_geom,sight_distance)
        target_buildingID = bds_shp[target_buildingIndex]['properties']['ID']
        #print('looking at building')
        #print(bds_shp[target_buildingIndex]['id'])
        cam_pt['t_building'] = target_buildingID
        cam_pt['eye_ctx'] = list(look_centre.coords)[0][0]
        cam_pt['eye_cty'] = list(look_centre.coords)[0][1]
        cam_pt['doorCtx'] = list(doorLoc.coords)[0][0]
        cam_pt['doorCty'] = list(doorLoc.coords)[0][1]
        #should find a better way rather than list to do the above process
        #theoretically the look centre would be a2d coordinate, find a properformat to store it
    
    #print(cam_pts[0].keys())
    out_path = '../rst/'
    
    if os.path.exists(out_path,) is False:
        os.makedirs(out_path)
        
    out_ori_csv = 'resstreet_result_infos.csv'
    mb.gen_io.camPtToCsv(cam_pts,out_path,out_ori_csv)
    
    #adding process for detectin multi-detection
    cam_pts = mb.fixMultiDetection(cam_pts,0.6)
        
    #the result would be the updated cam_pts dictionary for later operations
    
    out_uniq_csv = 'resstreet_result_infos_rmrepts.csv'
    
    mb.gen_io.camPtToCsv(cam_pts,out_path,out_uniq_csv)
    