# Onde paramos (passagem de bastão)

Atualizado em 26/11/2026 (escritorio). Leia este arquivo ao retomar o trabalho, em qualquer PC.

## Estado atual

Branch: `feat-gean-19-11-2026-dados-py`

| Arquivo | Situação |
|---|---|
| `data/*.json` | Padronizados e revisados (PR #1 já mergeado na `main`) |
| `dados.py` | Pronto: `ler`, `buscar_tipologia`, `buscar_cor`, `buscar_perfil`, `buscar_acessorio`, `buscar_margem` |
| `formulas.py` | Pronto: `avaliar(formula, L, A)`, com as duas travas e o `try/except` |
| `calculos.py` | **Em andamento.** Partes 1 a 3 prontas e testadas (box 1500 × 1900): `calcular_perfis` (cor 9) → 3,897 kg / R$ 214,33; `calcular_acessorios` → R$ 83,24; `calcular_chapas` → R$ 225,94, e erro se a folha passar de 875 × 1900 (vão máximo 1750 × 1900). Parte 4a pronta: `orcar(nome_tipologia, L, A, qtd=1, id_cor=None)` → 1 box 1500 × 1900 = **R$ 1148,11** (qtd 2 = 2296,22; cor 1 → perfis 353,26). Falta a 4b: `calcular_custos_externos` |
| `app.py` | Ainda é a versão antiga. Só vai mudar depois do `calculos.py` |

### Mini-curso de Python (`docs/curso/`)
- **Aula 01:** concluída.
- **Aula 02:** em andamento. Exercícios 2.1 a 2.7 feitos, com respostas `R:`/`R2:` no próprio arquivo, e já revisados. **Falta corrigir:** 2.3 (2º item, `R2` buscou no `acessorios.json` em vez da tipologia), 2.4 (`id` como texto; preço 54.0), 2.5 (rodar cada linha e copiar o nome do erro), 2.6 (usar só `item = box["perfis"][0]` e `perfil`, sem sobrescrever, e usar o `L`), 2.7 (comparar o tipo do `codigo` com o `1`; ler o `buscar_perfil` no `dados.py`). Depois, as 2 perguntas finais da aula.
- Para retomar: use a mensagem do `docs/curso/README.md`, dizendo que a aula 02 está em correção.

## Próximos passos
1. ~~Partes 1 a 3 do `calculos.py`~~ (feitas em 22 e 24/11).
2. ~~Parte 4a: `orcar`~~ (feita em 26/11). Ela dá o preço de **1 item**, sem custos externos, e não muda mais.
3. **Parte 4b (próxima, no escritorio):** `calcular_custos_externos(km_ida, funcionarios, dias_inteiros=0, meios_dias=0, remocao=0, preco_diesel=None)`, no `calculos.py`, depois da `orcar`. Esqueleto na conversa de 26/11. Regras:
   - `viagens = dias_inteiros + meios_dias` (cada dia = 1 ida e volta; retrabalho entra como mais um dia);
   - `km_total = km_ida × 2 × viagens`; deslocamento = `km_total ÷ consumo_km_litro × preco_diesel + km_total × desgaste_p_km`;
   - almoço = `funcionarios × dias_inteiros × almoco_funcionario_dia` (meio dia não tem almoço);
   - remoção = valor digitado (depende do tipo de peça, da altura, de andaime etc.; sem regra automática);
   - `preco_diesel` vazio → usa o do `margem.json`.
   - Testes: `(40, 3, dias_inteiros=2, meios_dias=1, remocao=200)` → km 240, deslocamento 200,70, almoço 180, total **580,70**; com `preco_diesel=6.00` → 560,00; `(40, 2, meios_dias=1)` → 66,90.
4. Depois: nível do **orçamento** (vários itens): desconto, comissão, custos e rateio nos itens (ver as decisões abaixo).
5. Depois: `app.py` com as rotas `/api/...`, e então a interface estilo terminal (HTML/CSS/JS em `templates/` e `static/`).

## Decisões já tomadas (não reabrir)
- **Preço:** cada material tem um único `valor`, o do fornecedor **mais caro**. `fornecedores` é só referência de onde comprar.
- **Cálculo sem descontos:** medidas "secas" (`L`, `A`, `L / 2`), sem desconto de trilho nem transpasse. A `taxa_producao` (1,23) absorve isso, mais as perdas e os erros. O sistema serve só para orçamento e alertas, e não gera lista de corte.
- **Ordem do orçamento:** perfis (kg × preço da cor × margem alumínio) + kit de acessórios (× margem acessórios) + chapa/vidro (× margem **vidros**, que vale também para o acrílico) → soma × `taxa_producao` → × quantidade. Os custos externos (deslocamento, remoção, almoço) são calculados uma vez por orçamento, sem margem e sem taxa.
- **Custos nunca aparecem separados para o cliente:** são diluídos no preço das aberturas. Todo percentual vira valor fixo em R$ sobre a base certa, e nunca se aplica % sobre o preço que já tem custos dentro. Ordem: itens (`orcar`) → desconto % sobre a base → comissão % (calculada **depois** do desconto) → + custos externos → rateio de tudo **proporcional ao valor** de cada item (um fator único; a diferença de centavos vai para o último item).
- **Quantidades** no `tipologias.json` são para **1 unidade** do produto.
- **Box acrílico:** cor padrão 9 (Anodizado Fosco). 1 chapa PET por folha (2 por box), sem aproveitamento.
- As **margens** (1,85 / 1,70 / 1,75) ainda serão revisadas na ponta do lápis: markup × margem real, mão de obra, impostos. A estrutura não muda, só os números no `margem.json`.
- As planilhas antigas tinham **margem dupla** (o "custo" já vinha com margem). Os preços do JSON são os corretos. Atenção a isso ao usar outras planilhas como base para novas tipologias.
- **Objetivo de longo prazo:** mais de 100 modelos, cadastros (clientes, fornecedores, materiais) e logística, substituindo o SIS.PO (Alumake) e as planilhas. O **Windel continua** com NF-e e contas a pagar/receber. Modelos são **dados** (receitas no `tipologias.json`), nunca uma função por modelo. Cadastros e pedidos devem ir para SQLite no futuro, mexendo só no `dados.py`.
- **Futuro (fora do foco de 2026):**
  - importar o XML da NF-e de compra: atualiza o preço da última compra por fornecedor e dá entrada no estoque. O cálculo continua usando o **maior** preço, e o relatório de compra recomenda o mais barato;
  - importar as notas dos postos para manter o diesel atualizado;
  - gerar o orçamento em PDF.
- **Foco de 2026:** terminar o cálculo. Basta o sistema dar os valores; o orçamento ainda é montado à mão.

## Como trabalhamos
- **Dois PCs:**
  - **"escritorio"**: projeto em `~/workbench/esquadrias-app`. Aqui o foco é **produzir** e adiantar o sistema, com explicações diretas e sem curso.
  - **"casa"**: projeto em `~/esquadrias-app`. Aqui o foco é **estudar** com calma (mini-curso em `docs/curso/`) e treinar aplicando no próprio sistema.
  - Ao começar em qualquer um dos dois: `git pull` e diga ao Claude em qual PC você está.
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
