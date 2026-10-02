from typing import Any
from dataclasses import asdict

from harness.executor import SearchHarness
from harness.policy import SolicitaBusca

# Importa os algoritmos
from algorithms.astar import a_star
from algorithms.elective import dfs
from algorithms.ucs import uniform_cost_search
from algorithms.greedy import greedy_search
from algorithms.bfs import bfs
from algorithms.beam import beam_search


def adaptador_padrao(funcao_busca):
    def wrapper(grade, **kwargs):
        # Captura os orçamentos suportando chaves em inglês e português
        max_exp = kwargs.get("max_expansions")
        if max_exp is None:
            max_exp = kwargs.get("max_expansoes", 10000)

        max_fron = kwargs.get("max_frontier_size")
        if max_fron is None:
            max_fron = kwargs.get("max_tamanho_fronteira", 20000)

        timeout = kwargs.get("timeout_ms")
        if timeout is None:
            timeout = kwargs.get("tempo_limite_ms", 2000.0)

        # Se qualquer orçamento for não-positivo, nega imediatamente (DENY)
        if (
            (max_exp is not None and max_exp <= 0)
            or (max_fron is not None and max_fron <= 0)
            or (timeout is not None and timeout <= 0)
        ):
            return {
                "status": "DENY",
                "found": False,
                "path": [],
                "path_cost": 0,
                "expanded_nodes": 0,
                "generated_nodes": 0,
                "max_frontier_size": 0,
                "reason": "Orçamento não positivo negado",
            }

        start, goal = (0, 0), (0, 0)
        for r in range(len(grade)):
            for c in range(len(grade[0])):
                if grade[r][c] == "S":
                    start = (r, c)
                elif grade[r][c] == "G":
                    goal = (r, c)

        extra_args = {}
        if funcao_busca == beam_search and kwargs.get("largura_feixe"):
            extra_args["beam_width"] = kwargs["largura_feixe"]

        # Executa a busca passando os limites de orçamento
        try:
            caminho, custo, exp, gen, fron = funcao_busca(
                grade,
                start,
                goal,
                max_expansions=max_exp,
                max_frontier_size=max_fron,
                **extra_args
            )
        except TypeError:
            caminho, custo, exp, gen, fron = funcao_busca(
                grade, start, goal, **extra_args
            )

        status = "ALLOW"
        reason = "Busca finalizada"

        # Verifica se atingiu ou estourou o limite de expansões
        if max_exp is not None and max_exp > 0 and exp >= max_exp:
            status = "ERROR"
            reason = "Limite de expansões excedido"

        caminho_listas = [list(pos) for pos in caminho] if caminho else []

        return {
            "status": status,
            "found": bool(caminho) and status == "ALLOW",
            "path": caminho_listas if status == "ALLOW" else [],
            "path_cost": custo if (caminho and status == "ALLOW") else 0,
            "expanded_nodes": exp,
            "generated_nodes": gen,
            "max_frontier_size": fron,
            "reason": reason,
        }

    return wrapper


harness = SearchHarness()
harness.registrar_algoritmo("astar", adaptador_padrao(a_star))
harness.registrar_algoritmo("ucs", adaptador_padrao(uniform_cost_search))
harness.registrar_algoritmo("greedy", adaptador_padrao(greedy_search))
harness.registrar_algoritmo("dfs", adaptador_padrao(dfs))
harness.registrar_algoritmo("bfs", adaptador_padrao(bfs))
harness.registrar_algoritmo("beam", adaptador_padrao(beam_search))


def execute_search(request: dict[str, Any]) -> dict[str, Any]:
    solicitacao = SolicitaBusca(
        algoritmo=request.get("algorithm", ""),
        id_mapa=request.get("map_id", ""),
        heuristica=request.get("heuristic"),
        largura_feixe=request.get("beam_width"),
        max_expansoes=request.get("max_expansions", 10000),
        max_tamanho_fronteira=request.get("max_frontier_size", 20000),
        tempo_limite_ms=request.get("timeout_ms", 2000.0),
    )
    resultado_obj = harness.executar(solicitacao)
    return asdict(resultado_obj)
