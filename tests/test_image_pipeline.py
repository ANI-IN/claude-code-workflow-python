"""The source of truth for "correct" in the image pipeline."""

import io

import pytest
from PIL import Image

from snapshot_service.pipeline.image_pipeline import (
    WEBP_MAX_DIMENSION,
    process_frame,
    process_frame_keeping_original,
)

JPEG_MAGIC = b"\xff\xd8\xff"
# WebP files start with "RIFF", a 4-byte size, then "WEBP".
RIFF_MAGIC = b"RIFF"
WEBP_MAGIC = b"WEBP"


def _jpeg_in_mode(mode: str) -> bytes:
    buffer = io.BytesIO()
    Image.new(mode, (32, 24)).save(buffer, format="JPEG")
    return buffer.getvalue()


def test_jpeg_passthrough_returns_the_frame(jpeg_frame: bytes) -> None:
    output = process_frame(jpeg_frame, output_format="jpeg")
    assert output == jpeg_frame
    assert output.startswith(JPEG_MAGIC)


def test_jpeg_is_the_default_format(jpeg_frame: bytes) -> None:
    assert process_frame(jpeg_frame) == jpeg_frame


def test_unsupported_format_is_rejected(jpeg_frame: bytes) -> None:
    with pytest.raises(ValueError, match="Unsupported output format"):
        process_frame(jpeg_frame, output_format="gif")  # type: ignore[arg-type]


def test_webp_output_has_riff_webp_magic_bytes(jpeg_frame: bytes) -> None:
    output = process_frame(jpeg_frame, output_format="webp")
    assert output[:4] == RIFF_MAGIC
    assert output[8:12] == WEBP_MAGIC


def test_webp_output_is_a_valid_webp_image_of_the_same_size(jpeg_frame: bytes) -> None:
    output = process_frame(jpeg_frame, output_format="webp")
    with Image.open(io.BytesIO(jpeg_frame)) as original:
        expected_size = original.size
    with Image.open(io.BytesIO(output)) as converted:
        converted.load()
        assert converted.format == "WEBP"
        assert converted.size == expected_size


@pytest.mark.parametrize("mode", ["L", "CMYK"])
def test_non_rgb_frames_convert_to_webp(mode: str) -> None:
    output = process_frame(_jpeg_in_mode(mode), output_format="webp")
    assert output[8:12] == WEBP_MAGIC


def test_undecodable_frame_raises_value_error() -> None:
    with pytest.raises(ValueError, match="not a decodable image"):
        process_frame(b"not an image", output_format="webp")


def test_non_jpeg_input_is_rejected() -> None:
    buffer = io.BytesIO()
    Image.new("RGB", (8, 8)).save(buffer, format="PNG")
    with pytest.raises(ValueError, match="not a decodable image"):
        process_frame(buffer.getvalue(), output_format="webp")


def test_frame_too_large_for_webp_is_rejected() -> None:
    buffer = io.BytesIO()
    Image.new("L", (WEBP_MAX_DIMENSION + 1, 1)).save(buffer, format="JPEG")
    with pytest.raises(ValueError, match="too large"):
        process_frame(buffer.getvalue(), output_format="webp")


def test_webp_conversion_keeps_the_original_frame(jpeg_frame: bytes) -> None:
    result = process_frame_keeping_original(jpeg_frame, output_format="webp")
    assert result.original == jpeg_frame
    assert result.output[:4] == RIFF_MAGIC
    assert result.output_format == "webp"


def test_keeping_original_for_jpeg_returns_the_same_bytes(jpeg_frame: bytes) -> None:
    result = process_frame_keeping_original(jpeg_frame)
    assert result.original == result.output == jpeg_frame
