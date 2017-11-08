'''ALP definitions file'''
'''copied from alp.h'''
#stuff excluded: LED control, code for backward compatibility, fn definitionss



'''
/***********************************************************************************/
/**                                                                               **/
/**   Project:      alp   (ALP DLL)                                               **/
/**   Filename:     alp.h : Header File                                           **/
/**                                                                               **/
/***********************************************************************************/
/**                                                                               **/
/**   (c) 2004-2013 ViALUX GmbH. All rights reserved.                             **/
/**                                                                               **/
/***********************************************************************************/
/**                                                                               **/
/**   Version:        12                                                          **/
/**                                                                               **/
/***********************************************************************************/
'''

ALP_DEFAULT = 0L

#=====return codes=====

ALP_OK =            0x00000000L        #    successfull execution 
ALP_NOT_ONLINE =          1001L        #    The specified ALP has not been found or is not ready. 
ALP_NOT_IDLE =            1002L        #    The ALP is not in idle state. 
ALP_NOT_AVAILABLE =       1003L        #    The specified ALP identifier is not valid. 
ALP_NOT_READY =           1004L        #    The specified ALP is already allocated. 
ALP_PARM_INVALID =        1005L        #    One of the parameters is invalid. 
ALP_ADDR_INVALID =        1006L        #    Error accessing user data. 
ALP_MEMORY_FULL =         1007L        #    The requested memory is not available. 
ALP_SEQ_IN_USE =          1008L        #    The sequence specified is currently in use. 
ALP_HALTED =              1009L        #    The ALP has been stopped while image data transfer was active. 
ALP_ERROR_INIT =          1010L        #    Initialization error. 
ALP_ERROR_COMM =          1011L        #    Communication error. 
ALP_DEVICE_REMOVED =      1012L        #    The specified ALP has been removed. 
ALP_NOT_CONFIGURED =      1013L        #    The onboard FPGA is unconfigured. 
ALP_LOADER_VERSION =      1014L        #    The function is not supported by this version of the driver file VlxUsbLd.sys. 
ALP_ERROR_POWER_DOWN =    1018L        #    waking up the DMD from PWR_FLOAT did not work (ALP_DMD_POWER_FLOAT) 


# ===== for ALP_DEV_STATE in AlpDevInquire ======

ALP_DEV_BUSY            = 1100L        #    the ALP is displaying a sequence or image data download is active 
ALP_DEV_READY           = 1101L        #    the ALP is ready for further requests 
ALP_DEV_IDLE            = 1102L        #    the ALP is in wait state 


# ===== for ALP_PROJ_STATE in AlpProjInquire =====

ALP_PROJ_ACTIVE         = 1200L        #    ALP projection active 
ALP_PROJ_IDLE           = 1201L        #    no projection active 


# =====  parameter =====

# ===== AlpDevInquire =====

ALP_DEVICE_NUMBER       = 2000L    #    Serial number of the ALP device 
ALP_VERSION             = 2001L    #    Version number of the ALP device 
ALP_DEV_STATE           = 2002L    #    current ALP status, see above 
ALP_AVAIL_MEMORY        = 2003L    #    ALP on-board sequence memory available for further sequence 
                                        #    allocation (AlpSeqAlloc); number of binary pictures 

# ===== Temperatures. Data format: signed long with 1 LSB=1/256 deg C ===== 
ALP_DDC_FPGA_TEMPERATURE =2050L    # V4100 Rev B: LM95231. External channel: DDC FPGAs Temperature Diode 
ALP_APPS_FPGA_TEMPERATURE=2051L    # V4100 Rev B: LM95231. External channel: Application FPGAs Temperature Diode 
ALP_PCB_TEMPERATURE      =2052L    # V4100 Rev B: LM95231. Internal channel. "Board temperature" 

# =====   AlpDevControl - ControlTypes & ControlValues =====
ALP_SYNCH_POLARITY      = 2004L    #  Select frame synch output signal polarity 
ALP_TRIGGER_EDGE        = 2005L    #  Select active input trigger edge (slave mode) 
ALP_LEVEL_HIGH          = 2006L    #  Active high synch output 
ALP_LEVEL_LOW           = 2007L    #  Active low synch output 
ALP_EDGE_FALLING        = 2008L    #  High to low signal transition 
ALP_EDGE_RISING         = 2009L    #  Low to high signal transition 

ALP_TRIGGER_TIME_OUT    = 2014L    #    trigger time-out (slave mode) 
ALP_TIME_OUT_ENABLE     =    0L    #    Time-out enabled (default) 
ALP_TIME_OUT_DISABLE    =    1L    #    Time-out disabled 

ALP_USB_CONNECTION      = 2016L    #    Re-connect after a USB interruption 

