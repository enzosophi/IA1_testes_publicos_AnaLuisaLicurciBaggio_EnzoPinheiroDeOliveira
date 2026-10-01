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

def valida_mapa(caminho_mapa: str) -> Tuple[bool, str,list[str]]:
    """a integridade do arquivo do mapa é considerada aplicada se o arquivo existir
    se o mapa não estiver vazio e suas linhas tiverem a mesma largura, se conter exatamente um inicio S e um objetivo G e se os caracteres forem validos (como S, G, ., #, 1-9)"""

    if not os.path.exists(caminho_mapa):
        return False, f"arquivo nao encontrado: {caminho_mapa}", []

        try:
            with open(caminho_mapa, "r", encoding="utf-8") as arquivo:
                linhas = [linha.rstrip("\r\n") for linha in arquivo.readlines()]
        except Exception as erro:
            return False, f"erro ao ler o arquivo: {erro}", []

    if not linhas or all(len(linha)==0 for linha in linhas):
        return False, "O mapa esta vazio",[]

    larg_esperada = len(linhas[0])
    qtd_inicio = 0
    qtd_objetivo = 0
    caracteres_validos = set("SG.#123456789")

    for indice_linha, linha in enumerate(linhas):
        if len(linha) != larg_esperada:
            return False, f"A linha {indice_linha} nao possui uma largura compativel",[]
        for caracter in linha:
            if caracter not in caracteres_validos:
                return False, f"caracter invalido '{caracter}'enconotrado no mapa", []
            if caracter == "S":
                qtd_inicio += 1
            elif caracter == "G":
                qtd_objetivo += 1

    if qtd_inicio != 1:
        return False, f"o mapa precisa ter exatamente um S (encontrados{qtd_inicio})",[]
    if qtd_objetivo != 1:
        return False, f"o mapa precisa ter exatamente um G (encontados{qtd_objetivod})",[]

    return True, "", linhas