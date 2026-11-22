# Aula 05: módulos, erros e depuração

**Objetivo:** entender como os arquivos do projeto conversam entre si (`import`), **ler uma mensagem de erro sozinho** e investigar um problema com `print`. No fim, o **desafio final** é a próxima parte do projeto.

---

## 1. Módulo é um arquivo `.py`

Cada arquivo `.py` é um **módulo**. O `import` carrega um módulo e dá acesso ao que tem dentro, usando `nome_do_modulo.coisa`:

```python
>>> import dados
>>> dados.buscar_cor(9)
{'id': 9, 'nome': 'Anodizado Fosco', 'preco_quilo': 55.0}
```

No projeto, cada arquivo tem uma função:

```
dados.py      → lê os JSON              (só ele abre arquivos)
formulas.py   → transforma "L / 2" em número
calculos.py   → usa os dois acima para fazer as contas
app.py        → (futuro) usa o calculos.py e responde ao navegador
```

### O que roda no `import`?

**Tudo o que está sem recuo** no arquivo é executado no momento do `import`. Normalmente isso é só `import`, `def` e constantes. Definir uma função não a executa.

Por isso uma linha solta no fim do `calculos.py`, como `dados = calcular_perfis(...)`, quebrava o `import calculos`: ela **rodava** na hora do import. Além disso, a variável `dados` ia **sobrescrever o módulo** `dados`.

> **Regra:** no arquivo do módulo ficam as **definições**. Os **testes** ficam no `python3` (ou num `treino_*.py`).

### Mudou o arquivo? Recarregue

O `python3` carrega o módulo **uma vez só**. Se você editar o `.py` com o `python3` aberto, ele continua usando a versão antiga. Há duas saídas:

```python
>>> exit()          # sai, depois abre de novo e repete os imports
```

ou

```python
>>> import importlib
>>> importlib.reload(calculos)
```

> Se aparecer `AttributeError: module 'x' has no attribute 'y'` para uma função que você **acabou de criar**, quase sempre falta recarregar.

---

## 2. Lendo um erro (traceback)

Quando algo dá errado, o Python mostra um **traceback**. Ele parece assustador, mas tem só três partes:

```
Traceback (most recent call last):
  File "<python-input-4>", line 1, in <module>
    calculos.calcular_perfis(box, 1500, 1900, cor)
  File "/home/gean/esquadrias-app/calculos.py", line 15, in calcular_perfis
    peso_total += medida_m * perfil["peso_metro"] * perfil["qtd"]
                                                    ~~~~~~^^^^^^^
KeyError: 'qtd'
```

**Leia de baixo para cima:**

1. **A última linha diz O QUÊ:** `KeyError: 'qtd'`, ou seja, foi pedida a chave `qtd` a um dicionário que não a tem.
2. **O bloco logo acima diz ONDE:** o arquivo `calculos.py`, a **linha 15**, na função `calcular_perfis`. Os `^^^^` apontam o pedaço exato: `perfil["qtd"]`.
3. **O que vem antes é o caminho** até lá: quem chamou quem.

### Os erros que você mais vai ver

| Erro | Significa | Exemplo real deste projeto |
|---|---|---|
| `NameError: name 'x' is not defined` | esse nome não existe **aqui** | `peso_final` usado fora da função, ou faltou o `import` |
| `AttributeError: module 'dados' has no attribute 'bucar_cor'` | o módulo não tem esse nome | erro de digitação (o Python até sugere: *Did you mean: 'buscar_cor'?*) ou faltou recarregar |
| `KeyError: 'qtd'` | o dicionário não tem essa chave | `perfil["qtd"]` em vez de `item["qtd"]` |
| `IndexError: list index out of range` | posição além do fim da lista | `cores[9]` numa lista de 9 itens |
| `TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'` | conta com `None` | `buscar_perfil` não achou nada e você multiplicou o resultado |
| `TypeError: ... takes 4 positional arguments but 1 was given` | número errado de argumentos | `calcular_perfis([...])` |
| `SyntaxError` / `IndentationError` | o código está mal escrito: falta `:`, `)` ou aspas, ou o recuo está errado | aparece antes de rodar qualquer coisa |
| `ValueError: Fórmula inválida: ...` | erro **nosso**, criado com `raise` | `formulas.avaliar("L +", ...)` |

> **Um `TypeError` com `NoneType`** quase sempre quer dizer que uma busca não achou nada **algumas linhas antes**. Procure qual `buscar_...` devolveu `None`.

---

## 3. Levantando seus próprios erros: `raise`

Quando o seu código detecta uma situação impossível, é melhor **parar com uma mensagem clara** do que seguir e dar um erro confuso depois:

```python
if perfil is None:
    raise ValueError(f"Perfil não encontrado: {item['codigo']}")
```

E para **tratar** um erro em vez de deixar o programa quebrar, use `try` / `except`, como o `formulas.py` faz:

```python
>>> import formulas
>>> try:
...     formulas.avaliar("L +", 1500, 1900)
... except ValueError as erro:
...     print("Deu problema:", erro)
...
Deu problema: Fórmula inválida: L + (...)
```

