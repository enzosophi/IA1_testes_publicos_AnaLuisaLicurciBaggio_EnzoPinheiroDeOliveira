from typing import Any, Dict, List, Optional
from harness.policy import SolicitaBusca

class AgenteControlador:
#vai propor as decisões de busca e iterar no loop de acordo com o harness
    def __init__(self, harness_execucao: Any) -> None:
        self.harness = harness_execucao
        self.historico_mensagens: List[Dict[str, Any]] = []

    def decidir_proxima_acao(
        self, id_mapa: str, algoritmos_para_testar: List[str]
    ) -> Dict[str, Any]:
    #com base no historico de tentatuvas vai deicdir qual sera a prxima ação
        algoritnos_testados = {
            msg["content"].get("algoritmo_solicitado")
            for msg in self.historico_mensagens
            if "content" in msg and isinstance(msg["content"], dict)
        }

        for alg in algoritmos_para_testar:
            if alg not in algoritnos_testados:
                heuristica = "manhattan" if alg in {"greedy", "astar", "beam"} else None
                largura_feixe = 5 if alg == "beam" else None

                return{
                    "tipo": "chamada_ferramenta",
                    "args": {
                        "algoritmo": alg,
                        "id_mapa": id_mapa,
                        "heuristica": heuristica,
                        "largura_feixe": largura_feixe,
                        "max_expansoes":10_000,
                        "max_tamanho_fronteira": 20_000,
                        "tempo_limite_ms": 2_000.0,
                    },
                }
        return {"tipo": "final", "motivo": "todas as buscas foram executadas"}

    def executar_loop{
        self, id_mapa: str, algoritmos_plano: List[str], max_passos: int = 10
    } -> Dict[str, Any]:
        for passo in range(max_passos):
            acao = self.decidir_proxima_acao(id_mapa, algoritmos_plano)

            if acao.get("tipo") == "final":
                return{
                    "status": "concluido",
                    "passos_executados": passo,
                    "historico": self.historico_mensagens,
                }

                argumentos = acao.get("args", {})
                solicitacao = SolicitaBusca{
                    algoritmo = argumentos.get("algoritmo"),
                    id_mapa=argumentos.get("id_mapa"),
                    heuristica=argumentos.get("heuristica"),
                    largura_feixe=argumentos.get("largura_feixe"),
                    max_expansoes=argumentos.get("max_expansoes", 10_000),
                    max_tamanho_fronteira=argumentos.get("max_tamanho_fronteira", 20_000),
                    tempo_limite_ms=argumentos.get("tempo_limite_ms", 2_000.0),
                }

                observacao_resultado = self.harness.executar(solicitacao)
                conteudo_observacao = {
                    "algoritmo_solicitado": argumentos.get("algoritmo"),
                    "status": observacao_resultado.status,
                    "encontrado": observacao_resultado.found,
                    "caminho": observacao_resultado.path,
                    "custo": observacao_resultado.path_cost,
                    "nos_expandidos":observacao_resultado.expanded_nodes,
                    "tempo_ms": observacao_resultado.execution_time_ms,
                    "motivo": observacao_resultado.reason,
                }

                self.historico_mensagens.append(
                    {"role": "tool", "content": conteudo_observacao}
                )