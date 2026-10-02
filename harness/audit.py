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