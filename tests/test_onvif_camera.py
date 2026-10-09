"""Tests for the ONVIF camera integration. No real network calls are made."""

import io
from typing import Any
from urllib.request import Request

import pytest

from snapshot_service.integrations import onvif_camera


def test_pull_snapshot_uses_tls_and_bearer_token(
    jpeg_frame: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, Any] = {}

    def fake_urlopen(request: Request, timeout: float) -> io.BytesIO:
        captured["request"] = request
        captured["timeout"] = timeout
        return io.BytesIO(jpeg_frame)

    monkeypatch.setattr(onvif_camera, "urlopen", fake_urlopen)
    frame = onvif_camera.pull_snapshot("cam-01.example.com", "secret")

    request: Request = captured["request"]
    assert frame == jpeg_frame
    assert request.full_url == "https://cam-01.example.com/onvif/snapshot"
    assert request.unredirected_hdrs["Authorization"] == "Bearer secret"
    # Redirected requests copy only request.headers, so the token must not be there.
    assert "Authorization" not in request.headers
    assert captured["timeout"] == onvif_camera.REQUEST_TIMEOUT_SECONDS
