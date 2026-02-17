import wave, threading, sys, yaml, os, subprocess, webbrowser, pathlib
from pynput import keyboard
from pynput.keyboard import Key
from piper import PiperVoice
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QInputDialog, QWidget, QMessageBox, QDialog, QComboBox, QVBoxLayout, QDialogButtonBox, QLabel
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QObject, Signal

DATA_PATH = "."
try:
    DATA_PATH = sys._MEIPASS
except:pass

CONF_PATH = os.path.join(DATA_PATH,"config.yaml")

def write_def_conf():
    global conf
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
TTS Voice: en_US-amy-medium""")
    conf = {}

if not os.path.exists(CONF_PATH):
    write_def_conf()
else:
    with open(CONF_PATH, "r") as f:
        conf = yaml.safe_load(f)

if conf is None:
    write_def_conf()

PROMPT_HOTKEY = conf.get("Prompt Hotkey") or "<ctrl>+<alt>+h"
QUIT_HOTKEY = conf.get("Quit Hotkey") or "<ctrl>+<alt>+x"
VOICE_HOTKEY = conf.get("Change Voice Hotkey") or "<ctrl>+<alt>+v"
SOUNDBOARD_HOTKEY = conf.get("Soundboard Hotkey").copy() or [
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
    dl = Signal()
    switch = Signal()

class ComboInputDialog(QDialog):
    def __init__(self, items:list[str], title:str, label:str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.selected = None
        
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel(label))
        
        self.combo = QComboBox()
        self.combo.addItems(items)
        layout.addWidget(self.combo)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def getSelected(self):
        if self.exec() == QDialog.DialogCode.Accepted:
            return self.combo.currentText(), True
        return None, False

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
bridge = Bridge()
win = QWidget()
win.hide()
tray = QSystemTrayIcon(QIcon("Discord-TTS-tray.png"),parent=app)
menu = QMenu("Discord-TTS")
voice = PiperVoice.load(os.path.join(DATA_PATH,f"{TTS_VOICE}.onnx"))
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
            with wave.open(os.path.join(DATA_PATH,"output.wav"),"wb") as wav_file:
                voice.synthesize_wav(t,wav_file)
            press_hotkey(SOUNDBOARD_HOTKEY)
    except:pass
    threading.Timer(.2,rdb).start()

def upd_voice(t:str):
    global TTS_VOICE, voice
    TTS_VOICE = t
    voice = PiperVoice.load(os.path.join(DATA_PATH,f"{TTS_VOICE}.onnx"))
    conf["TTS Voice"] = t
    with open(CONF_PATH,"w") as f:
        yaml.safe_dump(conf,f)

def get_voice():
    t, r = QInputDialog.getText(win,"Discord-TTS","Enter voice name (<language>-<name>-<low/medium/high>):")
    if not r: return
    exists = os.path.exists(os.path.join(DATA_PATH,f"{t}.onnx"))
    if not exists:
        if not os.path.exists(os.path.join(DATA_PATH,".venv")):
            if not os.path.exists(os.path.join(DATA_PATH,"requirements.txt")):
                with open(os.path.join(DATA_PATH,"requirements.txt"),"w") as f:
                    f.write(
"""piper-tts
pynput
PySide6
PyYAML
desktop""")
        if sys.platform != "win32":
            subprocess.call(f"cd {DATA_PATH} && python3 -m venv .venv && . .venv/bin/activate && pip3 install -r requirements.txt", shell=True)
        else:
            subprocess.call(f"cd {DATA_PATH} && python -m venv .venv && call .venv\\Scripts\\activate.bat && pip3 install -r requirements.txt", shell=True)
    if exists or (subprocess.call(f". .venv/bin/activate && python3 -m piper.download_voices {t}", shell=True) if sys.platform != "win32" else subprocess.call(f"call .venv\\Scripts\\activate.bat && python -m piper.download_voices {t}", shell=True)) == 0:
        upd_voice(t)
        QMessageBox.information(win,"Discord-TTS",f"Successfully installed {t}!")

def sw_voice():
    voices = []
    for f in pathlib.Path(DATA_PATH).iterdir():
        if not f.name.endswith(".onnx"): continue
        voices.append(f.name[:f.name.find(".onnx")])
    t, r = ComboInputDialog(voices,"Discord-TTS","Select a voice:",win).getSelected()
    if not r: return
    upd_voice(t)

bridge.trigger.connect(run)
bridge.dl.connect(get_voice)
bridge.switch.connect(sw_voice)

def prompt():
    global debounce
    if debounce: return
    debounce = True
    bridge.trigger.emit()

def open_conf():
    if sys.platform == "darwin":
        subprocess.run(["open",CONF_PATH])
    elif sys.platform == "win32":
        os.startfile(CONF_PATH)
    else:
        subprocess.run(["xdg-open",CONF_PATH])

def dl_voice():
    bridge.dl.emit()

def switch_voice():
    bridge.switch.emit()

def stop():
    global kb
    if h:
        h.stop()
    if thread.is_alive():
        thread.join(timeout=1)
    del kb
    app.quit()

menu_prompt = QAction("Speak...")
menu_prompt.triggered.connect(prompt)
menu_conf = QAction("Open Config")
menu_conf.triggered.connect(open_conf)
menu_dl = QAction("Download Voice...")
menu_dl.triggered.connect(dl_voice)
menu_vlist = QAction("Open Voice List")
menu_vlist.triggered.connect(lambda: webbrowser.open("https://github.com/rhasspy/piper/blob/master/VOICES.md"))
menu_switch = QAction("Switch Voice...")
menu_switch.triggered.connect(switch_voice)
menu_quit = QAction("Quit")
menu_quit.triggered.connect(stop)
menu.addActions([menu_prompt,menu_switch,menu_dl,menu_vlist,menu_conf,menu_quit])

tray.setContextMenu(menu)
tray.show()

def main():
    global h
    h = keyboard.GlobalHotKeys({
        PROMPT_HOTKEY: prompt,
        QUIT_HOTKEY: stop,
        VOICE_HOTKEY: switch_voice
    })
    h.start()
    h.join()

thread = threading.Thread(target=main, daemon=True)
thread.start()

sys.exit(app.exec())