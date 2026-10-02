import os
import csv
import time
from student_api import execute_search

# Definição dos mapas (ajuste os caminhos conforme sua pasta de mapas)
mapas = [
    # Pequenos (exemplo)
    "problems/maps/P01.txt",
    "problems/maps/P02.txt",
    "problems/maps/P03.txt",
    "problems/maps/P04.txt",
    "problems/maps/P05.txt",
    # Adicione mais 10 caminhos de mapas médios e grandes aqui...
]

algoritmos = ["bfs", "ucs", "greedy", "astar", "dfs"]
heuristicas = [
    None,
    "manhattan",
    "manhattan_2x",
]  # Ajuste conforme a implementação das suas heurísticas

resultados = []

print("Iniciando execução dos experimentos...")

for mapa in mapas:
    if not os.path.exists(mapa):
        continue

    for algo in algoritmos:
        # Algoritmos como BFS e UCS não usam heurística
        heurs = [None] if algo in ["bfs", "ucs", "dfs"] else heuristicas

        for heur in heurs:
            request = {
                "algorithm": algo,
                "map_id": mapa,
                "heuristic": (
                    heur if heur != "manhattan_2x" else "manhattan"
                ),  # Ajuste se sua API aceitar multiplier
                "max_expansions": 20000,
                "max_frontier_size": 50000,
                "timeout_ms": 5000.0,
            }

            # Se for teste de heurística dobrada (h2 = 2 * h1)
            if heur == "manhattan_2x":
                request["heuristic"] = "manhattan"
                # Aqui você pode passar um argumento extra se necessário na sua API

            inicio_tempo = time.perf_counter()
            res = execute_search(request)
            fim_tempo = time.perf_counter()

            resultados.append(
                {
                    "mapa": os.path.basename(mapa),
                    "algoritmo": algo,
                    "heuristica": heur or "N/A",
                    "status": res.get("status"),
                    "found": res.get("found"),
                    "path_cost": res.get("path_cost"),
                    "expanded_nodes": res.get("expanded_nodes"),
                    "generated_nodes": res.get("generated_nodes"),
                    "max_frontier_size": res.get("max_frontier_size"),
                    "execution_time_ms": (fim_tempo - inicio_tempo) * 1000,
                    "reason": res.get("reason"),
                }
            )

# Salva os resultados na pasta resultados/
os.makedirs("resultados", exist_ok=True)
csv_path = "resultados/experiment_metrics.csv"

with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
    writer.writeheader()
    writer.writerows(resultados)

print(f"Experimentos concluídos! Dados salvos em {csv_path}")
