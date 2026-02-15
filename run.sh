#!/bin/sh
# shellcheck disable=SC1091
. ./.venv/bin/activate
pip3 install -r requirements.txt
python3 main.py