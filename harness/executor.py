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