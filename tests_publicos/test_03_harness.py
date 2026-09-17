import pytest
from conftest import base_request, run


@pytest.mark.parametrize("algorithm", ["dijkstra_lib", "shell", "unknown", ""])
def test_algorithm_outside_allowlist_is_denied(algorithm):
    result = run(base_request(algorithm=algorithm))
    assert result["status"] == "DENY" and result["found"] is False
    assert result["reason"].strip()


@pytest.mark.parametrize("heuristic", ["euclidean_magic", "llm", "", 42])
def test_invalid_heuristic_is_denied(heuristic):
    result = run(base_request(algorithm="astar", heuristic=heuristic))
    assert result["status"] == "DENY" and result["reason"].strip()


@pytest.mark.parametrize("width", [0, -1, -50, "3"])
def test_invalid_beam_width_is_denied(width):
    result = run(base_request(algorithm="beam", beam_width=width, heuristic="manhattan"))
    assert result["status"] == "DENY" and result["reason"].strip()


@pytest.mark.parametrize("field,value", [
    ("max_expansions", 0), ("max_expansions", -1),
    ("max_frontier_size", 0), ("timeout_ms", 0),
])
def test_nonpositive_budget_is_denied(field, value):
    result = run(base_request(**{field: value}))
    assert result["status"] == "DENY"


@pytest.mark.parametrize("map_name", ["I01_missing_goal.txt", "I02_two_starts.txt", "I03_ragged.txt"])
def test_invalid_map_is_denied(map_name):
    result = run(base_request(map_name))
    assert result["status"] == "DENY" and result["reason"].strip()


def test_expansion_limit_interrupts_search():
    result = run(base_request("P06.txt", "bfs", max_expansions=2))
    assert result["status"] in {"ERROR", "TIMEOUT"}
    assert result["expanded_nodes"] <= 2 and result["reason"].strip()


def test_valid_request_is_allowed():
    result = run(base_request("P02.txt", "astar", heuristic="manhattan"))
    assert result["status"] == "ALLOW" and result["found"] is True
