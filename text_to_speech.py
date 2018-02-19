# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:39:23 2018

@author: zhpek
"""
import urllib.request
import vlc
import time

'''
Define URLs, params
'''
syn_url = "https://speech.platform.bing.com/synthesize"
token_url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
token_time = 0
audio_format = "audio-16khz-32kbitrate-mono-mp3"
'''
Functions
'''
def getToken(TTS_KEY):
    token_header = {'Ocp-Apim-Subscription-Key': TTS_KEY, 'Content-Length':0}
    token_req = urllib.request.Request(token_url,str.encode("a"), headers=token_header)
    token_r = urllib.request.urlopen(token_req)
    token = token_r.read()
    return(token)

def getAudio(name, token, audio_format = audio_format):
    syn_header = {'X-Microsoft-OutputFormat':audio_format,
                  'Content-Type': 'application/ssml+xml',
                  'Authorization': 'Bearer ' + token.decode('utf-8')
            }
    text = "Hello {}. Welcome back.".format(", ".join(str(i) for i in name))
    body = "<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'><break time='1000ms' /> {}</voice></speak>".format(text)
    syn_req = urllib.request.Request(syn_url, str.encode(body), headers=syn_header)
    syn_r = urllib.request.urlopen(syn_req)
    output = syn_r.read()
    return(output)

def playAudio(output):
    with open('play.mp3','wb') as f:
        f.write(output)
    p = vlc.MediaPlayer('./play.mp3')
    p.play()
    
def say(name, TTS_KEY):
    token = getToken(TTS_KEY)
    audio = getAudio(name, token)
    playAudio(audio)