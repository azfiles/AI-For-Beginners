"""Initialize an editable course volume once, then start the persistent kernel server."""
from pathlib import Path
import os
import shutil

root = Path("/course")
marker = root / ".initialized"
if not marker.exists():
    # Fail on a partially initialized directory rather than overwrite learner files.
    existing = list(root.iterdir())
    if existing:
        raise RuntimeError("Course volume is not empty and has no initialization marker; inspect it before retrying.")
    shutil.copytree("/opt/course", root, dirs_exist_ok=True)
    marker.write_text("Initialized from the container image. Learner edits are persistent.\n")
if not os.environ.get("JUPYTER_TOKEN"):
    raise RuntimeError("JUPYTER_TOKEN must be set.")
os.execvp("jupyter", ["jupyter", "lab", "--config=/opt/runtime/jupyter_server_config.py"])
