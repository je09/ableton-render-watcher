# RenderWatcher

A remote script for Ableton Live that copies your latest render into your project folder the moment the export finishes — named after the project, no extra steps.

No more digging through a Renders folder trying to remember which file is which.

---

## What it does

Every time you export audio in Ableton, RenderWatcher notices when the export is done, finds the new file in your Renders folder, and drops a copy right next to your `.als` file — named after the project.

**Example:** Your project is called `My Song`. Ableton exports it as `My Song 2024-05-12 123456.wav` into your Renders folder. RenderWatcher copies it to your project folder as `My Song.wav` — automatically, the moment the export finishes.

If you export stems (multiple tracks at once), RenderWatcher stays out of the way and skips the copy entirely.

---

## Requirements

- Ableton Live 11 or 12 (Standard or Suite) — Live 10 won't work
- macOS or Windows

---

## Installation

### Step 1 — Download RenderWatcher

Click the green **Code** button near the top of this page and choose **Download ZIP**.

Once downloaded, unzip the file. You'll get a folder called `RenderWatcher` — keep all the files inside it together.

---

### Step 2 — Find Ableton's Remote Scripts folder

Ableton has a special folder where it looks for remote scripts. You need to put `RenderWatcher` there.

**On Mac:**

1. Open **Finder**
2. In the menu bar at the top of your screen, click **Go → Home**
3. Open the `Music` folder, then `Ableton`, then `User Library`
4. Look for a folder called `Remote Scripts` — if it's not there, create it (right-click → New Folder)

The full path is: `~/Music/Ableton/User Library/Remote Scripts/`

**On Windows:**

1. Open **File Explorer**
2. Click the address bar at the top, paste this path, and press Enter — replace `YourName` with your actual Windows username:
   ```
   C:\Users\YourName\Documents\Ableton\User Library\Remote Scripts\
   ```
3. If the `Remote Scripts` folder doesn't exist, create it (right-click → New → Folder)

> Not sure where your User Library is? [Ableton explains how to find it here.](https://help.ableton.com/hc/en-us/articles/209072009-Installing-third-party-remote-scripts)

---

### Step 3 — Place the RenderWatcher folder

Move (or copy) the entire `RenderWatcher` folder into the `Remote Scripts` folder from Step 2.

The result should look like this:

```
Remote Scripts/
└── RenderWatcher/
    ├── RenderWatcher.py
    ├── config.py
    └── __init__.py
```

---

### Step 4 — Set your Renders folder path

RenderWatcher needs to know where Ableton saves your exports. You tell it by editing one line in a text file.

1. Open the `RenderWatcher` folder you just placed
2. Find the file called `config.py` and open it with a text editor:
   - **Mac:** right-click → Open With → **TextEdit**
   - **Windows:** right-click → Open With → **Notepad**
3. Find this line:
   ```
   RENDERS_FOLDER = os.path.expanduser("~/Music/Renders")
   ```
4. Replace `~/Music/Renders` with the actual path to the folder where Ableton saves your exports — this is the same folder you pick when Ableton asks where to save during export

   **Mac example:**
   ```
   RENDERS_FOLDER = "/Users/YourName/Music/Renders"
   ```
   **Windows example:**
   ```
   RENDERS_FOLDER = "C:/Users/YourName/Music/Renders"
   ```
   Keep the quotes. Use forward slashes `/` even on Windows.

5. Save the file (`Cmd + S` on Mac, `Ctrl + S` on Windows) and close the text editor

> **Tip — how to find the exact path:** On Mac, open Finder, navigate to your Renders folder, right-click it, hold `Option`, and choose **Copy "Renders" as Pathname**. On Windows, open the folder in File Explorer and click the address bar — the full path will appear, ready to copy.

---

### Step 5 — Activate RenderWatcher in Ableton

1. Open (or restart) **Ableton Live**
2. Open **Preferences:**
   - Mac: `Cmd + ,`
   - Windows: `Ctrl + ,`
3. Go to the **Link, Tempo & MIDI** tab (Live 12) or **MIDI Sync** tab (Live 11)
4. In the **Control Surface** section, click any empty dropdown and select **RenderWatcher**
5. Leave **Input** and **Output** set to **None** — RenderWatcher doesn't need a MIDI device
6. Close Preferences

If everything worked, you'll briefly see **"RenderWatcher: active"** in the thin status bar at the very bottom of the Ableton window.

---

## Using it

Nothing changes in how you work. Export as you normally would:

- `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows)
- or **File → Export Audio/Video…**

When the export finishes and the dialog closes, RenderWatcher copies the render to your project folder automatically.

> [Ableton docs: Exporting audio and video](https://www.ableton.com/en/manual/exporting-audio-and-video/)

---

## Troubleshooting

**Nothing shows up in my project folder**

- Check that the path in `config.py` exactly matches where Ableton is saving exports — open the export dialog and look at the save location, it needs to be character-for-character identical to what's in the config file.
- Make sure the project has been saved at least once. If the `.als` file hasn't been saved yet, there's no project folder to copy into.
- For more detail, check Ableton's log. On Mac it's at `~/Library/Preferences/Ableton/Live x.x.x/Log.txt` — open it in TextEdit and search for `RenderWatcher`.

**"RenderWatcher: active" never appeared**

- Double-check that the `RenderWatcher` folder is *inside* `Remote Scripts`, not just next to it (re-read Step 3).
- Restart Ableton after placing the folder — remote scripts only load at startup.
- Make sure you're on Live 11 or 12. Live 10 is not supported.

**It copied files during a stems export**

This shouldn't happen — RenderWatcher skips any export that produces multiple differently-named files at once. If it does, please [open an issue](https://github.com/je09/ableton-render-watcher/issues) and describe what happened.
