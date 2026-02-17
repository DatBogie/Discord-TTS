import wave, threading, sys
from pynput import keyboard
from pynput.keyboard import Key
from piper import PiperVoice
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QInputDialog, QWidget
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QObject, Signal

# You may edit the non-grayed-out text below until you see the line saying STOP.

# List of keys:
#   -   <ctrl>  :   Control
#   -   <alt>   :   Alt/Option (mac)
#   -   <cmd>   :   Windows Key/Super/Meta/CMD (mac)

# Replace text inside quotes, separate each key with a plus.
PROMPT_HOTKEY = "<ctrl>+<alt>+h"    # Default: "<ctrl>+<alt>+h"
QUIT_HOTKEY = "<ctrl>+<alt>+x"      # Default: "<ctrl>+<alt>+x"

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
"""

# Default:
[
    Key.ctrl_l,
    Key.alt_l,
    Key.ctrl_r,
    Key.alt_r
]

"""

# Set this to the same as it is at the end of line 5 in `setup.sh`/`setup.bat`.
# Don't change it if you didn't change it the setup script.
TTS_VOICE = "en_US-amy-medium"      # Default: "en_US-amy-medium"

# STOP

class Bridge(QObject):
    trigger = Signal()

app = QApplication(sys.argv)
bridge = Bridge()
win = QWidget()
win.hide()
tray = QSystemTrayIcon(QIcon("Discord-TTS-tray.png"),parent=app)
menu = QMenu("Discord-TTS")
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

def run():
    try:
        t,r = QInputDialog.getText(win,"Discord-TTS","Text to speak:")
        if r and t != "":
            with wave.open("output.wav","wb") as wav_file:
                voice.synthesize_wav(t,wav_file)
            press_hotkey(SOUNDBOARD_HOTKEY)
    except:pass

bridge.trigger.connect(run)

def prompt():
    global debounce
    if debounce: return
    debounce = True
    bridge.trigger.emit()
    threading.Timer(.2,rdb).start()

def stop():
    global kb
    if h:
        h.stop()
    if thread.is_alive():
        thread.join(timeout=1)
    del kb
    app.quit()

menu_prompt = QAction("Open")
menu_prompt.triggered.connect(prompt)
menu_quit = QAction("Quit")
menu_quit.triggered.connect(stop)
menu.addActions([menu_prompt,menu_quit])

tray.setContextMenu(menu)
tray.show()

def main():
    global h
    h = keyboard.GlobalHotKeys({
        PROMPT_HOTKEY: prompt,
        QUIT_HOTKEY: stop
    })
    h.start()
    h.join()

thread = threading.Thread(target=main, daemon=True)
thread.start()

sys.exit(app.exec())