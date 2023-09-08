# -*- coding: utf-8 -*-

from pytosim.api import (
    filebuffer as simbuf,
    string as simstr,
    symbol as simsym,
    window as simwin,
    types as simtypes,
    system as simsys,
    cmds as simcmds,
    ioutil,
)
from pytosim.api.constant import hNil, Nil
from . import spppath, sppstr, sppdebug, sppworkingfile


def SppCLangSwitchHeaderAndSource():
    # Speed up the later script and avoid problems
    ioutil.StartMsg("Switch between header and source ...")

    hbuf = simbuf.GetCurrentBuf()
    fpath = simbuf.GetBufName(hbuf)

    fbasename = spppath.SppPathGetBaseName(fpath)
    fext = spppath.SppPathGetExtName(fbasename)
    fextTag = simstr.tolower(f"{fext}.")

    hdrExts = ".h.hpp.hxx."
    srcExts = ".c.cpp.cxx."

    if sppstr.SppStrFind2(hdrExts, fextTag) >= 0:
        extsBuf = simbuf.NewBuf("__SPP_EXTS")
        simbuf.AppendBufLine(extsBuf, "c")
        simbuf.AppendBufLine(extsBuf, "cpp")
        simbuf.AppendBufLine(extsBuf, "cxx")
    elif sppstr.SppStrFind2(srcExts, fextTag) >= 0:
        extsBuf = simbuf.NewBuf("__SPP_EXTS")
        simbuf.AppendBufLine(extsBuf, "h")
        simbuf.AppendBufLine(extsBuf, "hpp")
        simbuf.AppendBufLine(extsBuf, "hxx")
    else:
        ioutil.EndMsg()
        return

    fnameWe = spppath.SppPathStripExt(fbasename)

    locBuf = simbuf.NewBuf("__SPP_LOC")
    count = simbuf.GetBufLineCount(extsBuf)
    targetFileBuf = hNil
    ln = 0
    while ln < count:
        ext = simbuf.GetBufLine(extsBuf, ln)
        fnameTryToFind = f"{fnameWe}.{ext}"
        symLocCount = simsym.GetSymbolLocationEx(
            fnameTryToFind, locBuf, 1, 1, 1
        )
        if symLocCount > 0:
            loc = simbuf.GetBufLine(locBuf, 0)  # type: simsym.Symbol

            sppworkingfile.SppWorkingFileAppend(loc.File)

            # EndMsg() must before SetCurrentBuf(), otherwise it won't focus 
            # in the source window 
            ioutil.EndMsg()

            targetFileBuf = simbuf.OpenBuf(loc.File)
            break

        ln = ln + 1

    ioutil.EndMsg()

    simbuf.CloseBuf(locBuf)
    simbuf.CloseBuf(extsBuf)    

    if targetFileBuf != hNil:
        simbuf.SetCurrentBuf(targetFileBuf)



def SppClangCheckIfSelectionCommentted(hwnd: simtypes.HWnd) -> bool:
    hbuf = simwin.GetWndBuf(hwnd)
    sel = simwin.GetWndSel(hwnd)

    # Check if it's comments or not
    for i in range(sel.lnFirst, sel.lnLast + 1):
        line = simbuf.GetBufLine(hbuf, i)
        nonWsIdx = sppstr.SppStrFindFirstNonWs(line, 0)
        if nonWsIdx < 0:
            continue

        # Found first non-whitespace index and check the comment prefix
        if sppstr.SppStrStartsWith(line, "//", nonWsIdx):
            continue

        return False
    else:
        return True


