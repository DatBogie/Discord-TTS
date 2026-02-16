import wave, sys, threading
from pynput import keyboard
from pynput.keyboard import Key
from tkinter import simpledialog
from piper import PiperVoice

# You may edit the non-grayed-out text below until you see the line saying STOP.

# List of keys:
#   -   <ctrl>  :   Control
#   -   <alt>   :   Alt/Option (mac)
#   -   <cmd>   :   Windows Key/Super/Meta/CMD (mac)

# Replace text inside quotes, separate each key with a plus.
PROMPT_HOTKEY = "<ctrl>+<alt>+h"
QUIT_HOTKEY = "<ctrl>+<alt>+x"

# Use auto-fill for list of available keys.
# (Type `Key.` (without the "`"s), then press CTRL+SPACE).
# No quotes; replace the lines between the square brackets ( []s ).
# Each key should be separated with a comma.
SOUNDBOARD_HOTKEY = [
    Key.ctrl_l,
    Key.alt_l,
    Key.ctrl_r,
    Key.alt_r
]

# Set this to the same as it is at the end of line 5 in `setup.sh`/`setup.bat`.
# Don't change it if you didn't change it the setup script.
TTS_VOICE = "en_US-amy-medium"

# STOP

voice = PiperVoice.load(f"./{TTS_VOICE}.onnx")
kb = keyboard.Controller()
debounce = False

def press_hotkey(l:list[Key]):
    for x in l:
        kb.press(x)
    for i in range(len(l)-1,-1,-1):
        kb.release(l[i])

def rdb():
    global debounce
    debounce = False

def prompt():
    global debounce
    if debounce: return
    debounce = True
    try:
        r = simpledialog.askstring("Discord-TTS","Text to speak:")
        if r is not None and r != "":
            with wave.open("output.wav","wb") as wav_file:
                voice.synthesize_wav(r,wav_file)
            press_hotkey(SOUNDBOARD_HOTKEY)
    except:pass
    threading.Timer(.2,rdb).start()

def quit():
    h.stop()
    sys.exit(0)

with keyboard.GlobalHotKeys({
    PROMPT_HOTKEY: prompt,
    QUIT_HOTKEY: quit
}) as h:
    h.join()
