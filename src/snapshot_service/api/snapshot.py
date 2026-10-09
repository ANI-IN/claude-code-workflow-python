"""Public route: validates the host, pulls a frame, runs it through the pipeline."""

import re

from snapshot_service.integrations.onvif_camera import pull_snapshot
from snapshot_service.pipeline.image_pipeline import FrameFormat, process_frame

HOST_PATTERN = re.compile(r"[a-zA-Z0-9.-]+")


def handle_snapshot(
    host: str, token: str, *, output_format: FrameFormat = "jpeg"
) -> bytes:
    """Return a snapshot frame from the camera at ``host`` in ``output_format``."""
    if not HOST_PATTERN.fullmatch(host):
        raise ValueError("Invalid host")
    raw = pull_snapshot(host, token)
    return process_frame(raw, output_format=output_format)
