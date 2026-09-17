"""Adapte somente este arquivo aos nomes usados no projeto da dupla."""

from typing import Any


def execute_search(request: dict[str, Any]) -> dict[str, Any]:
    """Encaminhe request ao SearchHarness e converta SearchResult em dict."""

    raise NotImplementedError(
        "Conecte este adaptador ao harness da dupla; não chame buscas diretamente."
    )
