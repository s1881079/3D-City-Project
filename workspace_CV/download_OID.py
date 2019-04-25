# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 11:09:02 2019

@author: hp
"""

import pandas as pd
#import numpy as np
import os
import tensorflow as tf
import io
#import logging
#import random
import sys
import hashlib
import PIL.Image
from urllib import request

sys.path.append('../models/research/object_detection/')
from utils import dataset_util
#the python file: '/models/research/object_detection/utils/dataset_utils.py'

#this script was run on eddie3 -result stored in scratch, should chage later

class open_image_dataset:
    classname_csv = 'https://storage.googleapis.com/openimages/2018_04/class-descriptions-boxable.csv'
    
    val_image_csv = 'https://storage.googleapis.com/openimages/2018_04/validation/validation-images-with-rotation.csv'
    val_box_csv = 'https://storage.googleapis.com/openimages/2018_04/validation/validation-annotations-bbox.csv'
    
    def download_val(self):
        print('start downloading csv stuff')
        folder = '/exports/eddie/scratch/s1881079/val'
        if os.path.exists(folder,) is False:
            os.makedirs(folder)
        image_csv_path = folder + '/image.csv'
        box_csv_path = folder + '/box.csv'
        classname_csv_path = folder + '/classname.csv'
        
        if os.path.exists(image_csv_path) is False:
            print('start downloading image csv')
            request.urlretrieve(self.val_image_csv,image_csv_path)
        if os.path.exists(box_csv_path) is False:
            print('start downloading box csv')
            request.urlretrieve(self.val_box_csv,box_csv_path)
        if os.path.exists(classname_csv_path) is False:
            print('start downloading calssname csv')
            request.urlretrieve(self.classname_csv,classname_csv_path)
            print('download val complete')
            
    def create_tfrecord(self,folder,keywords):
        format_error = 0
        url_error = 0
        door_img = 0
        print('start creating tfrecord')
        image_csv_path = folder + '/image.csv'
        box_csv_path = folder + '/box.csv'
        classname_csv_path = folder + '/classname.csv'
        
        df_image = pd.read_csv(image_csv_path)
        df_box = pd.read_csv(box_csv_path)
        df_classname = pd.read_csv(classname_csv_path,names=['labelID','LabelName'])
        
        data = df_classname[df_classname['LabelName'] == keywords]
        data = pd.merge(data,df_box,left_on = 'labelID',right_on = 'LabelName',how = 'right')
        data = pd.merge(data,df_image,left_on = 'ImageID',right_on = 'ImageID',how = 'right')
        data = data[data['labelID'].notna() & data['ImageID'].notna()]
        door_img = data.size
        
        folder_path = folder + '/' + keywords + '/'
        if os.path.exists(folder_path) is False:
            os.makedirs(folder_path)
            
        tfrecord_file = folder_path + keywords + '.tfrecord'
        writer = tf.python_io.TFRecordWriter(tfrecord_file)
        
        for index,row in data.iterrows():
            file_name = row['ImageID'] + '.jpg'
            file_path = folder_path + file_name
            if os.path.exists(file_path) is False:
                #print(row['OriginalURL'])
                try:
                    request.urlretrieve(row['OriginalURL'],file_path)
                except:
                    print('url retrieve failed, continue')
                    url_error += 1
                    continue
            with tf.gfile.GFile(file_path,'rb') as fid:
                encoded_jpg = fid.read()
            encoded_jpg_io = io.BytesIO(encoded_jpg)
            image = PIL.Image.open(encoded_jpg_io)
            if image.format != 'JPEG':
                print('file format error' + file_path)
                format_error += 1
                os.remove(file_path)
                continue
            image.close()
            key = hashlib.sha256(encoded_jpg).hexdigest()
            
            xmin = []
            ymin = []
            xmax = []
            ymax = []
            classes = []
            classes_text = []
            width = image.width
            height = image.height
            
            xmin.append(float(row['XMin']))
            xmax.append(float(row['XMax']))
            ymin.append(float(row['YMin']))
            ymax.append(float(row['YMax']))
            
            classes.append(int(1))
            classes_text.append(keywords.encode('utf8'))
            
            #===================== this part is influenced by the model packages - writing information to tfrecord file
            
            
            example = tf.train.Example(features=tf.train.Features(feature={
                'image/height': dataset_util.int64_feature(int(height)),
              'image/width': dataset_util.int64_feature(int(width)),
              'image/filename': dataset_util.bytes_feature(file_name.encode('utf8')),
              'image/source_id': dataset_util.bytes_feature(file_name.encode('utf8')),
              'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
              'image/encoded': dataset_util.bytes_feature(encoded_jpg),
              'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
              'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
              'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
              'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
              'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
              'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
              'image/object/class/label': dataset_util.int64_list_feature(classes),
            }))
    
            writer.write(example.SerializeToString())
            os.remove(file_path)
            print('file' + file_path)
        writer.close()
        print('create' + tfrecord_file + 'success')
        print('door img:' + str(door_img))
        print('format error:' + str(format_error))
        print('url error' + str(url_error))
        
    def create_val_tfrecord(self,keywords):
        self.download_val()
        self.create_tfrecord('/exports/eddie/scratch/s1881079/val',keywords)
        
        
        
dataset = open_image_dataset()
#dataset.download_val()
dataset.create_val_tfrecord('Door')
