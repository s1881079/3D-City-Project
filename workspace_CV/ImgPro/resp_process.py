#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:14:57 2019

@author: s1881079
"""
import re

from .bbx import ImgBbx
#from .gsv import GSVImg

from .ggvision import localize_objects


__all__ = ['respToBbxObj','objDetect']


def respToBbxObj(resp_objs,gsv_obj):
    lst_doors = []
    lst_windows = []
    lst_others = []
    for resp in resp_objs:
        bbx = ImgBbx(resp,gsv_obj)
        if bbx.name == 'Door':
            lst_doors.append(bbx)
        elif bbx.name == 'Window':
            lst_windows.append(bbx)
        else:
            lst_others.append(bbx)
    return lst_doors,lst_windows,lst_others


def objDetect(lst_gsv,img_fn):
    resps = localize_objects(img_fn)
    print('getting response back')
    print(resps)
    #img_id = int(img_fn[:-4])
    img_id = int(re.search('(\d+).jpg',img_fn).group(1))
    print('curretn processing img id:')
    gsv = lst_gsv[img_id]
    lst_doors,lst_windows,lst_others = respToBbxObj(resps,gsv)
    
    return lst_doors,lst_windows,lst_others 
    

