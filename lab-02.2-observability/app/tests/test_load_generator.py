import types
import load_generator


class DummyResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code


def dummy_post(url, json=None, timeout=None):
    """
    A dummy replacement for requests.post.
    Always returns HTTP 200 so load generator logic can run without external calls.
    """
    return DummyResponse(200)


def test_load_generator_runs_without_errors(monkeypatch):
    """
    Ensures that the load() / run_load() function executes end-to-end
    without performing real HTTP requests.
    """

    # Patch the requests.post inside load_generator module
    monkeypatch.setattr(
        load_generator,
        "requests",
        types.SimpleNamespace(post=dummy_post)
    )

    # Determine correct function based on module
    if hasattr(load_generator, "load"):          # FREE version
        load_generator.load("http://fake-url/predict", 5)

    elif hasattr(load_generator, "run_load"):    # PAID version
        load_generator.run_load("http://fake-url/predict", 5)

    else:
        raise AssertionError("No valid load function found in load_generator")

    # If no exception, the test passes.
    assert True
