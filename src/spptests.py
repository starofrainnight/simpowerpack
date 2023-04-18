from . import sppdebug as sppdbg, sppstr
from . import sppunittest as spput, spppath


def SppTests():
    sppdbg.SppTraceClear()
    sppdbg.SppTrace("* Checking SppStrFind() ...")

    lvalue = sppstr.SppStrFind2("0123456789", "234")
    spput.SppAssertEqual(lvalue, 2, "1")

    lvalue = sppstr.SppStrFind2("234", "234")
    spput.SppAssertEqual(lvalue, 0, "2")

    lvalue = sppstr.SppStrFind2("", "234")
    spput.SppAssertEqual(lvalue, -1, "3")

    lvalue = sppstr.SppStrFind2("2", "234")
    spput.SppAssertEqual(lvalue, -1, "4")

    lvalue = sppstr.SppStrFind2("0123456789", "2")
    spput.SppAssertEqual(lvalue, 2, "5")

    lvalue = sppstr.SppStrFind2("0", "2")
    spput.SppAssertEqual(lvalue, -1, "6")

    lvalue = sppstr.SppStrFind2("012", "2")
    spput.SppAssertEqual(lvalue, 2, "7")

    lvalue = sppstr.SppStrFind2("2", "2")
    spput.SppAssertEqual(lvalue, 0, "8")

    sppdbg.SppTrace("* Checking SppStrRFind() ...")

    lvalue = sppstr.SppStrRFind2("0123456789", "234")
    spput.SppAssertEqual(lvalue, 2, "1")

    sppdbg.SppTrace("* Checking SppPath ...")
    spput.SppAssertEqual(
        spppath.SppPathGetBaseName("d:\\dir\\text.txt"), "text.txt", "1"
    )

    # Don't end the buffer, otherwise you won't see the results window
    # SppEnd(hbuf)
