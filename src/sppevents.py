# -*- coding: utf-8 -*-
from pytosim.api import (event, filebuffer as simbuf, system as simsys, ioutil)
from pytosim.api.constant import *
from . import sppstr, sppworkingfile

@event.DocumentOpen
def SppOnDocumentOpen(sFile: str):
    if sppstr.SppStrStartsWith(sFile, "__SPP_", 0):
        return
    
    ioutil.StartMsg("Checking document codec ...")
    listBufTag = "__SPP_CODEC_FIXED_LIST"
    listBuf = simbuf.GetBufHandle(listBufTag)
    if listBuf == hNil:
        listBuf = simbuf.NewBuf(listBufTag)
    else:
        cnt = simbuf.GetBufLineCount(listBuf)

        for i in range(0, cnt):
            line = simbuf.GetBufLine(listBuf, i)
            if line == sFile:
                # If file already parsed, just  skip it
                ioutil.EndMsg()
                return          

    simsys.RunCmdLine(f'ensuregbkcodec.exe "{sFile}"', Nil, True)
    
    ioutil.EndMsg()
    
    if sppworkingfile.SppWorkingFileGetMatchThenRemove(sFile)>= 0:
        return

    fileBuf = simbuf.GetBufHandle(sFile)
    simbuf.CloseBuf(fileBuf)
    fileBuf = simbuf.OpenBuf(sFile)
    simbuf.SetCurrentBuf(fileBuf)

    simbuf.AppendBufLine(listBuf, sFile)
    simbuf.SetBufDirty(listBuf, False)
    

@event.DocumentClose
def SppOnDocumentClose(sFile: str):
    listBufTag = "__SPP_CODEC_FIXED_LIST"
    listBuf = simbuf.GetBufHandle(listBufTag)
    if listBuf == hNil:
        return
    
    ioutil.StartMsg("Closing document ...")
    cnt = simbuf.GetBufLineCount(listBuf)
    for i in range(0, cnt):
        line = simbuf.GetBufLine(listBuf, i)
        if line == sFile:
            simbuf.DelBufLine(listBuf, i)
            simbuf.SetBufDirty(listBuf, False)
            ioutil.EndMsg()
            return
        
    ioutil.EndMsg()
    