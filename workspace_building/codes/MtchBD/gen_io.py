#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:53:20 2019

@author: s1881079
"""
import fiona
import pandas as pd
from shapely import geometry as shg
import pyproj

__all__ = ['readShp','readGSVInfo','readCVMainRst','toSplGeom','camPtToCsv']


#general input and output

def readShp(shp_fn):
    '''
    read shapefile and return list of fiona objects
    '''

    shp = fiona.open(shp_fn,'r')

    
    l_shp = list(shp)
    shp.close()
    
    return l_shp

def readGSVInfo(csv_fn):
    '''
    read the googel street view infos, csv format, containing information:
        * camera status - img_id lan lon mapx mapy heading tilt fov
        * 2d door info - coordiante in image, height width
    store as list of campt object / campt dictionary
    
    ** CAUTION : This function is very similar to readCVMain(), consider merging
    
    Parameters
    ==========
    csv_fn : str
        file name of the csv file
        
    Returns
    =======
    list
        list of campt object/ campt dictionary
    '''
    data = pd.read_csv(csv_fn)
    rst = []
    
    osgb36 = pyproj.Proj(init = 'epsg:27700')
    wgs84 = pyproj.Proj(init='epsg:4326')
    
    for ind,rc in data.iterrows():
        mapx,mapy = pyproj.transform(wgs84,osgb36,rc.lon,rc.lat)
        
        #rst.append({'lat':rc.lat,'lon':rc.lon,'x':mapx,'y':mapy,'fov':rc.fov,'heading':rc.heading,'pitch':rc.url_pitch})
        #single test wiht door infos
        rst.append({'lat':rc.lat,'lon':rc.lon,'x':mapx,'y':mapy,'fov':rc.fov,'heading':rc.heading,'pitch':rc.url_pitch,'dr_cx':rc.door_cx,'dr_cy':rc.door_cy,'door_score':rc.score,'img_id':rc.id})
        
    return rst

def readCVMainRst(csv_fn):
    '''
    read the result of door detection process, csv format, containing information:
        * camera status - img_id lan lon mapx mapy heading tilt fov
        * 2d door info - coordiante in image, height width
    store as list of campt object / campt dictionary
    
    Parameters
    ==========
    csv_fn : str
        file name of the csv file
        
    Returns
    =======
    list
        list of campt object/ campt dictionary
    '''
    
    data = pd.read_csv(csv_fn)
    rst = []
    
    osgb36 = pyproj.Proj(init = 'epsg:27700')
    wgs84 = pyproj.Proj(init='epsg:4326')
    
    for ind,rc in data.iterrows():
        mapx,mapy = pyproj.transform(wgs84,osgb36,rc.lon,rc.lat)
        rst.append({'lat':rc.lat,'lon':rc.lon,'x':mapx,'y':mapy,'fov':rc.fov,'heading':rc.heading,'pitch':rc.pitch,'dr_cx':rc.ctx,'dr_cy':rc.cty,'door_score':rc.confidence,'img_id':rc.id})
        
    return rst

def toSplGeom(l_shp):
    '''
    from list of fiona object to list of shapely geometry object - extract the geometry of shp
    
    Parameters
    ==========
    l_shp : list
        list of fiona object, or other format that shapely supports
        
    Returns
    =======
    list
        list of shapely goem objects 
    '''
    
    l_geoms = []
    if l_shp[0]['geometry']['type'] == 'Polygon':
        pass
    else:
        print('input type: not polygon')
        return None
        
    for shp in l_shp:
        l_geoms.append(shg.shape(shp['geometry']))
        
    return l_geoms

def camPtToCsv(campt_dictlist,file_path,file_name):
    '''
    writing campt information to csv - actually suitable for dictionaries anyway
    
    Parameters
    ==========
    campt_dictlist : dict
    
    file_path : str
    
    file_name : str
    
    '''
    outfile_path = file_path + file_name
    outf = open(outfile_path,'w')
    #wirte header
    header = ','.join([i for i in campt_dictlist[0].keys()])
    outf.write(header)
    outf.write('\n')
    for camdict in campt_dictlist:
        rc = ','.join([str(i) for i in camdict.values()])
        outf.write(rc)
        outf.write('\n')
    

#def readReptToLDict(csv_fn):
#    data = pd.read_csv(csv_fn)
#    rst = []
#    
#    for ind,rc in data.iterrows():
#        
#        #rst.append({'lat':rc.lat,'lon':rc.lon,'x':mapx,'y':mapy,'fov':rc.fov,'heading':rc.heading,'pitch':rc.url_pitch})
#        #single test wiht door infos
#        rst.append({'lat':rc.lat,'lon':rc.lon,'x':mapx,'y':mapy,'fov':rc.fov,'heading':rc.heading,'pitch':rc.pitch,'dr_cx':rc.ctx,'dr_cy':rc.cty,'door_score':rc.confidence,'img_id':rc.id})
#        