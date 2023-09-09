# -*- coding: utf-8 -*-

from pytosim.api import (filebuffer as simbuf, types as simtypes, cmds as simcmds)
from pytosim.api.constant import hNil

def SppBufferReload(handle: simtypes.HBuffer):
    simbuf.SetCurrentBuf(handle)
    simcmds.Reload_File()

def SppBufferReloadFromFilePath(fpath: str):
    handle = simbuf.GetBufHandle(fpath)
    if handle != hNil:
        SppBufferReload(handle)                