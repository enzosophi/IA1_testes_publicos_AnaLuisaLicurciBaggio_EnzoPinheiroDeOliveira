from dataclasses import dataclass 
from typing import Any, Optional, Tuple
import os

@dataclass
class SolicitaBusca:
    """contrato de entrada que vai sollicitar busca"""
    alg: str
    id_mapa: str
    heuristica: Optional[str] = None
    largura_feixe: Optional[int] = None
    max_expansoes: int= 10_000
    max_tamanho_fronteira: int= 20_000
    tempo_limite_ms: float = 2_000.0

# vai verificar basicamente a intergidade de tal arquivo antes de ser executada a busca
def valida_mapa(caminho_mapa: str) -> Tuple[bool, str,list[str]]:
    """a integridade do arquivo do mapa é considerada aplicada se o arquivo existir
    se o mapa não estiver vazio e suas linhas tiverem a mesma largura, se conter exatamente um inicio S e um objetivo G e se os caracteres forem validos (como S, G, ., #, 1-9)"""

    if not os.path.exists(caminho_mapa):
        return False, f"arquivo nao encontrado: {caminho_mapa}", []
        #vai tentar abrir e ler as linhas do arquivo
    try:
        with open(caminho_mapa, "r", encoding="utf-8") as arquivo:
                linhas = [linha.rstrip("\r\n") for linha in arquivo.readlines()]
    except Exception as erro:
        return False, f"erro ao ler o arquivo: {erro}", []
    # mapa está vazio ou não
    if not linhas or all(len(linha)==0 for linha in linhas):
        return False, "O mapa esta vazio",[]

    larg_esperada = len(linhas[0])
    qtd_inicio = 0
    qtd_objetivo = 0
    caracteres_validos = set("SG.#123456789")
    #percorre linha a linha e caractere pra poder fazer as validacoes de dimensoes e conteudo
    for indice_linha, linha in enumerate(linhas):
        if len(linha) != larg_esperada:
            return False, f"A linha {indice_linha} nao possui uma largura compativel",[]
        #vai validar se o caracter pertence ao vocabulario que foi proposto no projeto
        for caracter in linha:
            if caracter not in caracteres_validos:
                return False, f"caracter invalido '{caracter}'enconotrado no mapa", []
            if caracter == "S":
                qtd_inicio += 1
            elif caracter == "G":
                qtd_objetivo += 1
    #ponto de inicio S e ponto objetivo G
    if qtd_inicio != 1:
        return False, f"o mapa precisa ter exatamente um S (encontrados{qtd_inicio})",[]
    if qtd_objetivo != 1:
        return False, f"o mapa precisa ter exatamente um G (encontados{qtd_objetivo})",[]
    #retorna true a representacao da grade
    return True, "", linhas

#vai ser o responsavel por gerenciar a autorizacao e as permissoes do harness
class PoliticaHarness:
    algoritmos_permitidos = {"bfs", "ucs", "greedy", "astar", "dfs", "beam"}
    heuristicas_permitidas= {"zero", "manhattan", "manhattan_x2"}

    @classmethod
    def autorizar(cls, solicitacao: SolicitaBusca) -> Tuple[bool, str]:
        #allowlist verificacao
        if not isinstance(solicitacao.algoritmo, str) or solicitacao.algoritmo not in cls.algoritmos_permitidos:
            return False, f"Algoritmo '{solicitacao.algoritmo}' nao esta na lista de algoritmos autorizados"
        #heuristica validação
        if solicitacao.algoritmo in {"greedy", "astar", "beam"}:
            if(
                not isinstance (solicitacao.heuristica, str)
                or solicitacao.heuristica not in cls.heuristicas_permitidas
            ):
                return False, f"heuristica invalida '{solicitacao.heuristica}'"
        elif solicitacao.heuristica is not None and solicitacao.heuristica != "zero":
            if(
                not isinstance(solicitacao.heuristica, str)
                or solicitacao.heuristica not in cls.heuristicas_permitidas
            ):
                return False, f"heuristica desconhecida: '{solicitacao.heuristica}'"

        #beam search
        if solicitacao.algoritmo == "beam":
            if(
                solicitacao.largura_feixe is None
                or isinstance(solicitacao.largura_feixe, bool)
                or not isinstance(solicitacao.largura_feixe, int)
                or solicitacao.largura_feixe <= 0
            ):
                return False, f"a largura do feixe é invalida '{solicitacao.largura_feixe}'"

        #validar orcamentos e limites
        if(
            isinstance(solicitacao.max_expansoes, bool)
            or not isinstance (solicitacao.max_expansoes, int)
            or solicitacao.max_expansoes <= 0
        ):
            return False, f"Orcamento do maximo de expansoes invalido: {solicitacao.max_expansoes}"

        if(
            isinstance(solicitacao.tempo_limite_ms, bool)
            or not isinstance(solicitacao.tempo_limite_ms, (int, float))
            or solicitacao.tempo_limite_ms <= 0
        ):
            return False, f"orcamento do tempo limite invalido: {solicitacao.tempo_limite_ms}"

        #validar mapa
        mapa_valido, motivo_mapa, _ = valida_mapa(solicitacao.id_mapa)
        if not mapa_valido:
            return False, motivo_mapa
        return True, "Solicitação autorizada"
