#!/usr/local/bin/python

#python Version 2.7.2
import numpy as np
import camera as cm
import channel as ch
import opticalChain as oc

class Telescope:
    def __init__(self, dir, atmFile=None):
        #***** Private Variables *****
        self.__cameraFile = dir+'/camera.txt'
        self.__opticalChainFile = dir+'/opticalChain.txt'
        self.__channelFile = dir+'/channels.txt'
        
        #***** Public Variables *****
        self.dir = dir
        self.name = dir.rstrip('/').split('/')[-1]
        self.camera = cm.Camera(self.__cameraFile)
        #Unpack channel file
        output = np.loadtxt(self.__channelFile, dtype=np.str)
        keyArr = output[0]
        elemArr = output[1:]
        #Create optic objects and store them into an array
        self.chanArr = []
        for elem in elemArr:
            dict = {}
            for i in range(len(keyArr)):
                dict[keyArr[i]] = elem[i]
            self.chanArr.append(ch.Channel(dict, self.camera, self.__opticalChainFile, atmFile))
        self.numChans = len(self.chanArr)
        #Gather channels into pixels
        self.pixels = {}
        for channel in self.chanArr:
            if channel.pixelID in self.pixels.keys():
                self.pixels[channel.pixelID].append(channel)
            else:
                self.pixels[channel.pixelID] = [channel]
