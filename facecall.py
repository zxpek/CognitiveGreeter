# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:19:53 2018

@author: zhpek
"""

from text_to_speech import *

import urllib.request, urllib.parse, io
from PIL import Image
import json
import requests
import cv2

'''
Params
'''
KEY = '{Your key here}'    
GROUP = "{YourGroupID}"
URL_BASE = "https://southeastasia.api.cognitive.microsoft.com/face/v1.0/"

'''
Capture
'''
def take_snapshot():
    cam = cv2.VideoCapture(1)
    ret, frame = cam.read()
    img_name = "image.jpg"
    cv2.imwrite(img_name, frame)
    print("{} written".format(img_name))
    cam.release()

'''
Detect
'''
def detect():
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': KEY
    }
    
    url = URL_BASE + "detect"
    img = Image.open("./image.jpg")
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format = 'jpeg')
    body = imgByteArr.getvalue()
    
    req = urllib.request.Request(url, body, headers)
    global response
    response = urllib.request.urlopen(req).read()
    faceIds = []
    for i in json.loads(response):
        faceIds.append(i['faceId'])
    return(faceIds)
    
'''
Identify
'''
def identify(faceIds):
    iden_headers = {
        # Request headers
        'Content-Type' : 'application/json',
        'Ocp-Apim-Subscription-Key': KEY,
    }
    
    bodyJson = {    
        "personGroupId":GROUP,
        "faceIds":faceIds,
        'maxNumOfCandidatesReturned': 1,
        "confidenceThreshold": 0.7
    }
    
    iden_url = URL_BASE + "identify"
    response = requests.request('POST', iden_url, json=bodyJson, headers=iden_headers)
    iden_result = response.json()
    identities = []
    for i in iden_result:
        try:
            identities.append(i['candidates'][0]['personId'])
        except:
            pass
        
    return(identities)

'''
Person
'''
def namePersons(identities):
    person_headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': KEY,
    }
    names = []
    for identity in identities:
        person_url = "https://southeastasia.api.cognitive.microsoft.com/face/v1.0/persongroups/{}/persons/{}".format(GROUP,identity)
        person_response = requests.request('GET', person_url, headers = person_headers)
        name = person_response.json()['name']
        names.append(name)
        print(name)
        
    return(names)
    
'''
Wrap
'''
def findFace():
    take_snapshot()
    faceIds = detect()
    identities = identify(faceIds)
    names = namePersons(identities)
    return(names)

