import json
from pathlib import Path

# Pasta "data" ao lado deste arquivo, funciona  de qualquer pasta onde o programa for iniciado.
PASTA_DADOS = Path(__file__).parent / "data"

def ler(nome):
    caminho = PASTA_DADOS / f"{nome}.json"
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def buscar_tipologia(nome):
    tipologias = ler("tipologias")
    return tipologias.get(nome)

def buscar_cor(id_cor):
    cores = ler("cores")
    for cor in cores:
        if cor["id"] == id_cor:
            return cor
    return None

def buscar_perfil(linha, codigo):
    perfis = ler("perfis")
    lista_da_linha = perfis.get(linha, [])
    for perfil in lista_da_linha:
        if perfil["codigo"] == codigo:
            return perfil
    return None

def buscar_acessorio(linha, codigo):
    acessorios = ler("acessorios")
    lista_da_linha = acessorios.get(linha, [])
    for acessorio in lista_da_linha:
        if acessorio["codigo"] == codigo:
            return acessorio
    return None

def buscar_margem():
    return ler("margem")