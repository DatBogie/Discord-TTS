#!/bin/sh
python3 -m venv .venv
# shellcheck disable=SC1091
. ./.venv/bin/activate
pip3 install -r requirements.txt
python3 -m piper.download_voices en_US-amy-medium