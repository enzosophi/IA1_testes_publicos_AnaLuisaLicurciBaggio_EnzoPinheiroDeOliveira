# Relatório Técnico: Agente de Busca com Harness
**Disciplina:** Inteligência Artificial I  
**Instituição:** Universidade Presbiteriana Mackenzie — Campus Alphaville  
**Docente:** Prof. Dr. Murilo Gazzola  
**Autores:** Enzo Pinheiro de Oliveira & Ana Luiza Licurci Baggio  

---

## 1. Visão Geral e Formulação do Problema
O presente projeto teve como objetivo construir algoritmos clássicos de busca em grafos aplicados a grades bidimensionais ponderadas, integrando-os obrigatoriamente a uma arquitetura de *Harness* de execução. O agente controlador propõe ações de busca que são interceptadas, validadas e auditadas antes de qualquer execução no ambiente.

* **Estado inicial ($S$):** Coordenada de partida na grade.
* **Estado objetivo ($G$):** Coordenada de destino.
* **Ações:** Movimentação ortogonal (Cima, Baixo, Esquerda, Direita).
* **Custos:** Células livres possuem pesos de 1 a 9; obstáculos (`#`) são intransitáveis.

---

## 2. Arquitetura do Harness e Políticas de Segurança
O Harness atuou como camada de governança externa, garantindo segurança e robustez através das seguintes políticas:
* **Allowlist:** Restringe a execução estritamente aos algoritmos registrados no catálogo.
* **Validação de Mapas e Argumentos:** Rejeita estruturas malformadas, ausência de $S$ ou $G$, e parâmetros inválidos.
* **Orçamentos e Limites:** Interrupção segura baseada em `max_expansions`, `max_frontier_size` e `timeout_ms` para evitar falhas por recursos excessivos (*Out-of-Memory*).
* **Validação de Saída:** Audita a integridade do caminho, ortogonalidade, ausência de colisões com obstáculos e exatidão do custo acumulado.

---

## 3. Métodos de Busca Implementados
* **BFS (Breadth-First Search):** Busca em largura orientada por profundidade (ótimo em passos para custos uniformes).
* **UCS (Uniform Cost Search):** Busca de custo uniforme guiada por $g(n)$ (ótimo em custos ponderados).
* **Greedy Best-First Search:** Busca gulosa guiada puramente pela heurística $h(n)$.
* **A\* Search:** Combinação de custo real e heurística $f(n) = g(n) + h(n)$ (ótimo e eficiente com heurísticas admissíveis).
* **DFS / Outras Variações:** Implementadas para fins comparativos e de exploração de ramos.

---

## 4. Plano Experimental e Análise de Resultados
Os experimentos foram conduzidos em múltiplos mapas de teste, avaliando métricas como custo do caminho, nós expandidos, nós gerados e tamanho máximo da fronteira.

### Gráficos Comparativos Obtidos:
1. **Custo Médio por Método:** `resultados/custo_por_metodo.png`
2. **Estados Expandidos por Método:** `resultados/expansoes_por_metodo.png`
3. **Tamanho Máximo da Fronteira:** `resultados/fronteira_por_metodo.png`

* **Discussão:** Os resultados demonstraram que o $A^*$ e o Greedy reduziram drasticamente o número de nós expandidos em comparação ao BFS e ao UCS, graças ao direcionamento da heurística de Manhattan. Em mapas sem solução (como o caso testado no mapa P03), as políticas de limite do harness asseguraram o encerramento seguro sem entrar em loops infinitos.

---

## 5. Questionário Obrigatório

### 1. Por que o BFS não garante menor custo em mapas ponderados?
* O algoritmo de busca em largura (BFS) expande os nós obrigatoriamente com base no menor nível de profundidade (número de passos/arestas).
* Assume que todas as transições possuem o mesmo custo unitário. Em mapas ponderados, onde diferentes células possuem custos de entrada variados (1 a 9).
* Um caminho com menos passos pode acumular um custo total superior ao de um caminho mais longo em termos de quantidade de saltos, mas composto por células de menor peso. Portanto, o BFS garante a otimização de passos, mas não a otimização de custo.

### 2. Por que o UCS pode expandir mais estados do que o A\*?
* O UCS expande os nós de forma radial e uniforme, com base exclusivamente no custo acumulado real $g(n)$, sem possuir nenhuma informação direcional sobre a localização do objetivo. 
* O $A^*$, por sua vez, utiliza uma função de avaliação $f(n) = g(n) + h(n)$, onde a heurística $h(n)$ fornece uma estimativa do custo restante até o objetivo. 
* Isso permite que o $A^*$ priorize a expansão de nós que estão mais próximos do objetivo, reduzindo o número de estados expandidos em comparação com o UCS, que acaba explorando caminhos menos promissores devido à falta de orientação heurística.

