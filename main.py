import wave, threading, sys, yaml, os, subprocess
from pynput import keyboard
from pynput.keyboard import Key
from piper import PiperVoice
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QInputDialog, QWidget
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QObject, Signal

DATA_PATH = "."
try:
    DATA_PATH = sys._MEIPASS
except:pass

CONF_PATH = os.path.join(DATA_PATH,"config.yaml")

if not os.path.exists(CONF_PATH):
    with open(CONF_PATH, "w") as f:
        f.write(
"""# (Incomplete) list of special keys:
#   -   <ctrl>  :   Control
#   -   <alt>   :   Alt/Option (mac)
#   -   <cmd>   :   Windows Key/Super/Meta/CMD (mac)

# Separate each key with a plus.
Prompt Hotkey: <ctrl>+<alt>+h
Quit Hotkey: <ctrl>+<alt>+x

# List of special keys: 'alt', 'alt_l', 'alt_r', 'alt_gr', 'backspace', 'caps_lock', 'cmd', 'cmd_l', 'cmd_r', 'ctrl', 'ctrl_l', 'ctrl_r', 'delete', 'down', 'end', 'enter', 'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'home', 'left', 'page_down', 'page_up', 'right', 'shift', 'shift_l', 'shift_r', 'space', 'tab', 'up', 'media_play_pause', 'media_stop', 'media_volume_mute', 'media_volume_down', 'media_volume_up', 'media_previous', 'media_next', 'insert', 'menu', 'num_lock', 'pause', 'print_screen', 'scroll_lock'
Soundboard Hotkey:
  - ctrl_l
  - alt_l
  - ctrl_r
  - alt_r

# Set this to the same as it is at the end of line 5 in `setup.sh`/`setup.bat`.
# Don't change it if you didn't change it the setup script.
TTS Voice: en_US-amy-medium"""
)

with open(CONF_PATH, "r") as f:
    conf = yaml.safe_load(f)

PROMPT_HOTKEY = conf.get("Prompt Hotkey") or "<ctrl>+<alt>+h"
QUIT_HOTKEY = conf.get("Quit Hotkey") or "<ctrl>+<alt>+x"
SOUNDBOARD_HOTKEY = conf.get("Soundboard Hotkey") or [
    "ctrl_l",
    "alt_l",
    "ctrl_r",
    "alt_r"
]
TTS_VOICE = conf.get("TTS Voice") or "en_US-amy-medium"

for i, k in enumerate(SOUNDBOARD_HOTKEY):
    SOUNDBOARD_HOTKEY[i] = getattr(Key,k,k)

class Bridge(QObject):
    trigger = Signal()

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
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

def open_conf():
    if sys.platform == "darwin":
        subprocess.run(["open",CONF_PATH])
    elif sys.platform == "win32":
        os.startfile(CONF_PATH)
    else:
        subprocess.run(["xdg-open",CONF_PATH])

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
menu_conf = QAction("Open Config")
menu_conf.triggered.connect(open_conf)
menu_quit = QAction("Quit")
menu_quit.triggered.connect(stop)
menu.addActions([menu_prompt,menu_conf,menu_quit])

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