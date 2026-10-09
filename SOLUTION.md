# Reference Solution: WebP Conversion

This branch, `solution/webp-conversion`, holds a finished result of the exercise: WebP conversion implemented in the snapshot pipeline, following the Explore, Plan, Code, Commit loop.

Use it only as a reference to compare against your own work. The `main` branch is the starting point, so do the exercises there first and check this branch afterward:

```bash
git diff main origin/solution/webp-conversion
```

## What changed

**`src/snapshot_service/pipeline/image_pipeline.py`**

- `process_frame(raw, output_format="webp")` now returns real WebP bytes instead of raising `NotImplementedError`.
- `encode_webp()` decodes the frame with Pillow and re-encodes it as WebP (quality 80). Frames in other color modes, such as grayscale or CMYK, are converted to RGB first.
- Camera bytes are untrusted, so Pillow is restricted to its JPEG decoder (`formats=["JPEG"]`). Other formats are rejected rather than handed to less-audited decoders.
- Bad input raises a clear `ValueError` instead of leaking Pillow-specific exceptions: `"Frame is not a decodable image"` for non-JPEG or corrupt bytes, and `"Frame is too large to encode as WebP"` for frames wider or taller than 16,383 pixels, the WebP limit.
- `process_frame_keeping_original()` returns a frozen `ProcessedFrame` dataclass holding both the original frame and the processed output. Because Python `bytes` are immutable, the original can never be modified by the pipeline.
- The JPEG passthrough behaves exactly as before.

**`src/snapshot_service/api/snapshot.py`**

- `handle_snapshot()` accepts an optional `output_format`, so the feature can be reached through the public route. The default stays `"jpeg"`, so existing callers are unaffected.

**`pyproject.toml`**

- Pillow moved from the `dev` extra into the runtime `dependencies`, because the pipeline now imports it at runtime. This is the answer to the "do we need a new dependency?" question from the Explore and Plan step.

**`tests/`**

- `test_webp_output_is_a_valid_webp_image_of_the_same_size` decodes the output with Pillow and checks its format and dimensions. This is the stronger test asked for in the plan revision ("add a test that asserts the output is valid WebP").
- New tests cover non-RGB frames, undecodable and non-JPEG input, frames too large for WebP, preserving the original frame, and requesting WebP through the API.

## Success criteria met

- `process_frame()` can return WebP bytes.
- The original frame is still available.
- `pytest` passes: 20 tests, including the WebP test that fails on `main`.
- `ruff check .`, `ruff format --check .`, and `mypy` pass with no issues.

## How to check it

```bash
git checkout solution/webp-conversion
pip install -e ".[dev]"
pytest
ruff check .
ruff format --check .
mypy
```

## Notes

- **Why Pillow?** It is the standard Python imaging library, ships prebuilt wheels with WebP support on all major platforms, and is already familiar to anyone who has loaded images for a computer-vision model. A native-free alternative would mean hand-building a WebP container around data that is not really WebP-encoded, which would pass a magic-byte test but fail a real decoder. The stronger test catches exactly that.
- **Decompression bombs.** Pillow warns about images above its `MAX_IMAGE_PIXELS` safety limit and raises `DecompressionBombError` above twice that limit. The pipeline turns that error into a `ValueError`. Real camera frames are far below either limit.
- **Scope.** The teaching point is the workflow, not the codec. A production service would also tune quality, consider lossless mode, and stream large frames.
