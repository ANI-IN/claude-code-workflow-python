"""Frame processing. Returns raw JPEG bytes, and can also emit a frame
encoded as WebP while keeping the original frame available.

This is the completed result of the Explore -> Plan -> Code -> Commit
exercise. The feature added here is WebP conversion.

Success criteria (all met):
  - process_frame() can return WebP bytes.
  - The original frame is still available.
  - pytest passes (tests/ is the source of truth).
"""

import io
from dataclasses import dataclass
from typing import Literal, get_args

from PIL import Image

FrameFormat = Literal["jpeg", "webp"]

SUPPORTED_FORMATS: tuple[str, ...] = get_args(FrameFormat)

WEBP_QUALITY = 80
WEBP_MAX_DIMENSION = 16383  # largest width or height the WebP format allows


@dataclass(frozen=True)
class ProcessedFrame:
    """The original camera frame alongside its processed copy."""

    original: bytes
    output: bytes
    output_format: FrameFormat


def encode_webp(raw: bytes, *, quality: int = WEBP_QUALITY) -> bytes:
    """Decode a raw JPEG camera frame and re-encode it as WebP.

    Camera bytes are untrusted, so only the JPEG decoder is allowed. Raises
    ``ValueError`` for input that is not a decodable JPEG or is too large for
    WebP, so callers get one clear error type for bad camera input.
    """
    try:
        with Image.open(io.BytesIO(raw), formats=["JPEG"]) as image:
            if max(image.size) > WEBP_MAX_DIMENSION:
                raise ValueError("Frame is too large to encode as WebP")
            # WebP stores RGB(A); convert modes such as CMYK or grayscale.
            rgb = image if image.mode in ("RGB", "RGBA") else image.convert("RGB")
            buffer = io.BytesIO()
            rgb.save(buffer, format="WEBP", quality=quality)
    # OSError covers unidentified and truncated images.
    except (OSError, Image.DecompressionBombError) as exc:
        raise ValueError("Frame is not a decodable image") from exc
    return buffer.getvalue()


def process_frame(raw: bytes, *, output_format: FrameFormat = "jpeg") -> bytes:
    """Return ``raw`` encoded in ``output_format``. ``raw`` is never modified."""
    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported output format: {output_format!r}")
    if output_format == "webp":
        return encode_webp(raw)
    # passthrough for jpeg
    return raw


def process_frame_keeping_original(
    raw: bytes, *, output_format: FrameFormat = "jpeg"
) -> ProcessedFrame:
    """Process ``raw`` and return it together with the untouched original."""
    output = process_frame(raw, output_format=output_format)
    return ProcessedFrame(original=raw, output=output, output_format=output_format)
