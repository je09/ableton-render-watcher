# ─────────────────────────────────────────────
#  RenderWatcher — config
#  Set this to the folder where Ableton saves your exports.
# ─────────────────────────────────────────────

import os

# Change this path to wherever you tell Ableton to save your exports.
# Mac example:     "/Users/YourName/Music/Renders"
# Windows example: "C:/Users/YourName/Music/Renders"
RENDERS_FOLDER = os.path.expanduser("~/Music/Renders")
