import heapq


def uniform_cost_search(grid, start, goal):
    pq = []
    heapq.heappush(pq, (0, start))

    came_from = {start: None}
    g_costs = {start: 0}

    expanded_nodes = 0
    generated_nodes = 1
    max_frontier = 1

    while pq:
        if len(pq) > max_frontier:
            max_frontier = len(pq)

        current_g, atual = heapq.heappop(pq)
        if current_g > g_costs.get(atual, float("inf")):
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
                if celula == "#":
                    continue

                custo_passo = int(celula) if str(celula).isdigit() else 1
                novo_g = current_g + custo_passo

                if proxima_pos not in g_costs or novo_g < g_costs[proxima_pos]:
                    g_costs[proxima_pos] = novo_g
                    came_from[proxima_pos] = atual
                    heapq.heappush(pq, (novo_g, proxima_pos))
                    generated_nodes += 1

    return None, 0.0, expanded_nodes, generated_nodes, max_frontier


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