def SppCLangSwitchCommentBlock():
    # Speed up the later script and avoid problems
    ioutil.StartMsg("Switch Comment ...")

    hwnd = simwin.GetCurrentWnd()
    hbuf = simwin.GetWndBuf(hwnd)
    sel = simwin.GetWndSel(hwnd)

    iLine = sel.lnFirst
    iCommentCount = 0
    iUnCommentCount = 0
    iLineCount = sel.lnLast - sel.lnFirst + 1

    if SppClangCheckIfSelectionCommentted(hwnd):
        # Commentted

        # Uncomment selections
        for i in range(sel.lnFirst, sel.lnLast + 1):
            line = simbuf.GetBufLine(hbuf, i)
            nonWsIdx = sppstr.SppStrFindFirstNonWs(line, 0)
            if nonWsIdx < 0:
                continue

            # Found first non-whitespace index and remove the comment prefix
            origSpaces = line[:nonWsIdx]
            restText = line[nonWsIdx:]
            if sppstr.SppStrStartsWith(restText, "//", 0):
                if restText[2] == " ":
                    restText = restText[3:]
                else:
                    restText = restText[2:]
                line = f"{origSpaces}{restText}"
                simbuf.DelBufLine(hbuf, i)
                simbuf.InsBufLine(hbuf, i, line)

    else:
        # Uncommentted

        # Comment selections
        for i in range(sel.lnFirst, sel.lnLast + 1):
            line = simbuf.GetBufLine(hbuf, i)
            nonWsIdx = sppstr.SppStrFindFirstNonWs(line, 0)
            if nonWsIdx < 0:
                continue

            # Found first non-whitespace index and insert the comment prefix
            origSpaces = line[:nonWsIdx]
            restText = line[nonWsIdx:]

            line = f"{origSpaces}// {restText}"
            simbuf.DelBufLine(hbuf, i)
            simbuf.InsBufLine(hbuf, i, line)

    line = simbuf.GetBufLine(hbuf, 0)
    sel.ichLim = len(line)
    simwin.SetWndSel(hwnd, sel)

    ioutil.EndMsg()


def SppClangInsertHeaderGuard():
    ioutil.StartMsg("Insert header guard")

    hwnd = simwin.GetCurrentWnd()
    hbuf = simwin.GetWndBuf(hwnd)

    systime = ioutil.GetSysTime(0)
    proginfo = simsys.GetProgramEnvironmentInfo()

    # Get a unique number for this device
    sn = sppstr.SppStrReplace(f"{proginfo.SerialNumber}", "-", "")[3:]

    year = sppstr.SppStrIntFormat(systime.Year, 4)
    month = sppstr.SppStrIntFormat(systime.Month, 2)
    day = sppstr.SppStrIntFormat(systime.Day, 2)
    hour = sppstr.SppStrIntFormat(systime.Hour, 2)
    minute = sppstr.SppStrIntFormat(systime.Minute, 2)
    second = sppstr.SppStrIntFormat(systime.Second, 2)
    milliseconds = sppstr.SppStrIntFormat(systime.Milliseconds, 3)
    wndCount = simwin.WndListCount()
    guard = f"_9M_{sn}{year}{month}{day}{hour}{hour}{minute}{second}{milliseconds}{hwnd}{hbuf}{wndCount}"

    prop = simbuf.GetBufProps(hbuf)

    # Add newline at the buffer end
    simbuf.InsBufLine(hbuf, prop.lnCount, "")
    simbuf.InsBufLine(hbuf, prop.lnCount, f"#endif // {guard}")
    simbuf.InsBufLine(hbuf, prop.lnCount, "")
    simbuf.InsBufLine(hbuf, 0, f"#ifndef {guard}")
    simbuf.InsBufLine(hbuf, 1, f"#define {guard}")
    simbuf.InsBufLine(hbuf, 2, "")

    ioutil.EndMsg()


