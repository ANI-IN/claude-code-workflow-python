"""Public route: validates the host, pulls a frame, runs it through the pipeline."""

import re

from snapshot_service.integrations.onvif_camera import pull_snapshot
from snapshot_service.pipeline.image_pipeline import process_frame

HOST_PATTERN = re.compile(r"[a-zA-Z0-9.-]+")


def handle_snapshot(host: str, token: str) -> bytes:
    """Return a processed snapshot frame from the camera at ``host``."""
    if not HOST_PATTERN.fullmatch(host):
        raise ValueError("Invalid host")
    raw = pull_snapshot(host, token)
    return process_frame(raw)
