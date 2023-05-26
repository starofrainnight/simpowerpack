# -*- coding: utf-8 -*-
from pytosim.api import (
    window as simwin,
    filebuffer as simbuf,
    string as simstr,
    cmds,
)
from . import sppstr


def SppOnKeyHome():
    hwnd = simwin.GetCurrentWnd()
    if hwnd == hNil:
        return

    sel = simwin.GetWndSel(hwnd)
    hbuf = simwin.GetWndBuf(hwnd)

    # if the first character on the line is white space,
    # then move forward to the first word on the line
    ichNonWs = sppstr.SppStrFindFirstNonWs()
    if ichNonWs == sel.ichFirst:
        if ichNonWs != 0:
            ich = 0
        else:
            ich = ichNonWs
    elif sel.ichFirst < ichNonWs:
        ich = 0
    else:
        ich = ichNonWs

    cmds.Beginning_of_Line()
    simbuf.SetBufIns(hbuf, sel.lnFirst, ich)
