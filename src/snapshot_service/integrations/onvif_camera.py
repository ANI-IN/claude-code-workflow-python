"""Pulls a raw JPEG snapshot from a camera over a TLS ONVIF endpoint."""

from urllib.request import Request, urlopen

REQUEST_TIMEOUT_SECONDS = 10


def pull_snapshot(host: str, token: str) -> bytes:
    """Fetch the current snapshot frame from the camera at ``host``.

    ``token`` comes from configuration; it is never hardcoded.
    """
    url = f"https://{host}/onvif/snapshot"
    request = Request(url)  # noqa: S310
    # Unredirected, so the token is never forwarded if the camera redirects.
    request.add_unredirected_header("Authorization", f"Bearer {token}")
    with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:  # noqa: S310
        body: bytes = response.read()
    return body
