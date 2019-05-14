#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:26:22 2019

@author: s1881079
"""
import os
import urllib.request as req
#import sign_url as su
import ggvision
import cx_Oracle
import pyproj
import re

class ImgBbx:
    
    metaHead = ['img_id','name','confidence','ctx','cty','height','width','right','left','bottom','top']
    
    def __init__(self,resp_obj,gsv_obj):
        self.in_img = gsv_obj
        #self.in_img = gsv_obj.id
        self.name = resp_obj.name
        self.confidence = resp_obj.score
        self.calcGeomAttr(resp_obj.bounding_poly.normalized_vertices)
        
    def calcGeomAttr(self,lst_veritces):
        x_list = []
        y_list = []
        for coor in lst_veritces:
            x_list.append(coor['x'])
            y_list.append(coor['y'])
            
        self.ctx = sum(x_list) / len(x_list)
        self.cty = sum(y_list) / len(y_list)
        self.height = max(y_list) - min(x_list)
        self.width = max(x_list) - min(x_list)
        self.right = max(x_list)
        self.left = min(x_list)
        self.bottom = max(y_list)
        self.top = min(y_list)
        
    def genSeqParaList(self):
        seq_lst = [self.in_img,self.name,self.confidence,self.ctx,self.cty,self.height,self.width,self.right,self.left,self.bottom,self.top]
        return seq_lst
        
    def getMetaHead(self):
        return(self.metaHead)


#================================================================cls imgae


class GSVImg():
    
    metaHead = ['id','lat','lon','alt','fov','heading','pitch']
    
    def __init__(self,iter_info):
        self.id, self.lat,self.lon,self.altitude, self.fov, self.heading, self.tilt= iter_info
        self.pitch = self.tilt - 90
        
    def genBaseGsvUrl(self):
        self.size = '640x640'
        url_template = 'https://maps.googleapis.com/maps/api/streetview?size={size}&location={lat},{lon}&fov={fov}&heading={heading}&pitch={pitch}'
        return url_template.format(**vars(self))
    
    def genSeqParaList(self):
        seq_list = [self.id,self.lat,self.lon,self.altitude,self.fov, self.heading, self.pitch]
        return(seq_list)
        
    def getMetaHead(self):
        return(self.metaHead)
    
    
#============================================================== operations for google street view processing
    
def ggeUrlToLstObj(txt_fname):
    '''
    from a txt file containing google earth urls to list of GSVImg objects
    '''
    
    with open(txt_fname,'r') as inf:
        urls = inf.readlines()
        
    inf.close()
    rst = []
    img_id = 0
    
    for url in urls:
        print(url)
        paras = re.search('\@(.*),',url).group()[1:-1].split(',')
        lat = float(paras[0])
        lon = float(paras[1])
        alt = float(paras[2][:-1])
        fov = float(paras[4][:-1])
        heading = float(paras[5][:-1])
        tilt = float(paras[6][:-1])
        gsv = GSVImg([img_id,lat,lon,alt,fov,heading,tilt])
        rst.append(gsv)
        img_id += 1
    
    return rst      
    
def genLstDlUrl(lst_gsv,key,sec):
    '''
    from a list of gsv objects to list of ready-to download urls
    '''
    lst_dlurl = []
    for gsv in lst_gsv:
        base_url = gsv.genBaseGsvUrl()
        config_url = base_url + '&key=' + key
        #sign_url = su.sign_url(config_url,sec)
        #if not signed
        sign_url = config_url
        lst_dlurl.append(sign_url)
    return lst_dlurl

def downloadImg(lst_dlurl,img_folder):
    '''
    download google street view images from a list of urls, storing in specified folder
    '''
    img_id = 0
    for url in lst_dlurl:
        req.urlretrieve(url,img_folder + str(img_id) + '.jpg')
        img_id += 1
    

    
#==============================================================general procession (config add here later)
    
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

#======================================================= computer vision processing
    


def respToBbxObj(resp_objs,gsv_obj):
    lst_doors = []
    lst_windows = []
    lst_others = []
    for resp in resp_objs:
        bbx = ImgBbx(resp,gsv_obj)
        if bbx.name == 'Door':
            lst_doors.appen(bbx)
        elif bbx.name == 'Window':
            lst_windows.append(bbx)
        else:
            lst_others.append(bbx)
    return lst_doors,lst_windows,lst_others

def genImgFnList(folder_path,num_img):
    lst_fn = []
    for i in range(num_img):
        img_fn = folder_path + str(i) + '.jpg'
        lst_fn.append(img_fn)
        
    return lst_fn


#======================================================= genral run and current main
    
def cvmain(img_folder):
    '''
    place fo storing cv main functions
    input: folder path storing the images for detecting
    after running: three csv files would be created to specified the parametres of the objects detected from images
    
    '''
    num_img = 13
    lst_fn = genImgFnList(img_folder,num_img)
    img_id = 0
    all_door = []
    all_window = []
    all_other  = []
    for img_fn in lst_fn:
        #img_id = int(re.search('\\(.*?).jpg').group)
        resps = ggvision.localize_objects(img_fn)
        lst_doors,lst_windows,lst_others = respToBbxObj(resps,img_id)
        all_door += lst_doors
        all_window += lst_windows
        all_other += lst_others
        #if use re.search then delete this
        img_id += 1
    writeObjInfoCsv(all_door,img_folder,'doorBbx.csv')
    writeObjInfoCsv(all_window,img_folder,'windowBbx.csv')
    writeObjInfoCsv(all_door,img_folder,'otherBbx.csv')
    
    
def gsvmain():
    '''
    place for storing gsv main funcitons
    after running: images would be downloaded to imgs folder
    a csv file name imgMeta.csv would be created to store metadata of the google street view images
    '''
    txt_fname = '.txt'
    key = getExtInfo('locked/key.txt')
    sec = getExtInfo('locked/sec.txt')
    
    img_folder = 'imgs/'
    if os.path.exists(img_folder,) is False:
        os.makedirs(img_folder)
    
    lst_gsv = ggeUrlToLstObj(txt_fname)
    lst_dlurl = genLstDlUrl(lst_gsv,key,sec)
    downloadImg(lst_dlurl,img_folder)
    writeObjInfoCsv(lst_gsv,img_folder,'imgMeta.csv')
    

def totalmain():
    '''
    attemp to get round of database and do it all in python codes
    
    '''
    txt_fname = 'src/gge_urls.txt'
    key = getExtInfo('../locked/GSVdl_key.txt')
    sec = getExtInfo('../locked/GSVdl_sec.txt')
    
    img_folder = 'imgs/'
    if os.path.exists(img_folder,) is False:
        os.makedirs(img_folder)
        
    lst_gsv = ggeUrlToLstObj(txt_fname)
    num_img = len(lst_gsv)
    
    #downloading GSV images 
    lst_dlurl = genLstDlUrl(lst_gsv,key,sec)
    downloadImg(lst_dlurl,img_folder)
    #upper tested
    
    #wrap the following as independent codes in vertual environment
    
    lst_fn = genImgFnList(img_folder,num_img)
    img_id = 0
    all_door = []
    all_window = []
    all_other  = []
    
    for img_fn in lst_fn:
        #img_id = int(re.search('\\(.*?).jpg').group)
        resps = ggvision.localize_objects(img_fn)
        gsv = lst_gsv[img_id]
        lst_doors,lst_windows,lst_others = respToBbxObj(resps,gsv)
        all_door += lst_doors
        all_window += lst_windows
        all_other += lst_others
        #if use re.search then delete this
        img_id += 1
        
    writeObjInfoCsv(all_door,img_folder,'doorBbx.csv')
    writeObjInfoCsv(all_window,img_folder,'windowBbx.csv')
    writeObjInfoCsv(all_door,img_folder,'otherBbx.csv')
    
    #return all_door,all_window,all_other
    cam_pts = convFormat(all_door)
    return cam_pts

def convFormat(lst_bbxs):
    '''
    the function for transforming format better integrate with previous codes
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
        confid = bbx.in_img.confidence
        
        mapx,mapy = pyproj.transform(wgs84,osgb36,lon,lat)
        
        rst.append({'lat':lat,'lon':lon,'x':mapx,'y':mapy,'fov':fov,'heading':heading,'pitch':pitch,'dr_cx':door_cx,'dr_cy':door_cy,'door_score':confid})
        
    return rst

#===================================================================after wards database attemp
def connect_dbs():
    act = 's1881079'
    pwd = getExtInfo('../locked/dbs_pwd.txt')
    connect_str = act + '/' + pwd + '@geosgen'
    
    try:
        conn = cx_Oracle.connect(connect_str)
    except:
        print('Cannot link to database')
        return None

    return conn

