# Declaração de Uso de Inteligência Artificial (IA_USAGE.md)

**Projeto:** Agente de Busca com Harness  
**Disciplina:** Inteligência Artificial I  
**Instituição:** Universidade Presbiteriana Mackenzie — Campus Alphaville  
**Docente:** Prof. Dr. Murilo Gazzola  
**Autores:** Enzo Pinheiro de Oliveira & Dupla  

---

## 1. Ferramentas Utilizadas
* **Google Gemini / Claude:** Utilizados como assistentes de desenvolvimento, depuração de código, estruturação de scripts de automação experimental e revisão teórica das respostas do questionário.

---

## 2. Finalidade de Cada Uso
1. **Desenvolvimento e Refatoração de Código:** Apoio na correção de algoritmos de busca clássica (BFS, UCS, Greedy, $A^*$), desempacotamento de tuplas na fronteira e refinamento das regras de validação no adaptador `student_api.py`.
2. **Automação Experimental:** Criação e ajuste de scripts em Python (`run_experiments.py` e `gerar_graficos.py`) para execução em lote dos mapas e geração dos gráficos analíticos.
3. **Documentação e Relatório:** Apoio na estruturação formal e acadêmica do relatório técnico e nas respostas detalhadas do questionário obrigatório (Seção 10).

---

## 3. Resumo de Interações e Prompts Relevantes
* *Prompt de automação:* Pedidos para criar um script em Python que localizasse automaticamente todos os mapas `.txt` na árvore de diretórios, executasse as variações de algoritmos e heurísticas, e exportasse as métricas consolidadas em formato CSV.
* *Prompt de refatoração:* Consultas para identificar o motivo de negação das políticas do harness (`ALLOW` vs `DENY`) ao testar o $A^*$ com $h=0$ e adaptação da string de envio para `"h0"`.

---

## 4. Trechos de Código e Texto Influenciados
* **Script de Experimentos (`run_experiments.py`):** Estrutura de varredura automática de mapas via `glob` e estruturação de dicionários para métricas por variante (`astar_h0`, `astar_manhattan`, `greedy_manhattan`, etc.).
* **Tratamento de Exceções no Harness:** Ajustes na validação de parâmetros de heurística e orçamentos para evitar que mapas sem solução (como o P03) gerassem falhas de execução (*Out-of-Memory* ou loops infinitos).

---

## 5. Verificações Realizadas pela Dupla
* **Testes Automatizados:** Toda a suíte de testes públicos (**T01 a T43**) foi executada e validada exaustivamente via terminal com o comando `python -m pytest tests_publicos -q`, garantindo **100% de aprovação** sem alterações indevidas nos testes fornecidos.
* **Validação Cruzada de Métricas:** Os dados gerados nos ficheiros CSV de experimentos foram inspecionados manualmente para assegurar a consistência entre os nós expandidos, custos de caminho e vereditos de autorização do harness.

---

## 6. Erros da IA Identificados e Corrigidos
* **Incompatibilidade de Tipos no Harness:** A IA sugeriu inicialmente passar `heuristic=None` para o teste de $h=0$ no $A^*$, o que era rejeitado pelas políticas rígidas de validação do harness. O erro foi identificado analisando o log de depuração (`DEBUG: heuristica invalida 'None'`) e corrigido substituindo por `"h0"`.
* **Tratamento de Listas Vazias:** Em uma versão inicial do script de experimentos, se os mapas não fossem encontrados nos caminhos rígidos (*hardcoded*), o script gerava um `IndexError` ao tentar escrever o cabeçalho do CSV. O problema foi corrigido implementando busca dinâmica por diretórios (`glob.glob`).