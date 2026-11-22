# Aula 01: variáveis e tipos

**Objetivo:** guardar valores com nome, entender os tipos básicos e fazer contas. No fim, você vai saber por que o resultado deu `3.8969999999999994` e não `3.897`.

---

## 1. Variável é uma etiqueta

Uma **variável** é um nome colado num valor. O `=` **não** significa "igual" como na matemática. Ele significa "guarde o valor da direita com o nome da esquerda".

```python
>>> largura = 1500
>>> altura = 1900
>>> largura
1500
```

Você pode trocar o valor depois. A etiqueta passa a apontar para o novo valor:

```python
>>> largura = 1200
>>> largura
1200
```

**Regras dos nomes:** letras minúsculas, números e `_`. Não podem começar com número, nem ter espaço ou acento (o Python até aceita acento, mas no projeto não usamos). Exemplos: `peso_total`, `medida_m`, `preco_quilo`.

Maiúsculas e minúsculas são diferentes: `L` e `l` são variáveis distintas.

---

## 2. Os tipos básicos

Todo valor tem um **tipo**. O comando `type()` mostra qual é:

| Tipo | Nome | Exemplo no projeto |
|---|---|---|
| `int` | número inteiro | `1500` (largura em mm), `qtd: 4` |
| `float` | número com vírgula (no Python é **ponto**) | `0.47` (peso por metro), `55.0` |
| `str` | texto ("string"), sempre entre aspas | `"BX1516"`, `"L / 2"` |
| `bool` | verdadeiro ou falso | `True`, `False` |
| `None` | "nada", ausência de valor | o que `buscar_cor(99)` devolve quando a cor não existe |

```python
>>> type(1500)
<class 'int'>
>>> type(0.47)
<class 'float'>
>>> type("BX1516")
<class 'str'>
>>> type(None)
<class 'NoneType'>
```

### Cuidado: `"1500"` não é `1500`

```python
>>> 1500 + 1
1501
>>> "1500" + 1
TypeError: can only concatenate str (not "int") to str
```

Com aspas é **texto**, e texto não se soma com número. É por isso que a fórmula `"L / 2"` precisa do `formulas.avaliar`: ela é texto e precisa ser transformada em conta.

Para converter: `int("1500")` vira `1500`, `float("0.47")` vira `0.47`, `str(1500)` vira `"1500"`.

---

## 3. Contas

| Operador | Faz | Exemplo | Resultado |
|---|---|---|---|
| `+` `-` `*` | soma, subtração, multiplicação | `1500 * 2` | `3000` |
| `/` | divisão (sempre dá `float`) | `1500 / 2` | `750.0` |
| `//` | divisão inteira (descarta a parte decimal) | `1500 // 1000` | `1` |
| `%` | resto da divisão | `1500 % 1000` | `500` |
| `**` | potência | `2 ** 3` | `8` |

A ordem é a da matemática: `*` e `/` antes de `+` e `-`. Use parênteses quando tiver dúvida.

```python
>>> largura = 1500
>>> largura_m = largura / 1000      # mm para metros
>>> largura_m
1.5
>>> peso_trilho = 1 * largura_m * 0.47     # qtd × metros × peso_metro
>>> peso_trilho
0.705
```

Esse é exatamente o cálculo de **um** perfil dentro da `calcular_perfis`.

### Atalhos: `+=`, `-=`, `*=`

```python
>>> peso_total = 0
>>> peso_total += 0.705     # o mesmo que: peso_total = peso_total + 0.705
>>> peso_total += 0.3
>>> peso_total
1.005
```

`+=` **soma ao que já existe**. Já `=` **substitui**. Essa diferença foi um dos erros na `calcular_perfis`.

---

## 4. O mistério do `3.8969999999999994`

```python
>>> 0.1 + 0.2
0.30000000000000004
```

Não é um erro do Python nem do seu código. O computador guarda números em binário, e alguns decimais (como 0,1) não têm representação exata em binário, assim como 1/3 não tem em decimal (0,3333...). Sobra um "resto" minúsculo.

**Solução:** arredondar **só no final**, na hora de mostrar o valor, com `round(valor, casas)`:

```python
>>> round(3.8969999999999994, 3)
3.897
>>> round(214.33499999999995, 2)
214.33
```

Por que só no final? Se você arredonda no meio das contas, o erro de cada arredondamento se acumula. É a regra do projeto: *"arredonda só no final"*, dentro do `orcar`.

---

## 5. Textos e f-strings

```python
>>> codigo = "BX1516"
>>> descricao = "Trilho Superior"
>>> codigo + " - " + descricao          # + junta textos
'BX1516 - Trilho Superior'
>>> len(codigo)                          # quantos caracteres
6
>>> descricao.upper()
'TRILHO SUPERIOR'
```

### f-string: colocar variáveis dentro do texto

Coloque um `f` antes das aspas e as variáveis entre `{ }`:

