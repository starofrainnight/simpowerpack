# -*- coding: utf-8 -*-
from pytosim.api import (
    event,
    filebuffer as simbuf,
    system as simsys,
    cmds as simcmds,
    ioutil,
)
from pytosim.api.constant import *
from . import sppstr, sppworkingfile, spppath, sppbuffer


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

    sppbuffer.SppBufferReloadFromFilePath(sFile)

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

    simsys.RunCmdLine(
        f'clang-format -i --style=file --fallback-style=none "{sFile}"',
        Nil,
        True,
    )

    # Refresh the buffer
    sppbuffer.SppBufferReloadFromFilePath(sFile)
