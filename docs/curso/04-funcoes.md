# Aula 04: funções

**Objetivo:** criar suas próprias funções e entender **parâmetros**, **`return`** e **escopo** (onde uma variável existe). Foram os três pontos que travaram a `calcular_perfis`.

---

## 1. Para que serve uma função

Uma função é uma **receita com nome**: você escreve uma vez e usa quantas vezes quiser, com ingredientes diferentes.

```python
def area_m2(L, A):
    return (L / 1000) * (A / 1000)
```

- `def`: "vou definir uma função".
- `area_m2`: o nome dela.
- `(L, A)`: os **parâmetros**, os "ingredientes" que ela recebe.
- `return ...`: o **resultado** que ela devolve para quem chamou.

**Definir** não executa nada. A função só roda quando é **chamada**:

```python
>>> area_m2(1500, 1900)
2.85
>>> area_m2(1000, 2100)
2.1
```

Na chamada, os valores entram nos parâmetros **pela ordem**: `1500` vai para `L` e `1900` vai para `A`.

> **Para digitar uma função no `python3`:** depois do `def`, cada linha começa com `...` e precisa do recuo (4 espaços). Para terminar, aperte Enter numa linha vazia.

---

## 2. `return` × `print`: a diferença mais importante

```python
def com_print(L, A):
    print((L / 1000) * (A / 1000))

def com_return(L, A):
    return (L / 1000) * (A / 1000)
```

```python
>>> x = com_print(1500, 1900)
2.85                    # MOSTROU na tela...
>>> print(x)
None                    # ...mas não DEVOLVEU nada!
>>> y = com_return(1500, 1900)
>>> y * 2               # o valor voltou e dá para usar em outra conta
5.7
```

- `print` **mostra** o valor para você ver. Esse valor não volta para o código.
- `return` **devolve** o valor para quem chamou. É assim que o `orcar` vai conseguir usar o resultado da `calcular_perfis`.
- Uma função **sem `return`**, ou com um `return` vazio, devolve `None`.

### O `return` encerra a função na hora

```python
def exemplo():
    return 1
    print("isso nunca aparece")     # código morto
    return 2
```

```python
>>> exemplo()
1
```

Foi o que aconteceu com o `return peso_total` no meio da `calcular_perfis`: o cálculo do custo, que vinha depois dele, nunca rodava.

### Devolvendo vários valores: use um dicionário

```python
def peso_e_custo(peso, preco_quilo):
    custo = peso * preco_quilo
    return {"peso_kg": peso, "custo": custo}
```

```python
>>> r = peso_e_custo(3.897, 55.0)
>>> r["custo"]
214.335
```

---

## 3. Escopo: onde uma variável existe

As variáveis criadas **dentro** de uma função são **locais**: elas nascem quando a função começa e somem quando ela termina.

```python
def calcula():
    peso_final = 10
    return peso_final * 2
```

```python
>>> calcula()
20
>>> peso_final
NameError: name 'peso_final' is not defined
```

Era isso que acontecia na última linha antiga do `calculos.py`: `peso_final` e `valor_perfil` só existiam **dentro** da função.

**Como tirar um valor de dentro da função?** Só pelo `return`. E quem chamou guarda o resultado numa variável:

```python
>>> resultado = calcula()
>>> resultado
20
```

### Parâmetros também são locais

```python
def dobra(valor):
    valor = valor * 2
    return valor
```

```python
>>> x = 5
>>> dobra(x)
10
>>> x          # o x de fora não mudou
5
```

---

## 4. Use o que você já recebeu

Se um dado **já chegou** como parâmetro, use-o direto. Não busque de novo:

```python
# ❌ cor já É a cor completa; buscar de novo é errado (e procura o id 55.0)
def custo_aluminio(peso, cor):
    return peso * dados.buscar_cor(cor["preco_quilo"])

# ✅
def custo_aluminio(peso, cor):
    return peso * cor["preco_quilo"]
```

Antes de escrever uma linha, pergunte: **"esse dado eu já tenho em alguma variável?"**

