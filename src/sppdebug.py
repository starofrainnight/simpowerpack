import pytosim.api.system as simsys
import pytosim.api.filebuffer as simbuf


def SppGetDebugOutputBuf():
    hbuf = simbuf.GetBufHandle("__SPP_DEBUG__")
    if hbuf == 0:
        hbuf = simbuf.NewBuf("__SPP_DEBUG__")
        simbuf.SetCurrentBuf(hbuf)
    return hbuf


def SppTrace(msg):
    hbuf = SppGetDebugOutputBuf()
    simbuf.AppendBufLine(hbuf, msg)
    simbuf.SetBufDirty(hbuf, False)


def SppTraceMacroState():
    hbuf = SppGetDebugOutputBuf()
    simsys.DumpMacroState(hbuf)
    simbuf.SetBufDirty(hbuf, False)


def SppTraceClear():
    hbuf = SppGetDebugOutputBuf()
    simbuf.ClearBuf(hbuf)
    simbuf.SetBufDirty(hbuf, False)