ALP_DEV_DMDTYPE         = 2021L    #    Select DMD type; only allowed for a new allocated ALP-3 high-speed device 
ALP_DMDTYPE_XGA         =    1L    #    1024*768 mirror pixels (0.7" Type A, D3000) 
ALP_DMDTYPE_SXGA_PLUS   =    2L    #    1400*1050 mirror pixels (0.95" Type A, D3000) 
ALP_DMDTYPE_1080P_095A  =    3L    #    1920*1080 mirror pixels (0.95" Type A, D4x00) 
ALP_DMDTYPE_XGA_07A     =    4L    #    1024*768 mirror pixels (0.7" Type A, D4x00) 
ALP_DMDTYPE_XGA_055A    =    5L    #    1024*768 mirror pixels (0.55" Type A, D4x00) 
ALP_DMDTYPE_XGA_055X    =    6L    #    1024*768 mirror pixels (0.55" Type X, D4x00) 
ALP_DMDTYPE_WUXGA_096A  =    7L    #    1920*1200 mirror pixels (0.96" Type A, D4100) 
ALP_DMDTYPE_DISCONNECT  =  255L    #    behaves like 1080p (D4100) 

ALP_DEV_DISPLAY_HEIGHT  =  2057L    # number of mirror rows on the DMD 
ALP_DEV_DISPLAY_WIDTH   =  2058L    # number of mirror columns on the DMD 

ALP_DEV_DMD_MODE        =  2064L    # query/set DMD PWR_FLOAT mode, valid options: ALP_DEFAULT (normal operation: "wake up DMD"), ALP_DMD_POWER_FLOAT 
ALP_DMD_POWER_FLOAT     =   1L    # power down, release micro mirrors from deflected state 

ALP_PWM_LEVEL           =  2063L    # PWM pin duty-cycle as percentage: 0..100%; after AlpDevAlloc: 0% 

# ===== AlpDevControlEx =====
ALP_DEV_DYN_SYNCH_OUT1_GATE = 2023L
ALP_DEV_DYN_SYNCH_OUT2_GATE = 2024L
ALP_DEV_DYN_SYNCH_OUT3_GATE = 2025L



# ===== AlpSeqControl - ControlTypes =====
ALP_SEQ_REPEAT          = 2100L    #    Non-continuous display of a sequence (AlpProjStart) allows 
                                        #    for configuring the number of sequence iterations. 
ALP_SEQ_REPETE  = ALP_SEQ_REPEAT    #  According to the typo made in primary documentation (ALP API description) 
ALP_FIRSTFRAME          = 2101L    #    First image of this sequence to be displayed. 
ALP_LASTFRAME           = 2102L    #    Last image of this sequence to be displayed. 

ALP_BITNUM              = 2103L    #    A sequence can be displayed with reduced bit depth for faster speed. 
ALP_BIN_MODE            = 2104L    #    Binary mode: select from ALP_BIN_NORMAL and ALP_BIN_UNINTERRUPTED (AlpSeqControl) 

ALP_BIN_NORMAL          = 2105L    #    Normal operation with progammable dark phase 
ALP_BIN_UNINTERRUPTED   = 2106L    #    Operation without dark phase 

ALP_PWM_MODE            = 2107L    # ALP_DEFAULT, ALP_FLEX_PWM 
ALP_FLEX_PWM            = 3L    # ALP_PWM_MODE: all bit planes of the sequence are displayed as
                                        #fast as possible in binary uninterrupted mode;
                                        #use ALP_SLAVE mode to achieve a custom pulse-width modulation timing for generating gray-scale 

ALP_DATA_FORMAT         = 2110L    #    Data format and alignment 
ALP_DATA_MSB_ALIGN      =    0L    #    Data is MSB aligned (default) 
ALP_DATA_LSB_ALIGN      =    1L    #    Data is LSB aligned 
ALP_DATA_BINARY_TOPDOWN =    2L    #    Data is packed binary, top row first; bit7 of a byte = leftmost of 8 pixels 
ALP_DATA_BINARY_BOTTOMUP=    3L    #    Data is packed binary, bottom row first 
        # XGA:   one pixel row occupies 128 byte of binary data. 
        #        Byte0.Bit7 = top left pixel (TOPDOWN format) 
        # 1080p and WUXGA: one pixel row occupies 256 byte of binary data. 
        #        Byte0.Bit7 = top left pixel (TOPDOWN format) 
        # SXGA+: one pixel row occupies 176 byte of binary data. First byte ignored. 
        #        Byte1.Bit7 = top left pixel (TOPDOWN format) 

