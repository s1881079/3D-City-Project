#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:58:26 2019

@author: s1881079
"""

import SemSticker as ss


if __name__ == '__main__':
    config_data = ss.readConfigToDict('config.json')
    
    if ss.valConfigInfo(config_data):
        ss.semStick(config_data)
    else:
        print('invalid config file information')