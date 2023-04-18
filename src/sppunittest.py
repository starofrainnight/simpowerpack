from pytosim.api import filebuffer
from pytosim.api.types import HBuffer
from . import sppdebug


def SppAssertEqual(a, b, msg):
    if a == b:
        result = "Passed"
    else:
        result = "Failed"

    msg = f"ASSERT:{result}: {msg}: {a} == {b}"

    sppdebug.SppTrace(msg)


def SppAssertEqual2(a, b):
    SppAssertEqual(a, b, "NONE")
