import os
import shutil

import Live
from _Framework.ControlSurface import ControlSurface
from .config import RENDERS_FOLDER

AUDIO_EXTENSIONS = (".wav", ".aiff", ".flac")


class RenderWatcher(ControlSurface):

    def __init__(self, c_instance):
        super().__init__(c_instance)

        self._app = Live.Application.get_application()
        self._prev_dialog_count = 0
        # Snapshot: {full_path: mtime} — tracks both new files and overwrites
        self._renders_snapshot = {}

        self._app.add_open_dialog_count_listener(self._on_dialog_count_changed)

        self.log_message("RenderWatcher: loaded ✓")
        self.show_message("RenderWatcher: active")

    # ── Main hook ──────────────────────────────────────────────────────────

    def _on_dialog_count_changed(self):
        current = self._app.open_dialog_count

        if current > 0 and self._prev_dialog_count == 0:
            self._renders_snapshot = self._audio_files_snapshot()
            self.log_message(f"RenderWatcher: snapshot taken ({len(self._renders_snapshot)} files)")

        elif current == 0 and self._prev_dialog_count > 0:
            self._try_copy_new_render()

        self._prev_dialog_count = current

    # ── Copying ────────────────────────────────────────────────────────────

    def _try_copy_new_render(self):
        file_path = self.song().file_path
        if not file_path:
            return

        current = self._audio_files_snapshot()

        # Find files that appeared OR were overwritten (mtime changed)
        changed = {
            path for path, mtime in current.items()
            if path not in self._renders_snapshot
            or self._renders_snapshot[path] != mtime
        }

        if not changed:
            self.log_message("RenderWatcher: no changed files, skipping")
            return

        if len(changed) > 1:
            # If all files share the same base name — it's wav+mp3 from one render, not stems
            basenames = {os.path.splitext(os.path.basename(p))[0] for p in changed}
            if len(basenames) > 1:
                self.log_message(f"RenderWatcher: {len(changed)} changed files, {len(basenames)} names — stems render, skipping")
                self.show_message("RenderWatcher: stems render detected, skipping")
                return
            # Same name, multiple formats (wav + mp3) — prefer WAV
            wav_files = [p for p in changed if p.lower().endswith(".wav")]
            src = wav_files[0] if wav_files else next(iter(changed))
        else:
            src = next(iter(changed))

        src_ext = os.path.splitext(src)[1].lower()
        project_folder = os.path.dirname(file_path)
        # Derive name from the project folder, stripping the " Project" suffix
        folder_name = os.path.basename(project_folder)
        project_name = folder_name.removesuffix(" Project")
        dest = os.path.join(project_folder, f"{project_name}{src_ext}")

        try:
            shutil.copy2(src, dest)
            self.log_message(f"RenderWatcher: copied '{os.path.basename(src)}' → '{dest}'")
            self.show_message(f"✓ Render saved: {project_name}{src_ext}")
        except Exception as e:
            self.log_message(f"RenderWatcher ERROR: {e}")
            self.show_message(f"RenderWatcher: copy failed — {e}")

    # ── Helpers ────────────────────────────────────────────────────────────

    def _audio_files_snapshot(self):
        """Returns {full_path: mtime} for all audio files in RENDERS_FOLDER."""
        if not os.path.isdir(RENDERS_FOLDER):
            self.log_message(f"RenderWatcher: renders folder not found: {RENDERS_FOLDER}")
            return {}

        result = {}
        for f in os.listdir(RENDERS_FOLDER):
            if f.lower().endswith(AUDIO_EXTENSIONS):
                fpath = os.path.join(RENDERS_FOLDER, f)
                try:
                    result[fpath] = os.path.getmtime(fpath)
                except OSError:
                    pass
        return result

    # ── Cleanup ────────────────────────────────────────────────────────────

    def disconnect(self):
        try:
            self._app.remove_open_dialog_count_listener(self._on_dialog_count_changed)
        except Exception:
            pass
        super().disconnect()
