from ctypes import *
import os
x=os.getcwd() #==dirty method, couldn't find dlls otherwise==
os.chdir('C:\\git\\Olfalab_Voyeur_protocols_and_files\\Python\\Utilities\\Polygon\\Drivers')
cdll.LoadLibrary('Mightex_LEDDriver_SDK.dll')
libc=CDLL('Mightex_LEDDriver_SDK.dll')
os.chdir(x)
del x
import time

class TLedChannelData(Structure):
    _pack_ = 1
    _fields_ = [("Normal_CurrentMax", c_int),
                ("Normal_CurrentSet", c_int),
                ("Strobe_CurrentMax", c_int),
                ("Strobe_RepeatCnt", c_int),
                ("Strobe_RepeatCnt", c_int),
                ("Strobe_Profile", c_int),
                ("Trigger_CurrentMax", c_int),
                ("Trigger_Polarity", c_int),
                ("Trigger_Profile", c_int)]
        
def LED_init():
    returnvalue=libc.MTUSB_LEDDriverInitDevices()
    if returnvalue==1:
        print str(returnvalue) + " LED controller initialized\n"
    elif returnvalue > 1:
        print "WARNING!! " + str(returnvalue) + "devices found\n"
    DeviceHandle=libc.MTUSB_LEDDriverOpenDevice(0)
    return DeviceHandle


def LED_set(DeviceHandle):
    channelSet = range(1,14) #one-based indexing
    ChannelParams=TLedChannelData(1000,1000)
    
    for channel in channelSet:
        returnvalue=libc.MTUSB_LEDDriverSetNormalPara(DeviceHandle,channel,ChannelParams)


def LED_on(DeviceHandle):
    start=time.clock()
    channelSet = range(1,14) #one-based indexing
    
    for channel in channelSet:
        returnvalue=libc.MTUSB_LEDDriverSetMode(DeviceHandle,channel,1)
        #print "Ch" +str(channel)+" enabled with value " + str(returnvalue) + " (0 is success)"
    end = time.clock()
    print 'Time turn on LED '  + str(end-start)+'s'
    
def LED_off(DeviceHandle):
    channelSet = range(1,14) #one-based indexing
    for channel in channelSet:
        returnvalue=libc.MTUSB_LEDDriverSetMode(DeviceHandle,channel,0)
        #print "Ch" +str(channel)+" disabled with value " + str(returnvalue) + " (0 is success) \n"
    

def LED_uninit(DeviceHandle):
    returnvalue=libc.MTUSB_LEDDriverCloseDevice(DeviceHandle)
    print "LED un-initialized with value " + str(returnvalue) + " (0 is success) \n"