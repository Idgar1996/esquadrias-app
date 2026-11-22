# Aula 02: listas e dicionários

**Objetivo:** entender as duas "caixas" que guardam vários valores. Os arquivos JSON do projeto são feitos só delas. Saber **o que tem dentro de cada caixa** evita o `KeyError` e o `buscar_...` desnecessário.

---

## 1. Lista: valores em fila, acessados pela posição

Uma lista é escrita com `[ ]`. Os itens são separados por vírgula:

```python
>>> fornecedores = ["Aluita", "Alpa", "Fixasul"]
>>> fornecedores[0]          # a contagem começa no ZERO
'Aluita'
>>> fornecedores[2]
'Fixasul'
>>> fornecedores[-1]         # -1 = o último
'Fixasul'
>>> len(fornecedores)        # quantos itens
3
```

Acessar uma posição que não existe dá erro:

```python
>>> fornecedores[3]
IndexError: list index out of range
```

### Mexendo na lista

```python
>>> fornecedores.append("Vedugal")      # adiciona no fim
>>> fornecedores
['Aluita', 'Alpa', 'Fixasul', 'Vedugal']
>>> "Alpa" in fornecedores               # está na lista?
True
```

---

## 2. Dicionário: valores com etiqueta, acessados pela chave

Um dicionário é escrito com `{ }` e guarda pares **chave: valor**. Ele é a "ficha" de alguma coisa:

```python
>>> cor = {"id": 9, "nome": "Anodizado Fosco", "preco_quilo": 55.0}
>>> cor["nome"]
'Anodizado Fosco'
>>> cor["preco_quilo"]
55.0
```

Na **lista** você pergunta "qual o item da **posição** 2?". No **dicionário** você pergunta "qual o valor da **chave** `nome`?".

### O erro mais comum: `KeyError`

```python
>>> cor["qtd"]
KeyError: 'qtd'
```

Esse erro quer dizer "esse dicionário **não tem** essa chave". Foi o erro do `perfil["qtd"]`: o `qtd` existe na **tipologia**, não no **perfil**.

Para ver as chaves que um dicionário tem:

```python
>>> cor.keys()
dict_keys(['id', 'nome', 'preco_quilo'])
>>> "qtd" in cor
False
```

### `.get()`: buscar sem quebrar

```python
>>> cor.get("qtd")              # se não existir, devolve None em vez de dar erro
>>> cor.get("qtd", 0)           # ou o valor padrão que você escolher
0
```

O `dados.buscar_tipologia` usa `tipologias.get(nome)`. Por isso ele devolve `None` quando o nome não existe, em vez de quebrar.

### Mudando e adicionando

```python
>>> cor["preco_quilo"] = 58.0           # muda uma chave que já existe
>>> cor["fornecedor"] = "Aluita"        # cria uma chave nova
```

---

## 3. Caixas dentro de caixas: o JSON do projeto

A estrutura dos dados do projeto é sempre uma destas três:

- **uma lista de dicionários**: `cores.json` (uma lista de fichas de cor);
- **um dicionário de listas de dicionários**: `perfis.json` (`linha` → lista de fichas de perfil);
- **um dicionário de dicionários**: `tipologias.json` (`nome` → ficha da tipologia, que dentro tem listas).

Para chegar num valor, você vai "descendo" um nível de cada vez, um `[ ]` por nível.

```python
>>> import dados
>>> cores = dados.ler("cores")          # lista
>>> cores[0]                            # dicionário (a 1ª cor)
{'id': 1, 'nome': 'Branco Brilhante', 'preco_quilo': 49.0}
>>> cores[0]["nome"]                    # texto
'Branco Brilhante'
```

Agora a tipologia. Desça **um nível de cada vez** e olhe o que aparece:

```python
>>> box = dados.buscar_tipologia("box-acrilico-2f")
>>> box.keys()
dict_keys(['descricao', 'linha', 'cor_padrao', 'imagem', 'perfis', 'acessorios', 'chapas'])
>>> box["linha"]
'linha-box-acrilico'
>>> box["perfis"]          # uma LISTA de dicionários
>>> box["perfis"][0]       # o 1º dicionário da lista
{'codigo': 'BX1516', 'qtd': 1, 'medida': 'L', 'posicao': 'Trilho superior'}
>>> box["perfis"][0]["qtd"]
1
```

### Dois dicionários diferentes sobre o mesmo perfil

Este é **o** ponto que causou os erros na `calcular_perfis`:

| De onde vem | Exemplo | O que tem |
|---|---|---|
| A **tipologia** (`box["perfis"][0]`), o que chamamos de `item` | `{'codigo': 'BX1516', 'qtd': 1, 'medida': 'L', 'posicao': ...}` | **quanto** e **qual medida** usar **neste produto** |
| O **perfis.json** (`dados.buscar_perfil(...)`), o que chamamos de `perfil` | `{'codigo': 'BX1516', 'descricao': ..., 'peso_metro': 0.47, ...}` | **o que o perfil é**: peso, fornecedores e imagem |

O `codigo` é a **ponte** entre os dois: com o código que vem do `item`, você busca o `perfil`.

> **Pergunta para fazer sempre:** "o dado que eu preciso está em qual dicionário?". Na dúvida, dê `print(item)` e `print(perfil)` e olhe.

---

## ✍️ Exercícios

Todos no `python3`, dentro de `~/esquadrias-app`, começando com `import dados`.

