# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Pricing/quoting app for aluminum windows and doors ("esquadrias"). Code, identifiers, data keys and user-facing strings are in Portuguese — keep it that way. The project was migrated from Laravel/SQLite to Python/Flask with JSON files as the data store (see git history).

## Commands

```bash
source venv/bin/activate        # local venv (Python 3.12): Flask 3.1, PyInstaller
python app.py                   # dev server, debug mode, http://127.0.0.1:5000
```

Run from the repo root: `app.py` opens `data/*.json` with relative paths. There is no requirements.txt, test suite, or linter config yet. PyInstaller is installed in the venv (intended for packaging as an executable), but there is no spec file yet.

## Architecture

- `app.py` is the whole backend. `carregar_dados()` re-reads **all** JSON files on every request (so edits to `data/` show up without a restart), and each route returns one dataset as JSON: `/perfis`, `/cores`, `/margem`, `/vidros`, `/acessorios`.
- `static/` and `templates/` exist but are empty; no frontend yet.
- `data/` is the database:
  - `perfis.json`, `acessorios.json` — objects keyed by product line (e.g. `"linha-box-acrilico"`), each a list of items identified by `codigo`. Profiles are priced by weight (`peso_metro`, `unidade: "kg/m"`) × the color's `preco_quilo`; accessories have `valor` per `unidade`.
  - `cores.json` — list of finishes (`id`, `nome`, `preco_quilo`).
  - `vidros.json` — list of glass types (`id`, `cor`, `espessura_mm`, `valor` per m²).
  - `tipologias.json` — the "recipe" of each product (e.g. `box-acrilico-2f`): lists of `perfis`, `acessorios` and `chapas` referencing `codigo`s from the files above, with `qtd` and formula strings (`medida`, `largura`, `altura`) in mm using `L` (width) and `A` (height) of the opening. Quantities are for **one** unit; the quote multiplies by the number of units.
  - `margem.json` — profit multipliers per category (`margens_lucro`: aluminio/acessorios/vidros) and fixed costs (`custos`: `valor_por_km`, removal of old frames).

## Data conventions

The JSON files are edited by hand. Keep these conventions when adding data or code:
- Keys are lowercase snake_case, no accents or hyphens. Measurements are numbers in mm with an `_mm` suffix, never strings like `"4mm"`.
- Every material has a single `valor` = the **most expensive** supplier's price. `fornecedores` is always a list of names and is reference only (where to buy); calculation code never picks a supplier.
- `unidade` is one of `"kg/m"` (profiles), `"un"`, `"m"`, `"m2"`, `"chapa"`. Sheet items (`"chapa"`, and glass) carry `chapa_largura_mm` / `chapa_altura_mm`.
- Profiles have an optional `imagem` filename, intended for `static/img/`.
- The system only prices quotes and raises alerts (e.g. a leaf larger than the PET sheet); it does **not** produce cut lists. Formulas intentionally use the plain opening sizes (`L`, `A`, `L / 2`) without cutting allowances or overlap; a production rate (`margens_lucro.taxa_producao`, 1.23, applied to material cost before external costs like travel) absorbs those differences. Don't "correct" formulas by adding allowances.
- Quote order: each group is priced separately — profiles (sum of qtd × length × `peso_metro` → total kg × color `preco_quilo` × aluminio margin), accessories "kit" (sum of each item × acessorios margin), sheet/glass (sheets or m² × the **vidros** margin, also for the acrylic/PET sheet); the group subtotals are summed, × `taxa_producao`, × number of units; external costs (travel, removal, meals) are added last, once per quote (not per unit), with **no** margin or rate.
- `chapas` items are priced as `qtd` × whole-sheet `valor`; their `largura`/`altura` formulas exist only to warn when a leaf doesn't fit in `chapa_largura_mm` × `chapa_altura_mm`.

The user is learning and prefers to make changes by hand, including the hard parts: explain step by step (what and why) and review their work. Do not create code files unless explicitly asked, and prefer approaches that are simple to understand.
