# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Convertidor.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/delag/OneDrive/Escritorio/Juan Avendaño/Convertidor/.venv/Lib/site-packages/pdfplumber', 'pdfplumber'), ('C:/Users/delag/OneDrive/Escritorio/Juan Avendaño/Convertidor/.venv/Lib/site-packages/pandas', 'pandas'), ('C:/Users/delag/OneDrive/Escritorio/Juan Avendaño/Convertidor/.venv/Lib/site-packages/openpyxl', 'openpyxl')],
    hiddenimports=['pdfplumber', 'pandas', 'openpyxl', 'tkinter', 'psutil'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ConvertirPDFaExcel_v2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
