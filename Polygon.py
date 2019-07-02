from ctypes import *
import os
import time

VMirror=0 #1 is enable, 0 is disable
HMirror=1

x=os.getcwd() #==dirty method, couldn't find dlls otherwise==
os.chdir('C:\\DMD_drivers\\MightexPolygon')
cdll.LoadLibrary('MT_Polygon400_SDK.dll')
libc=CDLL('MT_Polygon400_SDK.dll')
os.chdir(x)
del x

class tPtnSetting(Structure):
    _fields_ = [("bitDepth", c_int),    #1,4,8
                ("PtnNumber", c_int),   #range: [1, 96/bitDepth]
                ("ABuffer1", c_int),    #reserved, set to 0
                ("TrigType", c_int),    #0,1,2,3
                ("TrigDelay", c_int),   #microseconds after external TTL pulse to display frame (trigtype =  2 or 3)
                ("TrigPeriod", c_int),  #inter-frame-interval in microsecs. only for TrigType = 1.
                ("ExposureTime", c_float),#frame duration in microsecs. cannot be > trigPeriod. 0 = trigPeriod.
                ("LEDSelection", c_int),#channel 1=0, channel2 =1...
                ("ABuffer2", c_int)]    #reserved, set to 0
    


def Polygon_init():
    returnvalue=libc.MTPLG_InitDevice(-1) #-1 = autodetect
    if returnvalue > 1:
        print "WARNING: MULTIPLE POLYGONS DETECTED"
    elif returnvalue == -3:
        print "DEVICE CONFIGURATION NOT FOUND\n"
        print "Config files must be in {dir with .dlls}\MT_Polygon400_SDK\DSIGeeeeeeeeeeee00010140421001"
    else:
        print str(returnvalue) + " Polygon device(s) successfully initialized \n"
        PolygonHandle = returnvalue 
    returnvalue=libc.MTPLG_ConnectDev(PolygonHandle)
    print "Polygon connected with value: " + str(returnvalue) + " (0 is success) \n"
    
    if returnvalue != 0:
        raise ValueError('Polygon could not initialize')
    
    '''===mirror reversal of image==='''
    returnvalue=libc.MTPLG_SetDevDisplaySetting(PolygonHandle, VMirror, HMirror)
    #print "Mirror reversals set with value " + str(returnvalue) + " (0 is success) \n"
    return PolygonHandle
    
'''===pattern sequence==='''
def Polygon_initPtn(PolygonHandle, PtnSetting):
    #set display mode to pattern sequence and set parameters
    displaymode = 1 #0 = single image, 1 = pattern sequence
    returnvalue=libc.MTPLG_SetDevDisplayMode(PolygonHandle, displaymode)
    #print returnvalue
    returnvalue=libc.MTPLG_SetDevPtnSetting(PolygonHandle, PtnSetting)
    print "Pattern settings: " +str(returnvalue)

def Polygon_uploadPtn(PolygonHandle,HBitmapSet):
    #upload patterns to polygon for a single trial
    #NOTE: MANUAL IS WRONG! THE PATTERNS ARE 1-indexed, NOT 0-indexed
    start=time.clock()
    for i in range(len(HBitmapSet)):
        returnvalue=libc.MTPLG_SetDevPtnDef(PolygonHandle, i+1, HBitmapSet[i])
        #print "Patterns uploaded with: "+str(returnvalue)
    end = time.clock()
    print 'Time to upload ' + str(len(HBitmapSet)) + ' ptns: ' + str(end-start)+'s'
def Polygon_uninit(PolygonHandle):
    returnvalue=libc.MTPLG_DisconnectDev(PolygonHandle)
    print "Polygon disconnected with value: " + str(returnvalue) + " (0 is success) \n"
    libc.MTPLG_UnInitDevice()
    
def Polygon_stopPtn(PolygonHandle):
    libc.MTPLG_StopPattern(PolygonHandle)
    
def Polygon_startPtn(PolygonHandle):
    libc.MTPLG_StartPattern(PolygonHandle)
    
def Polygon_uploadImg(PolygonHandle, HBitmap):
    returnvalue=libc.MTPLG_SetDevClrImg(PolygonHandle, HBitmap)
    print "Single image uploaded with " + str(returnvalue)
    
def Polygon_setDisplay(PolygonHandle, displaymode):
    returnvalue=libc.MTPLG_SetDevDisplayMode(PolygonHandle, displaymode)
    
def Polygon_nextPtn(PolygonHandle):
    #go to next ptn under command trigger mode
    returnvalue = libc.MTPLG_NextPattern(PolygonHandle);
    
