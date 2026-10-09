"""The source of truth for "correct". The WebP test is written to fail
until the feature is implemented during the Code step."""

import pytest

from snapshot_service.pipeline.image_pipeline import process_frame

JPEG_MAGIC = b"\xff\xd8\xff"
# WebP files start with "RIFF", a 4-byte size, then "WEBP".
RIFF_MAGIC = b"RIFF"
WEBP_MAGIC = b"WEBP"


def test_jpeg_passthrough_returns_the_frame(jpeg_frame: bytes) -> None:
    output = process_frame(jpeg_frame, output_format="jpeg")
    assert output == jpeg_frame
    assert output.startswith(JPEG_MAGIC)


def test_jpeg_is_the_default_format(jpeg_frame: bytes) -> None:
    assert process_frame(jpeg_frame) == jpeg_frame


def test_unsupported_format_is_rejected(jpeg_frame: bytes) -> None:
    with pytest.raises(ValueError, match="Unsupported output format"):
        process_frame(jpeg_frame, output_format="gif")  # type: ignore[arg-type]


# This should pass once WebP conversion is implemented.
def test_webp_output_has_riff_webp_magic_bytes(jpeg_frame: bytes) -> None:
    output = process_frame(jpeg_frame, output_format="webp")
    assert output[:4] == RIFF_MAGIC
    assert output[8:12] == WEBP_MAGIC
