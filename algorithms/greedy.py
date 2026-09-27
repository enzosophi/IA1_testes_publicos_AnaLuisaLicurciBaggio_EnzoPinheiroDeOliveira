import heapq

def heuristica(a, b):
    # Distância Manhattan para grades 4-direcionais
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def greedy_search(grid, start, goal):
    # A fila guarda: (h_score, posicao_atual, caminho_percorrido)
    pq = []
    h_inicial = heuristica(start, goal)
    heapq.heappush(pq, (h_inicial, start, [start]))
    
    visited = set()
    
    while pq:
        h, atual, caminho = heapq.heappop(pq)
        
        if atual == goal:
            return caminho
            
        if atual in visited:
            continue
            
        visited.add(atual)
        
        r, c = atual
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in movimentos:
            nr, nc = r + dr, c + dc
            
            # Verifica se está dentro dos limites do grid
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                celula = grid[nr][nc]
                
                # Ignora se for obstáculo
                if celula == '#':
                    continue
                    
                proxima_pos = (nr, nc)
                if proxima_pos not in visited:
                    h_novo = heuristica(proxima_pos, goal)
                    # A prioridade na fila é apenas a heurística h(n)
                    heapq.heappush(pq, (h_novo, proxima_pos, caminho + [proxima_pos]))
                    
    return None