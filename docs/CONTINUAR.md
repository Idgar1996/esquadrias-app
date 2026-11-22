# Onde paramos (passagem de bastão)

Atualizado em 22/11/2026. Leia este arquivo ao retomar o trabalho, em qualquer PC.

## Estado atual

Branch: `feat-gean-19-11-2026-dados-py`

| Arquivo | Situação |
|---|---|
| `data/*.json` | Padronizados e revisados (PR #1 já mergeado na `main`) |
| `dados.py` | Pronto: `ler`, `buscar_tipologia`, `buscar_cor`, `buscar_perfil`, `buscar_acessorios`, `buscar_margem` |
| `formulas.py` | Pronto: `avaliar(formula, L, A)`, com as duas travas e o `try/except` |
| `calculos.py` | **Em andamento.** Parte 1 (`calcular_perfis`) pronta e testada: box 1500 × 1900, cor 9 → `{'peso_kg': 3.8969999999999994, 'custo': 214.33499999999995}` |
| `app.py` | Ainda é a versão antiga. Só vai mudar depois do `calculos.py` |

### Pendências no `calculos.py` (Parte 1) — concluídas em 22/11
1. `formulas.avalias` → `formulas.avaliar` (erro de digitação).
2. Falta o restante da função depois da linha do `medida_m`:
   ```python
           peso_total += item["qtd"] * medida_m * perfil["peso_metro"]

       custo = peso_total * cor["preco_quilo"]
       return {"peso_kg": peso_total, "custo": custo}
   ```
   Atenção ao recuo: `peso_total +=` fica **dentro** do `for`; `custo` e `return` ficam **fora** dele.
3. Na f-string do `raise`, use aspas simples dentro: `{item['codigo']}`.
4. Teste esperado (box 1500 × 1900, cor 9 Anodizado Fosco):
   ```python
   >>> import dados, calculos
   >>> box = dados.buscar_tipologia("box-acrilico-2f")
   >>> cor = dados.buscar_cor(9)
   >>> calculos.calcular_perfis(box, 1500, 1900, cor)
   {'peso_kg': 3.897..., 'custo': 214.33...}
   ```

### Mini-curso de Python (`docs/curso/`)
- **Aula 01:** concluída.
- **Aula 02:** em andamento. Exercícios 2.1 a 2.7 feitos, com respostas `R:`/`R2:` no próprio arquivo, e já revisados. **Falta corrigir:** 2.3 (2º item, `R2` buscou no `acessorios.json` em vez da tipologia), 2.4 (`id` como texto; preço 54.0), 2.5 (rodar cada linha e copiar o nome do erro), 2.6 (usar só `item = box["perfis"][0]` e `perfil`, sem sobrescrever, e usar o `L`), 2.7 (comparar o tipo do `codigo` com o `1`; ler o `buscar_perfil` no `dados.py`). Depois, as 2 perguntas finais da aula.
- Para retomar: use a mensagem do `docs/curso/README.md`, dizendo que a aula 02 está em correção.

## Próximos passos
1. ~~Terminar e testar a `calcular_perfis`~~ (feito; as pendências acima já foram aplicadas no código).
2. **Parte 2:** `calcular_acessorios(tipologia, L, A)`: soma `qtd × valor` de cada acessório. Os itens com unidade `"m"` (borracha) usam `qtd × medida/1000 × valor`. Devolve o custo do kit, **sem margem**. A ideia é você escrever sozinho, só a partir desta descrição.
3. **Parte 3:** `calcular_chapas(tipologia, L, A)`: `qtd × valor` da chapa, mais um alerta se `largura`/`altura` (fórmulas) passarem de `chapa_largura_mm`/`chapa_altura_mm`.
4. **Parte 4:** `orcar(...)`: busca a tipologia e a cor (usa `cor_padrao` se nenhuma for informada), chama as três funções, aplica as margens por grupo, `× taxa_producao`, `× quantidade` e `+ custos externos` (uma vez por orçamento, sem margem). Arredonda só no final.
5. Depois: `app.py` com as rotas `/api/...`, e então a interface estilo terminal (HTML/CSS/JS em `templates/` e `static/`).

## Decisões já tomadas (não reabrir)
- **Preço:** cada material tem um único `valor`, o do fornecedor **mais caro**. `fornecedores` é só referência de onde comprar.
- **Cálculo sem descontos:** medidas "secas" (`L`, `A`, `L / 2`), sem desconto de trilho nem transpasse. A `taxa_producao` (1,23) absorve isso, mais as perdas e os erros. O sistema serve só para orçamento e alertas, e não gera lista de corte.
- **Ordem do orçamento:** perfis (kg × preço da cor × margem alumínio) + kit de acessórios (× margem acessórios) + chapa/vidro (× margem **vidros**, que vale também para o acrílico) → soma × `taxa_producao` → × quantidade → + custos externos (deslocamento, remoção, almoço), sem margem.
- **Quantidades** no `tipologias.json` são para **1 unidade** do produto.
- **Box acrílico:** cor padrão 9 (Anodizado Fosco). 1 chapa PET por folha (2 por box), sem aproveitamento.
- As **margens** (1,85 / 1,70 / 1,75) ainda serão revisadas na ponta do lápis: markup × margem real, mão de obra, impostos. A estrutura não muda, só os números no `margem.json`.
- As planilhas antigas tinham **margem dupla** (o "custo" já vinha com margem). Os preços do JSON são os corretos. Atenção a isso ao usar outras planilhas como base para novas tipologias.
- **Objetivo de longo prazo:** cobrir todos os modelos e substituir o SIS.PO (Alumake) e as planilhas.

## Como trabalhamos
- O código é escrito **à mão, por você**. O Claude explica parte por parte (o quê e por quê), passa os testes e revisa. Ele não cria arquivos de código, a não ser que você peça.
- **"Dúvida rápida:"** no início da mensagem = pergunta paralela. Resposta curta, e depois voltamos ao assunto.
- Teste cada parte no `python3`. Mudou o arquivo, recarregue: `exit()` e entre de novo, ou `importlib.reload(modulo)`.
- `jsoncheck` (função no `~/.bashrc`) valida os JSON. Num PC novo, ela precisa ser recriada.

## Retomar em outro PC

### 0. PC sem WSL (começando do zero)
1. **Instalar o WSL:** abra o **PowerShell como Administrador** e rode:
   ```powershell
   wsl --install
   ```
   Reinicie o PC. O Ubuntu abre sozinho e pede um usuário e uma senha: **use o usuário `idgar`**, assim os caminhos ficam iguais aos deste PC (`/home/idgar/...`), e a conversa do Claude é encontrada sem ajustes.
2. **Ferramentas básicas**, no terminal do Ubuntu:
   ```bash
   sudo apt update && sudo apt install -y git python3-venv python3-pip unzip
   ```
3. **Claude Code:**
   ```bash
   curl -fsSL https://claude.ai/install.sh | bash
   ```
   Feche e abra o terminal. Rode `claude` uma vez para fazer o login.
4. **Função `jsoncheck`**: cole no final do `~/.bashrc` (`nano ~/.bashrc`) e depois rode `source ~/.bashrc`:
   ```bash
   jsoncheck() {
       local pasta="${1:-data}"
       local erros=0
       for f in "$pasta"/*.json; do
           if msg=$(python3 -m json.tool "$f" 2>&1 >/dev/null); then
               echo "✔ $f"
           else
               echo "✘ $f → $msg"
               erros=$((erros + 1))
           fi
       done
       if [ "$erros" -eq 0 ]; then echo "Tudo OK"; else echo "$erros arquivo(s) com erro"; fi
   }
   ```
5. Siga os passos 1 a 3 abaixo. Para o clone, crie antes a pasta: `mkdir -p ~/workbench && cd ~/workbench`.
6. **Restaurar a conversa do Claude** (o zip que foi para o Google Drive): baixe o zip no Windows e, no Ubuntu, rode:
   ```bash
   mkdir -p ~/.claude/projects
   unzip "/mnt/c/Users/<usuário do Windows>/Downloads/claude-esquadrias.zip" -d ~/.claude/projects/
   cd ~/workbench/esquadrias-app
   claude --resume
   ```
   Escolha a conversa mais recente na lista.

### Passos gerais
1. **Acesso ao GitHub por SSH** (só na primeira vez):
   ```bash
   ssh-keygen -t ed25519            # Enter em tudo
   cat ~/.ssh/id_ed25519.pub        # copie e cadastre no GitHub: Settings → SSH and GPG keys
   ssh -T git@github.com            # deve responder "Hi Idgar1996!"
   git config --global user.name "idgar"
   git config --global user.email "<seu e-mail>"
   ```
2. **Clonar e preparar:**
   ```bash
   git clone git@github.com:Idgar1996/esquadrias-app.git
   cd esquadrias-app
   git checkout feat-gean-19-11-2026-dados-py
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Claude Code:** a conversa e as anotações do Claude ficam só no PC original. No PC novo, abra `claude` na pasta do projeto e peça: *"leia o docs/CONTINUAR.md e vamos continuar de onde paramos"*. O `CLAUDE.md` é carregado automaticamente.
4. **Ao terminar o trabalho no outro PC**, atualize este arquivo, faça commit e push. Ao voltar para este PC, rode `git pull` antes de continuar.
