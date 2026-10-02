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
