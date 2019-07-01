#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:14:57 2019

@author: s1881079
"""
#import re

from .bbx import Bbx
#from .. import simg.SemImg
#from .gsv import GSV

import sys
sys.path.append('../')
from simg import SemImg

from .ggvision import localize_objects


__all__ = ['respToBbxObjs','genSimgLst']


def respToBbxObjs(resp_objs):
    '''
    ggvision response (per image) to boundingbox objects
    '''
    lst_doors = []
    lst_windows = []
    lst_others = []
    for resp in resp_objs:
        bbx = Bbx(resp)
        if bbx.name == 'Door':
            lst_doors.append(bbx)
        elif bbx.name == 'Window':
            lst_windows.append(bbx)
        else:
            lst_others.append(bbx)
    return [lst_doors,lst_windows,lst_others]


def objDetect(lst_gsv,img_fn):
    '''
    turned into ghost function after modulized
    '''
    resps = localize_objects(img_fn)
    print('getting response back')
    print(resps)
    #img_id = int(img_fn[:-4])
    #img_id = int(re.search('(\d+).jpg',img_fn).group(1))
    print('curretn processing img id:')
    #gsv = lst_gsv[img_id]
    lst_doors,lst_windows,lst_others = respToBbxObjs(resps)
    
    return lst_doors,lst_windows,lst_others 
    

def genSimgLst(lst_gsv,image_folder):
    lst_simg = []
    
    for gsv in lst_gsv:
        imgdir = image_folder + gsv.fn
        resps = localize_objects(imgdir)
        lst_bbxs = respToBbxObjs(resps)
        simg_obj = SemImg(gsv,lst_bbxs)
        lst_simg.append(simg_obj)
        
    
#    for img_fn in lst_imgfn:
#        resps = localize_objects(img_fn)
#        img_id = int(re.search('(\d+).jpg',img_fn).group(1))
#        gsv = lst_gsv[img_id]
#        lst_bbx = respToBbxObjs(resps)
#        simg_obj = SemImg(gsv,lst_bbx)
#        lst_simg.append(simg_obj)
        
    return lst_simg
        
        
