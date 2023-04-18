# -*- coding: utf-8 -*-

from . import sppdebug as sppdbg


def SppStrFind(s: str, sub: str, start: int = 0, end: int = -1) -> int:
    sLen = len(s)
    subLen = len(sub)

    if end < 0:
        end = sLen

    if start >= end:
        return -1

    cmpLen = end - start
    if subLen > cmpLen:
        return -1

    if subLen <= 0:
        return start

    cmpEnd = end - subLen + 1
    for sIdx in range(start, cmpEnd):
        lIdx = sIdx
        for rIdx in range(0, subLen):
            if s[lIdx] != sub[rIdx]:
                break
            lIdx = lIdx + 1
        else:
            return sIdx

    return -1


def SppStrFind2(s: str, sub: str) -> int:
    return SppStrFind(s, sub, 0, -1)


def SppStrRFind(s: str, sub: str, start: int = 0, end: int = -1) -> int:
    sLen = len(s)
    subLen = len(sub)

    if end < 0:
        end = sLen

    if start >= end:
        return -1

    cmpLen = end - start
    if subLen > cmpLen:
        return -1

    if subLen <= 0:
        return end

    cmpEnd = end - subLen + 1
    for sIdx in range(cmpEnd - 1, start - 1, -1):
        lIdx = sIdx
        for rIdx in range(0, subLen):
            lvalue = s[lIdx]
            rvalue = sub[rIdx]
            if s[lIdx] != sub[rIdx]:
                break
            lIdx = lIdx + 1
        else:
            return sIdx

    return -1


def SppStrRFind2(s: str, sub: str) -> int:
    return SppStrRFind(s, sub, 0, -1)
