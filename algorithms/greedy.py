import heapq


def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def greedy_search(
    grid, start, goal, max_expansions=10000, max_frontier_size=20000, **kwargs
):
    pq = []
    h_inicial = heuristica(start, goal)
    heapq.heappush(pq, (h_inicial, start))

    came_from = {start: None}
    visited = set([start])

    expanded_nodes = 0
    generated_nodes = 1
    max_frontier = 1

    while pq:
        if len(pq) > max_frontier:
            max_frontier = len(pq)

        # Verifica o limite antes de expandir
        if expanded_nodes >= max_expansions:
            return [], float("inf"), expanded_nodes, generated_nodes, max_frontier

        h, atual = heapq.heappop(pq)

        if not isinstance(atual, (list, tuple)) or len(atual) != 2:
            continue

        expanded_nodes += 1

        if atual == goal:
            caminho, custo = reconstruir_caminho_e_custo(grid, came_from, atual)
            return caminho, custo, expanded_nodes, generated_nodes, max_frontier

        r, c = atual
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            proxima_pos = (nr, nc)

            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                celula = grid[nr][nc]
                if celula != "#" and proxima_pos not in visited:
                    visited.add(proxima_pos)
                    came_from[proxima_pos] = atual
                    h_novo = heuristica(proxima_pos, goal)
                    heapq.heappush(pq, (h_novo, proxima_pos))
                    generated_nodes += 1

    return [], 0.0, expanded_nodes, generated_nodes, max_frontier


def reconstruir_caminho_e_custo(grid, came_from, atual):
    caminho = []
    custo = 0.0
    while atual is not None:
        caminho.append(atual)
        if came_from.get(atual) is not None:
            r, c = atual
            celula = grid[r][c]
            custo += int(celula) if str(celula).isdigit() else 1.0
        atual = came_from.get(atual)
    caminho.reverse()
    return caminho, custo
