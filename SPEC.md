# Especificação do Cookbook / Cookbook Specification

> Versão 1.0 · documento de referência interno (PT-BR). Define **como** o cookbook é organizado, escrito, executado e mantido. O **quê** está no `INDEX.md`.
> Decisões fixadas: repositório privado de uso próprio · notebooks executados no **Google Colab** · **Python 3.12 + uv + Zensical** · apenas **dados públicos**.

---

## 1. Princípios

1. **Organizado por problema, não por ferramenta.** A unidade é a *receita-mãe*: um problema, todas as stacks viáveis.
2. **Executável ou não existe.** Toda afirmação de desempenho vem de um notebook que roda e grava resultados.
3. **Comparável.** Stacks de uma mesma receita usam os mesmos dados, splits, seeds e métricas.
4. **Decisão antes de código.** Cada receita começa com um mapa de decisão; o código serve à escolha.
5. **Uma fonte de verdade.** Código é único (inglês); só a narrativa é traduzida. Metadados vivem em YAML, tabelas de benchmark são geradas.
6. **Datado e versionado.** Toda receita registra versões pinadas e a data da última verificação.

---

## 2. Conceitos

| Termo | Definição |
|---|---|
| **Receita-mãe** (recipe) | Um problema do índice (ex.: `N1.01`). Contém documento bilíngue, metadados e um ou mais notebooks. |
| **Stack** | Uma forma concreta de resolver o problema (ex.: `optbinning + LogisticRegression`). Um notebook por stack. |
| **Eixo de variação** (variation axis) | Uma variável de decisão explorada e medida (ex.: estratégia de binning, taxa de desbalanceamento, tamanho de amostra). |
| **Nível** | `L1` introdutório · `L2` intermediário · `L3` avançado · `L4` SOTA. A receita tem um nível de **entrada**; cada stack tem seu próprio nível. Assim uma receita cobre do L1 ao L4. |
| **Projeto integrador** (project) | Um item da Parte P (ex.: `P1.01`). Combina receitas em um sistema E2E com três camadas: mínima (L1), produção (L3), SOTA (L4). |
| **Modo de execução** | `smoke` (subamostra, CPU, poucos minutos; usado no CI) ou `full` (resultado oficial, no Colab). |

---

## 3. Estrutura do repositório

```
ds-ai-cookbook/
├── README.md                     # visão geral e início rápido
├── INDEX.md                      # índice mestre (fonte do esqueleto)
├── SPEC.md                       # este documento
├── Makefile                      # atalhos: make help
├── pyproject.toml · uv.lock      # ambiente (Python 3.12, uv)
├── config/
│   ├── site.base.toml            # configuração do site (Zensical) editável à mão
│   └── cookbook.yml              # github_repo (links do Colab)
├── .pre-commit-config.yaml       # nbstripout, ruff, render, validate
├── .github/workflows/
│   ├── ci.yml                    # lint, validação, testes, smoke, build do site
│   └── colab.yml                 # publica notebooks pt/en no branch colab
├── templates/
│   ├── recipe/   (recipe.yaml, index.pt.md, index.en.md, notebooks/01-stack-template.ipynb)
│   └── project/  (project.yaml, index.pt.md, index.en.md)
├── src/cookbook/                 # pacote instalado nos notebooks
│   ├── env.py                    #   Colab, seeds, hardware, versões
│   ├── data.py                   #   registro de datasets, download com cache e checksum
│   ├── results.py                #   Timer, summarize, save_result validado
│   ├── credit.py                 #   Gini, KS, ECE, PSI/CSI, pontos, cortes, lucro, motivos, calibrador
│   ├── home_credit.py            #   Home Credit: carregador, limpeza, split, features, gêmeo sintético
│   ├── validation.py             #   validadores JSON Schema
│   └── schemas/                  #   recipe · project · result .schema.json
├── tools/
│   ├── scaffold.py               #   INDEX.md → pastas "planned"; promote → "draft"
│   ├── validate.py               #   metadados, docs, notebooks, resultados, frescor
│   ├── render.py                 #   catálogos, quadros-resumo, benchmarks, navegação
│   ├── build_site.py             #   site bilíngue com Zensical (pt em /, en em /en/)
│   ├── run_notebooks.py          #   execução com papermill (smoke/full, --offline)
│   ├── set_repo.py               #   aponta badges e instalações para config/cookbook.yml
│   └── split_notebooks.py        #   notebook-fonte → versões pt/en
├── tests/                        # pytest (o teste "slow" faz o ciclo completo)
├── docs/                         # conteúdo do site (fonte dos dois idiomas)
│   ├── index.pt.md · index.en.md # início + bloco PROGRESS gerado
│   ├── glossary.pt.md · glossary.en.md
│   ├── recipes/
│   │   └── N-finance-economics/
│   │       ├── part.yaml         # títulos da parte e das seções
│   │       ├── index.*.md        # catálogo da parte (gerado)
│   │       └── N1/
│   │           ├── index.*.md    # catálogo da seção (gerado)
│   │           └── N1.01-application-scorecard-woe-iv/
│   │               ├── recipe.yaml
│   │               ├── index.pt.md · index.en.md
│   │               ├── notebooks/       # notebooks-fonte bilíngues
│   │               ├── results/         # *.full.json versionados; *.smoke.json ignorados
│   │               └── assets/          # figuras, diagramas
│   └── projects/
│       ├── index.*.md            # catálogo de projetos (gerado)
│       └── P1-credit/
│           ├── group.yaml · index.*.md
│           └── P1.01-e2e-credit-decision-engine/
│               ├── project.yaml · index.pt.md · index.en.md
│               ├── notebooks/ · results/ · assets/
└── data/                         # cache local, no .gitignore
```

