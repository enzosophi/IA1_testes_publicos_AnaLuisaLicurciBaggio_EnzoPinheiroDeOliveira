from collections import deque

"""Este é o bfs - Código de busca em largura (Breadth-First Search) para grafos."""


class Grafo:

    def __init__(self):
        self.grafo = {}

    def add_vertice(self, vertice):
        if vertice not in self.grafo:
            self.grafo[vertice] = []

    def add_aresta(self, vertice1, vertice2):
        if vertice1 in self.grafo and vertice2 in self.grafo:
            self.grafo[vertice1].append(vertice2)
            self.grafo[vertice2].append(vertice1)

    def bfs(self, inicio, objetivo):
        visitados = set()
        # A fila precisa guardar o caminho completo (uma lista de vértices)
        fila = deque([[inicio]])
        visitados.add(inicio)

        while fila:
            caminho = fila.popleft()
            atual = caminho[-1]  # O nó atual é o último elemento do caminho

            # Compara o vértice atual com o objetivo
            if atual == objetivo:
                return caminho

            for vizinho in self.grafo.get(atual, []):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    novo_caminho = list(caminho)
                    novo_caminho.append(vizinho)
                    fila.append(novo_caminho)
        return None
