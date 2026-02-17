#!/bin/sh
VERSION="1.0"
# shellcheck disable=SC1091
. ./.venv/bin/activate
pip3 install pyinstaller
pyinstaller main.py -n Discord-TTS --onefile --noconfirm --collect-all piper
cp dist/Discord-TTS .
zip "dist/Discord-TTS-$VERSION.zip" Discord-TTS-tray.png config.yaml Discord-TTS
rm Discord-TTS