**Por que tudo dentro de `docs/`:** o site é montado a partir de `docs/`; manter notebooks, resultados e figuras ao lado do texto evita links quebrados e deixa cada receita autocontida.

### 3.1 Pastas das partes

| Parte | Pasta | | Parte | Pasta |
|---|---|---|---|---|
| A | `A-foundations` | | H | `H-stats-causal` |
| B | `B-data-engineering` | | I | `I-platforms` |
| C | `C-analysis-features` | | J | `J-llmops` |
| D | `D-classical-ml` | | K | `K-dataops` |
| E | `E-deep-learning` | | L | `L-generative-sciences` |
| F | `F-ai-engineering` | | M | `M-technical-audit` |
| G | `G-mlops` | | N | `N-finance-economics` |

Projetos: `docs/projects/P1-credit`, `P2-fraud-aml`, `P3-markets`, `P4-macro`, `P5-socioeconomics`, `P6-financial-platforms`, `P7-other-domains`.

---

## 4. Convenções de nomes

| Item | Regra | Exemplo |
|---|---|---|
| ID de receita | Exatamente como no `INDEX.md`: `<Parte><Seção>.<NN>` | `N1.01`, `L2.04` |
| ID de projeto | `P<grupo>.<NN>` | `P1.01` |
| Pasta | `<ID>-<slug>` | `N1.01-application-scorecard-woe-iv` |
| Slug | inglês, kebab-case, ≤ 6 palavras, **imutável** após criado (links dependem dele) | `imbalanced-data` |
| Notebook de stack | `NN-<stack-slug>.ipynb`, `01`–`79` | `01-optbinning-logistic.ipynb` |
| Notebook de eixo transversal | `80`–`89` (eixos comparados entre stacks) | `80-axis-sample-size.ipynb` |
| Notebook de benchmark | `90-benchmark.ipynb` (agrega `results/`) | |
| Resultados | `results/<notebook-stem>__<stack>[__<variante>].<run_mode>.json` (gerado por `save_result`) | `results/01-optbinning-logistic__optbinning-logistic.full.json`, `results/80-axis-binning__optbinning__bins-10.full.json` |
| Figuras | `assets/<notebook-stem>-<descrição>.png` (ou `.svg`) | `assets/01-optbinning-logistic-iv.png` |

Ordem dos notebooks de stack: do mais simples ao mais avançado (L1 → L4).

---

## 5. Bilinguismo

**Documentos.** Dois arquivos lado a lado: `index.pt.md` e `index.en.md` (`tools/build_site.py` publica cada idioma como um site separado: PT em `/`, EN em `/en/`). Mesma estrutura de seções, mesma ordem, mesmas âncoras. O PT-BR é a língua de autoria; o EN é tradução fiel, não resumo.

**Notebooks.** Um único **notebook-fonte** por stack. Células de código são compartilhadas (código, comentários e saídas impressas em inglês). Células de texto aparecem em pares, cada uma com a tag `lang:pt` ou `lang:en`:

```
[markdown, tags: lang:pt]  ## 2. Dados
[markdown, tags: lang:en]  ## 2. Data
[code,     sem tag]        df = load_dataset(...)
```

