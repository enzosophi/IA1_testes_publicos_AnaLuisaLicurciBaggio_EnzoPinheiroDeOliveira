from dataclasses import asdict, dataclass
import json
from typing import Any, Dict, List

@dataclass
class RegistroAuditoria:
    #vai representar o registro da auditoria para cada solicitação feita
    solicitacao: Dict[str, Any]
    status_decisao: str
    motivo: str
    resultado_busca: Dict[str,Any]

class HarnessAuditoria:
    #vai gerenciar o registro da auditoria e o historico do harnes

    def __init__(self) -> None:
        #vai iniciar a lista e armazenar os logs
        self._registros: List[RegistroAuditoria] =[]

    def registrar(
        self,
        solicitacao: Dict[str, Any],
        status_decisao: str,
        motivo: str,
        resultado_busca: Dict[str, Any],
    ) -> None:

    #vai registar a imteração no log de auditoria
    registro = RegistroAuditoria(
        solicitacao=solicitacao,
        status_decisao=status_decisao,
        motivo=motivo,
        resultado_busca=resultado_busca
    )
    self._registros.append(registro)
