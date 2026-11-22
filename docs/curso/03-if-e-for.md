# Aula 03: `if`, `for` e o acumulador

**Objetivo:** tomar decisões (`if`) e repetir uma ação para cada item de uma lista (`for`). Juntando os dois com um **acumulador**, você tem o coração de todas as funções do `calculos.py`.

---

## 1. Comparações dão `True` ou `False`

| Operador | Significa | Exemplo | Resultado |
|---|---|---|---|
| `==` | igual (dois `=`!) | `9 == 9` | `True` |
| `!=` | diferente | `"m" != "un"` | `True` |
| `>` `<` `>=` `<=` | maior, menor... | `1960 > 900` | `True` |
| `is None` | é "nada"? | `perfil is None` | depende |
| `in` | está dentro? | `"Alpa" in fornecedores` | `True` |

> `=` **guarda** um valor. `==` **compara** dois valores. Confundir os dois é muito comum.

Para combinar comparações: `and` (as duas precisam ser verdade), `or` (basta uma) e `not` (inverte).

```python
>>> largura_folha = 750
>>> largura_folha > 900 or 1900 > 1960     # passou da chapa em alguma medida?
False
```

---

## 2. `if` / `elif` / `else`: decidir

```python
>>> unidade = "m"
>>> if unidade == "m":
...     print("cobra por metro")
... elif unidade == "un":
...     print("cobra por unidade")
... else:
...     print("unidade desconhecida")
...
cobra por metro
```

**Três regras de ouro:**
1. A linha do `if` termina com **`:`**.
2. O que pertence ao `if` fica **recuado** (4 espaços). O recuo **é** a sintaxe: é ele que diz o que está dentro e o que está fora.
3. `elif` e `else` são opcionais.

No projeto:

```python
if perfil is None:
    raise ValueError(f"Perfil não encontrado: {item['codigo']}")
```

Isso significa: "se a busca não achou nada, pare tudo com uma mensagem clara".

---

## 3. `for`: repetir para cada item

```python
>>> fornecedores = ["Aluita", "Alpa", "Fixasul"]
>>> for nome in fornecedores:
...     print("Comprar em:", nome)
...
Comprar em: Aluita
Comprar em: Alpa
Comprar em: Fixasul
```

Leia assim: **"para cada `nome` dentro de `fornecedores`, faça o bloco recuado"**. A variável `nome` muda a cada volta: primeiro `"Aluita"`, depois `"Alpa"` e por fim `"Fixasul"`. O nome dessa variável é você quem escolhe (`item`, `cor`, `x`...). Escolha um que diga o que ela é.

Com uma lista de dicionários, cada volta entrega **um dicionário inteiro**:

```python
>>> import dados
>>> box = dados.buscar_tipologia("box-acrilico-2f")
>>> for item in box["perfis"]:
...     print(item["codigo"], item["qtd"], item["medida"])
...
BX1516 1 L
BX1006 1 L
BX1517 2 A
BX507 2 L / 2
BX1518 4 A
BX1518 2 L
```

---

## 4. O acumulador: o padrão mais importante do curso

Para **somar** algo de todos os itens:

```python
total = 0                     # 1. ANTES do for: cria o acumulador zerado
for item in lista:            # 2. para cada item...
    total += item["qtd"]      # 3. DENTRO do for: SOMA ao que já tem (+=)
print(total)                  # 4. DEPOIS do for: usa o resultado
```

Os quatro passos, e **onde cada um fica**, são o que importa:

| Passo | Onde fica | Se errar... |
|---|---|---|
| `total = 0` | **antes** do `for` | se ficar dentro, zera a cada volta |
| `total += ...` | **dentro** do `for` | se usar `=`, só sobra o último item |
| usar o `total` | **depois** do `for` (recuo do `for`) | se ficar dentro, roda a cada volta, com o total incompleto |

Teste:

```python
>>> total = 0
>>> for item in box["perfis"]:
...     total += item["qtd"]
...
>>> total
12
```

### Fazendo a volta "na mão"

Para entender um `for`, coloque um `print` **dentro** dele e veja cada volta:

```python
>>> total = 0
>>> for item in box["perfis"]:
...     total += item["qtd"]
...     print(item["codigo"], "-> total até agora:", total)
...
BX1516 -> total até agora: 1
BX1006 -> total até agora: 2
BX1517 -> total até agora: 4
...
```

### `for` com `if` dentro: filtrar

```python
>>> cores = dados.ler("cores")
>>> for cor in cores:
...     if cor["preco_quilo"] > 55:
...         print(cor["nome"])
...
Amadeirado
Anodizado Brilhante
```

Repare nos **dois níveis de recuo**: o `if` está dentro do `for`, e o `print` está dentro do `if`.

---

## ✍️ Exercícios

No `python3`, com `import dados`, `box = dados.buscar_tipologia("box-acrilico-2f")` e `cores = dados.ler("cores")`.

**3.1** Faça um `for` que imprima **o nome e o preço** de cada cor, no formato `Branco Brilhante: R$ 49.00` (use f-string com `:.2f`).

**3.2** Conte **quantas** cores custam exatamente 55,00 o quilo. Use um acumulador que começa em `0` e faz `+= 1`.
> Esperado: `4`

**3.3** Encontre a cor **mais cara**. Dica: comece com `mais_cara = cores[0]` e, dentro do `for`, troque por `cor` se ela custar mais que a `mais_cara` atual.
> Esperado: `Amadeirado` (78.0)

**3.4** Some os **metros totais** de perfil do box com L = 1500 e A = 1900. Para cada item, use `formulas.avaliar(item["medida"], L, A) / 1000` (com `import formulas`) e multiplique pela `qtd`.
> Esperado: `18.9` (ou algo como `18.900000000000002`)

**3.5** Percorra `box["acessorios"]` e some a `qtd` **só** dos itens que **não** têm a chave `"medida"`. Dica: `"medida" not in item`.
> Esperado: `13`

**3.6** Uma folha do box tem largura `L / 2` e altura `A`. A chapa PET mede 900 × 1960 mm. Faça um `if` que imprima `"ALERTA: folha maior que a chapa"` se a folha passar da chapa em alguma das medidas, ou `"OK"` caso contrário. Teste com:
- L = 1500, A = 1900 → esperado: `OK`;
- L = 2000, A = 1900 → esperado: `ALERTA`;
- L = 1500, A = 2000 → esperado: `ALERTA`.

**3.7** O código abaixo tem **dois** erros de posição. Ache-os sem rodar e depois rode para confirmar:
```python
for item in box["perfis"]:
    total = 0
    total += item["qtd"]
    print("Total:", total)
```
> O certo é imprimir uma única linha: `Total: 12`

---

## ✅ Resumo

- `==` compara e `=` guarda. `and`, `or` e `not` combinam comparações.
- `if`, `for` e `def` terminam com `:` e o bloco **recuado** pertence a eles.
- `for x in lista:` roda o bloco uma vez para cada item.
- **Acumulador:** zera **antes**, soma com `+=` **dentro** e usa **depois**.
- Na dúvida, coloque um `print` dentro do `for` e assista às voltas.
