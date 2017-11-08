import getch
import os
import numpy as np
import matplotlib.pyplot as plt
import ALP
import Patterns
import time

keypress='1'
command='None'

LR_STEP=1
UD_STEP=1
WIDTH_STEP=1
HEIGHT_STEP=1
Width = 48
Height = 40
esc_char=chr(27).encode()


#===define ALP field of illumination===
Patterns.ImWidth = Width #60
Patterns.ImHeight = Height #50

DMDWidth=1024
DMDHeight=768


#===initialize image===
x1=271 #x is row, y is column 
x2=x1+Height
y1=464
y2=y1+Width

'''
  #(a,b,c,d)
    x1,x2: right(-) left (+)
    y1,y2: down(-) up (+)

("+str(x1)+", "+str(y1)+")" + " ("+str(x2)+", "+str(y2)+")"
'''



stimulated=np.zeros([DMDHeight,DMDWidth])
stimulated[x1:x2,y1:y2]=255

#create checkerboard for use as mask
checkerboard=Patterns.checkerboard(9)/255 #use as mask

ptn=Patterns.checkerboard(10)
new_seq=Patterns.ALPimg([ptn])
stimulated_foo=new_seq[0]


#===initalize ALP===
ALP.init()
bitnum = 8L
picnum = 1L
stimon_time = 100000L
stimoff_time = 0L

seq_id=ALP.seq_alloc(bitnum,picnum)
ALP.seq_timing(seq_id, stimon_time, stimoff_time)
ALP.seq_upload(seq_id, [stimulated])

update=True
checkerboard_mode=True
b=1
while keypress != esc_char:
    keypress=getch.getch()
    
    upload_alp=False
    if keypress=='o':
        LR_STEP=LR_STEP+1
    elif keypress=='p':
        LR_STEP=max(0,LR_STEP-1)
    elif keypress=='k':
        UD_STEP=UD_STEP+1
    elif keypress=='l':
        UD_STEP=max(0,UD_STEP-1)
    elif keypress=='8':
        Height=min(DMDHeight,Height+HEIGHT_STEP)
        upload_alp=True
    elif keypress=='2':
        Height=max(1,Height-HEIGHT_STEP)
        upload_alp=True        
    elif keypress=='4':
        Width=Width+(WIDTH_STEP)
        upload_alp=True
    elif keypress=='6':
        Width=max(1,Width-WIDTH_STEP)
        upload_alp=True  
    elif keypress=='\r':
        plt.imshow(stimulated)
        plt.show()
    elif keypress=='m':
        update = not update
    elif keypress=='i':
        checkerboard=checkerboard[::-1] #invert checkerboard
        upload_alp=True
    elif keypress=='c':
        b=1
        checkerboard_mode=not checkerboard_mode
        upload_alp=True
    elif keypress=='b': #black
        b=not b
        upload_alp=True
    elif keypress=='n':
        #b=np.load('../Pattern/ALP_intensity.npy')
        #b=np.zeros(b.shape)+100.0
        upload_alp=True
        
        
    #===update image===
    # move images 
    if keypress == 'a':
        y1=max(0,y1-LR_STEP)
        upload_alp=True
    elif keypress == 'd':
        y1=min(DMDWidth,y1+LR_STEP)
        upload_alp=True
    elif keypress == 'w':
        x1=max(0,x1-UD_STEP)
        upload_alp=True
        image_changed=1
    elif keypress == 's':
        x1=min(DMDHeight,x1+UD_STEP)
        upload_alp=True        
    
    x2=min(DMDHeight,x1+Height)
    y2=min(DMDWidth,y1+Width)

    stimulated[:]=0 #clear
    '''
    #==frame==
    stimulated[x1,y1:y2]=255.0*b
    stimulated[x2,y1:y2]=255.0*b
    stimulated[x1:x2,y1]=255.0*b
    stimulated[x1:x2,y2]=255.0*b
    '''
    #==checkerboard==
    stimulated[x1:x2,y1:y2]=255.0
    
    #stimulated[x1:x2,y1:y2] = stimulated[x1:x2,y1:y2] * checkerboard
    
    
    '''
    #==grid of dots===
    stimulated[:]=0
    xs=range(x1,x2,20)
    ys=range(y1,y2,20)
    for x in xs:
        for y in ys:
            stimulated[x,y]=255
    
    
    if checkerboard_mode:
        pass
        #stimulated[x1:x2,y1:y2] = stimulated[x1:x2,y1:y2] * checkerboard
    '''

    os.system('cls')

    #past=now
    #now=time.time()

    if update == False:
        upload_alp = False
    else:
        upload_alp = True
    if upload_alp:
        #===upload image===
        ALP.stop()
        ALP.seq_upload(seq_id, [stimulated])
        ALP.seq_start_loop(seq_id)
    
    print keypress
    print "PRESS ESCAPE TO QUIT"
    print "("+str(x1)+", "+str(y1)+")" + " ("+str(x2)+", "+str(y2)+")"
    print "Move Left/CamBottom(a) or  Right/CamTop(d) by " + str(LR_STEP) +" pixels"
    print "Increase(o) or Decrease(p)\n" 
    print "Move Up/CamRight(w) or  Down/CamLeft(s) by " + str(UD_STEP) +" pixels"
    print "Increase(k) or Decrease(l)\n"
    print "Height: " + str(Height) + " increase(8) or decrease(2)"
    print "Width: " + str(Width)+ " increase(4) or decrease(6)"
    print "Enter: display image"
    print "(i)nvert checkerboard"
    print "(b)lack"
    print "(n)ormalize"
    print "Update (M)ode update is: " + str(update)
    
    
  

ALP.stop()
ALP.shutdown()



