@echo off
SET VERSION=1.0
.\.venv\Scripts\activate
pip3 install pyinstaller
pyinstaller main.py -n Discord-TTS --onefile -w --noconfirm --collect-all piper
copy /Y dist\Discord-TTS.exe .
zip "Discord-TTS-%VERSION%.zip" Discord-TTS-tray.png config.yaml Discord-TTS.exe
del Discord-TTS.exe