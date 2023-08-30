# -*- coding: utf-8 -*-
from pytosim.api import (event, filebuffer as simbuf, system as simsys)
from pytosim.api.constant import *

@event.DocumentOpen
def SppOnDocumentOpen(fpath: str):
    listBufTag = "__SPP_CODEC_FIXED_LIST"
    listBuf = simbuf.GetBufHandle(listBufTag)
    if listBuf == hNil:
        listBuf = simbuf.NewBuf(listBufTag)
    else:
        cnt = simbuf.GetBufLineCount(listBuf)

        for i in range(0, cnt):
            line = simbuf.GetBufLine(listBuf, i)
            if line == fpath:
                # If file already parsed, just  skip it
                return

    simsys.RunCmdLine(f'ensuregbkcodec.exe "{fpath}"', Nil, True)
    fileBuf = simbuf.GetBufHandle(fpath)
    simbuf.CloseBuf(fileBuf)
    fileBuf = simbuf.OpenBuf(fpath)
    simbuf.SetCurrentBuf(fileBuf)

    simbuf.AppendBufLine(listBuf, fpath)
    simbuf.SetBufDirty(listBuf, False)

@event.DocumentClose
def SppOnDocumentClose(fpath: str):
    listBufTag = "__SPP_CODEC_FIXED_LIST"
    listBuf = simbuf.GetBufHandle(listBufTag)
    if listBuf == hNil:
        return
    
    cnt = simbuf.GetBufLineCount(listBuf)
    for i in range(0, cnt):
        line = simbuf.GetBufLine(listBuf, i)
        if line == fpath:
            simbuf.DelBufLine(listBuf, i)
            simbuf.SetBufDirty(listBuf, False)
            return
    