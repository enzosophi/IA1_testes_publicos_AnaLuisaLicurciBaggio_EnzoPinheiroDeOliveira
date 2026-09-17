from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from student_api import execute_search
except ImportError as exc:
    raise RuntimeError(
        "Renomeie student_api_template.py para student_api.py e adapte-o ao projeto."
    ) from exc


def run(request: dict) -> dict:
    result = execute_search(request)
    assert isinstance(result, dict), "O adaptador deve retornar dict."
    return result


def valid_path(grid: list[str], path) -> bool:
    if not path:
        return False
    blocked = "#"
    for row, col in path:
        if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[row]):
            return False
        if grid[row][col] == blocked:
            return False
    return all(
        abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
        for a, b in zip(path, path[1:])
    )


def base_request(map_name="P01.txt", algorithm="bfs", **updates):
    request = {
        "algorithm": algorithm,
        "map_id": str(Path(__file__).parent / "maps" / map_name),
        "heuristic": None,
        "beam_width": None,
        "max_expansions": 10_000,
        "max_frontier_size": 20_000,
        "timeout_ms": 2_000,
    }
    request.update(updates)
    return request
