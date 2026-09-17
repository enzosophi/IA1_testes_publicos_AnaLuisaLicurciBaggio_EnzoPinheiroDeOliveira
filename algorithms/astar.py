import heapq


def heuristica(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, goal):
    fila = []
    h_inicial = heuristica(start, goal)
    heapq.heappush(fila, (h_inicial, 0, start, [start]))

    m_custo = {start: 0}

    while fila:
        f, custo_atual, atual, caminho = heapq.heappop(fila)

        if atual == goal:
            return caminho, custo_atual

        linha, coluna = atual

        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for d_linha, d_coluna in movimentos:
            nova_linha, nova_coluna = linha + d_linha, coluna + d_coluna

            if 0 <= nova_linha < len(grid) and 0 <= nova_coluna < len(grid[0]):
                celula = grid[nova_linha][nova_coluna]

                if celula == "#":
                    continue

                custo_passo = int(celula) if celula.isdigit() else 1
                novo_custo = custo_atual + custo_passo

                proxima_pos = (nova_linha, nova_coluna)

                if proxima_pos not in m_custo or novo_custo < m_custo[proxima_pos]:
                    m_custo[proxima_pos] = novo_custo
                    h = heuristica(proxima_pos, goal)
                    heapq.heappush(
                        fila,
                        (
                            novo_custo + h,
                            novo_custo,
                            proxima_pos,
                            caminho + [proxima_pos],
                        ),
                    )

        return None, float("inf")
