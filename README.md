# Discord-TTS

A simple python script that allows you to use TTS in a Discord (or other app's) VC via Soundux (or any other soundboard program that allows setting custom shortcuts).

## Requirements

1. Python 3 (see below for Linux:)  
    Just search "tkinter" in your software app/GUI package manager. Or, from the terminal:
    - On Arch:

    ```sh
    sudo pacman -S --needed tk
    ```

    - On Ubuntu/Mint/other derivatives:

    ```sh
    sudo apt install --needed python3-tk
    ```

    - On Fedora:

    ```sh
    sudo dnf install python3-tkinter
    ```

2. Any soundboard program that allows setting custom shortcuts.

## Installation

> [!Important]
> Ensure you have all of the necessary dependancies before following this guide!

1. Clone this repository.  
   If you have [`git`](https://git-scm.com/install/) installed:

   ```sh
   git clone https://github.com/DatBogie/Discord-TTS.git
   ```

   Otherwise:
   - On [the repository page](https://github.com/DatBogie/Discord-TTS) (likely the page you're on right now), click the green "<> Code" button, then the "Download ZIP" button.
   - Extract the `Discord-TTS-main.zip` file to somewhere permanent (like your Documents folder).

2. Run either `setup.sh` or `setup.bat` (only run `setup.bat` if you're on Windows).  
   **If you'd like to change the TTS voice**:
   - Open [the list of Piper-TTS voices](https://github.com/rhasspy/piper/blob/master/VOICES.md).
   - On line 5 of whichever setup script (either `setup.sh` or `setup.bat`), replace `en_US-amy-medium` with your desired voice, following the format `<language>-<name>-<low/medium/high>`, where language is the text in parenthesis (eg. `en_US`) in the list.
   - Make sure to follow step 2 in the Usage section, and change the value of `TTS_VOICE` on line 25 in `main.py`!

## Usage

Simply run either `run.sh` or `run.bat` (only run `run.bat` on Windows). You will have to re-run the app upon closing it or upon restarting your computer for it to work.  

To configure this program:

1. Open `main.py` in a text editor. VSCode is recommended. (If it asks you to use a virtual environment/venv it found, click "Yes.")

2. Follow the instructions provided by the text on lines starting with a `#`; only change the values of variables in all caps.
