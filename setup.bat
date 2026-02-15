@echo off
python -m venv .venv
.\.venv\Scripts\activate.bat
pip3 install -r requirements.txt
python -m piper.download_voices en_US-amy-medium