`tools/split_notebooks.py` gera `pt/` e `en/` filtrando por tag. O workflow `colab.yml` publica as versões geradas no branch `colab`; os badges "Open in Colab" apontam para lá.

**Terminologia.** Termos técnicos consagrados ficam em inglês no texto PT (feature, pipeline, embedding, fine-tuning, threshold), em *itálico* na primeira ocorrência da página. O `docs/glossary.pt.md` / `.en.md` é a referência; termo novo entra no glossário antes de ser usado.

---

## 6. Metadados

### 6.1 `recipe.yaml`

Validado por `src/cookbook/schemas/recipe.schema.json`. Itens `planned` exigem só identidade, nível, ambiente e ciclo de revisão; a partir de `draft` exigem também `summary`, `stacks`, `datasets` e `metrics`. O campo `index_hint` guarda a coluna de stacks do `INDEX.md`. Campos:

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | sim | ID do índice (`N1.01`) |
| `slug` | sim | slug imutável |
| `title.pt` / `title.en` | sim | títulos |
| `part`, `section` | sim | `N`, `N1` |
| `level` | sim | nível de entrada `L1`–`L4` |
| `status` | sim | ver §11 |
| `summary.pt` / `summary.en` | sim | 1–2 frases: problema e resultado |
| `prerequisites` | não | IDs de receitas a ler antes |
| `related` | não | IDs relacionados (↔ do índice) |
| `tags` | não | palavras-chave livres |
| `stacks[]` | sim (≥1 quando `status ≥ draft`) | ver abaixo |
| `variation_axes[]` | não | eixos explorados: `id`, `name.pt/en`, `values`, `notebook` |
| `datasets[]` | sim | `name`, `url`, `license`, `size_mb`, `sha256` (opcional), `loader` |
| `metrics.primary` / `metrics.secondary` | sim | métrica principal de comparação e demais |
| `environment.python` | sim | `"3.12"` |
| `environment.colab_runtime` | sim | `cpu`, `gpu-t4`, `gpu-l4`, `gpu-a100`, `tpu` |
| `last_verified` | sim | data da última execução `full` bem-sucedida, **entre aspas** (`"YYYY-MM-DD"`), senão o YAML a converte em objeto de data e o schema rejeita. Vale para todas as datas. |
| `review_cycle_months` | sim | ver §12 |
| `references[]` | não | `title`, `url`, `type` (paper, docs, book, blog), `accessed` |

Cada item de `stacks[]`:

| Campo | Descrição |
|---|---|
| `id` | slug da stack (`optbinning-logistic`) |
| `name` | nome legível |
| `level` | `L1`–`L4` |
| `notebook` | caminho relativo (`notebooks/01-optbinning-logistic.ipynb`) |
| `packages` | dict `pacote: versão exata` |
| `gpu` | `none`, `optional`, `required` |
| `runtime_min` | `{smoke: n, full: n}` estimativa em minutos |
| `cost` | `free`, `low`, `medium`, `high` (custo de rodar `full`) |
| `maturity` | `experimental`, `emerging`, `stable`, `legacy` |
| `learning_curve` | `low`, `medium`, `high` |

### 6.2 `project.yaml`

Validado por `src/cookbook/schemas/project.schema.json`. Além dos campos comuns (`id`, `slug`, `title`, `status`, `summary`, `datasets`, `last_verified`, `review_cycle_months`, `references`):

| Campo | Descrição |
|---|---|
| `group` | `P1`–`P7` |
| `domain` | `credit`, `fraud-aml`, `markets`, `macro`, `socioeconomics`, `financial-platforms`, `other` |
| `recipes` | IDs combinados (do índice) |
| `tiers.L1` / `tiers.L3` / `tiers.L4` | `goal.pt/en`, `notebooks[]`, `stack` (lista de tecnologias) |
| `business_metrics` | métricas de negócio (ex.: taxa de aprovação, perda esperada) |
| `regulatory` | normas aplicáveis (ex.: `CMN 4.966`, `LGPD`) |

### 6.3 Resultados (`results/*.json`)

Validado por `src/cookbook/schemas/result.schema.json` e gravado por `cookbook.results.save_result`. Todo notebook grava um arquivo por modo de execução com: `recipe_id`, `notebook`, `stack`, `run_mode`, `timestamp`, `git_sha`, `hardware` (cpu, gpu, ram_gb), `versions` (python + pacotes), `dataset` (nome + hash), `params`, `metrics` (`{nome: {mean, std, n}}`), `time_s` (treino, inferência), `peak_mem_mb`. A tabela de benchmark nos documentos é **gerada** a partir dos arquivos `*.full.json` (`tools/render.py`), nunca digitada. Resultados `smoke` não são versionados.

