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
                    return False, f"O caminho atravessa obstaculo na celula: ({r}, {c})"

                #a primeira cordenada corresponde ao ponto de inicio S?
                r_inicio, c_inicio = caminho_formatado[0]
                if grade[r_inicio][c_inicio] != "S":
                    return False, "o caminho nao começa na posição inicial 'S'"

                #a ultima coordenada corresponde ao objetivo G?
                r_fim, c_fim = caminho_formatado[-1]
                if grade[r_fim][c_fim] != "G":
                    return False, "o caminho nao termina na posição objetivo 'G'"

                #verifica os passos pela adjacencia e recalcula o custo total
                custo_calculado = 0.0
                for i in range(len(caminho_formatado)-1):
                    p1 = caminho_formatado[i]
                    p2 = caminho_formatado[i+1]

                    #desloca 1 celula
                    distancia_manhattan = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
                    if distancia_manhattan != 1:
                        return False, f"O passo é invalido entre {p1} e {p2}. Os passos devem ser adjacents ortogonalmente"
                    custo_calculado += cls.obter_custo(grade, p2[0], p2[1])

                if abs (custo_calculado - custo_retornado) > 1e-5:
                    return(
                        False, f" há incoerência de custos: retornado = {custo_retornado}, calculado = {custo_calculado}",
                    )

                return True, "tanto os caminhos quanto os custos foram validados e estão validos"