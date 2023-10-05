# -*- coding: utf-8 -*-
from pytosim.api import window as simwin, filebuffer as simbuf, cmds, ioutil
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
    if sel.fExtended:
        if sel.lnFirst == sel.lnLast:
            line = simbuf.GetBufLine(hbuf, sel.lnFirst)

            firstPart = line[: sel.ichFirst]

            secondPart = line[sel.ichFirst : sel.ichLim]

            thirdPart = line[sel.ichLim :]

            line = f"{firstPart}{openChar}{secondPart}{closeChar}{thirdPart}"
            simbuf.PutBufLine(hbuf, sel.lnFirst, line)

            sel.ichFirst = sel.ichFirst + len(openChar)
            sel.ichLim = sel.ichLim + len(openChar)
            simwin.SetWndSel(hwnd, sel)
        else:
            line = simbuf.GetBufLine(hbuf, sel.lnFirst)
            firstPart = line[: sel.ichFirst]
            secondPart = line[sel.ichFirst :]
            line = f"{firstPart}{openChar}{secondPart}"
            simbuf.PutBufLine(hbuf, sel.lnFirst, line)

            line = simbuf.GetBufLine(hbuf, sel.lnLast)
            firstPart = line[: sel.ichLim]
            secondPart = line[sel.ichLim :]
            line = f"{firstPart}{closeChar}{secondPart}"
            simbuf.PutBufLine(hbuf, sel.lnLast, line)

            sel.ichFirst = sel.ichFirst + len(openChar)
            simwin.SetWndSel(hwnd, sel)
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
