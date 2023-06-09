# -*- coding: utf-8 -*-
from pytosim.api import ioutil


def SppCLangIdeInstall():
    # Ctrl+/,  "/" = 47, "Ctrl+/" = 1071
    ioutil.AssignKeyToCmd(1071, "SppClangSwitchCommentBlock")
    # Alt+o
    ioutil.AssignKeyToCmd(
        ioutil.KeyFromChar("o", 0, 0, 1), "SppCLangSwitchHeaderAndSource"
    )
    # F11, trigger the window list
    ioutil.AssignKeyToCmd(ioutil.KeyFromChar("F11", 0, 0, 0), "Window_List")

    # Bind "Jump_To_Definition" function
    # Ctrl+=, "=" = 61, "Ctrl+=" = 1085, "Ctrl+Shift+=" = 1853
    ioutil.AssignKeyToCmd(1853, "SuperJumpToDefinition")

    # (
    ioutil.AssignKeyToCmd(808, "SppOnOpenParenKeyPressed")

    # [, it not works with simple symbol!
    # ioutil.AssignKeyToCmd(91, "SppOnOpenSquareBracketKeyPressed")

    # {
    ioutil.AssignKeyToCmd(891, "SppOnOpenBraceKeyPressed")

    # "
    ioutil.AssignKeyToCmd(802, "SppOnOpenDoubleQuoteKeyPressed")

    # ', it not works with simple symbol!
    ioutil.AssignKeyToCmd(39, "SppOnOpenSingleQuoteKeyPressed")

    # <
    ioutil.AssignKeyToCmd(828, "SppOnOpenAngleBracketKeyPressed")
