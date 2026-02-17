#!/bin/sh
VERSION="1.0"
# shellcheck disable=SC1091
. ./.venv/bin/activate
pip3 install pyinstaller
pyinstaller main.py -n Discord-TTS -w --noconfirm
cp -rf dist/Discord-TTS.app .
zip -r "dist/Discord-TTS-$VERSION.zip" Discord-TTS-tray.png config.yaml Discord-TTS.app
rm -rf Discord-TTS.app