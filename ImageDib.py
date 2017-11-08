"""Helper functions for Image object."""
"""EC: script googled from http://d.hatena.ne.jp/chrono-meter/20090905/p3"""
"""minor modifications e.g. gdi path made by EC 09/10/14"""

from ctypes import *
from ctypes.wintypes import *
windll.LoadLibrary('C:\Windows\System32\gdi32.dll')
gdi=WinDLL('C:\Windows\System32\gdi32.dll')


def todib(image):
    """Image.tostring('raw', rawmode, stride=0, ystep=1)

    "rawmode" is a pixel format. (ex. RGB, GBR...)
    "stride" is a line buffer size includes padding data.
    "ystep" indicates a vertical direction. If ystep is 1,
    then top to bottom. If ystep is -1, then bottom to top.
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')

    #Note: image.bits != sizeof(encoded pixel)
    bits = 24
    linesize = (bits * image.size[0] + 7) / 8 # a line size
    stride = int((linesize + 3) / 4) * 4 # alignment to sizeof(DWORD)

    ystep = -1

    return image.tostring('raw', 'BGR', stride, ystep)


class BITMAPINFOHEADER(Structure):
    _fields_ = [
        ('biSize', DWORD),
        ('biWidth', LONG),
        ('biHeight', LONG),
        ('biPlanes', WORD),
        ('biBitCount', WORD),
        ('biCompression', DWORD),
        ('biSizeImage', DWORD),
        ('biXPelsPerMeter', LONG),
        ('biYPelsPerMeter', LONG),
        ('biClrUsed', DWORD),
        ('biClrImportant', DWORD),
        ]

    def __init__(self, w, h):
        self.biSize = sizeof(self)
        self.biWidth = w
        self.biHeight = h
        self.biPlanes = 1
        self.biBitCount = 24
        self.biSizeImage = w * h * 3


def tohbitmap(image):
    """convert Image object to win32 HBITMAP (int. not
    pywintypes.HANDLE object)

    If you call pywin32's function with result, do below codes:
    >>> from pywintypes import HANDLE
    >>> result = HANDLE(result)
    """
    result = 0

    hDC = gdi.CreateCompatibleDC(0)
    try:
        dataptr = c_void_p()
        result = gdi.CreateDIBSection(
            hDC, byref(BITMAPINFOHEADER(*image.size)), 0,
            byref(dataptr), None, 0)

        hOldBitmap = gdi.SelectObject(hDC, result)
        try:
            buf = todib(image)
            memmove(dataptr, buf, len(buf))
        finally:
            gdi.SelectObject(hDC, hOldBitmap)

    finally:
        gdi.DeleteDC(hDC)

    return result
