def heuristica(a, b):
    """Calcula a distancia Manhattan entre dois pontos a e b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def beam_search(grid, start, goal, beam_width=5):
    fronteira = [start]
    came_from = {start: None}

    expanded_nodes = 0
    generated_nodes = 1
    max_frontier_size = 1

    while fronteira:
        if len(fronteira) > max_frontier_size:
            max_frontier_size = len(fronteira)

        proxima_fronteira = []

        for atual in fronteira:
            expanded_nodes += 1

            if atual == goal:
                caminho, custo = reconstruir_caminho_e_custo(grid, came_from, atual)
                return (
                    caminho,
                    custo,
                    expanded_nodes,
                    generated_nodes,
                    max_frontier_size,
                )

            r, c = atual

            movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dr, dc in movimentos:
                nr, nc = r + dr, c + dc
                proxima_pos = (nr, nc)

                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                    celula = grid[nr][nc]

                    if celula != "#" and proxima_pos not in came_from:
                        came_from[proxima_pos] = atual
                        proxima_fronteira.append(proxima_pos)
                        generated_nodes += 1

        if not proxima_fronteira:
            break

        # Otimização do beam search: ordena a próxima fronteira com base na heurística e mantém apenas os melhores beam_width nós
        proxima_fronteira.sort(key=lambda pos: heuristica(pos, goal))
        # Mantém apenas os melhores beam_width nós
        fronteira = proxima_fronteira[:beam_width]

    return None, 0, expanded_nodes, generated_nodes, max_frontier_size


def reconstruir_caminho_e_custo(grid, came_from, atual):
    """Reconstroi o caminho de tras para frente, a partir do objetivo até o inicio"""

    caminho = []
    custo = 0

    while atual is not None:
        caminho.append(atual)

        if came_from[atual] is not None:
            r, c = atual
            celula = grid[r][c]
            custo += int(celula) if celula.isdigit() else 1

        atual = came_from[atual]

    caminho.reverse()
    return caminho, custo
