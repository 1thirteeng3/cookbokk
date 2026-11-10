.PHONY: help set-repo setup hooks scaffold promote validate render check test test-all smoke docs docs-build split lint format outdated

RUN := uv run

help:            ## Lista os comandos / List commands
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

setup:           ## Cria o ambiente (.venv) com todos os extras e instala os hooks
	uv sync --all-extras
	$(RUN) pre-commit install

set-repo:        ## Aponta badges do Colab e instalações para o github_repo de config/cookbook.yml
	$(RUN) python tools/set_repo.py

scaffold:        ## Cria pastas planejadas a partir do INDEX.md (não sobrescreve)
	$(RUN) python tools/scaffold.py init
	$(RUN) python tools/render.py

promote:         ## Promove um item para rascunho: make promote ID=N1.01
	$(RUN) python tools/scaffold.py promote $(ID)
	$(RUN) python tools/render.py

roadmap:         ## Regenera ROADMAP.md e config/roadmap.yml (ordem de implementação)
	$(RUN) python tools/roadmap.py

validate:        ## Valida metadados, docs, notebooks e resultados
	$(RUN) python tools/validate.py

render:          ## Regenera catálogos, quadros-resumo e resultados
	$(RUN) python tools/render.py

check: lint validate  ## Tudo que o CI verifica, menos notebooks e site
	$(RUN) python tools/render.py --check
	$(RUN) python tools/roadmap.py --check
	$(RUN) pytest -m "not slow"

test:            ## Testes rápidos
	$(RUN) pytest -m "not slow"

test-all:        ## Todos os testes (inclui execução de notebook e build do site)
	$(RUN) pytest

smoke:           ## Executa notebooks em modo smoke: make smoke ID=N1.01 (ou ID=--all)
	$(RUN) python tools/run_notebooks.py $(ID)

smoke-offline:   ## Igual a smoke, com gêmeos sintéticos (sem download): make smoke-offline ID=P1.01
	$(RUN) python tools/run_notebooks.py --offline $(ID)

outdated:        ## Lista itens além do ciclo de revisão
	$(RUN) python tools/validate.py --outdated

split:           ## Gera versões pt/en dos notebooks em build/colab
	$(RUN) python tools/split_notebooks.py docs build/colab

docs:            ## Prévia local do site em PT (make docs LANG_SITE=en para inglês)
	$(RUN) python tools/build_site.py serve --lang $(or $(LANG_SITE),pt)

docs-build:      ## Build dos dois sites com Zensical (site/ e site/en/), modo estrito
	$(RUN) python tools/build_site.py build

lint:            ## Ruff
	$(RUN) ruff check src tools tests docs

format:          ## Formata código e notebooks
	$(RUN) ruff format src tools tests docs
	$(RUN) ruff check --fix src tools tests docs
