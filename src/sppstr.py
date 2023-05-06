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


def SppStrFindFirstNonWs(s: str, first: int) -> int:
    sLen = len(s)
    if sLen <= 0:
        return -1

    if first < 0:
        first = 0
    elif first >= sLen:
        first = sLen - 1

    for i in range(first, sLen):
        if (s[i] == " ") or (s[i] == "\t"):
            continue

        return i

    return -1


def SppStrFindFirstWs(s: str, first: int) -> int:
    sLen = len(s)
    if sLen <= 0:
        return -1

    if first < 0:
        first = 0
    elif first >= sLen:
        first = sLen - 1

    for i in range(first, sLen):
        if (s[i] != " ") and (s[i] != "\t"):
            continue

        return i

    return -1


def SppStrStartsWith(s: str, sub: str, first: int) -> bool:
    sLen = len(s)
    if first < 0:
        first = 0
    elif first >= sLen:
        first = sLen - 1

    subLen = len(sub)
    if subLen > (sLen - first):
        return False

    for j in range(0, subLen):
        if s[first + j] != sub[j]:
            return False

    return True


def SppStrEndsWith(s: str, sub: str) -> bool:
    sLen = len(s)
    subLen = len(sub)
    if subLen > sLen:
        return False

    for j in range(subLen - 1, -1, -1):
        if s[j] != sub[j]:
            return False

    return True
