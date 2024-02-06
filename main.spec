# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['D:/workspaces/routine_checking_app_ws/Routine-Checking-App'],  # Replace with the path to your source code
             binaries=[],
             datas=[  # Add all the additional files you need to include here
                 ('database/schema.sql', 'database'),  # Include your schema.sql file
                 ('resources/*.png', 'resources'),  # Include all .png files from the 'resources' directory
                 ('resources/*.ico', 'resources'),  # Include all .png files from the 'resources' directory
                 # Add more as needed
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Routine_Checking_App',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='resources/window_icon_icon.ico')  # Use your main window icon here

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Routine_Checking_App')