def SppCLangWrapCppExtern():
    ioutil.StartMsg("Wrap CPP externs for C")

    hwnd = simwin.GetCurrentWnd()
    hbuf = simwin.GetWndBuf(hwnd)
    lnFirst = simwin.GetWndSelLnFirst(hwnd)
    lnLast = simwin.GetWndSelLnLast(hwnd)

    lnPos = lnFirst
    simbuf.InsBufLine(hbuf, lnPos, "#ifdef __cplusplus")
    lnPos = lnPos + 1
    simbuf.InsBufLine(hbuf, lnPos, 'extern "C" {')
    lnPos = lnPos + 1
    simbuf.InsBufLine(hbuf, lnPos, "#endif /* __cplusplus */")
    lnPos = lnPos + 1
    simbuf.InsBufLine(hbuf, lnPos, "")
    lnPos = lnPos + 1

    lnPos = lnLast + (lnPos - lnFirst) + 1
    simbuf.InsBufLine(hbuf, lnPos, "")
    lnPos = lnPos + 1
    simbuf.InsBufLine(hbuf, lnPos, "#ifdef __cplusplus")
    lnPos = lnPos + 1
    simbuf.InsBufLine(hbuf, lnPos, "}")
    lnPos = lnPos + 1
    simbuf.InsBufLine(hbuf, lnPos, "#endif /* __cplusplus */")

    ioutil.EndMsg()


def SppCLangJumpToDefinition():
    ioutil.StartMsg("Jump to definition ...")
    hwnd = simwin.GetCurrentWnd()
    hbuf = simwin.GetWndBuf(hwnd)
    lnFirst = simwin.GetWndSelLnFirst(hwnd)

    # Check if a
    line = simbuf.GetBufLine(hbuf, lnFirst)
    idx = sppstr.SppStrFindFirstNonWs(line, 0)
    if idx < 0:
        ioutil.EndMsg()
        return

    if line[idx] != "#":
        ioutil.EndMsg()

        simcmds.Jump_To_Definition()
        return

    idxDoubleQuote = sppstr.SppStrFind(line, '"', 0, -1)
    idxLessThanSign = sppstr.SppStrFind(line, "<", 0, -1)
    if idxDoubleQuote < 0 and idxLessThanSign < 0:
        ioutil.EndMsg()
        return

    if idxDoubleQuote > idxLessThanSign:
        # '"'
        idxDoubleQuoteEnd = sppstr.SppStrFind(
            line, '"', idxDoubleQuote + 1, -1
        )
        fpath = line[idxDoubleQuote + 1, idxDoubleQuoteEnd]
    else:
        # '<'
        idxLessThanSignEnd = sppstr.SppStrFind(
            line, ">", idxLessThanSign + 1, -1
        )
        fpath = line[idxLessThanSign + 1, idxLessThanSignEnd]
    
    hbuf = simbuf.NewBuf("__SPP_SYMBOL_LOCS.h")
    fpath = sppstr.SppStrReplace(fpath, "/", "\\")
    fbasename = spppath.SppPathGetBaseName(fpath)        
    
    # Fix the symbol from idiot GetCurSymbol()
    fbasename = sppstr.SppStrReplace(fbasename, simstr.CharFromAscii(2), "\.")

    # We must stop the msgbox before SetCurrentBuf(), so it's allowed to popup.
    ioutil.EndMsg()
  
    count = simsym.GetSymbolLocationEx(fbasename, hbuf, 1, 1, 0)
    if count == 1:
        # Found only one matched, just directly open that file
        loc = simbuf.GetBufLine(hbuf, 0)
        simbuf.SetCurrentBuf(simbuf.OpenBuf(loc.file))
    else:
        # Force to popup the mulit-matched window
        simbuf.AppendBufLine(hbuf, f'#include "{fbasename}"')
        simbuf.SetBufIns(hbuf, 0, 12)
        simbuf.SetCurrentBuf(hbuf)
        simcmds.Jump_To_Definition()
    
    simbuf.CloseBuf(hbuf)


def SppCLangCheckIfCSourceFile(fpath: str) -> bool:
    fext = spppath.SppPathGetExtName(fpath)
    cexts = ".h.hpp.hxx.inl.c.cpp.cxx."
    return sppstr.SppStrFind(cexts, fext, 0, -1) >= 0
