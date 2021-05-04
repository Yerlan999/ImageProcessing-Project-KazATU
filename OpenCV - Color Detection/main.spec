# -*- mode: python -*-
from pathlib import Path

block_cipher = None


a = Analysis(['main.py'],
             pathex=[Path('C:/Users/Sony/Desktop/University/OpenCV/OpenCV - Color Detection/main.py')],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += []

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

ic_p = Path('C:/Users/Sony/Desktop/University/OpenCV/OpenCV - Color Detection/icon/icon.ico')

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='KazATUProgram',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon=str(ic_p))
