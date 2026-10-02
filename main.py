import os
from agent.controller import AgenteControlador
from harness.executor import SearchHarness

#import dos algoritmos
from algorithms.bfs import Grafo
from algorithms.ucs import uniform_cost_search
from algorithms.greedy import greedy_search
from algorithms.astrar import a_star
from algorithms.elective import dfs

def cria_configura_harness() -> SearchHarness:
    #registra as funcoes de busca no catálogo
    harness = SearchHarness()

    harness.registrar_algoritmo("bfs", Grafo.bfs)
    harness.registrar_algoritmo("ucs", uniform_cost_search)
    harness.registrar_algoritmo("greedy", greedy_search)
    harness.registrar_algoritmo("astar", a_star)
    harness.registrar_algoritmo("dfs", dfs)
    harness.registrar_algoritmo("beam", dfs)

    return harness

def main() -> None:
    print("Agente de busca com Harness")
    print(" Ana Luisa Licurci Baggio")
    print(" Enzo Pinheiro de Oliveira")

    harness= cria_configura_harness()
    agente = AgenteControlador(harness_execucao=harness)

    caminho_mapa = os.path.join("problems", "maps", "P01.txt")
    plano_busca = ["bfs", "ucs", "astar"]

    print(f"Agent loop está sendo executado para o mapa {caminho_mapa}")

    resultado = agente.executar_loop(
        id_mapa = caminho_mapa, algoritmos_plano=plano_busca
    )

    print("\n Resultado do agente")
    print(f"status final- {resultado.get('status')}")
    print(f"passos executados- {resultado.get('passos_executados')}")

    print("\n Log de auditoria")
    print(harness.auditoria.exportar_json())

if __name__ == "__main__":
    main() 