#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 14:12:34 2019

@author: s1881079
"""

#from .simg import SemImg
import numpy as np

__all__ = ['getBbxsByType','findUniqueDetection']

def getBbxsByType(lst_simg,tp_name = 'Door'):
    rst = []
    if tp_name == 'Door':
        for simg in lst_simg:
            simg.linkBbxGsvID()
            rst += simg.alldoors
        pass
    elif tp_name == 'Window':
        for simg in lst_simg:
            simg.linkBbxGsvID()
            rst += simg.allwindows
        pass
    elif tp_name == 'Others':
        for simg in lst_simg:
            simg.linkBbxGsvID()
            rst += simg.allothers
        pass
    else:
        print('wrong type name')
        
    return rst

def filtWithDoors(lst_simg):
    rst = []
    for simg in lst_simg:
        if simg.alldoors != []:
            rst.append(simg)
            
    return rst

def orderByGsvID(lst_simg):
    lst_simg.sort(key = lambda x:x.gsvid)
    
    
#def fixMultiDetection(lst_simg,min_dis):
#    conf_objs = []
#    workspace = []
#    
#    imgid_list = [i.gsvid for i in lst_simg]
#    imgid_list = list(set(imgid_list))
#    
#    orderByGsvID(lst_simg)
#    
#    for doorBbx in lst_simg[0].alldoors:
#        workspace.append(doorBbx.susObj)
#        
#    last_block_count = len(workspace)
#    
#    for ilk in range(1,len(imgid_list)):
#        temp_block = lst_simg[ilk].alldoors
#        if (imgid_list[ilk] - imgid_list[ilk-1]) == 1:
#            fixReptt(workspace,temp_block,last_block_count,min_dis)
#        else:
#            for i in temp_block:
#                i.susObj.setAllSimg([lst_simg[ilk]])
#                workspace.append(i)
#                
#        last_block_count = len(temp_block)
#        
#    last_simg = lst_simg[0]
#        
#    for ilk in range(len(imgid_list)):
#        this_simg = lst
#    
#    
#def fixReptt(fixed_rst,temp_block,last_block_count,min_dis):
#    posb_resptt = []
#    new_uniq = temp_block[:]
#    
    
#test for new structure
    
def findUniqueDetection(lst_simg,min_dis):
    '''
    return new list indicaitng uniqeu objects
    
    Parameters
    ==========
    lst_simg : list
        list of semImg object
    min_dis
        minimum distance for separating two different objects in reality
        
    Returns
    =======
    list
        list of SuspObj objects indicating unique doors detected
    '''
    alll_doorbbxs = getBbxsByType(lst_simg,'Door')
    alll_doorobjs = [i.susObj for i in alll_doorbbxs]
    print('length of susdoors',len(alll_doorobjs))
    for i in alll_doorbbxs:
        print(i)
    dis_mat = caulcObjDisMatrix(alll_doorobjs)
    rowid_arr,colid_arr = np.where(dis_mat < min_dis)
    
    worked_list = []
    trans = []
    unique_row = np.unique(rowid_arr)
    #print('lenth of unique_row',len(unique_row))
    for i in unique_row:
        if i in worked_list:
            continue
        lst_col = []
        for k in range(len(rowid_arr)):
            if rowid_arr[k] == i:
                if rowid_arr[k] >= colid_arr[k]:
                    continue
                lst_col.append(colid_arr[k])
                worked_list.append(colid_arr[k])
        trans.append([i,lst_col])
        
    unique_objs = []
    for rc in trans:
        obj = alll_doorobjs[rc[0]]
        if len(rc[1]) == 0:
            newobj = obj
        else:
            for repid in rc[1]:
                rep = alll_doorobjs[repid]
                newobj = obj.mergeObj(rep)
        print(newobj)
        unique_objs.append(newobj)
        
    return unique_objs
    
    
def caulcObjDisMatrix(lst_doors):
    '''
    calculate distance matrix
    
    Parameters
    ==========
    lst_doors : list
        list of SuspObj object
        
    Returns
    =======
    numpy.array
        distance matrix
    '''
    dim = len(lst_doors)
    dis_mat = np.zeros([dim,dim])
    for i in range(dim):
        for j in range(dim):
            if i >= j:
                continue
            
            dis_mat[i][j] = lst_doors[i].calcDis(lst_doors[j])
            
    return dis_mat
            
            