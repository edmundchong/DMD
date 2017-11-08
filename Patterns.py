from PIL import Image
import ImageDib
from ctypes import *
from copy import deepcopy
from numpy.random import permutation, randint
import numpy as np
from configobj import ConfigObj
from listquote import LineParser 
import os
import getch

#TODO: convert to OOP

#Mightex Settings
ImWidth=608
ImHeight=684

#Vialux ALP Settings
ALP_dim = [768,1024] #Height 768. Width 1024
ALP_offset = [286,449]
'''
#ALP Settings #should set by Patterns.ImWidth = ... before any function calls
ImWidth=60
ImHeight=50
'''

scaling={'10x':[1.0, 0.5], '20x':[350.0/ImHeight,630/ImWidth],'vialux':[1/17.0,1/17.0]}

def ALPimg(seq):
    """
    for ALP DMD, spots are defined within a small portion of the whole array
    (DMD is partially illuminated). Images are initially defined as xy values within this small portion
    this function converts those images to be part of the entire array (0 value outside the field)
    """
    new_seq=[]
    for ptn in seq:
        new_ptn = np.zeros([ALP_dim[0],ALP_dim[1]])
        x1 = ALP_offset[0]
        x2 = x1 + ImHeight
        y1 = ALP_offset[1]
        y2 = y1 + ImWidth
        new_ptn[x1:x2, y1:y2] = ptn
        new_seq.append(new_ptn)
    
    return new_seq
        
def col2pix(y,objective,length_um):
    #field of stimulation is divided into grid of columns
    #used in training: to create large columns of L v R stimulation
    #function converts column number --> 2D array of pixel values
    #***NOTE that x, y are cartesian coordinates. this is swapped from matrix indices!! (confusing)
    #an additional swap is made because the projected image is rotated from the original matrix, so your 
    #x, y is now rotated and flipped
    
        
    height_scale=scaling[objective][0]
    width_scale=scaling[objective][1]

    #transform to pixel size
    height=np.floor(length_um * height_scale)
    width=np.floor(length_um * width_scale)

    x_max,y_max=get_grid_max(length_um,objective)
    if (y > y_max):
        print ' y is: '+', y_max is '+str(y_max)
        raise ValueError('col2pix: y coordinate is greater than max')

    topleft = [y*height,0] #here the swap from cartesian to matrix is confusing
    bottomright = [(y+1)*height-1,ImWidth-1]
    
    ptn=np.zeros([ImHeight,ImWidth])
    ptn[topleft[0]:bottomright[0]+1,topleft[1]:bottomright[1]+1]=255
    
    
    return ptn

