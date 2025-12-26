# tests/test_workflow.py

from workflow import IncidentWorkflow


def test_workflow_execution():
    workflow = IncidentWorkflow()
    result = workflow.run("High memory usage")

    assert "alert" in result
    assert "commander_output" in result
    assert "investigator_output" in result
