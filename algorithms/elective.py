def dfs(grid, start, goal):
    stack = [start]
    visited = set([start])
    came_from = {start: None}

    expanded = 0
    generated = 1
    max_frontier = 1

    while stack:
        if len(stack) > max_frontier:
            max_frontier = len(stack)

        atual = stack.pop()
        expanded += 1

        if atual == goal:
            caminho, custo = reconstruir_caminho_e_custo(grid, came_from, atual)
            return caminho, custo, expanded, generated, max_frontier

        row, col = atual
        for d_linha, d_coluna in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nova_linha, nova_coluna = row + d_linha, col + d_coluna
            proxima_pos = (nova_linha, nova_coluna)

            if 0 <= nova_linha < len(grid) and 0 <= nova_coluna < len(grid[0]):
                cell = grid[nova_linha][nova_coluna]

                if cell != "#" and proxima_pos not in visited:
                    visited.add(proxima_pos)
                    came_from[proxima_pos] = atual
                    stack.append(proxima_pos)
                    generated += 1

    return None, 0, expanded, generated, max_frontier


def reconstruir_caminho_e_custo(grid, came_from, atual):
    caminho = []
    custo = 0
    while atual is not None:
        caminho.append(atual)
        if came_from[atual] is not None:
            r, c = atual
            celula = grid[r][c]
            custo += int(celula) if str(celula).isdigit() else 1
        atual = came_from[atual]
    caminho.reverse()
    return caminho, custo
