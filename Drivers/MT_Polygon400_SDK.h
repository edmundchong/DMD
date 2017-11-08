typedef int SDK_RETURN_CODE;
typedef unsigned int DEV_HANDLE;

#ifdef SDK_EXPORTS
#define SDK_API extern "C" __declspec(dllexport) SDK_RETURN_CODE _cdecl
#define SDK_HANDLE_API extern "C" __declspec(dllexport) DEV_HANDLE _cdecl
#define SDK_POINTER_API extern "C" __declspec(dllexport) unsigned short * _cdecl
#else
#define SDK_API extern "C" __declspec(dllimport) SDK_RETURN_CODE _cdecl
#define SDK_HANDLE_API extern "C" __declspec(dllimport) DEV_HANDLE _cdecl
#define SDK_POINTER_API extern "C" __declspec(dllimport) unsigned short * _cdecl
#endif

#define DSI_IMGHEIGHT 684
#define DSI_IMGWIDTH 608

typedef struct
{
  double LensDistort;
  int LensCenterOffX;
  int LensCenterOffY;
  double TZDistort;
  int TZCenterOffX;
  int TZCenterOffY;
}tDSILTC;

typedef struct
{
	int left;
	int top;
	int right;
	int bottom;
}tRECT;

typedef struct
{
   unsigned short int x;
   unsigned short int y;
}tWordPoint;

typedef struct
{
  int bitDepth; 	//value can be either 1,4,8
  int PtnNumber;	//value in the range [1,96]
  int ABuffer1; 	//reserved, must be set to 0
  int TrigType; 	//value can be 0,1,2,3
  int TrigDelay;	// in microseconds.
  int TrigPeriod;	// in microseconds.
  int ExposureTime;	//in microseconds.
  int LEDSelection;	//0 for Red, 1 for Green, 2 for Blue
  int ABuffer2;		//reserved, must be set to 0
}tPtnSetting;

typedef struct
{
  int Enable; 		//0 to disable output trigger, 1 to enable.
  int TrigDelay;	//in microseconds(us)
  int TrigPulseWidth;//in microseconds(us)
  int ABuffer1;		//reserved, must be set to 0
  int ABuffer2;		//reserved, must be set to 0
}tOutTrigSetting;


SDK_API MTPLG_InitDevice(int DeviceCount, int* DevIPs);
SDK_API MTPLG_GetDeviceModuleNo(int DeviceIndex, char* ModuleNo);
SDK_API MTPLG_GetDeviceIPAddr(int DeviceIndex);
SDK_API MTPLG_GetDeviceLEDChannelNumber(int DeviceIndex);
SDK_API MTPLG_GetDeviceLEDChannelDescrpt(int DeviceIndex,int ChannelIndex,char* ModuleNo);
SDK_API MTPLG_SetDevCorrectionFlag(int DeviceIndex, int Flag);
SDK_API MTPLG_SetDevInterpolationMethod(int DeviceIndex, int aMethod);
SDK_API MTPLG_SetDevCorrectionType(int DeviceIndex, int Type);
SDK_API MTPLG_SetDevLTCoeff(int DeviceIndex, int LDFlag, int TZFlag, tDSILTC* LTCoeff);
SDK_API MTPLG_SetDevGCGLookupTable(int DeviceIndex, tWordPoint GCCTable[DSI_IMGHEIGHT][DSI_IMGWIDTH]);
SDK_API MTPLG_ConnectDev(int DeviceIndex);
SDK_API MTPLG_DisconnectDev(int DeviceIndex);
SDK_API MTPLG_ChangeDevIPAddr(int DeviceIndex, int NewIPAddr);
SDK_API MTPLG_SetDevLEDCurrent(int DeviceIndex, int RLED, int GLED,int BLED);
SDK_API MTPLG_SetDevDisplaySetting(int DeviceIndex, int VMirror, int HMirror);
SDK_API MTPLG_SetDevDisplayMode(int DeviceIndex, int Mode);
SDK_API MTPLG_SetDevClrImg(int DeviceIndex, HBITMAP hbitmap);
SDK_API MTPLG_SetDevClrImgEx(int DeviceIndex, HBITMAP hbitmap);//caller responsible for bitmap handle release
SDK_API MTPLG_SetDevPtnSetting(int DeviceIndex, tPtnSetting* ASetting);
SDK_API MTPLG_SetDevPtnDef(int DeviceIndex, int PatternIndex, HBITMAP hbitmap, int DNCFlag = 0);
SDK_API MTPLG_SetDevPtnDefEx(int DeviceIndex, int PatternIndex, HBITMAP hbitmap, int DNCFlag = 0);//caller responsible for bitmap handle release
SDK_API MTPLG_SetOutTrigSetting(int DeviceIndex, tOutTrigSetting* ASetting);
SDK_API MTPLG_StartPattern(int DeviceIndex);
SDK_API MTPLG_StopPattern(int DeviceIndex);
SDK_API MTPLG_NextPattern(int DeviceIndex);
SDK_API MTPLG_IMGCorrection(int DeviceIndex, byte* InData, byte* OutData,
                            int ImgWidth,int ImgHeight,int BPP, tRECT* prect = NULL);
SDK_API MTPLG_IMGCorrectionEx(int DevIndex, HBITMAP hbitmapI, HBITMAP hbitmapO, tRECT* prect = NULL);
SDK_API MTPLG_UnInitDevice(void);