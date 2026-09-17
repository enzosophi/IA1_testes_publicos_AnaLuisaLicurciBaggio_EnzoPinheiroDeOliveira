def dfs(grid, start, goal):
    stack = [(start, [start])]
    visited = set()

    expanded_nodes = 0
    generated_nodes = 0

    while stack:
        atual, caminho = stack.pop()

        if atual == goal:
            return caminho, expanded_nodes, generated_nodes

        if atual in visited:
            continue

        visited.add(atual)
        expanded_nodes += 1

        row, col = atual

        movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for d_linha, d_coluna in movements:
            nova_linha, nova_coluna = row + d_linha, col + d_coluna

            if 0 <= nova_linha < len(grid) and 0 <= nova_coluna < len(grid[0]):
                cell = grid[nova_linha][nova_coluna]

                if cell == "#":
                    continue

                next_pos = (nova_linha, nova_coluna)
                stack.append((next_pos, caminho + [next_pos]))

    return None, expanded_nodes, generated_nodes
