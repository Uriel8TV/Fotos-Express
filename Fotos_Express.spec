# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icono.ico', '.'),  # Empaqueta el icono dentro del ejecutable para que no falle al iniciar
    ],
    hiddenimports=['reportlab', 'PIL', 'PIL.Image', 'PIL.ImageTk'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Foto-Express',        # Nombre final del archivo ejecutable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                  # Comprime el ejecutable para que pese menos
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,             # EVITA que se abra la molesta ventana negra de consola detrás de la app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icono.ico'           # Aplica el icono visual al archivo .exe en Windows
)
