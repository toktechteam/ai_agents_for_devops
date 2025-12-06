from src.workflow import run_workflow


class DummyAgent:
    def complete(self, msg):
        class R:
            content = "dummy analysis"
        return R()


def test_workflow():
    output = run_workflow("cmd", DummyAgent(), "CPU spike")
    assert "dummy analysis" in output
