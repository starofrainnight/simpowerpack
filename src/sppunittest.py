from pytosim.api import filebuffer
from pytosim.api.types import HBuffer
import sppdebug


def SppAssertEqual(a, b):
    if a == b:
        result = True
    else:
        result = False

    msg = f"ASSERT: {a} == {b}, RESULT: {result}"

    sppdebug.SppTrace(msg)