ALP_SEQ_PUT_LOCK        =  2119L    # ALP_DEFAULT: Lock Sequence Memory in AlpSeqPut;
     #Not ALP_DEFAULT: do not lock, instead allow writing sequence image data even currently displayed 


ALP_FIRSTLINE           =  2111L    #    Start line position at the first image 
ALP_LASTLINE            =  2112L    #    Stop line position at the last image 
ALP_LINE_INC            =  2113L    #    Line shift value for the next frame 
ALP_SCROLL_FROM_ROW     =  2123L    #    combined value from ALP_FIRSTFRAME and ALP_FIRSTLINE 
ALP_SCROLL_TO_ROW       =  2124L    #    combined value from ALP_LASTFRAME and ALP_LASTLINE 

#    Frame Look Up Table (FLUT): sequence settings select how to use the FLUT.
#    The look-up table itself is shared across all sequences.
#    (use ALP_FLUT_SET_MEMORY controls for accessing it) 

ALP_FLUT_MODE           = 2118L    # Select Frame LookUp Table usage mode: 
ALP_FLUT_NONE           =    0L    # linear addressing, do not use FLUT (default) 
ALP_FLUT_9BIT           =    1L    # Use FLUT for frame addressing: 9-bit entries 
ALP_FLUT_18BIT          =    2L    # Use FLUT for frame addressing: 18-bit entries 

ALP_FLUT_ENTRIES9       = 2120L    # Determine number of FLUT entries; default=1
                    #Entries: supports all values from 1 to ALP_FLUT_MAX_ENTRIES9 
ALP_FLUT_OFFSET9        = 2122L    # Determine offset of FLUT index; default=0
                                   #Offset supports multiples of 256;
                                   # For ALP_FLUT_18BIT, the effective index is half of the 9-bit index.
                                   #--> "ALP_FLUT_ENTRIES18" and "ALP_FLUT_FRAME_OFFSET18" are 9-bit settings divided by 2 
                                   #    The API does not reject overflow! (FRAME_OFFSET+ENTRIES > MAX_ENTRIES).
                                   #The user is responsible for correct settings. 

ALP_SEQ_DMD_LINES        = 2125L   # Area of Interest: Value = MAKELONG(StartRow, RowCount)


# AlpSeqInquire 
ALP_BITPLANES            = 2200L    #    Bit depth of the pictures in the sequence 
ALP_PICNUM               = 2201L    #    Number of pictures in the sequence 
ALP_PICTURE_TIME         = 2203L    #    Time between the start of consecutive pictures in the sequence in microseconds, 
                                        #    the corresponding in frames per second is 
                                        #    picture rate [fps] = 1 000 000 / ALP_PICTURE_TIME [us] 
ALP_ILLUMINATE_TIME      = 2204L    #    Duration of the display of one picture in microseconds 
ALP_SYNCH_DELAY          = 2205L    #    Delay of the start of picture display with respect 
                                        #    to the frame synch output (master mode) in microseconds 
ALP_SYNCH_PULSEWIDTH     = 2206L    #    Duration of the active frame synch output pulse in microseconds 
ALP_TRIGGER_IN_DELAY     = 2207L    #    Delay of the start of picture display with respect to the 
                                        #    active trigger input edge in microseconds 
ALP_MAX_SYNCH_DELAY      = 2209L    #    Maximal duration of frame synch output to projection delay in microseconds 
ALP_MAX_TRIGGER_IN_DELAY = 2210L    #    Maximal duration of trigger input to projection delay in microseconds 

ALP_MIN_PICTURE_TIME     = 2211L    #    Minimum time between the start of consecutive pictures in microseconds 
ALP_MIN_ILLUMINATE_TIME  = 2212L    #    Minimum duration of the display of one picture in microseconds 
                                        #    depends on ALP_BITNUM and ALP_BIN_MODE 
ALP_MAX_PICTURE_TIME     = 2213L    #    Maximum value of ALP_PICTURE_TIME 

                                        #     _TIME = ALP_ON_TIME + ALP_OFF_TIME 
                                        #    ALP_ON_TIME may be smaller than ALP_ILLUMINATE_TIME 
ALP_ON_TIME              = 2214L    #    Total active projection time 
ALP_OFF_TIME             = 2215L    #    Total inactive projection time 

# ===== AlpProjInquire & AlpProjControl ==== & ...Ex - InquireTypes, ControlTypes & Values 
ALP_PROJ_MODE            = 2300L    #    Select from ALP_MASTER and ALP_SLAVE mode 
ALP_MASTER               = 2301L    #    The ALP operation is controlled by internal 
                                     #    timing, a synch signal is sent out for any 
                                     #    picture displayed 
ALP_SLAVE                = 2302L    #    The ALP operation is controlled by external 
                                     #    trigger, the next picture in a sequence is 
                                     #    displayed after the detection of an external 
                                     #    input trigger signal. 
