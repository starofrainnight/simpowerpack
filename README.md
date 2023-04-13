# Source Insight Macro PowerPack (SIMPP)

A series Source Insight macros for helping your life easier.

## Build

The macro files not directly write by Source Insight Macro language but generate by a transpiler [pytosim](https://github.com/starofrainnight/pytosim).

Before build the macros, you must prepare the python3 environment first:

    python3 -m pip install -r requirements.txt

All macro files will generated by execute commands below:

    python3 ./build.py
