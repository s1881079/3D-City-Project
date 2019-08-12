#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:29:22 2019

@author: s1881079
"""

import pyproj
from .bbx import Bbx

__all__ = ['getExtInfo','writeObjInfoCsv']

def getExtInfo(ei_path):
    '''
    read security information from exterior paths
    '''
    with open(ei_path) as infile:
        einfo = infile.readline()
        
    return einfo

def writeObjInfoCsv(lst_objs,folder,filename):
    '''
    write images meta data 
    
    '''
    if len(lst_objs) == 0:
        return None
    else:
        pass
    
    
    metafile = folder + filename
    with open(metafile, 'w') as wfile:
        headlist = lst_objs[0].getMetaHead()
        line = ','.join(str(i) for i in headlist)
        wfile.write(line + '\n')
        for obj in lst_objs:
            paralist = obj.genSeqParaList()
            line = ','.join(str(i) for i in paralist)
            wfile.write(line + '\n')
            
    wfile.close()


def convFormat(lst_bbxs):
    '''
    ghost function - might not be needed any more since converted to objects- the function for transforming format better integrate with previous codes
    '''
    rst = []
    for bbx in lst_bbxs:
        lat = bbx.in_img.lat
        lon = bbx.in_img.lon
        fov = bbx.in_img.fov
        heading = bbx.in_img.heading
        pitch = bbx.in_img.pitch
        door_cx = bbx.ctx
        door_cy = bbx.cty
        confid = bbx.confidence
        
        osgb36 = pyproj.Proj(init = 'epsg:27700')
        wgs84 = pyproj.Proj(init='epsg:4326')
        
        mapx,mapy = pyproj.transform(wgs84,osgb36,lon,lat)
        
        rst.append({'lat':lat,'lon':lon,'x':mapx,'y':mapy,'fov':fov,'heading':heading,'pitch':pitch,'dr_cx':door_cx,'dr_cy':door_cy,'door_score':confid})
        
    return rst

