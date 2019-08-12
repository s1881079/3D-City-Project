#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:36:05 2019

@author: s1881079
"""


import SemSticker as ss
import time


if __name__ == '__main__':
    print('module loaded, start testing process')
    start = time.time()
    
    #config_data = ss.readConfigToDict('testConfig.json')
    config_data = ss.readConfigToDict('demo_config.json')
    config_ed = time.time()
    conf_time = config_ed - start
    print('config file read, time:',conf_time)
    
    if ss.valConfigInfo(config_data):
        ss.semStick(config_data)
        after_ed = time.time()
        eval_pros = after_ed - config_ed
        print('run time comsuming:',eval_pros)
    else:
        print('invalid config file information')
        exit(0)