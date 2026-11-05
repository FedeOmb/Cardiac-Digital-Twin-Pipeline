import paraview.web.venv

import logging
import os
from pathlib import Path

from paraview import simple
from ptc.apps.lite import Lite
from trame.widgets import client


# CONFIG
import sys

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True
)
LOG = logging.getLogger("trame-docker")

DEFAULT_ALLOWED_ROOTS = "/data:/mnt"

ALLOWED_ROOTS = [
    Path(p).resolve()
    for p in os.environ.get(
        "MESH_ALLOWED_ROOTS",
        DEFAULT_ALLOWED_ROOTS
    ).split(os.pathsep)
    if p.strip()
]

ALLOWED_EXTENSIONS = {
    ".vtk",
    ".vtp",
    ".vtu",
    ".vtm",
    ".pvtu",
    ".pvtp",
}

def validate_mesh_path(raw_path):

    if not raw_path:
        raise ValueError("No mesh path specified")

    candidate = Path(str(raw_path)).expanduser()
    path = candidate.resolve(strict=True)

    if not any(path.is_relative_to(root) for root in ALLOWED_ROOTS):
        raise ValueError(
            f"Path not allowed: {path}"
        )

    if not path.is_file():
        raise ValueError("Path is not a file")

    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported format: {path.suffix}"
        )

    return path


# PARAVIEW initialization
view = simple.GetActiveViewOrCreate("RenderView")

simple.SetActiveView(view)
simple.Render(view)

# Template Paraview Lite from PTC
web_app = Lite()

server = web_app.server
controller = server.controller

current_reader = None


# update PTC components
def notify_ptc():

    events = [
        "on_data_loaded",
        "on_active_proxy_change",
        "on_data_change",
    ]

    for event_name in events:
        event = getattr(controller, event_name, None)
        
        if event is None:
            continue
        try:
            exists = getattr(event, "exists", None)
            if callable(exists) and not exists():
                continue
            event()

        except Exception:
            LOG.exception(
                "Error updating PTC event: %s",
                event_name
            )

    # application update
    if hasattr(web_app, "update"):
        web_app.update()


def load_mesh_from_url(mesh_path=None):

    global current_reader

    if not mesh_path:
        LOG.info("No mesh parameter in URL.")
        return

    new_reader = None

    try:
        path = validate_mesh_path(mesh_path)

        LOG.info("loading mesh: %s", path)
        new_reader = simple.OpenDataFile(str(path))
        new_reader.UpdatePipeline()

        new_display = simple.Show(new_reader, view)
        new_display.Representation = "Surface"

        simple.SetActiveView(view)
        simple.SetActiveSource(new_reader)

        if current_reader is not None:
            simple.Hide(current_reader, view)
            simple.Delete(current_reader)

        current_reader = new_reader
        view.ResetCamera()
        simple.Render(view)

        notify_ptc()

    except Exception:
        LOG.exception(
            "Error loading mesh: %s",
            mesh_path
        )
        if new_reader is not None and new_reader is not current_reader:
            try:
                simple.Delete(new_reader)
            except Exception:
                pass


with web_app.side_left:
    client.ClientTriggers(
        mounted=(
            load_mesh_from_url,
            "[new window.URLSearchParams(window.location.search).get('mesh')]"
        )
    )

# Server startup
if __name__ == "__main__":

    LOG.info("Avvio ParaView Lite - Cardiac Mesh Viewer")

    web_app.start()