---

## 7. Anatomia do documento de receita

Seções fixas, nesta ordem (os templates já as trazem com instruções):

| # | Seção PT / EN | Conteúdo mínimo |
|---|---|---|
| 0 | Cabeçalho | título, ID, nível, tags, tempo de leitura; quadro-resumo gerado do YAML |
| 1 | Problema e contexto / Problem and context | quando aparece, quem enfrenta, critério de sucesso |
| 2 | Mapa de decisão / Decision map | fluxograma Mermaid "se X então Y" + tabela de atalhos |
| 3 | Stacks candidatas / Candidate stacks | tabela comparativa (pros, contras, casos de uso, custo, maturidade, curva) + um parágrafo por stack |
| 4 | Passo a passo por stack / Step-by-step per stack | resumo dos passos de cada notebook + badge Colab; o detalhe fica no notebook |
| 5 | Eixos de variação / Variation axes | por eixo: valores testados, efeito medido (gráfico/tabela), recomendação |
| 6 | Benchmark comparativo / Comparative benchmark | tabela gerada entre marcadores `<!-- BENCHMARK:START -->` e `<!-- BENCHMARK:END -->` + leitura dos resultados |
| 7 | Validação / Validation | checklist de como saber que está certo |
| 8 | Armadilhas / Pitfalls | ≥ 3, cada uma: sintoma → causa → correção; demonstradas em notebook quando possível |
| 9 | Do protótipo à produção / From prototype to production | o que muda em escala, monitoramento, links para G/J/K |
| 10 | Referências / References | papers, docs oficiais, data de acesso |

---

## 8. Anatomia do notebook de stack

Seções fixas (ver `templates/recipe/notebooks/01-stack-template.ipynb`; o `make promote` copia e preenche):

| # | Seção | Regras |
|---|---|---|
| H | Cabeçalho | título, ID, stack, nível, runtime Colab, tempo estimado, badge Colab |
| 0 | Parâmetros | célula com tag `parameters` (papermill): `RUN_MODE`, `SEED`, `DATA_DIR`, `SAMPLE_FRAC` |
| 1 | Setup | detecção de Colab, instalação com versões exatas, seeds, registro de hardware |
| 2 | Dados | download com cache e checksum, inspeção mínima, split fixo e documentado |
| 3 | Solução | passo a passo da stack, uma ideia por célula, comentários explicando o *porquê* |
| 4 | Validação | métricas primária e secundárias, gráficos de diagnóstico |
| 5 | Eixos de variação | loops parametrizados sobre os eixos da stack |
| 6 | Armadilhas demonstradas | reprodução controlada de 1+ erro comum e sua correção |
| 7 | Resultados | gravação do JSON no `result.schema.json` |
| 8 | Conclusão | o que aprendemos, quando usar esta stack, próximos passos |

**Regras de código.** Saídas removidas antes do commit (`nbstripout`), exceto em `results/`. Sem caminhos absolutos. Sem segredos. Toda célula roda de cima para baixo após *Restart & Run All*. Modo `smoke` deve terminar em ≤ 10 min em CPU.

---

## 9. Projetos integradores

Documento com seções fixas (ver `templates/project/`):

| # | Seção | Conteúdo |
|---|---|---|
| 1 | Contexto de negócio / Business context | problema, atores, decisão apoiada |
| 2 | Métricas de sucesso / Success metrics | negócio + técnicas + restrições (latência, custo, regulação) |
| 3 | Dados / Data | bases públicas, dicionário, limitações, vieses |
| 4 | Arquitetura / Architecture | diagrama Mermaid por camada |
| 5 | Camada L1, versão mínima / Minimal tier | sistema funcional em 1 notebook, decisões simples |
| 6 | Camada L3, produção / Production tier | pipelines, deploy, monitoramento, testes |
| 7 | Camada L4, SOTA / SOTA tier | técnicas de fronteira e seu ganho medido sobre L3 |
| 8 | Riscos, regulação e auditoria / Risk, regulation, audit | normas, checklist de auditoria (Parte M), fairness |
| 9 | Receitas utilizadas / Recipes used | tabela ID → onde entra no projeto |
| 10 | Extensões / Extensions | variações e próximos passos |
| 11 | Referências / References | |

