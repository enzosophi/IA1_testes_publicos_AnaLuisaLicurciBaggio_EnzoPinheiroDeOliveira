# Testes públicos — Projeto de IA I

Este pacote é entregue aos alunos. Copie `tests_publicos/` e
`student_api_template.py` para a raiz do repositório. Renomeie o template para
`student_api.py` e altere somente o adaptador para chamar a implementação da
dupla.

Contrato obrigatório:

```python
def execute_search(request: dict) -> dict:
    """Executa a solicitação exclusivamente por meio do harness."""
```

O resultado deve conter: `status`, `found`, `path`, `path_cost`,
`expanded_nodes`, `generated_nodes`, `max_frontier_size`,
`execution_time_ms` e `reason`. Cada posição do caminho deve ser uma lista ou
tupla `[linha, coluna]`.

Execute na raiz do projeto:

```bash
python -m pytest tests_publicos -q
```

Os testes públicos verificam o contrato, correção básica das buscas, políticas
do harness, limites, validação de saída e auditoria. A avaliação também usa
casos reservados com o mesmo contrato.
