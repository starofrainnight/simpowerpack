# -*- coding: utf-8 -*-

import pytosim.api.string as strapi
from . import sppstr


def SppPathGetSep() -> str:
    return "\\"


def SppPathGetBaseName(path: str) -> str:
    pathLen = len(path)
    if pathLen <= 0:
        return ""

    baseNameIdx = sppstr.SppStrRFind2(path, "\\")
    return path[baseNameIdx + 1 : pathLen]
