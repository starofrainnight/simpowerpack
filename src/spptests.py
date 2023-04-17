import sppstr
import sppdebug
from sppunittest import SppBegin, SppEnd, SppAssertEqual


def SppTests():
    lvalue = sppstr.SppStrFind2("0123456789", "234")
    SppAssertEqual(lvalue, 2)

    lvalue = sppstr.SppStrFind2("234", "234")
    SppAssertEqual(lvalue, 0)

    lvalue = sppstr.SppStrFind2("", "234")
    SppAssertEqual(lvalue, -1)

    lvalue = sppstr.SppStrFind2("2", "234")
    SppAssertEqual(lvalue, -1)

    lvalue = sppstr.SppStrFind2("0123456789", "2")
    SppAssertEqual(lvalue, 2)

    lvalue = sppstr.SppStrFind2("0", "2")
    SppAssertEqual(lvalue, -1)

    lvalue = sppstr.SppStrFind2("012", "2")
    SppAssertEqual(lvalue, 2)

    lvalue = sppstr.SppStrFind2("2", "2")
    SppAssertEqual(lvalue, 0)

    # Don't end the buffer, otherwise you won't see the results window
    # SppEnd(hbuf)
