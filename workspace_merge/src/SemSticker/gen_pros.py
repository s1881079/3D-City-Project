#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:10:16 2019

@author: s1881079
"""

#import ImgPro as ip
from . import ImgPro as ip
#import MtchBD as mb
from . import MtchBD as mb

from .bdComps import SuspObj

from .simg_process import *

import os

__all__ = ['urlToSimg','locateDoors','writeDoors']

def urlToSimg(config_dict,*,outputCamloc = False,outBbxloc = False):
    '''
    from urls to SemImg objects
    
    Parameters
    ==========
    url_txt : str
        txt containing the urls of google street view - curretly support format from google earth online
    
    img_folder : str
        image folder to store the downloaded google street views
        
    key_txt : str
        file directory for txt storing google api key information
        
    outpouCamloc : bool
        whether or not to write camera location as csv file (into intm_output folder)
        
    outBbxloc : bool
        whether or not to write prelimier objected detected location as csv file (into intm_output folder)
        
        
    Returns
    =======
    list
        list of SemImg objects
        
    '''
    #key = ip.gen_process.getExtInfo(key_txt)
    key_txt = config_dict['authority']['key_txt']
    key = ip.gen_process.getExtInfo(key_txt)
    input_form = config_dict['input_data']['input_form']
     
    
    #download googl street view from txt url form
    if input_form == 'gge_url_txt': 
        url_txt = config_dict['input_data']['url_txt']
        dlimg_folder = config_dict['intm_info']['img_folder']
        
        if os.path.exists(dlimg_folder,) is False:
            os.makedirs(dlimg_folder)
            
        lst_gsv = ip.urlTxtToLstGsv(url_txt)
        ip.downloadGSV(lst_gsv,dlimg_folder,key)
        print('google street view downloaded')
        img_folder = dlimg_folder
        base_fn = url_txt.split('/')[-1][:-4]
        
    #img folder + csv info form
    elif input_form == 'gsvImg_and_infoCsv':
        gsv_folder = config_dict['input_data']['ori_gsv_folder']
        gsv_info_csv = config_dict['input_data']['gsv_info_csv']
        lst_gsv = ip.csvParaToLstGsv(gsv_info_csv)
        img_folder = gsv_folder
        base_fn = gsv_info_csv.split('/')[-1][:-4]
        
    #pure csv paras for downloading gsv
    elif input_form == 'gsv_para_csv':
        gsv_para_csv = config_dict['input_data']['gsv_info_csv']
        dlimg_folder = config_dict['intm_info']['img_folder']
        
        if os.path.exists(dlimg_folder,) is False:
            os.makedirs(dlimg_folder)
        
        lst_gsv = ip.csvParaToLstGsv(gsv_para_csv)
        ip.downloadGSV(lst_gsv,dlimg_folder,key)
        print('google street view downloaded')
        img_folder = dlimg_folder
        base_fn = gsv_para_csv.split('/')[-1][:-4]
    
    #might need selection control function in simg_process 
    print(config_dict['authority'])
    gg_cv_cred = config_dict['authority']['gg_credential']
    
    lst_simgs = control_genLstSimg(lst_gsv,img_folder,config_dict['pros_params'],gg_cv_cred)
    
#    if detection_src == 'Google_Cloud_Vision':
#        lst_simgs = ip.resp_process.genSimgLst(lst_gsv,img_folder)
#    elif detection_src == 'Customize_Model':
#        lst_simgs = ['stuff to do here']
#    else:
#        print('invalid detection keyword, check codes')
#        return None
    
    outputCamloc = config_dict['intm_info']['write_Simg_Info']
    outBbxloc = config_dict['intm_info']['write_Bbx_Info']
    
    
    if outputCamloc['Execute'] == 'True':
        writeCampts(lst_simgs,outputCamloc['out_folder'],base_fn)
        
    if outBbxloc['Execute'] == 'True':
        writeBbxs(lst_simgs,outBbxloc['out_folder'],base_fn)
    
    return lst_simgs

def control_genLstSimg(lst_gsv,img_folder,pros_params,gg_cv_cred):
    segment_img = pros_params['Image_Segmentation']['Execute']
    detection_src = pros_params['object_detection_src']
    
    if segment_img == 'True':
        print('conducting image segmentation process')
        lst_simg = []
        if detection_src == 'Google_Cloud_Vision':
            print('inside select gcv_seg branch')
            for gsv in lst_gsv:
                lst_simg.append(ip.extSegSimg(gsv,img_folder,gg_cv_cred,detection_src))
        #TODO: adding hardcode form adn tensorflow form
    else:
        lst_simg = ip.resp_process.genSimgLst(lst_gsv,img_folder,gg_cv_cred)
        
    return lst_simg
        

    
def locateDoors(lst_simg,config_dict):
    '''
    find door locations by line of sight hitting strategy
    
    Parameters
    ==========
    lst_simg : list
        list of SemImg objects containing information includiing camera GI and objects detected
        
    bdshp_fdir : str
        file directory of the building footprint
        
    sight_distance : int
        furthest distance of sight, used in builidng finding and line of sight geneation
        
    min_sepdoor : float
        minimum distance for two doors to be considered seperate
        
    Returns
    =======
    list
        list of SuspObj objects indicating doors in reality
    '''
    
    bdshp_fdir = config_dict['input_data']['bd_shp']
    sight_distance = config_dict['pros_params']['sight_distance']
    min_sepdoor = config_dict['pros_params']['min_objsep']
    
    
    bds_shp = mb.readShp(bdshp_fdir)
    bds_geom = mb.toSplGeom(bds_shp)
    
    for simg in lst_simg:
    #generate visible fan
        simg.genVisFan(sight_distance)
        #overlap with the total map and return candidate buildings
        candi_bds = mb.bd_geom.bdsWithinSight(simg.visFan,bds_geom)
        #generage line of sight for particular object - semimg.genBbxCtLines()
#        if config_dict['pros_params']['Image_Segmentation']['Execute'] == 'True':
#            simg.genBbxCtLines(sight_distance,'Door',False)
#        else:
#            simg.genBbxCtLines(sight_distance,'Door')   
        simg.genBbxCtLines(sight_distance,'Door')  
        
        for drbbx in simg.alldoors:
            dr_id = 0
            susobj_id = 'gsv' + str(simg.gsvid) + '_' + 'com_' + str(dr_id)
            dlos = drbbx.los
            #find first hit and door loc using candidate building as input
            candi_bd_id,door_ct,tar_bd_geom = mb.los_process.findFirstHit(dlos,candi_bds)
            tar_bd_id = bds_geom.index(candi_bds[candi_bd_id])
            #print('tar_bdid',tar_bd_id)
            target_buildingID = bds_shp[tar_bd_id]['properties']['ID']
            target_building_base = bds_shp[tar_bd_id]['properties']['min']
            #the third dimension
            tar_bd_base_alt = target_building_base + simg._gsv.altitude - 2.5
            door_coord = list(door_ct.coords)[0]
            door_height = getZValue(simg,drbbx,door_coord,tar_bd_base_alt)
            comp_type = 'Door'
            sobj_info = [[simg],susobj_id,comp_type,target_buildingID,door_coord[0],door_coord[1],door_height]
            #print()
            dr_susobj = SuspObj(sobj_info)
            drbbx.setSusObj(dr_susobj)
            dr_id += 1
        
    #after this process, all bbx would contain the suspect object information
    uniq_objs = findUniqueDetection(lst_simg,min_sepdoor)
    
    return uniq_objs
    

def writeDoors(lst_doors,config_out):
    '''
    write door suspobj to csv
    '''
    #pending function for writing door object to csv
    
    out_folder = config_out['result_folder']
    out_csv = config_out['output_csv']
    
    ip.gen_process.writeObjInfoCsv(lst_doors,out_folder,out_csv)
    
    out_gml = 'Door.gml'
    writeDoorCityGML(lst_doors,out_folder,out_gml)


def writeCampts(lst_simgs,out_folder,base_fn):
    '''
    write camerapoints(simg) to csv
    '''
    out_camloc_csv = base_fn + '_camloc.csv'
    ip.gen_process.writeObjInfoCsv(lst_simgs,out_folder,out_camloc_csv)


def writeBbxs(lst_simgs,out_folder,base_fn):
    '''
    write bounding box objects to csv
    '''
    out_door_csv = base_fn + '_doorbbx.csv'
    all_door = getBbxsByType(lst_simgs,'Door')
    ip.gen_process.writeObjInfoCsv(all_door,out_folder,out_door_csv)
    
    out_window_csv = base_fn + '_windowbbx.csv'
    all_window = getBbxsByType(lst_simgs,'Window')
    ip.gen_process.writeObjInfoCsv(all_window,out_folder,out_window_csv)
    
    out_other_csv = base_fn + '_otherbbx.csv'
    all_others = getBbxsByType(lst_simgs,'Others')
    ip.gen_process.writeObjInfoCsv(all_others,out_folder,out_other_csv)

def writeDoorCityGML(lst_doors,out_folder,out_gml):
    metafile = out_folder + out_gml
    with open(metafile, 'w') as wfile:
        for door in lst_doors:
            line = door.outCityGML()
            wfile.write(line + '\n')
            
    wfile.close()

#might still add some format checking and error system
    
