# DS & AI Cookbook

Coleção pessoal de receitas end-to-end, organizada por **problema**, do nível introdutório ao SOTA, com foco em sistemas financeiros, economia e socioeconomia. Bilíngue (PT-BR / EN).

**Stack:** Python 3.12 · uv · Zensical · Google Colab · apenas dados públicos.

## Início rápido

```bash
make setup                 # cria .venv com uv (todos os extras) e instala os hooks
make docs                  # prévia do site em http://localhost:8000 (LANG_SITE=en para inglês)
make help                  # todos os comandos
```

Antes do primeiro push, edite `config/cookbook.yml` (`github_repo: <seu-usuario>/ds-ai-cookbook`) e rode `make set-repo`. No Colab, crie os segredos `GH_TOKEN` (token do GitHub somente leitura para este repositório) e, para bases do Kaggle, `KAGGLE_API_TOKEN` (SPEC.md §13 e §14).

## Escrever uma receita

```bash
make promote ID=N1.01      # planned → draft, com templates preenchidos
make smoke ID=N1.01        # executa os notebooks em modo smoke
make render                # regenera resumo, benchmark, catálogos e navegação
make validate              # checa tudo
```

Fluxo completo em SPEC.md §16.

## Mapa do repositório

| Caminho | Conteúdo |
|---|---|
| [`INDEX.md`](INDEX.md) | Índice mestre: 15 partes, 587 receitas-mãe, 54 projetos integradores |
| [`SPEC.md`](SPEC.md) | Como o cookbook é organizado, escrito, executado e mantido |
| [`docs/`](docs/) | Conteúdo do site: receitas, projetos, notebooks e resultados |
| [`templates/`](templates/) | Templates de receita e de projeto |
| [`src/cookbook/`](src/cookbook/) | Pacote usado pelos notebooks (seeds, dados, resultados, esquemas) |
| [`tools/`](tools/) | scaffold, validate, render, build_site, run_notebooks, split_notebooks, set_repo |
| [`docs/projects/P1-credit/P1.01-e2e-credit-decision-engine/`](docs/projects/P1-credit/P1.01-e2e-credit-decision-engine/) | Projeto-piloto: motor de concessão de crédito E2E |
| [`config/`](config/) | Configuração editável do site e do repositório |

## Status

- [x] Passo 1: especificação e templates
- [x] Passo 2: esqueleto executável (ambiente, pacote, ferramentas, site bilíngue, CI, 641 itens planejados)
- [x] Passo 3: projeto-piloto P1.01 (8 notebooks L1/L3/L4, documento bilíngue; resultados `full` pendentes da execução no Colab)
- [ ] Passo 4: priorização em ondas
