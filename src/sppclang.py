# -*- coding: utf-8 -*-

from pytosim.api import (
    filebuffer as simbuf,
    string as simstr,
    symbol as simsym,
    ioutil,
)
from . import spppath, sppstr, sppdebug


def SppCLangSwitchHeaderAndSource():
    hbuf = simbuf.GetCurrentBuf()
    fpath = simbuf.GetBufName(hbuf)

    fbasename = spppath.SppPathGetBaseName(fpath)
    fext = spppath.SppPathGetExtName(fbasename)
    fextTag = simstr.tolower(f"{fext}.")

    hdrExts = ".h.hpp.hxx."
    srcExts = ".c.cpp.cxx."

    if sppstr.SppStrFind2(hdrExts, fextTag) >= 0:
        extsBuf = simbuf.NewBuf()
        simbuf.AppendBufLine(extsBuf, "c")
        simbuf.AppendBufLine(extsBuf, "cpp")
        simbuf.AppendBufLine(extsBuf, "cxx")
    elif sppstr.SppStrFind2(srcExts, fextTag) >= 0:
        extsBuf = simbuf.NewBuf()
        simbuf.AppendBufLine(extsBuf, "h")
        simbuf.AppendBufLine(extsBuf, "hpp")
        simbuf.AppendBufLine(extsBuf, "hxx")
    else:
        return

    fnameWe = spppath.SppPathStripExt(fbasename)

    locBuf = simbuf.NewBuf()
    count = simbuf.GetBufLineCount(extsBuf)
    ln = 0
    while ln < count:
        ext = simbuf.GetBufLine(extsBuf, ln)
        fnameTryToFind = f"{fnameWe}.{ext}"
        symLocCount = simsym.GetSymbolLocationEx(
            fnameTryToFind, locBuf, 1, 1, 1
        )
        if symLocCount > 0:
            loc = simbuf.GetBufLine(locBuf, 0)  # type: simsym.Symbol
            targetFileBuf = simbuf.OpenBuf(loc.File)
            if targetFileBuf != hNil:
                simbuf.SetCurrentBuf(targetFileBuf)
            break

        ln = ln + 1

    simbuf.CloseBuf(locBuf)
    simbuf.CloseBuf(extsBuf)


def SppClangSwitchCommentBlock():
    pass