def checkerboard(square_size):
    """
    create checkerboard pattern.
    square_size: in pixels
    """
    h, w = ImHeight, ImWidth
    sq = square_size
    
    coords = np.ogrid[0:h, 0:w]
    idx = (coords[0] // sq + coords[1] // sq) % 2
    vals = np.array([255, 0])
    ptn = vals[idx]
    
    return ptn

def createProtocolImage(ptn1,ptn2,objective):
    ptnImg=np.zeros((ImHeight,ImWidth,3),'uint8')
    ptnImg[:,:,1]=ptn1 #Green channel: Go / left-lick
    ptnImg[:,:,0]=ptn2 #Red channel: NoGo / right-lick
    
    img=Image.fromarray(ptnImg)
    
     
    heightscale=scaling[objective][0]
    widthscale=scaling[objective][1]   
    
    new_height=int(ImHeight/heightscale)
    new_width=int(ImWidth/widthscale)

    img=img.resize((new_width,new_height))
    
    img=img.rotate(90)
    img=img.transpose(Image.FLIP_TOP_BOTTOM)
    return img

def createProtocolImage_split(PatternSets,objective):
    """"create one image for S+, one for S- (or left and right)
    #accepts list 'PatternSets' of length 2, first element is S+ / left, second element is S- / right
   
    """
    
    ptnImg=[np.zeros((ImHeight,ImWidth,3),'uint8'),np.zeros((ImHeight,ImWidth,3),'uint8')] 
    
    for i in range(2):
        intensity_levels=len(PatternSets[i])
        
        if i == 0:
            rgb = 1 # green for left
        elif i == 1:
            rgb = 0 # red for (r)ight
        
        #now scale color of each frame in Pattern sequence; later frames are more intense
        ptn_seq=PatternSets[i]

        for ptn_index in range(len(ptn_seq)):
            scale_factor=ptn_index + 1
            ptnImg[i][:,:,rgb]=ptnImg[i][:,:,rgb]+ptn_seq[ptn_index]*scale_factor/intensity_levels
    
    
    #image transforms
    heightscale=scaling[objective][0]
    widthscale=scaling[objective][1]   
    new_height=int(ImHeight/heightscale)
    new_width=int(ImWidth/widthscale)
    
    img=[[]]*len(ptnImg)
    for i in range(len(img)):
        img[i]=Image.fromarray(ptnImg[i])
        img[i]=img[i].resize((new_width,new_height))
        img[i]=img[i].rotate(90)
        img[i]=img[i].transpose(Image.FLIP_TOP_BOTTOM)
    
    
    #==combine the two images===
    img_w,img_h=img[0].size
    two_img=Image.new('RGBA',(img_w*2+5,img_h),(255,255,255,0))
    offset=(0,0)
    two_img.paste(img[0],offset)
    offset=(img_w+5,0)
    two_img.paste(img[1],offset)
       
    return two_img

def createSpotsImage(spots,objective,rgb,spotsize,mode='gridmode'):
    """
    create image for an ordered list of spots
    earlier spots will appear dimmer and later spots appear brighter
    
    rgb: allows some (limited) color picking
    e.g. [0]r [0,1]rg, [0,1,2]rgb, [1,2]gb, [1]g [2]b
    
    mode: gridmode -- spots defined as xy values
          pixmode  -- spots defined as pixel values, require no further conversion
    """
    
    if mode=='gridmode':
        seq=[]
        for this_spot in spots:
            print this_spot
            seq.append(grid2pix(this_spot[0],this_spot[1],objective,spotsize))
    
    
    ptnImg=np.zeros((ImHeight,ImWidth,3),'uint8')

    intensity_levels=len(seq)

    for spot_index in range(len(seq)):
        scale_factor=spot_index + 1
         
        for c in rgb:
            ptnImg[:,:,c]=ptnImg[:,:,rgb]+seq[spot_index]*scale_factor/intensity_levels
        
    

    
    img=Image.fromarray(ptnImg)
    
     
    heightscale=scaling[objective][0]
    widthscale=scaling[objective][1]   
    
    new_height=int(ImHeight/heightscale)
    new_width=int(ImWidth/widthscale)

    img=img.resize((new_width,new_height))
    
    img=img.rotate(90)
    img=img.transpose(Image.FLIP_TOP_BOTTOM)
    return img

def divisors(n):
    #function adapted from 
    #http://stackoverflow.com/questions/171765/what-is-the-best-way-to-get-all-the-divisors-of-a-number
    large_divisors = []
    all_divisors = []
    for i in xrange(1, int(np.sqrt(n) + 1)):

        if n % i == 0:
            all_divisors.append(i)
        if i != n / i:
            large_divisors.insert(0, n / i)
    for divisor in large_divisors:
        all_divisors.append(divisor)
    return all_divisors

def divisor_gc(arr):
    #find GREATEST COMMON divisor in a list/numpy array
    arr=np.unique(np.array(arr)) #convert to numpy array if it isn't already
    arr.sort() #sort in ascending order

    all_divisors = []    
    for n in arr:
        if n < 1:
            continue
        this_divisors = divisors(n)
        all_divisors.append(this_divisors)
    
    candidates = all_divisors[0]
    candidates.sort(reverse=True)
    
    for i in candidates:
        candidate_in_all=True
        
        for j in all_divisors:
            if i not in j:
                candidate_in_all=False
                break
        
        if candidate_in_all:
            return i

    return 0 #greatest common denominator not found

def EmptyField_seq(nFrames):
    PatternSet=[]
    for i in range(nFrames):
        ptn=np.zeros([ImHeight,ImWidth])
        PatternSet.append(ptn)
    
    return PatternSet

def FullField(nFrames):
    PatternSet=[]
    for i in range(nFrames):
        ptn=np.ones([ImHeight,ImWidth])
        ptn=ptn*255
        PatternSet.append(ptn)
    
    return PatternSet

def get_grid_max(length_um,objective):
    #returns max (x,y) coordinates for grid
    #note zero-indexing
    height_scale=scaling[objective][0]
    width_scale=scaling[objective][1]

    #transform to pixel size
    height=np.floor(length_um * height_scale)
    width=np.floor(length_um * width_scale)
    
    x_max = np.floor(ImWidth / width) #number of spots in one (image) row but (projected image) column
    y_max = np.floor(ImHeight / height) #number of spots in one (image) column but (projected image) row
    
    x_max=x_max - 1 #zero-indexing
    y_max=y_max - 1
    
    return x_max, y_max

def getStoredPattern(target):
    targetdir='C:/VoyeurData/ref_images/'
    filename=targetdir+target+'.png'
    try:
        img=Image.open(filename)
    except IOError:
        print "WARNING: " + filename + ' does not exist'
        return [0]
    ptn=np.array(img)
    ptn=[ptn.astype('float')]
    return ptn

def grid2pix(x,y,objective,length_um):
    #field of stimulation is divided into grid of squares
    #each square is assigned a coordinate (x,y), starting from top left (0,0)
    #some pixels will be left over on bottom right
    #function converts (x,y) --> 2D array of pixel values
    #***NOTE that x, y are cartesian coordinates. this is swapped from matrix indices!! (confusing)
    #an additional swap is made because the projected image is rotated from the original matrix, so your 
    #x, y is now rotated and flipped
    
        
    height_scale=scaling[objective][0]
    width_scale=scaling[objective][1]

    #transform to pixel size
    height=np.floor(length_um * height_scale)
    width=np.floor(length_um * width_scale)

    x_max,y_max=get_grid_max(length_um,objective)
    if (x > x_max) or (y > y_max):
        print 'x is: '+str(x)+' y is: '+str(y)+', x_max is '+str(x_max)+' y_max is '+str(y_max)
        raise ValueError('grid2pix: x or y coordinate is greater than max')

    topleft = [y*height,x*width] #here the swap from cartesian to matrix is confusing
    bottomright = [(y+1)*height-1,(x+1)*width-1]
    
    ptn=np.zeros([ImHeight,ImWidth])
    ptn[topleft[0]:bottomright[0]+1,topleft[1]:bottomright[1]+1]=255
    
    
    return ptn

def grid_ind2xy(coord,direction,gridsize,objective):
    #convert between single value index and (x,y) coordinate on grid
    
    x_max,y_max=get_grid_max(gridsize,objective)
    x_n = x_max + 1 #get number of x units 
    y_n = y_max + 1
    if direction == 'forward':
        #from index to x,y
        ind = coord
        x = np.mod(ind,x_n)
        y = np.floor(ind/x_n)
        return [x,y]
    elif direction == 'reverse':
        #from x,y to index
        x,y=coord
        ind = int(x_n*y + x)
        return ind
    else:
        raise ValueError('grid_ind2xy: Direction supplied is not recognized')

def HalfField(nFrames,half):
    PatternSet=[]
    for i in range(nFrames):
        ptn=np.zeros([ImHeight,ImWidth])

        if half == 1: #top half
            ptn[0:ImHeight/2,:]=255
        elif half == 2:
            ptn[ImHeight/2:,:]=255
        PatternSet.append(ptn)
    
    return PatternSet

def nonoverlapping_squares(nsquares,xsize,ysize,nmask=0):
    """nmask: negative mask. Single ImHeight x ImWidth array.
     squares will be forbidden within this mask"""
    
    #generate first square
    ptn=np.zeros([ImHeight,ImWidth,nsquares+1])
    
    #set the first matrix of square set to be the negative mask (or zeros if no mask)
    if np.sum(nmask) == 0:
        pass
    else:
        ptn[:,:,0]=nmask 
    
    maxLoops = 1000 #number of iterations (count) before giving up finding non-overlapping patterns
    for ptnIndex in range(1,nsquares+1):
        flag = True
        count = 0

        while flag and count < maxLoops:
            ptn[:,:,ptnIndex]=np.zeros([ImHeight,ImWidth])
            x=randint(0,ImHeight-xsize-1)
            y=randint(0,ImWidth-ysize-1)
            ptn[x:x+xsize,y:y+ysize,ptnIndex]=255
            
            #sum this pattern with all previous patterns. if there is no overlap, then the max of any entry will be 255
            if np.amax(ptn[:,:,0:ptnIndex+1].sum(axis=2)) == 255: 
                flag = False #successfully generated non-overlapping pattern, can exit loop
            count = count + 1
            print str(ptnIndex)+': '+str(count)
        
        if count > (maxLoops - 1):
            return ptn,ptn
            raise ValueError('Error! {maxLoops} iterations without non-overlapping pattern generated'.format(maxLoops=maxLoops))
    
    ptn = ptn[:,:,1:] #remove the 1st element of set (negative mask)
    return ptn

def parse_mouse_config(mouse):
    config_dir = os.environ.get("mouse_config_dir")
    
    if config_dir < 1:
        config_dir='C:\\voyeur_rig_config\\stim_params\\'
    
    configFilename=config_dir+str(mouse)+'.conf'   
    
    if os.path.isfile(configFilename)== False:
        print "MOUSE CONFIGURATION FILE  " + configFilename + " IS NOT PRESENT"
    else:
        print "MOUSE CONFIGURATION FILE  " + configFilename + " FOUND"
    
    conf = ConfigObj(configFilename, list_values=False) #returns everything as string
    
    
    #=====parse datatypes=====
    list_vars=['excluded_spots','stimA','stimB',
               'A_spots','A_isProbe','A_timing','A_ratios','A_labels',
               'B_spots','B_isProbe','B_timing','B_ratios','B_labels']
    
    int_vars=['debias','spot_size','spot_dur','SOA','initialtrials','laserdur','order','probeMode','stepdelay']
    
    
    float_vars=['reinforcementpercentage']
    
    #parse lists (numeric lists only, for string lists need to modify listquote.LineParser
    listreader=LineParser()
    for var in list_vars:
        if var in conf:
            #===handle tab and newline===
            conf[var] = conf[var].replace('\t','')
            conf[var] = conf[var].replace('\n','')
            
            conf[var] = listreader.feed(conf[var])

    #convert integers
    for var in int_vars:
        if var in conf:
            conf[var] = int(conf[var])

    #convert float
    for var in float_vars:
        if var in conf:
            conf[var] = float(conf[var])
    
    return conf

def Ptn2Char(ptn):
    #handle ALP patterns
    #flatten pattern sequence to a list, then put in ctype char vector
    ptn_list=[]
    for frame in ptn:
        #flatten frame and add it to list
        ptn_list.extend(frame.flatten().tolist())
    
    alp_seqdata = c_ubyte * len(ptn_list)
    alp_seqdata = alp_seqdata()
    
    #now transfer elementwise from list to char vector (is there better way?)
    for i in range(len(alp_seqdata)):
        alp_seqdata[i]=int(ptn_list[i])
    return alp_seqdata

def Ptn2HBitmap(PatternSet):
    HBitmapSet=[]
    for ptn in PatternSet:
        img=Image.fromarray(ptn) 
        img=img.convert('1') #black and white
        himg=ImageDib.tohbitmap(img)
        HBitmapSet.append(himg)
        
    return HBitmapSet

def RandomPatterns(nPixels,nFrames):
    PatternSet=[]
    pixelIndices=[]
    for h in range(ImHeight):
        for w in range(ImWidth):
            pixelIndices.append([h,w])

    pixelIndices_foo=deepcopy(pixelIndices)

    for i in range(nFrames):
        pixelIndices_foo=permutation(pixelIndices_foo)
        pixelset = pixelIndices_foo[0:nPixels]
        ptn= np.zeros([ImHeight,ImWidth])
        
        for thisPixel in pixelset:
            x=thisPixel[0]
            y=thisPixel[1]
            ptn[x,y]=255
        PatternSet.append(ptn)
        
    return PatternSet

def randomSquare(nFrames,size,half=0):
    PatternSet=[]
    ptn=np.zeros([ImHeight,ImWidth])
    x=randint(0,ImHeight-size-1)
    if half == 2: #put square in bottom half
        y=randint(ImHeight/2,ImWidth-size-1)
    else:
        y=randint(0,ImWidth-size-1)
    ptn[x:x+size,y:y+size]=255
    for i in range(nFrames):
        #print i
        #print ptn
        PatternSet.append(ptn)
    print PatternSet
    return PatternSet

def rand_xy(objective,length_um, n_spots, spacing, ref_spots=np.array([-99,-99])):
    #pick random x,y coordinate to define non-overlapping spots
    #spacing: minimum euclidean distance between spots, measured by number of spots
    #e.g. 1 means spots cannot be above, below, left, or right, but can be diagonal [distance = sqrt(2)]
    #can also supply ref_spots (n-by-2 array) that new spots must not overlap with
    #spacing < 0 means spots can overlap

    x_max,y_max=get_grid_max(length_um,objective)
    if ref_spots.shape==(2L,):
        ref_spots=ref_spots.reshape(1L,2L) #if only one spot, need to reshape for concatenation later
        
    new_spots=np.zeros((n_spots,2)) - 99 #container holding all spot values, initialized to -99 (to avoid affecting distance calc)
    
    for i in range(n_spots):
        
        max_loop=10000
        all_spots=np.concatenate([new_spots, ref_spots],axis=0)
        for j in range(max_loop):
            x=randint(0,x_max)
            y=randint(0,y_max)
            
            euclid_dist=np.sqrt(np.sum((all_spots-[x,y])**2,1))
            if euclid_dist.min() > spacing: 
                new_spots[i,:]=[x,y]
                break
            elif j==max_loop-1:
                raise ValueError('max iterations reached, no possible spot found')
            
    return new_spots

def rand_seq(objective,length_um, n, seq_length, excluded_spots=np.array([-99,-99])):
    #return n random sequences, each with seq_length
    #use excluded_spots ( numpy array) to exclude spots from sequence
     
    if excluded_spots.shape==(2L,):
        excluded_spots=excluded_spots.reshape(1L,2L) #if only one spot, need to reshape for concatenation later
        
    seqs = []
    for i in xrange(n):        
        max_loop=10000
        for j in xrange(max_loop):
            spots = rand_xy(objective,length_um,seq_length,0,excluded_spots) #generate spots not in excluded list
            spots=spots.tolist()

            if spots in seqs:
                if j==max_loop-1:
                    raise ValueError('max iterations reached, no possible seq found')
            else:
                seqs.append(spots) #sequence found
                break
    return seqs

def rebello():
    #return left half v right half (slightly separated) stimulation for conceptual replication of Rebello
    #top v bottom is not good bec fibres of passage
    objective='10x'

    height_scale=scaling[objective][0]
    width_scale=scaling[objective][1]

    #transform to pixel size
    length_um=300
    separation=80
    height=np.floor(length_um * height_scale)
    #width=np.floor(length_um * width_scale)

    #left
    topleft=[0,0]
    bottomright=[height-1,ImWidth-1]

    ptn1=np.zeros([ImHeight,ImWidth])
    ptn1[topleft[0]:bottomright[0]+1,topleft[1]:bottomright[1]+1]=255
    

    #right
    topleft=[height+separation,0]
    bottomright=[height+separation+height-1,ImWidth-1]

    ptn2=np.zeros([ImHeight,ImWidth])
    ptn2[topleft[0]:bottomright[0]+1,topleft[1]:bottomright[1]+1]=255
    
    return ptn1,ptn2

def sequence(nFrames,length_um,squares_per_frame,pair,objective,nmask=0):
    xscale=scaling[objective][0]
    yscale=scaling[objective][1]

    #transform to pixel dimensions
    xsize=np.floor(length_um * xscale)
    ysize=np.floor(length_um * yscale)    
    
    squares_needed=(squares_per_frame+squares_per_frame*pair)*nFrames #if pair = 1, need to generate another set
    squares=nonoverlapping_squares(squares_needed, xsize, ysize,nmask)

    '''
    #have one empty frame following each pattern frame
    ptn=zeros([ImHeight,ImWidth,squares_needed*2])
    for counter in range(squares_needed):
        ptn[:,:,counter*2]=frames[:,:,counter]
    '''

    #merge squares into frames
    if pair == 0:
        seq=[]
        for counter in range(nFrames):
            startInd = counter * squares_per_frame
            endInd = startInd + squares_per_frame
            print counter
            seq.append(squares[:,:,startInd:endInd].sum(axis=2))
        
        return seq
    elif pair == 1:
        squares1,squares2=np.split(squares,2,axis=2) #split squares into two sets
        seq1=[]
        seq2=[]
        
        for counter in range(nFrames):
            startInd = counter * squares_per_frame
            endInd = startInd + squares_per_frame
            seq1.append(squares1[:,:,startInd:endInd].sum(axis=2))
            seq2.append(squares2[:,:,startInd:endInd].sum(axis=2))
        
        return seq1, seq2


def sequence2(nFrames,length_um,squares_per_frame,pair,objective,nmask=0):
    xscale=scaling[objective][0]
    yscale=scaling[objective][1]

    #transform to pixel dimensions
    xsize=np.floor(length_um * xscale)
    ysize=ImHeight  
    
    ptn=np.zeros([ImHeight,ImWidth])
    x=0
    ptn[x:x+xsize,0:]=255
    return ptn

def spot2seq(spots,spot_size,spot_timing,objective,mode):
    """
     mode -- grid: spots in grid mode, have to be converted to pixels
            pix: spots in pixel mode   
    """
    nspots=len(spots)
    spot_timing=np.array(spot_timing)
    frame_switches = np.unique(spot_timing)
    frame_array=np.zeros([nspots,len(frame_switches)]) 
    #array of binary values, row is spot number, column is frame switch
    #1 means spot is present in *after* that frame switch
    
    for i in range(len(frame_switches)):
        switch_time = frame_switches[i]
        spots_present = (switch_time >= spot_timing[:,0]) * (switch_time < spot_timing[:,1]) 
        frame_array[:,i] = spots_present
    
    #create sequence of frames
    #grid2pix(1,0,'10x',self.gridsize)+Patterns.grid2pix(2,2,'10x',self.gridsize)
    seq=[]
    for i in range(len(frame_switches)):
        #start with empty frame
        frame = EmptyField_seq(1)[0]
        spots_present = frame_array[:,i]
        spots_present = np.where(spots_present==True)[0]
        this_spots = [spots[x] for x in spots_present]
        
        for j in this_spots:
            if mode == 'grid':
                frame = frame + grid2pix(j[0],j[1],'10x',spot_size)
            elif mode == 'pix':
                frame = frame + j
                
        #handle overlapping spots -- normalize all pixel values to 255
        frame[frame>255]=255
        
        seq.append(frame)
    
    return [seq, frame_switches]

def spot2seq_simple(spots,spot_size,spot_dur,SOA,objective,mode='grid'):
    """convert multiple spots into sequence of frame presentations, if each spot has same duration and SOA
    
    spot_size -- in um
    spot_dur -- in ms
    SOA -- duration between onset of one spot and onset of following spot
    spots -- list of spots to be presented, each element is [x,y] index of spot
    mode -- grid: spots in grid mode, have to be converted to pixels
            pix: spots in pixel mode
    
    """    
    #create list of onset and offset times for each spot
    spot_timing=[]
    for i in range(len(spots)):
        if i == 0:
            on = 0
        else:
            on = i * SOA
        
        off = on + spot_dur
        spot_timing.append([on,off])
    
    #let spot2seq do the actual conversion
    [seq, frame_switches] = spot2seq(spots,spot_size,spot_timing,objective,mode)
        
    return [seq, frame_switches]
    
def storeRefImage(ptn,target):
    targetdir='C:/VoyeurData/ref_images/'
    filename=targetdir+target+'.png'
    img=Image.fromarray(ptn)
    img=img.convert('L')
    img.save(filename)

