import os
import csv
import glob
from student_api import execute_search

# Procura automaticamente por todos os ficheiros de mapa (.txt)
mapas = glob.glob("**/P*.txt", recursive=True)
if not mapas:
    mapas = [
        f
        for f in glob.glob("**/*.txt", recursive=True)
        if "requirement" not in f and "README" not in f
    ]

print(f"Mapas encontrados: {mapas}")
if not mapas:
    print("Aviso: Nenhum mapa .txt encontrado.")
    exit(1)

# Dicionário para separar os resultados por método/variante exata
resultados_por_metodo = {
    "bfs": [],
    "ucs": [],
    "dfs": [],
    "greedy_manhattan": [],
    "astar_h0": [],
    "astar_manhattan": [],
}

print("Iniciando execução dos experimentos...")

for mapa in mapas:
    # 1. BFS
    res = execute_search({"algorithm": "bfs", "map_id": mapa})
    if isinstance(res, dict):
        res["metodo_variante"] = "bfs"
        resultados_por_metodo["bfs"].append(res)

    # 2. UCS
    res = execute_search({"algorithm": "ucs", "map_id": mapa})
    if isinstance(res, dict):
        res["metodo_variante"] = "ucs"
        resultados_por_metodo["ucs"].append(res)

    # 3. DFS (se aplicável)
    try:
        res = execute_search({"algorithm": "dfs", "map_id": mapa})
        if isinstance(res, dict):
            res["metodo_variante"] = "dfs"
            resultados_por_metodo["dfs"].append(res)
    except Exception:
        pass

    # 4. Greedy (Manhattan)
    res = execute_search(
        {
            "algorithm": "greedy",
            "map_id": mapa,
            "heuristic": "manhattan",
            "max_expansions": 20000,
            "max_frontier_size": 50000,
            "timeout_ms": 5000.0,
        }
    )
    if isinstance(res, dict):
        res["metodo_variante"] = "greedy_manhattan"
        resultados_por_metodo["greedy_manhattan"].append(res)

    # 5. A* com h=0 ("h0")
    res = execute_search(
        {
            "algorithm": "astar",
            "map_id": mapa,
            "heuristic": "h0",
            "max_expansions": 20000,
            "max_frontier_size": 50000,
            "timeout_ms": 5000.0,
        }
    )
    if isinstance(res, dict):
        res["metodo_variante"] = "astar_h0"
        resultados_por_metodo["astar_h0"].append(res)

    # 6. A* com Manhattan
    res = execute_search(
        {
            "algorithm": "astar",
            "map_id": mapa,
            "heuristic": "manhattan",
            "max_expansions": 20000,
            "max_frontier_size": 50000,
            "timeout_ms": 5000.0,
        }
    )
    if isinstance(res, dict):
        res["metodo_variante"] = "astar_manhattan"
        resultados_por_metodo["astar_manhattan"].append(res)

os.makedirs("resultados", exist_ok=True)
todos_dados = []

# Salva um CSV individual para cada método e agrupa para o consolidado
# Salva um CSV individual para cada método e agrupa para o consolidado
for metodo, lista_res in resultados_por_metodo.items():
    if not lista_res:
        continue

    dados_metodo = []
    # Note que precisamos de associar o mapa correspondente a cada resultado na ordem em que foram executados
    # Se percorreu os mapas num loop externo, pode capturar o mapa diretamente:
    for i, res in enumerate(lista_res):
        # Mapeia o algoritmo base a partir da variante (ex: 'astar_h0' -> 'astar')
        alg_base = metodo.split("_")[0]

        item = {
            "metodo_variante": metodo,
            "algoritmo": alg_base,
            "map_id": mapas[i % len(mapas)],  # Associa o mapa correspondente
            "status": res.get("status"),
            "found": res.get("found"),
            "path_cost": res.get("path_cost"),
            "expanded_nodes": res.get("expanded_nodes"),
            "generated_nodes": res.get("generated_nodes"),
            "max_frontier_size": res.get("max_frontier_size"),
            "reason": res.get("reason"),
        }
        dados_metodo.append(item)
        todos_dados.append(item)

    # Grava o CSV específico do método
    sub_csv_path = f"resultados/{metodo}_metrics.csv"
    with open(sub_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dados_metodo[0].keys())
        writer.writeheader()
        writer.writerows(dados_metodo)

# Grava o CSV consolidado geral
if todos_dados:
    consolidado_path = "resultados/experiment_metrics.csv"
    with open(consolidado_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=todos_dados[0].keys())
        writer.writeheader()
        writer.writerows(todos_dados)

print("Experimentos concluídos com sucesso!")
print(
    "Foram criados ficheiros individuais por método na pasta 'resultados/' (ex: astar_h0_metrics.csv, greedy_manhattan_metrics.csv) e o consolidado geral."
)