ALP_PROJ_STEP            = 2329L    #    ALP operation should run in ALP_MASTER mode,
                                    #    but each frame is repeatedly displayed
                                    #    until a trigger event is received.
                                    #    Values (conditions): ALP_LEVEL_HIGH |
                                    #    LOW, ALP_EDGE_RISING | FALLING.
                                    #    ALP_DEFAULT disables the trigger and
                                    #    makes the sequence progress "as usual".
                                    #    If an event is "stored" in edge mode due
                                    #    to a past edge, then it will be
                                    #    discarded during
                                    #    AlpProjControl(ALP_PROJ_STEP). 
ALP_PROJ_SYNC             = 2303L    #    Select from ALP_SYNCHRONOUS and ALP_ASYNCHRONOUS mode 
ALP_SYNCHRONOUS           = 2304L    #    The calling program gets control back after completion 
                                     #    of sequence display. 
ALP_ASYNCHRONOUS          = 2305L    #    The calling program gets control back immediatelly. 

ALP_PROJ_INVERSION        = 2306L    #  Reverse dark into bright 
ALP_PROJ_UPSIDE_DOWN      = 2307L    #  Turn the pictures upside down 

ALP_PROJ_STATE            = 2400L    # Inquire only 


ALP_FLUT_MAX_ENTRIES9     = 2324L    # Inquire FLUT size 
                                     # Transfer FLUT memory to ALP. Use AlpProjControlEx and pUserStructPtr of type tFlutWrite. 
ALP_FLUT_WRITE_9BIT       = 2325L    # 9-bit look-up table entries 
ALP_FLUT_WRITE_18BIT      = 2326L    # 18-bit look-up table entries  



# Sequence Queue API Extension: 
ALP_PROJ_QUEUE_MODE       = 2314L
ALP_PROJ_LEGACY           = 0L        #  ALP_DEFAULT: emulate legacy mode: 1 waiting position. AlpProjStart replaces enqueued and still waiting sequences 
ALP_PROJ_SEQUENCE_QUEUE   = 1L        #  manage active sequences in a queue 

ALP_PROJ_QUEUE_ID         = 2315L    # provide the QueueID (ALP_ID) of the most recently enqueued sequence (or ALP_INVALID_ID) 
ALP_PROJ_QUEUE_MAX_AVAIL  = 2316L    # total number of waiting positions in the sequence queue 
ALP_PROJ_QUEUE_AVAIL      = 2317L    # number of available waiting positions in the queue 
    # bear in mind that when a sequence runs, it is already dequeued and does not consume a waiting position any more 
ALP_PROJ_PROGRESS         = 2318L    # (AlpProjInquireEx) inquire detailled progress of the running sequence and the queue 
ALP_PROJ_RESET_QUEUE      = 2319L    # Remove all enqueued sequences from the queue. The currently running sequence is not affected. ControlValue must be ALP_DEFAULT 
ALP_PROJ_ABORT_SEQUENCE   = 2320L    # abort the current sequence (ControlValue=ALP_DEFAULT) or a specific sequence (ControlValue=QueueID); abort after last frame of current iteration 
ALP_PROJ_ABORT_FRAME      = 2321L    # similar, but abort after next frame 
                                     # Only one abort request can be active at a time. If it is requested to
                                     # abort another sequence before the old request is completed, then
                                     # AlpProjControl returns ALP_NOT_IDLE. (Please note, that AlpProjHalt
                                     # and AlpDevHalt work anyway.) If the QueueID points to a sequence
                                     # behind an indefinitely started one (AlpProjStartCont) then it returns
                                     # ALP_PARM_INVALID in order to prevent dead-locks. 
ALP_PROJ_WAIT_UNTIL        = 2323L    # When does AlpProjWait complete regarding the last frame? or after picture time of last frame 
ALP_PROJ_WAIT_PIC_TIME     = 0L        #  ALP_DEFAULT: AlpProjWait returns after picture time 
ALP_PROJ_WAIT_ILLU_TIME    = 1L        #  AlpProjWait returns after illuminate time (except binary uninterrupted sequences, because an "illuminate time" is not applicable there) 

''' #== TODO : HOW TO MAKE UNSIGNED LONG IN PYTHON?
define ALP_FLAG_QUEUE_IDLE                1UL
define ALP_FLAG_SEQUENCE_ABORTING        2UL
define ALP_FLAG_SEQUENCE_INDEFINITE    4UL    /* AlpProjStartCont: this loop runs indefinitely long, until aborted */
define ALP_FLAG_FRAME_FINISHED            8UL    /* illumination of last frame finished, picture time still progressing */
'''


