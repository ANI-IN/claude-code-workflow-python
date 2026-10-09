"""Frame processing. Today it only returns the raw JPEG bytes.

FEATURE TASK (for the Explore -> Plan -> Code -> Commit exercise):
Add WebP conversion here. The snapshot pipeline should be able to
return a WebP-encoded frame while preserving the original.

Success criteria:
  - process_frame() can return WebP bytes.
  - The original frame is still available.
  - pytest passes (tests/ is the source of truth).
"""

from typing import Literal, get_args

FrameFormat = Literal["jpeg", "webp"]  # webp not implemented yet

SUPPORTED_FORMATS: tuple[str, ...] = get_args(FrameFormat)


def process_frame(raw: bytes, *, output_format: FrameFormat = "jpeg") -> bytes:
    """Return ``raw`` encoded in ``output_format``."""
    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported output format: {output_format!r}")
    if output_format == "webp":
        raise NotImplementedError("WebP conversion not implemented yet")
    # passthrough for jpeg today
    return raw
