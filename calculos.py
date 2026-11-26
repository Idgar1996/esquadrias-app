import dados
import formulas

def calcular_perfis(tipologia, L, A, cor):
    linha = tipologia["linha"]
    peso_total = 0

    for item in tipologia["perfis"]:
        perfil = dados.buscar_perfil(linha, item["codigo"])
        if perfil is None:
            raise ValueError(f"Perfil não encontrado: {item['codigo']}")
        medida_m = formulas.avaliar(item["medida"], L, A) / 1000
        peso_total += medida_m * perfil["peso_metro"] * item["qtd"]
    valor_perfil = peso_total * cor["preco_quilo"]
    return {"peso_kg": peso_total, "custo": valor_perfil}

def calcular_acessorios(tipologia, L, A):
    linha = tipologia["linha"]
    valor_total = 0

    for item in tipologia["acessorios"]:
        acessorio = dados.buscar_acessorio(linha, item["codigo"])
        if acessorio is None:
            raise ValueError(f"Acessório não encontrado: {item['codigo']}")

        if "medida" in item:
            medida_m = formulas.avaliar(item["medida"], L, A) / 1000
            custo_item = item["qtd"] * medida_m * acessorio["valor"]
        else:
            custo_item = item["qtd"] * acessorio["valor"]
        valor_total += custo_item

    return {"custo": valor_total}

def calcular_chapas(tipologia, L, A):
    linha = tipologia["linha"]
    valor_total = 0

    for item in tipologia["chapas"]:
        chapa = dados.buscar_acessorio(linha, item["codigo"])

        if chapa is None:
            raise ValueError(f"Chapa não encontrada: {item['codigo']}")

        largura = formulas.avaliar(item["largura"], L, A)
        altura = formulas.avaliar(item["altura"], L, A)

        if largura > chapa["chapa_largura_maxima_mm"]:
            raise ValueError(f"Largura da folha ({largura:.0f}mm) maior que a largura padrão máxima {chapa['chapa_largura_maxima_mm']}mm!")
        if altura > chapa["chapa_altura_maxima_mm"]:
            raise ValueError(f"Altura da folha ({altura:.0f}mm) maior que a altura padrão máxima {chapa['chapa_altura_maxima_mm']}mm!")

        valor_total += item["qtd"] * chapa["valor"]

    return {"custo": valor_total}

def orcar(nome_tipologia, L, A, qtd=1, id_cor=None):
    tipologia = dados.buscar_tipologia(nome_tipologia)
    if tipologia is None:
        raise ValueError(f"Tipologia não encontrada: {nome_tipologia}")

    if id_cor is None:
        id_cor = tipologia["cor_padrao"]
    cor = dados.buscar_cor(id_cor)
    if cor is None:
        raise ValueError(f"Cor não encontrada: {id_cor}")

    margens = dados.buscar_margem()["margens_lucro"]

    perfis = calcular_perfis(tipologia, L, A, cor)
    acessorios = calcular_acessorios(tipologia, L, A)
    chapas = calcular_chapas(tipologia, L, A)
    valor_perfis = perfis["custo"] * margens["aluminio"]
    valor_acessorios = acessorios["custo"] * margens["acessorios"]
    valor_chapas = chapas["custo"] * margens["vidros"]

    subtotal = valor_perfis + valor_acessorios + valor_chapas
    valor_unitario = subtotal * margens["taxa_producao"]

    valor_total = valor_unitario * qtd

    return {
        "tipologia": tipologia["descricao"],
        "medidas": f"{L} X {A}",
        "cor": cor["nome"],
        "peso_kg": round(perfis["peso_kg"], 3),
        "perfis": round(valor_perfis, 2),
        "acessorios": round(valor_acessorios, 2),
        "chapas": round(valor_chapas, 2),
        "valor_unitario": round(valor_unitario, 2),
        "quantidade": qtd,
        "total": round(valor_total, 2)
    }