#!/usr/bin/env python3

import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    'excludes': [],
    'optimize': 2
}

setup(
    name='Warehouse Map',
    version='1.0.0',
    description='Visual mapper for warehouse items',
    executables=[Executable('main.pyw', base=('Win32GUI' if sys.platform == 'win32' else None))],
    options={'build_exe': build_exe_options}
)
