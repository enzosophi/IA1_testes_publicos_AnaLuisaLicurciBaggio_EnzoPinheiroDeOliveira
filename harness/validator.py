from typing import Any, List, Tuple

class ValidadorResultado:
    #vai ser o responsavel por validar a consistencia do caminho e das metricas
    @staticmethod
    def obter_custo(grade: List[str], linha: int, coluna: int) -> float:
        #vai calcular o custo de entrada d uma celula, identificando o caractere daquela celula
        caracter = grade[linha][coluna]

        if caracter in {"S", "."}:
            return 1.0
        elif caracter == "G":
            return 1.0
        elif caracter.isdigit():
            return float(caracter)
        return 1.0

    @classmethod
    def validar_caminho(
        cls, grade: List[str], caminho:List[Any], custo_retornado: float
    ) -> Tuple[bool, str]:
    #vai validar o caminho ao passo que analisa as posicoes, obstavulos, a adjacencia e os custos.
    #Então, se o caminho estiver vazio, nenhuma ação vai ser necessaria
    
    if not caminho:
        return True, "não existe nenhum caminho que precise ser validado"

        num_linhas = len(grade)
        num_colunas = len(grade[0])

        #coordenadas no formato das tuplas, linhas e colunas

        caminho_formatado = []
        for no in caminho:
            if isinstance(no, (list,tuple))and len(no) == 2:
                caminho_formatado.append((int(no[0]), int(no[1])))
            else:
                return False, "O formato de coordenada está invalido"
        
        #checa se as coordenadas são validas
        for r, c in caminho_formatado:
            if r < 0 or r>= num_linhas or c< 0 or c>= num_colunas:
                return False, f"coordenada fora da grade: ({r}, {c})"
            if grade[r][c] == "#":
                return False f"O caminho atravessa obstaculo na celula: ({r}, {c})"