Notebooks do projeto seguem a ordem `10-` (L1), `30-` (L3), `40-` (L4).

---

## 10. Benchmark e reprodutibilidade

- **Splits congelados**: definidos uma vez por receita (função em `src/cookbook/data.py` ou no notebook `01`), com seed e estratificação documentadas. Séries temporais: sempre split temporal.
- **Repetições**: métricas reportadas como média ± desvio sobre k folds ou ≥ 3 seeds. Diferenças sem significância são declaradas como empate.
- **Mesmo hardware por receita** no modo `full` (o `colab_runtime` declarado). Hardware e versões vão no JSON.
- **Custo e tempo** são métricas de primeira classe: tempo de treino, de inferência (por 1k amostras) e memória de pico.
- **Baseline obrigatório**: toda receita compara contra um baseline trivial (dummy, naive, regra simples).

---

## 11. Ciclo de vida e Definition of Done

| Status | Significado |
|---|---|
| `planned` | existe no índice e tem pasta-esqueleto |
| `draft` | conteúdo em produção |
| `review` | completo, aguardando revisão (técnica + tradução) |
| `done` | atende à Definition of Done |
| `outdated` | passou do `review_cycle_months` ou quebrou no CI |

**Definition of Done (receita):**
- [ ] `recipe.yaml` válido no schema; `status: done`; `last_verified` preenchido
- [ ] `index.pt.md` e `index.en.md` com todas as seções, sem `TODO`
- [ ] Todos os notebooks rodam em `smoke` no CI e em `full` no Colab
- [ ] `results/*.full.json` presentes e tabela de benchmark gerada
- [ ] Baseline incluído; ≥ 2 stacks (salvo receitas conceituais); ≥ 1 eixo de variação medido
- [ ] ≥ 3 armadilhas com correção
- [ ] Versões exatas pinadas; dados com licença registrada
- [ ] Referências com data de acesso
- [ ] Termos novos adicionados ao glossário

---

## 12. Manutenção

| Partes | `review_cycle_months` |
|---|---|
| F, J (AI Engineering, LLMOps), E4, E5 | 3 |
| B, G, K, L, M, E1–E3, E6 | 6 |
| A, C, D, H, I, N | 12 |

O CI marca como `outdated` receitas vencidas ou com notebook quebrado. Atualização de versão de pacote = rodar `full`, atualizar `last_verified` e regenerar benchmark.

---

## 13. Dados públicos

- Nunca versionar dados. Download pelo notebook, com cache (`DATA_DIR`; no Colab, opcionalmente montado no Google Drive).
- Registrar licença, URL, tamanho e, quando estável, `sha256`.
- Dados que exigem login (ex.: Kaggle) usam credenciais via `google.colab.userdata` ou variável de ambiente, nunca no notebook.
- Em `smoke`, usar subamostra determinística (`SAMPLE_FRAC`) ou um arquivo pequeno de amostra gerado do original.
- Dados pessoais (mesmo públicos): seguir LGPD; preferir agregados ou sintéticos.
- **Gêmeos sintéticos e modo offline.** Datasets que exigem login (ex.: Home Credit) têm um gêmeo sintético com as mesmas colunas, distribuições plausíveis e os mesmos problemas de qualidade (`home-credit-synthetic`). O parâmetro `OFFLINE=True` (passado por `run_notebooks.py --offline`, usado no CI e nos testes) troca a base real pelo gêmeo. Um notebook com `RUN_MODE="full"` e `OFFLINE=True` deve falhar: números do gêmeo servem para testar código, nunca entram nos documentos.

---

## 14. Google Colab

- **Abrir:** badges apontam para o branch `colab`, que o CI preenche com as versões `pt/` e `en/` dos notebooks. O Colab abre repositórios privados após autorizar o GitHub na primeira vez.
- **Pacote `cookbook`:** instalado no setup a partir do repositório privado, com um *fine-grained personal access token* (somente leitura deste repositório) guardado no segredo `GH_TOKEN` do Colab (menu 🔑). Nunca colar o token no notebook.
- **Instalação:** `uv pip install --system` com as versões exatas do `recipe.yaml`. A versão do Python no Colab segue o runtime do Google e pode diferir de 3.12. O alvo oficial é 3.12; divergências relevantes vão em Armadilhas.
- **GPU:** o `colab_runtime` do YAML diz qual acelerador escolher. Notebooks com `gpu: required` verificam o acelerador na seção 1 e param com mensagem clara se ele não estiver disponível.
- **Persistência:** dados e checkpoints grandes ficam em `/content/drive/MyDrive/cookbook-data` (Drive montado), passando via `DATA_DIR`. Resultados `results/*.json` são baixados ou commitados manualmente após a execução `full`.
- **Sessões longas:** notebooks com `full > 60 min` salvam checkpoints e retomam de onde pararam.

