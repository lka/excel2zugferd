# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['excel2zugferd.py'],
    pathex=[],
    binaries=[],
    datas=[('_internal/Fonts', 'Fonts'), ('./.venv/Lib/site-packages/drafthorse/schema', 'drafthorse/schema'), ('_internal/version.json', '.'), ('_internal/sRGB2014.icc', '.')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='excel2zugferd',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='excel2zugferd',
)
