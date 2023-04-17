# -*- coding: utf-8 -*-


def SppStrFind(s: str, sub: str, start: int = 0, end: int = -1):
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


def SppStrFind2(s: str, sub: str):
    return SppStrFind(s, sub, 0, -1)
