# -*- coding: utf-8 -*-
from pytosim.api import filebuffer as simbuf, types as simtypes
from pytosim.api.constant import hNil

def SppWorkingFileBufferOpen() -> simtypes.HBuffer:
    hbuf = simbuf.GetBufHandle("__SPP_WORKING_FILES")
    if hbuf == hNil:
        hbuf = simbuf.NewBuf("__SPP_WORKING_FILES")
        simbuf.SetBufDirty(hbuf, False)

    return hbuf

def SppWorkingFileBufferClose():
    hbuf = simbuf.GetBufHandle("__SPP_WORKING_FILES")
    if hbuf != hNil:
        simbuf.CloseBuf(hbuf)

def SppWorkingFileAppend(fname: str):
    hbuf = SppWorkingFileBufferOpen()
    simbuf.AppendBufLine(hbuf, fname)
    simbuf.SetBufDirty(hbuf, False)

def SppWorkingFileGetMatch(fname: str) -> int:
    hbuf = SppWorkingFileBufferOpen()
    cnt = simbuf.GetBufLineCount(hbuf)        
    for idx in range(0, cnt):
        line = simbuf.GetBufLine(hbuf, idx)
        if line == fname:
            return idx
        
    return -1

def SppWorkingFileGetMatchThenRemove(fname: str) -> int:
    hbuf = SppWorkingFileBufferOpen()
    idx = SppWorkingFileGetMatch(fname)
    if idx >= 0:
        simbuf.DelBufLine(hbuf, idx)
        simbuf.SetBufDirty(hbuf, False)
    cnt = simbuf.GetBufLineCount(hbuf)
    if cnt <= 0:
        SppWorkingFileBufferClose()

    return idx

