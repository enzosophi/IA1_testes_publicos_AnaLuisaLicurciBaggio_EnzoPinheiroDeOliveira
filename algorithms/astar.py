import heapq


def heuristica(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, goal):
    fila = []

    heapq.heappush(fila, (heuristica(start, goal), 0, start))

    came_from = {start: None}
    m_custo = {start: 0}

    expanded_nodes = 0
    generated_nodes = 1
    max_frontier = 1

    while fila:
        if len(fila) > max_frontier:
            max_frontier = len(fila)

        f, custo_atual, atual = heapq.heappop(fila)

        if m_custo.get(atual, float("inf")) < custo_atual:
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
                novo_custo = custo_atual + custo_passo

                if proxima_pos not in m_custo or novo_custo < m_custo[proxima_pos]:
                    m_custo[proxima_pos] = novo_custo
                    came_from[proxima_pos] = atual
                    h = heuristica(proxima_pos, goal)
                    heapq.heappush(fila, (novo_custo + h, novo_custo, proxima_pos))
                    generated_nodes += 1

    return None, 0, expanded_nodes, generated_nodes, max_frontier


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
