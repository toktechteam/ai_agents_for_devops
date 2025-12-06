from types import SimpleNamespace

import load_generator


class DummyResponse:
    def __init__(self, status_code: int = 200) -> None:
        self.status_code = status_code


def dummy_post(url, json, timeout=5):  # noqa: D401
    """Always returns a 200 OK dummy response."""
    return DummyResponse(200)


def test_send_requests_monkeypatch(monkeypatch):
    # Patch requests.post with our dummy_post
    monkeypatch.setattr(load_generator, "requests", SimpleNamespace(post=dummy_post))
    load_generator.send_requests("http://test/predict", 5)
    # No assertion needed; the function should run without raising exceptions.
