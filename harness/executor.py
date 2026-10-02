from dataclasses import asdict, dataclass
import time
from typing import Any, Dict, List, Optional, Tuple

from harness.audit import HarnessAuditoria
from harness.policy import PoliticaHarness, SolicitaBusca, valida_mapa
from harness.validator import ValidadorResultado

@dataclass
class ResultadoBusca:
    status: str
    found: bool
    path: List[Any]
    path_cost: float
    expanded_nodes: int
    generated_nodes: int
    max_frontier_size: int
    execution_time_ms:float
    reason: str = ""

class SearchHarness:

    def __init__(self, catalogo_busca: Optional[Dict[str, Any]] = None) -> None:
        self.politica = PoliticaHarness()
        self.validador = ValidadorResultado()
        self.auditoria = HarnessAuditoria()
        self.catalogo_busca = catalogo_busca or {}

    def registrar_algoritmo(self, nome: str, funcao_busca: Any) -> None:
        self.catalogo_busca[nome]= funcao_busca

    def autorizar(self, solicitacao: SolicitaBusca) -> Tuple[bool, str]:
        return self.politica.autorizar(solicitacao)

    def executar(self, solicitacao: SolicitaBusca) -> ResultadoBusca:
        inicio_tempo = time.perf_counter()

        permitido, motivo_autorizacao = self.autorizar(solicitacao)
        if not permitido:
            resultado_negado = ResultadoBusca{
                status="DENY",
                found=False,
                path=[],
                path_cost=0.0,
                expanded_nodes=0,
                generated_nodes=0,
                max_frontier_size=0,
                execution_time_ms=0.0,
                reason=motivo_autorizacao,
            }

            self.auditoria.registrar(
                solicitacao-asdict(solicitacao),
                status_decisao="DENY",
                motivo=motivo_autorizacao,
                resultado_busca=asdict(resultado_negado),
            )
            return resultado_negado

        valido, motivo_mapa, grade = validar_mapa(solicitacao.id_mapa)
        if not valido:
            resultado_erro_mapa = ResultadoBusca(
                status="DENY",
                found=False,
                path=[],
                path_cost=0.0,
                expanded_nodes=0,
                generated_nodes=0,
                max_frontier_size=0,
                execution_time_ms=0.0,
                reason=motivo_mapa,
            )

            self.auditoria.registrar(
                solicitacao=asdict(solicitacao),
                status_decisao="DENY",
                motivo=motivo_mapa,
                resultado_busca=asdict(resultado_erro_mapa),
            )
            return resultado_erro_mapa
        
        funcao_algoritmo = self.catalogo.busca.get(solicitacao.algoritmo)
        if not funcao_algoritmo:
            resultado_ausente = ResultadoBusca(
                status="DENY",
                found=False,
                path=[],
                path_cost=0.0,
                expanded_nodes=0,
                generated_nodes=0,
                max_frontier_size=0,
                execution_time_ms=0.0,
                reason=f"algoritmo '{solicitacao.algoritmo}' não impplementado no catalogo",
            )
            return resultado_ausente

        try:
            resposta_busca = funcao_algoritmo(
                grade=grade,
                heuristica=solicitacao.heuristica,
                largura_feixe=solicitacao.largura_feixe,
                max_expansoes=solicitacao.max_expansoes,
                max_tamanho_fronteira=solicitacao.max_tamanho_fronteira,
                tempo_limite_ms=solicitacao.tempo_limite_ms,
            )

            fim_tempo = time.perf_counter()
            tempo_execucao_ms = (fim_tempo - inicio_tempo)*1000.0

            status_final = resposta_busca.get("status", "ALLOW")
            motivo_final = resposta_busca.get("reason", "busca concluida")
            caminho = resposta_busca.get("path", [])
            custo = float(resposta_busca.get("path_cost", 0.0))
            encontrou = resposta_busca.get("found", False)

            if status_final == "ALLOW" and encontrou:
                caminho_valido, motivo_validacao = self.validador.validar_caminho(
                    grade, caminho, custo
                )
                if not caminho_valido:
                status_final = "ERROR"
                motivo_final = f"falaha na validacao do caminho: {motivo_validacao}"
                encontrou = False
                caminho = []
                custo = 0.0

            resultado = ResultadoBusca(
                status=status_final,
                found=encontrou,
                path=caminho,
                path_cost=custo,
                expanded_nodes=int(resposta_busca.get("expanded_nodes", 0)),
                generated_nodes=int(resposta_busca.get("generated_nodes", 0)),
                max_frontier_size=int(resposta_busca.get("max_frontier_size", 0)),
                execution_time_ms=round(tempo_execucao_ms, 4),
                reason=motivo_final,
            )

        except Exception as erro:
            fim_tempo = time.perf_counter()
            tempo_execucao_ms = (fim_tempo - inicio_tempo)*1000.0
            resultado = ResultadoBusca(
                status="ERROR",
                found=False,
                path=[],
                path_cost=0.0,
                expanded_nodes=0,
                generated_nodes=0,
                max_frontier_size=0,
                execution_time_ms=round(tempo_execucao_ms, 4),
                reason=f"excecao não tratada durante a busca: {str(erro)}",
            )

        self.auditoria.registrar(
            solicitacao=asdict(solicitacao),
            status_decisao=resultado.status,
            motivo= resultado.reason,
            resultado_busca = asdict(resultado),
        )

        return resultado