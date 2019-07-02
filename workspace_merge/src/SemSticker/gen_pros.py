#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:10:16 2019

@author: s1881079
"""

import ImgPro as ip
import MtchBD as mb

from bdComps import SuspObj

from simg_process import *

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
    key = config_dict['authority']['key_txt']
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
        
    #img folder + csv info form
    elif input_form == 'gsvImg_and_infoCsv':
        gsv_folder = config_dict['input_data']['ori_gsv_folder']
        gsv_info_csv = config_dict['input_data']['gsv_info_csv']
        lst_gsv = ip.csvParaToLstGsv(gsv_info_csv)
        img_folder = gsv_folder
    
    #might need selection control function in simg_process 
    
    lst_simgs = control_genLstSimg(lst_gsv,img_folder,config_dict['pros_params'])
    
#    if detection_src == 'Google_Cloud_Vision':
#        lst_simgs = ip.resp_process.genSimgLst(lst_gsv,img_folder)
#    elif detection_src == 'Customize_Model':
#        lst_simgs = ['stuff to do here']
#    else:
#        print('invalid detection keyword, check codes')
#        return None
    
    out_folder = '../../intm_output/'
    base_fn = url_txt.split('/')[-1][:-4]
    
    if outputCamloc:
        writeCampts(lst_simgs,out_folder,base_fn)
        
    if outBbxloc:
        writeBbxs(lst_simgs,out_folder,base_fn)
    
    return lst_simgs

def control_genLstSimg(lst_gsv,img_folder,pros_params):
    segment_img = pros_params['Image_Segmentation']['Execute']
    detection_src = pros_params['object_detection_src']
    
    if segment_img == 'True':
        lst_simg = []
        if detection_src == 'Google_Cloud_Vision':
            print('inside select gcv_seg branch')
            for gsv in lst_gsv:
                lst_simg.append(ip.extSegSimg(gsv,img_folder,detection_src))
        #TODO: adding hardcode form adn tensorflow form
    else:
        lst_simg = ip.resp_process.genSimgLst(lst_gsv,img_folder)
        
    return lst_simg
        

    
def locateDoors(lst_simg,bdshp_fdir,sight_distance = 50,min_sepdoor =  0.6):
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
    bds_shp = mb.readShp(bdshp_fdir)
    bds_geom = mb.toSplGeom(bds_shp)
    
    for simg in lst_simg:
    #generate visible fan
        simg.genVisFan(sight_distance)
        #overlap with the total map and return candidate buildings
        candi_bds = mb.bd_geom.bdsWithinSight(simg.visFan,bds_geom)
        #generage line of sight for particular object - semimg.genBbxCtLines()
        simg.genBbxCtLines(sight_distance,'Door')
        
        for drbbx in simg.alldoors:
           dlos = drbbx.los
        #find first hit and door loc using candidate building as input
           candi_bd_id,door_ct,tar_bd_geom = mb.los_process.findFirstHit(dlos,candi_bds)
           tar_bd_id = bds_geom.index(candi_bds[candi_bd_id])
           target_buildingID = bds_shp[tar_bd_id]['properties']['ID']
           door_coord = list(door_ct.coords)[0]
           sobj_info = [[simg],target_buildingID,door_coord[0],door_coord[1]]
           print()
           dr_susobj = SuspObj(sobj_info)
           drbbx.setSusObj(dr_susobj)
        
    #after this process, all bbx would contain the suspect object information
    uniq_objs = findUniqueDetection(lst_simg,0.6)
    
    return uniq_objs
    

def writeDoors(lst_doors,out_folder,out_csv):
    '''
    write door suspobj to csv
    '''
    #pending function for writing door object to csv
    ip.gen_process.writeObjInfoCsv(lst_doors,out_folder,out_csv)


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


#might still add some format checking and error system
    