O `try`/`except` vai ser usado no `app.py`, para mostrar o erro ao usuário em vez de derrubar o servidor.

---

## 4. Depurando: investigar em vez de adivinhar

Quando o resultado sai **errado, mas sem erro nenhum**, siga este roteiro:

1. **Calcule um caso na mão.** Ex.: trilho superior, 1 × 1,5 m × 0,47 = **0,705 kg**.
2. **Coloque `print` dentro do `for`** para ver cada volta:
   ```python
   print("item:", item)
   print("perfil:", perfil)
   print("medida_m:", medida_m, "peso_total:", peso_total)
   ```
3. **Compare** a primeira volta com a sua conta à mão. O primeiro número diferente mostra onde está o erro.
4. **Apague os `print`** de investigação quando terminar.

Também ajuda ir direto ao `python3` e testar **um pedaço** isolado:

```python
>>> item = box["perfis"][0]
>>> item.keys()                 # o que tem aqui?
>>> formulas.avaliar(item["medida"], 1500, 1900)
1500
```

---

## ✍️ Exercícios

**5.1** Para cada traceback, diga **o que** deu errado, **em qual linha** e **como você corrigiria**:

a)
```
  File "/home/gean/esquadrias-app/calculos.py", line 24, in <module>
    dados = calcular_perfis([peso_final, valor_perfil ])
NameError: name 'peso_final' is not defined
```
b)
```
  File "/home/gean/esquadrias-app/calculos.py", line 12, in calcular_perfis
    medida_m = formulas.avalias(item["medida"], L, A) / 1000
AttributeError: module 'formulas' has no attribute 'avalias'. Did you mean: 'avaliar'?
```
c)
```
  File "/home/gean/esquadrias-app/calculos.py", line 15, in calcular_perfis
    peso_total = medida_m * dados.buscar_perfil(linha, item["qtd"]) * ...
TypeError: unsupported operand type(s) for *: 'float' and 'NoneType'
```

**5.2** Provoque de propósito, no `python3`, um exemplo de cada erro: `NameError`, `KeyError`, `IndexError`, `TypeError` e `SyntaxError`. Leia a mensagem de cada um.

**5.3** Escreva um `try`/`except` que tente `formulas.avaliar("L / 0", 1500, 1900)` e, se der `ValueError`, imprima `Fórmula com problema` em vez de quebrar.

**5.4** Abra o `python3`, importe o `calculos`, adicione um `print` dentro do `for` da `calcular_perfis` (no arquivo) e chame a função **sem** sair do `python3`. O `print` aparece? Por quê? Faça aparecer com o `importlib.reload`. Depois **apague** o `print`.

**5.5** Sem olhar o arquivo, desenhe (em papel ou em texto) quem importa quem entre `dados.py`, `formulas.py` e `calculos.py`. Depois confira com as primeiras linhas de cada arquivo.

---

## 🏁 Desafio final: a Parte 2 do projeto

Agora você tem tudo o que precisa para escrever **sozinho** a próxima função do `calculos.py`:

**`calcular_acessorios(tipologia, L, A)`**
- Percorre `tipologia["acessorios"]`.
- Para cada item, busca o acessório com `dados.buscar_acessorio(linha, codigo)`. Se não achar, levanta `ValueError`.
- Se a `unidade` do acessório for `"m"` (a borracha), o custo é `qtd × medida_em_metros × valor`. A medida vem da fórmula do item, que é avaliada pelo `formulas.avaliar`.
- Senão, o custo é `qtd × valor`.
- Soma tudo num acumulador e devolve `{"custo": ...}`, **sem margem**.

**Teste:**
```python
>>> import importlib, dados, calculos
>>> box = dados.buscar_tipologia("box-acrilico-2f")
>>> calculos.calcular_acessorios(box, 1500, 1900)
{'custo': 83.24}            # pode aparecer com "restos", como 83.24000000000001
```

Para conferir parte por parte, estes são os custos de cada item com 1500 × 1900:

| Código | Unidade | Custo |
|---|---|---|
| NYL3280000 | un | 0,40 |
| ROL260 FIXA | un | 2,72 |
| PUX154 | un | 1,32 |
| NYL3270000 | un | 0,56 |
| 003-73x9 (4 × L) | m | 32,40 |
| 003-73x9 (4 × A) | m | 41,04 |
| NYL590 | un | 4,80 |

Pergunte-se em cada linha: **"esse dado está no `item` ou no `acessorio`?"** (dica: `unidade` e `valor` estão no `acessorio`; `qtd` e `medida` estão no `item`).

---

## ✅ Resumo

- Cada `.py` é um módulo. O `import` executa **tudo o que está sem recuo** no arquivo, por isso não deixe chamadas soltas lá.
- Editou o arquivo? `exit()` e entre de novo, ou `importlib.reload(modulo)`.
- Traceback: leia **de baixo para cima**. A última linha diz **o quê**, o bloco acima diz **onde**.
- Um `TypeError` com `None` geralmente vem de uma busca que não achou nada.
- Resultado errado sem erro? Faça a conta na mão e use `print` dentro do `for` para comparar.
