import heapq

def uniform_cost_search(grid, start, goal):
    # A fila guarda: (g_score, posicao_atual, caminho_percorrido)
    pq = []
    heapq.heappush(pq, (0, start, [start]))
    
    # Dicionário para guardar o menor custo g encontrado para cada posição
    g_costs = {start: 0}
    
    while pq:
        current_g, atual, caminho = heapq.heappop(pq)
        
        if atual == goal:
            return caminho, current_g
            
        # Se encontrarmos um caminho mais curto para este nó anteriormente, ignoramos
        if current_g > g_costs.get(atual, float('inf')):
            continue
            
        r, c = atual
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in movimentos:
            nr, nc = r + dr, c + dc
            
            # Verifica limites do grid
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                celula = grid[nr][nc]
                
                # Pula se for obstáculo
                if celula == '#':
                    continue
                
                # Custo de entrada na célula (conforme regras do projeto)
                custo_passo = int(celula) if str(celula).isdigit() else 1
                novo_g = current_g + custo_passo
                
                proxima_pos = (nr, nc)
                
                # Se ainda não visitou ou encontrou um caminho mais barato, atualiza
                if proxima_pos not in g_costs or novo_g < g_costs[proxima_pos]:
                    g_costs[proxima_pos] = novo_g
                    heapq.heappush(pq, (novo_g, proxima_pos, caminho + [proxima_pos]))
                    
    return None, float('inf')