---

## 5. Valor padrão de parâmetro

```python
def aplicar_margem(valor, margem=1.85):
    return valor * margem
```

```python
>>> aplicar_margem(100)          # usa o padrão 1.85
185.0
>>> aplicar_margem(100, 1.70)    # ou o que você passar
170.0
```

Também dá para passar o parâmetro **pelo nome**, em qualquer ordem: `aplicar_margem(margem=1.75, valor=100)`.

---

## 6. Lendo a `calcular_perfis` com olhos novos

```python
def calcular_perfis(tipologia, L, A, cor):        # recebe 4 ingredientes
    linha = tipologia["linha"]                    # variável local
    peso_total = 0                                # acumulador (antes do for)

    for item in tipologia["perfis"]:              # cada linha da receita
        perfil = dados.buscar_perfil(linha, item["codigo"])   # ponte pelo código
        if perfil is None:
            raise ValueError(f"Perfil não encontrado: {item['codigo']}")
        medida_m = formulas.avaliar(item["medida"], L, A) / 1000
        peso_total += item["qtd"] * medida_m * perfil["peso_metro"]   # soma (dentro)

    custo = peso_total * cor["preco_quilo"]       # depois do for
    return {"peso_kg": peso_total, "custo": custo}   # um único return, no fim
```

Agora todos os conceitos estão aí: parâmetros, variáveis locais, acumulador, `if`, `for`, dicionários e `return`.

---

## ✍️ Exercícios

Crie o arquivo `treino_aula4.py` na raiz do projeto. Escreva as funções nele e, no final do arquivo, as chamadas com `print(...)`. Rode com `python3 treino_aula4.py`.

**4.1** Escreva `area_m2(L, A)`, que devolve a área em m².
> `print(area_m2(1500, 1900))` → `2.85`

**4.2** Escreva `mm_para_m(valor_mm)`. Depois reescreva a `area_m2` **usando** a `mm_para_m`. Funções podem chamar outras funções.

**4.3** Escreva `aplicar_margem(valor, margem)`, que devolve `valor × margem`.
> `print(aplicar_margem(214.335, 1.85))` → aproximadamente `396.52`

**4.4** Escreva `preco_da_cor(id_cor)`, que usa `dados.buscar_cor` e devolve **só o preço do quilo**. Se a cor não existir, deve levantar `ValueError("Cor não encontrada: 99")`, com o id certo na mensagem.
> `preco_da_cor(9)` → `55.0`; `preco_da_cor(99)` → erro com a mensagem

**4.5** Escreva `total_de_pecas(tipologia)`, que devolve a soma das `qtd` dos perfis. É o exercício 3.4 da Aula 03, agora dentro de uma função.
> Com o box → `12`

**4.6** Escreva `folha_cabe_na_chapa(L, A)`, que devolve `True` se uma folha (`L / 2` × `A`) cabe numa chapa de 900 × 1960, e `False` se não cabe.
> `(1500, 1900)` → `True`; `(2000, 1900)` → `False`

**4.7** Sem rodar, diga o que cada `print` mostra. Depois confira:
```python
def f1(x):
    print(x * 2)

def f2(x):
    return x * 2

def f3(x):
    return x * 2
    return x * 3

print(f1(5))
print(f2(5))
print(f3(5))
```

**4.8** Este código dá erro. Diga qual é e por quê, depois conserte **sem** usar variáveis fora da função:
```python
def calcula_custo(peso, preco):
    custo = peso * preco

calcula_custo(3.897, 55.0)
print(custo)
```

---

## ✅ Resumo

- `def nome(parametros):` define, e `nome(valores)` executa.
- `return` **devolve** e encerra a função. `print` só **mostra**. Sem `return`, a função devolve `None`.
- Para devolver várias coisas, use um dicionário.
- Variáveis de dentro da função **não existem fora** dela. O único caminho para fora é o `return`.
- Se o dado já chegou num parâmetro, use-o direto. Não busque de novo.
