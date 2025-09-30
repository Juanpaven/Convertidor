# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files

# Limpiar el path para evitar conflictos con numpy
sys.path = [p for p in sys.path if 'numpy' not in p.lower()]

# Datos adicionales necesarios
datas = []
datas += collect_data_files('pandas')
datas += collect_data_files('numpy')
datas += collect_data_files('pdfplumber')
datas += collect_data_files('openpyxl')

a = Analysis(
    ['Convertidor.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'numpy',
        'numpy._core',
        'numpy._core._multiarray_umath',
        'numpy.core',
        'numpy.core._multiarray_umath',
        'numpy.linalg._umath_linalg',
        'pandas',
        'pandas._libs',
        'pandas._libs.tslibs.timedeltas',  
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.offsets',
        'pandas._libs.join',
        'pandas._libs.lib',
        'pandas.io.formats.style',
        'pandas.plotting',
        'pdfplumber',
        'pdfplumber.pdf',
        'pdfplumber._typing',
        'openpyxl',
        'openpyxl.styles',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'PIL',
        'PIL._tkinter_finder'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pytest',
        'IPython',
        'jupyter'
    ],
    noarchive=False,
    optimize=0,
)

# Filtrar archivos problemáticos
a.datas = [x for x in a.datas if not ('numpy' in x[1] and x[1].endswith('.py'))]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ConvertirPDFaExcel_Final',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Mantener consola para debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)