**2.1** Carregue `cores = dados.ler("cores")`. Descubra:
- quantas cores existem (esperado: `9`);
R:
>>> import dados
>>> dados #Esse só rodei para ver o que aparece
<module 'dados' from '/home/gean/esquadrias-app/dados.py'>
>>> cores = dados.ler("cores")
>>> len(cores)
9
>>>
- o nome da primeira e o da última cor (esperado: `Branco Brilhante` e `Anodizado Fosco`);
R: 
>>> cores[0]["nome"]
'Branco Brilhante'
>>> cores[8]["nome"]
'Anodizado Fosco'
>>>

- o `preco_quilo` da cor na posição 5. Antes de testar, preveja qual cor é.
R:
>>>>cores[5]["preco_quilo"]
78.0
>>>>cores[5]
'Amadeirado' ( a cor na posição 5 corresponde a 6a cor na lista)


**2.2** Carregue `margem = dados.ler("margem")`. Que comando mostra a margem de **vidros**? E o **valor por km**?
> Esperado: `1.75` e `1.5`
R:
>>> margem["margens_lucro"]["vidros"]
1.75
>>> margem["custos"]["valor_por_km"]
1.5

**2.3** Com `box = dados.buscar_tipologia("box-acrilico-2f")`, chegue nestes valores, cada um numa única linha:
- a `medida` da travessa (4º perfil). Esperado: `'L / 2'`;
R:
>>> box["perfis"][3]["medida"]
'L / 2'

- a `qtd` das cantoneiras NYL590 (último acessório). Esperado: `8`;
R:
>>> box["acessorios"][6]["qtd"]
8
R2:
>>> box["linha-box-acrilico"][-1]
{'codigo': 'NYL590', 'descricao': 'Cantoneira de montagem das folhas', 'valor': 0.6, 'fornecedores': ['Aluita'], 'unidade': 'un'}
>>>

- a `largura` da chapa (1º item de `chapas`). Esperado: `'L / 2'`.
R:
box["chapas"][0]["largura"]
'L / 2'

**2.4** Monte, **à mão**, o dicionário de uma cor nova: id 10, nome "Preto Brilhante", preço 53.0. Depois mude o preço para 54.0 e acrescente a chave `"fornecedor"` com o valor `"Aluita"`. Imprima o dicionário.
R:
>>> cores.append({"id": 10, "nome":"Preto Brilhante", "preco":53.0})
>>> cores[9]["preco"]=54.0
>>> cores[9]
{'id': 10, 'nome': 'Preto Brilhante', 'preco': 54.0}
#não consegui adicionar o fornecedor nem mudar "preco" para "preco_por_quilo"
R2:
>>> cores = dados.ler("cores")
>>> cores.append({"id": "10", "nome" : "Preto Brilhante", "preco_quilo": 53.0})
>>> cores[9]["preco_quilo"]
53.0
>>> cores[9]["preco_quilo"]=53.0
>>> cores[9]
{'id': '10', 'nome': 'Preto Brilhante', 'preco_quilo': 53.0}
>>> cores[9]["fornecedor"]="Aluita"
>>> cores[9]
{'id': '10', 'nome': 'Preto Brilhante', 'preco_quilo': 53.0, 'fornecedor': 'Aluita'}

**2.5** Sem testar, diga qual dá erro e qual erro é. Depois confira:
```python
cores[9]
cores[0]["preco"]
cores[0].get("preco")
box["perfis"]["qtd"]
```
> Dica para o último: `box["perfis"]` é uma lista ou um dicionário?
R: o segundo, NameError, pois não tem "preco" e sim "preco_por_quilo" bem como o terceiro. o box["perfis"] é um dicionario.
R2: O segundo é TypeError, o get retorna None, O box["perfis"] é uma lista e o erro que da é o IndexError. O cores[9] da o erro NameError

**2.6** Com `perfil = dados.buscar_perfil("linha-box-acrilico", "BX1516")` e `item = box["perfis"][0]`, escreva a conta do peso desse trilho com L = 1500, pegando **cada número do dicionário certo** (`item["qtd"]`, `perfil["peso_metro"]`).
> Esperado: `0.705`
>>>>
>>> perfil = dados.buscar_perfil("linha-box-acrilico", "BX1516")
>>> perfil
{'codigo': 'BX1516', 'descricao': 'Trilho Superior', 'peso_metro': 0.47, 'fornecedores': ['Aluita', 'Alpa', 'Fixasul'], 'unidade': 'kg/m', 'imagem': 'BX1516.png'}
>>> peso_metro = perfil["peso_metro"]
>>> peso_metro
0.47
>>> item = dados.buscar_tipologia("box-acrilico-2f")
>>> perfil = item["perfis"]
>>> qtd_perfil = perfil[1]["qtd"]
>>> qtd_perfil
1
>>> L = 1500
>>> L_mm = 1500 / 1000
>>> calculo = L_mm * qtd_perfil * peso_metro
>>> calculo
0.705

**2.7** Por que `dados.buscar_perfil("linha-box-acrilico", 1)` devolve `None`? Responda com suas palavras.
R: pois não foi definida nenhuma variável à qual o valor buscado fosse atribuido
---

## ✅ Resumo

- **Lista** `[ ]`: itens em ordem, acessados pela **posição** (começa em 0). Erro típico: `IndexError`.
- **Dicionário** `{ }`: pares chave → valor, acessados pela **chave**. Erro típico: `KeyError`. Use `.keys()` para ver as chaves e `.get()` para buscar sem quebrar.
- No JSON, desça **um `[ ]` por nível**.
- `item` (da tipologia) diz **quanto** usar; `perfil` (do perfis.json) diz **o que é**. O `codigo` liga os dois.
