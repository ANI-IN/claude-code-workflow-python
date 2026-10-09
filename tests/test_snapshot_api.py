"""Tests for the public snapshot route."""

import pytest

from snapshot_service.api import snapshot


@pytest.mark.parametrize(
    "host",
    ["", "camera.local/../admin", "camera.local:8080", "cam era", "cam;rm -rf"],
)
def test_invalid_host_is_rejected(host: str, monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_if_called(host: str, token: str) -> bytes:
        raise AssertionError("camera must not be contacted for an invalid host")

    monkeypatch.setattr(snapshot, "pull_snapshot", fail_if_called)
    with pytest.raises(ValueError, match="Invalid host"):
        snapshot.handle_snapshot(host, "token")


def test_valid_host_pulls_and_processes_the_frame(
    jpeg_frame: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[str, str]] = []

    def fake_pull(host: str, token: str) -> bytes:
        calls.append((host, token))
        return jpeg_frame

    monkeypatch.setattr(snapshot, "pull_snapshot", fake_pull)
    assert snapshot.handle_snapshot("cam-01.example.com", "secret") == jpeg_frame
    assert calls == [("cam-01.example.com", "secret")]