```python
>>> peso = 3.8969999999999994
>>> f"O box pesa {peso} kg"
'O box pesa 3.8969999999999994 kg'
>>> f"O box pesa {peso:.3f} kg"          # :.3f = 3 casas decimais
'O box pesa 3.897 kg'
>>> custo = 214.33499999999995
>>> f"Custo: R$ {custo:.2f}"
'Custo: R$ 214.33'
```

É isso que o `raise ValueError(f"Perfil não encontrado: {item['codigo']}")` faz.

> **Aspas dentro de f-string:** se o texto usa `"`, use `'` dentro das chaves: `f"... {item['codigo']}"`.

---

## 6. `print` × mostrar no `>>>`

No `python3` interativo, digitar só o nome mostra o valor. **Dentro de um arquivo `.py`**, nada aparece sem `print()`:

```python
>>> print("Peso:", 0.705, "kg")
Peso: 0.705 kg
```

---

## ✍️ Exercícios

Faça no `python3`. Antes de apertar Enter, **escreva sua previsão**.

**1.1** Crie as variáveis `L = 1500` e `A = 1900`. Calcule a **área do vão em m²** (largura em metros × altura em metros) e guarde em `area`. 
> Esperado: `2.85`
R: print(f"{area:.2f}") -> 2.8m²
R2: print(f"{area:.3f}") -> 2.85m²
R3: 
>>> L = 1500
>>> A = 1900
>>> L_metro = 1500 / 1000
>>> A_metro = 1900 / 1000
>>> area = L_metro / A_metro
>>> area 2.8499999999999996

**1.2** Qual o tipo de cada um? Preveja e depois confira com `type()`:
`1900`, `1.9`, `"1900"`, `1900 / 1000`, `1900 // 1000`, `None`, `True`
R: "int", "float", "string", "float", "int", "nonw", "boolean"
R2: "int", "float", "str", "float", "int", "NoneType", "bool"

**1.3** O box tem 4 montantes de altura `A` (BX1518, 0,17 kg/m). Usando `A = 1900`, calcule o peso dos 4 montantes em kg.
> Esperado: aproximadamente `1.292`
R: 1.292

**1.4** Comece com `peso_total = 0`. Some, **com `+=` e um por vez**, os pesos destes perfis do box (L=1500, A=1900):
- trilho superior: 1 × 1,5 m × 0,47
- trilho inferior: 1 × 1,5 m × 0,20
- laterais: 2 × 1,9 m × 0,20

> Esperado: por volta de `1.765` (pode aparecer um "resto" como `1.7650000000000001`)
R: 1,765
R2: 1.765

**1.5** O que acontece se, no exercício anterior, você usar `=` em vez de `+=`? Teste e explique com suas palavras.
R: Aparece o mesmo resultado pois eu separei os valores de cada perfil em variáveis, sendo ts para trilho superior, ti para trilho inferior e lt para laterias, e no fim como usei o peso_total = ts + ti + lt o resultado deu certo independente de usar += ou =.
R2: usando o += ele soma os valores sendo 0.705, 1.005 e 1.765 os valores respectvamente (rodei peso_total logo após += para testar) e rodando só com o = ele me retorna cada 0.705, 0.3 e 0.76, pois ele não soma mas sim substitui o valor do peso_total

**1.6** Usando f-string, monte o texto `Box 1500 x 1900 mm - 2.85 m²`, a partir das variáveis `L`, `A` e `area`.
R: print(f"Box {L} x {A} - {area}m²")
R2: print(f"Box {L} x {A} mm - {area/1000000} m²")
R3: print(f"Box {L} x {A} mm - {area:.2f} m²")
>>> print(f"Box {L} x {A} mm - {area} m²")
Box 1500 x 1900 mm - 2.8499999999999996 m²
>>> print(f"Box {L} x {A} mm - {area:.2f} m²")
Box 1500 x 1900 mm - 2.85 m²
>>>

**1.7** Preveja e depois teste. Qual dá erro e por quê?
```python
"BX" + "1516"
"BX" + 1516
"BX" + str(1516)
1500 + int("400")
```
R: o primeiro funciona pois é junção de string + string, o segundo não pois é string com int, o terceiro funciona pois é uma string + um int sendo convertido em string por str() bem como o quarto que é um int + uma string convertida em int pelo int().

**1.8** Arredonde `214.33499999999995` para 2 casas e `0.1 + 0.2` para 1 casa.
R: round(214.33499999999995, 2) e round((0.1 + 0.2), 1)
R2: Foi força do hábito de digitar o início com maiúscula, no python3 rodei com muníscula mesmo.

---

## ✅ Resumo

- `=` guarda um valor com um nome. `+=` soma ao valor que já existe.
- Tipos: `int`, `float`, `str`, `bool`, `None`. Texto (`"1500"`) não é número (`1500`).
- `/` sempre devolve `float`. `float` às vezes mostra "restos" como `0.30000000000000004`: arredonde só no final, com `round()`.
- f-string: `f"texto {variavel}"`. Use `{valor:.2f}` para fixar 2 casas.
