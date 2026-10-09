"""Shared test fixtures."""

import io

import pytest
from PIL import Image

FRAME_SIZE = (64, 48)


@pytest.fixture
def jpeg_frame() -> bytes:
    """A small, real JPEG frame, like the ones cameras return."""
    buffer = io.BytesIO()
    Image.new("RGB", FRAME_SIZE, color=(200, 30, 30)).save(buffer, format="JPEG")
    return buffer.getvalue()
