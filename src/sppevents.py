# -*- coding: utf-8 -*-
from pytosim.api import (event, filebuffer as simbuf, system as simsys, ioutil)
from pytosim.api.constant import *
from . import sppstr, sppworkingfile, spppath

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

    # NOTE: We won't clear the list, because we might open that file multi-times   
    
@event.DocumentSaveComplete
def SppOnDocumentSaveComplete(sFile: str):
    # Format the document when it's c/cpp sources
    fext = spppath.SppPathGetExtName(sFile)
    cexts = ".h.hpp.hxx.inl.c.cpp.cxx."
    if sppstr.SppStrFind(cexts, fext, 0, -1) < 0:
        return

    simsys.RunCmdLine(f'clang-format -i --style=file --fallback-style=none "{sFile}"', Nil, True)

    # Refresh the buffer
    curBuf  = simbuf.GetCurrentBuf()
    fileBuf = simbuf.GetBufHandle(sFile)

    if curBuf == fileBuf:
        isCurBuf = True
    else:
        isCurBuf = False

    simbuf.CloseBuf(fileBuf)    
    fileBuf = simbuf.OpenBuf(sFile)

    if isCurBuf:
        simbuf.SetCurrentBuf(fileBuf)
