import dados
import formulas

def calcular_perfis(tipologia, L, A, cor):
    linha = tipologia["linha"]
    peso_total = 0

    for item in tipologia["perfis"]:
        perfil = dados.buscar_perfil(linha, item["codigo"])
        if perfil is None:
            raise ValueError(f"Perfil não encontrado: {item ["codigo"]}")
        medida_m = formulas.avalias(item["medida"], L, A) / 1000