### 3. Em quais condições o $A^*$ garante optimalidade?
O $A^*$ garante a optimalidade (encontrar o menor custo absoluto) considerando dois conceitos principais:
* **Consistência:** Para busca em grafo com lista de fechados, a heurística deve satisfazer a desigualdade triangular, ou seja, $h(n) \le c(n, a, n') + h(n')$ para todo nó $n$, ação $a$ e sucessor $n'$. Isso garante que o custo estimado nunca superestime o custo real e que o primeiro caminho encontrado para um nó seja o de menor custo.
* **Admissibilidade:** Para busca em árvore, a heurística deve ser **admissível**, ou seja, nunca superestimar o custo real para alcançar o objetivo ($h(n) \le h^*(n)$). Isso garante que o $A^*$ sempre encontrará o caminho ótimo, mesmo sem a consistência estrita de grafo.

### 4. O que mudou quando a heurística Manhattan foi multiplicada por 2?
* Ao multiplicar por 2, a heurística passa a superestimar o custo real em diversos cenários, perdendo a propriedade de admissibilidade.
* O efeito prático observado foi uma "ganância" excessiva do algoritmo, que passou a priorizar caminhos que pareciam mais promissores com base na heurística inflada.
* Com isso, o algoritmo perdeu a garantia matemática de optimalidade, podendo retornar caminhos subótimos (mais caros em termos de custo total) em detrimento da velocidade.

### 5. Qual foi o efeito da largura $k$ em Beam Search (caso escolhido)?
* A largura do feixe ($k$) define o limite máximo de nós mantidos na fronteira a cada nível de expansão.
* Valores maiores de $k$ aumentam a diversidade de caminhos explorados e, consequentemente, a chance de encontrar o caminho ótimo, mas elevam o consumo de memória e o tempo de execução.
* Valores menores de $k$ levam a uma exploração mais restrita, potencialmente descartando caminhos promissores e resultando em soluções subótimas. Portanto, a escolha de $k$ representa um *trade-off* direto entre eficiência computacional e qualidade da solução.

### 6. Qual é a diferença entre o agente decidir e o harness autorizar?
* O agente controlador atua como o componente de tomada de decisão: ele analisa o problema, seleciona qual ferramenta de busca utilizar e define os parâmetros da solicitação. No entanto, o agente não possui autonomia operacional direta. 
* O *harness* atua como uma camada de governança externa e soberana, responsável por interceptar a chamada e avaliar se a ação cumpre estritamente as políticas de segurança, Allowlist, orçamentos e integridade, emitindo um veredito de `ALLOW` ou `DENY`.

### 7. Por que um prompt de sistema não substitui as políticas do harness?
* Instruções em linguagem natural baseadas em prompts de sistema em modelos de IA são probabilísticas, maleáveis e vulneráveis a falhas de interpretação, desvios contextuais e ataques de *prompt injection*. 
* Em contraste, o *harness* é implementado como uma arquitetura de código determinística e programática, capaz de aplicar validações rígidas, bloqueios de segurança do tipo *fail-safe* e auditorias imunes a ambiguidades textuais.

### 8. Como o harness validou um caminho antes de aceitá-lo?
Através do módulo de validação (`ValidadorResultado`), que executa verificações estruturais rigorosas:
* Confirma se o caminho tem início em $S$ e término em $G$.
* Valida se cada transição entre os estados é estritamente ortogonal (4 direções).
* Assegura que nenhuma coordenada do caminho atravessa obstáculos (`#`).
* Recalcula e audita se o custo total devolvido confere exatamente com a soma dos custos de transição das células do mapa.

### 9. Qual política evitou o maior risco ou erro no experimento?
* A política de orçamento de expansões (`max_expansions`) e timeout (`timeout_ms`). Em cenários de mapas complexos ou na ausência total de solução (como testado no mapa P03), algoritmos desprovidos de limites cairiam em loops infinitos ou esgotariam os recursos de memória RAM da máquina (*Out-of-Memory*). Os limites garantiram a interrupção segura e controlada da execução.

### 10. Qual compromisso foi observado entre qualidade, tempo e memória?
Observou-se o *trade-off* clássico da teoria de Inteligência Artificial:
* **BFS / UCS:** Garantem qualidade estrutural ou de custo, mas sacrificam memória e tempo devido à expansão radial extensiva.
* **Greedy:** É extremamente rápido e consome pouca memória, mas sacrifica a qualidade e a optimalidade da solução.
* **$A^*$ (com heurística admissível):** Representa o ponto de equilíbrio ideal, alcançando alta eficiência computacional e economia de memória sem abrir mão da garantia de menor custo.

---

## 6. Conclusão
O projeto permitiu consolidar a integração entre os métodos clássicos de busca em IA e as arquiteturas modernas de controle por *Harness*. Verificou-se empiricamente que o uso de heurísticas admissíveis no $A^*$ otimiza significativamente o desempenho sem comprometer a garantia de optimalidade, enquanto as políticas de segurança e orçamentos asseguram robustez operacional frente a entradas complexas ou inviáveis.