---

## 15. Estilo de escrita

- Segunda pessoa, direto ("Use X quando..."). Frases curtas.
- Toda recomendação traz a condição em que vale ("para < 100k linhas", "quando a latência importa").
- Números vêm dos resultados; nada de "muito mais rápido" sem medição.
- Uma ideia por parágrafo; tabelas para comparação; Mermaid para fluxo.
- Citações: link no texto + entrada em Referências.

---

## 16. Ferramentas e fluxo de trabalho

### 16.1 Primeira vez

```bash
make setup                       # uv sync --all-extras + hooks do pre-commit
# editar config/cookbook.yml: github_repo: <seu-usuario>/ds-ai-cookbook
make set-repo                    # atualiza badges do Colab e instalações nos notebooks
make docs                        # site local em http://127.0.0.1:8000
```

### 16.2 Escrever uma receita

```bash
make promote ID=N1.01            # planned → draft: copia templates, preenche ID, títulos e links do Colab
# 1. renomear stack e notebook (01-todo-stack.ipynb → 01-<stack>.ipynb) e atualizar recipe.yaml
# 2. escrever os notebooks; testar com
make smoke ID=N1.01              # papermill em modo smoke, cwd = pasta da receita
# 3. rodar o modo full no Colab e commitar results/*.full.json
make render                      # quadro-resumo, benchmark, resultados por camada, catálogos
make validate                    # draft: TODO/placeholders viram avisos; review/done: erros
```

Ao terminar: `status: review` no YAML, revisar (técnica + tradução), depois `status: done` e `last_verified`.

### 16.3 O que é gerado (não editar à mão)

| Arquivo | Gerado por | A partir de |
|---|---|---|
| `.zensical.<lang>.toml` (ignorado pelo git) | `build_site.py` | `config/site.base.toml` + navegação por idioma + seletor de idioma |
| catálogos de parte, seção, grupo e projetos | `render.py` | `part.yaml`, `group.yaml`, YAML dos itens |
| blocos `SUMMARY`, `BENCHMARK`, `PROGRESS` | `render.py` | YAML dos itens + `results/*.full.json` |
| pastas `planned` e páginas-esqueleto | `scaffold.py init` | `INDEX.md` (uma vez; nunca sobrescreve) |
| branch `colab` | `colab.yml` | notebooks-fonte |

O pre-commit roda `render` e `validate`; o CI falha se algo gerado estiver desatualizado (`render.py --check`).

### 16.4 Site (Zensical)

O site usa o [Zensical](https://zensical.org), sucessor do Material for MkDocs. Como ele aceita um idioma por site e não executa plugins de terceiros (como o antigo `mkdocs-static-i18n`), `tools/build_site.py`:

1. monta `build/site-src/<lang>/` com links simbólicos (`index.pt.md` → `index.md`), deixando de fora o outro idioma, notebooks, YAML e JSON;
2. gera `.zensical.<lang>.toml` a partir de `config/site.base.toml`, com idioma, navegação e seletor de idioma (`extra.alternate`);
3. compila PT em `site/` e EN em `site/en/`, em modo estrito.

`docs/assets/javascripts/lang-switch.js` faz o seletor levar à **mesma página** no outro idioma (supõe o site na raiz do domínio; ajuste se publicar em subcaminho). Cada parte e seção tem página de catálogo que funciona como índice na navegação (`navigation.indexes`), e a navegação é podada (`navigation.prune`): com 641 itens, sem poda o site passaria de 500 MB. O cabeçalho das páginas **não** leva `status` (chave reservada pelo tema); o status vive só no YAML. O Zensical está em versão 0.x: atualize com `uv lock --upgrade-package zensical` e rode `make docs-build`.

### 16.5 Datasets

Novos datasets entram em `src/cookbook/data.py` via `register(DatasetSpec(...))` (bases de domínio podem ter módulo próprio, como `cookbook.home_credit`, que registra a base real e o gêmeo sintético). Depois do primeiro download verificado, preencha o `sha256`. O dataset `synthetic-credit` é gerado localmente e serve só para testes, CI e smoke.
