# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 12:15:54 2018

@author: zhpek
"""

from text_to_speech import *
from facecall import *
import threading
import time
       
        
def greet():
    names = findFace()
    if len(names) > 0:
        say(names)
        time.sleep(10)
        
def run():
    detected = {}
    while True:
        try:
            names = findFace()
            readNames = []
            for name in names:
                if name not in detected:
                    print('Adding {} to detected'.format(name))
                    detected[name] = 0

                if time.time() - detected[name]> 600:
                    print('Have not seen {} recently.'.format(name))
                    readNames.append(name)
                    detected[name] = time.time()
            print(readNames)
            if len(readNames) > 0:
                say(readNames)
                time.sleep(10)
            print(detected)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Terminating.")
            break
'''
Run
'''
if __name__ == "__main__":
#    take_snapshot()
    run()
