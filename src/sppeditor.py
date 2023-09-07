# -*- coding: utf-8 -*-
from pytosim.api import (
    window as simwin,
    filebuffer as simbuf,
    cmds,
    ioutil
)
from . import sppstr


def SppOnKeyHome():
    hwnd = simwin.GetCurrentWnd()
    if hwnd == hNil:
        return

    ioutil.StartMsg("Jump to home...")

    sel = simwin.GetWndSel(hwnd)
    hbuf = simwin.GetWndBuf(hwnd)

    # if the first character on the line is white space,
    # then move forward to the first word on the line
    line = simbuf.GetBufLine(hbuf, sel.lnFirst)
    ichNonWs = sppstr.SppStrFindFirstNonWs(line, 0)
    if ichNonWs == sel.ichFirst:
        ich = 0
    elif sel.ichFirst < ichNonWs:
        if sel.ichFirst == 0:
            ich = ichNonWs
        else:
            ich = 0
    else:
        ich = ichNonWs

    cmds.Beginning_of_Line()
    simbuf.SetBufIns(hbuf, sel.lnFirst, ich)
    ioutil.EndMsg()


def SppOnPairCharKeyPressed(openChar, closeChar):
    hwnd = simwin.GetCurrentWnd()
    if hwnd == hNil:
        return

    sel = simwin.GetWndSel(hwnd)
    hbuf = simwin.GetWndBuf(hwnd)
    selText = simbuf.GetBufSelText(hbuf)
    if len(selText) > 0:
        selText = f"{openChar}{selText}{closeChar}"
        simbuf.SetBufSelText(hbuf, selText)
    else:
        simbuf.SetBufSelText(hbuf, openChar)


def SppOnOpenParenKeyPressed():
    SppOnPairCharKeyPressed("(", ")")


def SppOnOpenBraceKeyPressed():
    SppOnPairCharKeyPressed("{", "}")


def SppOnOpenSquareBracketKeyPressed():
    SppOnPairCharKeyPressed("[", "]")


def SppOnOpenAngleBracketKeyPressed():
    SppOnPairCharKeyPressed("<", ">")


def SppOnOpenDoubleQuoteKeyPressed():
    SppOnPairCharKeyPressed('"', '"')


def SppOnOpenSingleQuoteKeyPressed():
    SppOnPairCharKeyPressed("'", "'")
