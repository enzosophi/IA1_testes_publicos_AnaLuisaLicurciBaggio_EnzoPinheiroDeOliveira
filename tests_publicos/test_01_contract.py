import pytest
from conftest import base_request, run


REQUIRED = {
    "status", "found", "path", "path_cost", "expanded_nodes",
    "generated_nodes", "max_frontier_size", "execution_time_ms", "reason",
}


def test_result_has_required_fields():
    assert REQUIRED <= set(run(base_request()))


@pytest.mark.parametrize("field", [
    "expanded_nodes", "generated_nodes", "max_frontier_size",
])
def test_metric_is_nonnegative_integer(field):
    value = run(base_request())[field]
    assert isinstance(value, int) and not isinstance(value, bool) and value >= 0


def test_execution_time_is_nonnegative_number():
    value = run(base_request())["execution_time_ms"]
    assert isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def test_success_reason_is_string():
    assert isinstance(run(base_request())["reason"], str)


def test_status_vocabulary():
    assert run(base_request())["status"] in {"ALLOW", "DENY", "ERROR", "TIMEOUT"}
