import pytest
from conftest import base_request, run, valid_path


@pytest.mark.parametrize("algorithm", ["bfs", "ucs", "greedy", "astar"])
def test_adjacent_goal(algorithm):
    result = run(base_request("P01.txt", algorithm, heuristic="manhattan"))
    assert result["status"] == "ALLOW" and result["found"] is True
    assert result["path"] == [[0, 0], [0, 1]] or result["path"] == [(0, 0), (0, 1)]
    assert result["path_cost"] == pytest.approx(1)


@pytest.mark.parametrize("algorithm", ["bfs", "ucs", "greedy", "astar"])
def test_no_solution_terminates(algorithm):
    result = run(base_request("P03.txt", algorithm, heuristic="manhattan"))
    assert result["status"] == "ALLOW" and result["found"] is False
    assert result["path"] == []


@pytest.mark.parametrize("algorithm", ["bfs", "ucs", "astar"])
def test_cycle_map_returns_valid_path(algorithm):
    grid = ["S..", ".#.", "..G"]
    result = run(base_request("P05.txt", algorithm, heuristic="manhattan"))
    assert result["found"] is True and valid_path(grid, result["path"])
    assert len(result["path"]) - 1 == 4


def test_bfs_minimizes_steps_not_weight():
    result = run(base_request("P04.txt", "bfs"))
    assert len(result["path"]) - 1 == 2 and result["path_cost"] == pytest.approx(10)


@pytest.mark.parametrize("algorithm", ["ucs", "astar"])
def test_cost_search_avoids_expensive_cell(algorithm):
    result = run(base_request("P04.txt", algorithm, heuristic="manhattan"))
    assert result["found"] is True and result["path_cost"] == pytest.approx(4)


def test_astar_zero_heuristic_matches_ucs_cost():
    ucs = run(base_request("P04.txt", "ucs"))
    astar = run(base_request("P04.txt", "astar", heuristic="zero"))
    assert astar["path_cost"] == pytest.approx(ucs["path_cost"])
