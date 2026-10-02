from collections import deque


def bfs(
    grid, inicio, objetivo, max_expansions=10000, max_frontier_size=20000, **kwargs
):
    fila = deque([inicio])
    came_from = {inicio: None}

    expanded_nodes = 0
    generated_nodes = 1
    max_frontier = 1

    num_linhas = len(grid)
    num_colunas = len(grid[0])

    while fila:
        if len(fila) > max_frontier:
            max_frontier = len(fila)

        # Verifica o limite antes de expandir mais um nó
        if expanded_nodes >= max_expansions:
            return [], float("inf"), expanded_nodes, generated_nodes, max_frontier

        atual = fila.popleft()

        if not isinstance(atual, (list, tuple)) or len(atual) != 2:
            continue

        expanded_nodes += 1

        if atual == objetivo:
            caminho, custo = reconstruir_caminho_e_custo(grid, came_from, atual)
            return caminho, custo, expanded_nodes, generated_nodes, max_frontier

        r, c = atual
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in movimentos:
            novo_r, novo_c = r + dr, c + dc
            proxima_pos = (novo_r, novo_c)

            if 0 <= novo_r < num_linhas and 0 <= novo_c < num_colunas:
                celula = grid[novo_r][novo_c]
                if celula != "#" and proxima_pos not in came_from:
                    came_from[proxima_pos] = atual
                    fila.append(proxima_pos)
                    generated_nodes += 1

    return [], float("inf"), expanded_nodes, generated_nodes, max_frontier


def reconstruir_caminho_e_custo(grid, came_from, objetivo):
    caminho = []
    custo = 0.0
    atual = objetivo
    while atual is not None:
        caminho.append(atual)
        if came_from.get(atual) is not None:
            if isinstance(atual, (list, tuple)) and len(atual) == 2:
                r, c = atual
                celula = grid[r][c]
                custo += int(celula) if str(celula).isdigit() else 1
        atual = came_from.get(atual)
    caminho.reverse()
    return caminho, custo
