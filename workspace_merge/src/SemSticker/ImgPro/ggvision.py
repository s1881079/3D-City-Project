#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:30:31 2019

@author: s1881079
"""

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def localize_objects(file_name,gg_api_cred):

    # Instantiates a client
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../../locked/GSVdl-600f404afce8.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=gg_api_cred
    #environment credential setting - notice: not availale if clone
    
    client = vision.ImageAnnotatorClient()
    
    # The name of the image file to annotate
    #file_name = os.path.join(
    #    os.path.dirname(__file__),
    #    'resources/wakeupcat.jpg')
    
    #test image
    #file_name = 'imgs/5.jpg'
    
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)
    
    # Performs label detection on the image file
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations
    
    #print('Number of objects found: {}'.format(len(objects)))
    #for object_ in objects:
    #    print('\n{} (confidence: {})'.format(object_.name, object_.score))
    #    print('Normalized bounding polygon vertices: ')
    #    for vertex in object_.bounding_poly.normalized_vertices:
    #        print(' - ({}, {})'.format(vertex.x, vertex.y))
    
    #print(objects)
    return objects

#localize_objects('imgs_pre/5.jpg')