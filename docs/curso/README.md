# Mini-curso de Python: do zero ao `calculos.py`

Curso curto, feito com os dados do **próprio projeto** (box, perfis, cores, margens). Ele parte do zero: não precisa saber nada de Python.

## As aulas

| Aula | Assunto | Por que importa no projeto |
|---|---|---|
| [01](01-variaveis-e-tipos.md) | Variáveis, números, textos, `None` | Toda conta do orçamento usa isso. Explica o `3.8969999999999994` |
| [02](02-listas-e-dicionarios.md) | Listas e dicionários | Os JSON viram listas e dicionários. Resolve o `KeyError` |
| [03](03-if-e-for.md) | `if`, `for` e acumulador | Percorrer os perfis e somar os pesos (`+=`) |
| [04](04-funcoes.md) | Funções: parâmetros, `return`, escopo | Cada parte do `calculos.py` é uma função |
| [05](05-modulos-e-erros.md) | `import`, ler erros, depurar com `print` | Entender o traceback sozinho. Termina com o **desafio final** |

Faça na ordem. Cada aula leva de 30 a 60 minutos.

## Como estudar

1. **Leia a explicação** e **digite** os exemplos no `python3`, sem copiar e colar. Digitar é o que fixa.
2. Antes de apertar Enter, **tente prever** o resultado. Se errar a previsão, foi ali que você aprendeu algo.
3. Faça os **exercícios**. Muitos têm o resultado esperado, para você conferir sozinho.
4. Errou? **Leia a última linha do erro** antes de pedir ajuda (a Aula 5 ensina isso).

### Preparando o terminal

```bash
cd ~/esquadrias-app
von                 # ativa o venv
python3             # abre o Python interativo (o prompt muda para >>>)
```

- Para sair do `python3`: `exit()` ou Ctrl+D.
- Os exemplos que usam `import dados` só funcionam se o `python3` for aberto **dentro de `~/esquadrias-app`**.
- Linhas que começam com `>>>` são para digitar no `python3`. As linhas sem `>>>` logo abaixo são a resposta que ele mostra.
- Linhas com `...` aparecem quando um bloco continua (depois de `for`, `if` ou `def`). Para terminar o bloco, aperte **Enter numa linha vazia**.

### Arquivos de treino

Alguns exercícios pedem um arquivo `.py`. Crie-os **na raiz do projeto**, com o nome `treino_aulaN.py` (ex.: `treino_aula4.py`), e rode assim:

```bash
python3 treino_aula4.py
```

Para eles não irem para o GitHub, adicione esta linha ao `.gitignore`:

```
treino_*.py
```

## Usando o curso em outra conversa com o Claude

Abra o `claude` dentro de `~/esquadrias-app` e cole a mensagem abaixo, trocando o número da aula:

> Vamos fazer a **Aula 01** do mini-curso em `docs/curso/`. Leia o `docs/curso/README.md` e o arquivo da aula. Seja meu professor: eu não sei nada de Python. Explique em partes pequenas e espere eu testar no `python3` antes de seguir. **Não me dê as respostas dos exercícios.** Quando eu errar, aponte onde está o erro e dê uma dica, mas me deixe corrigir. Ao final, faça 2 perguntas rápidas para ver se entendi. Responda em português.

Se for só tirar uma dúvida sobre um exercício:

> Estou na Aula 03, exercício 3.4. Meu código é este: (cole aqui). Está certo? Se não, me dê só uma dica.
