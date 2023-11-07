# -*- coding: utf-8 -*-
from pytosim.api import (
    event,
    filebuffer as simbuf,
    system as simsys,
    cmds as simcmds,
    ioutil,
)
from pytosim.api.constant import *
from . import sppstr, sppworkingfile, spppath, sppbuffer, sppclang


@event.DocumentOpen
def SppOnDocumentOpen(sFile: str):
    if sppstr.SppStrStartsWith(sFile, "__SPP_", 0):
        return

    if not sppclang.SppCLangCheckIfCSourceFile(sFile):
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


@event.DocumentSave
def SppOnDocumentSave(sFile: str):
    # Some source insight 3 version does not have DocumentSaveComplete event, so
    # we keep using the DocumentSave event instead.

    # Format the document when it's c/cpp sources
    if not sppclang.SppCLangCheckIfCSourceFile(sFile):
        return

    buf = simbuf.GetBufHandle(sFile)
    if not simbuf.IsBufDirty(buf):
        return

    ioutil.StartMsg("Saving ...")

    # Save the document to disk before format
    simbuf.SaveBuf(buf)
    simsys.RunCmdLine(
        f'cmd /c clang-format -i --style=file --fallback-style=none "{sFile}"',
        Nil,
        True,
    )

    # Refresh the buffer
    sppbuffer.SppBufferReloadFromFilePath(sFile)

    ioutil.EndMsg()
