# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ['interface/main.py'],
    pathex=['.'],              # adiciona “app/” como caminho de busca
    binaries=[],
    # aqui: copie “data/.env” para dentro de uma pasta “data” no bundle
    datas=[('data/.env', 'data')],
    hiddenimports=['modulos'],  # se ainda precisar forçar modulos.py
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,    # <-- certifique-se de que “a.datas” está aqui
    name='main',
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
