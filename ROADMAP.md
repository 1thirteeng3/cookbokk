# Roadmap de implementação

> Gerado por `tools/roadmap.py` a partir do catálogo. Não edite à mão: mude as regras no script e rode `make roadmap`.

Este roteiro ordena **todos os 641 itens** do cookbook (587 receitas e 54 projetos integradores) em 15 ondas, com número de ordem único de 1 a 641.

## 1. Como a ordem foi decidida

1. **Quem já é citado vem primeiro.** O projeto-piloto (P1.01) aponta para 22 receitas que ainda não existem. Escrevê-las fecha o piloto e dá resultados reais para citar.
2. **Fundações antes de aplicações.** A Parte A e toda receita usada por 4 ou mais projetos formam o núcleo, para que nenhum projeto reescreva uma técnica básica.
3. **Projetos puxam as receitas de que precisam.** Do crédito ao socioeconômico, cada projeto integrador espera as receitas que ele cita e só então é escrito. Uma receita é escrita para o primeiro projeto que a usa. Assim, cada onda termina com um playbook completo e utilizável.
4. **Finanças, economia e socioeconomia primeiro**, como definido no índice: P1 a P6 antes de P7 (outros domínios).
5. **O que nenhum projeto exige entra por último**, agrupado por parte (cobertura).
6. **Dentro de cada grupo**, a ordem é por parte e seção, do nível L1 ao L4.

## 2. Resumo das ondas

| Onda | Foco | Receitas | Projetos | Pontos | Acumulado |
|---|---|---:|---:|---:|---:|
| [W0](#w0-piloto-fechado) | Piloto fechado | 22 | 1 | 61 | 23/641 (3%) |
| [W1](#w1-nucleo-transversal) | Núcleo transversal | 60 | 0 | 159 | 83/641 (12%) |
| [W2](#w2-credito) | Crédito | 55 | 9 | 227 | 147/641 (22%) |
| [W3](#w3-fraude-pldaml-e-compliance) | Fraude, PLD/AML e compliance | 37 | 5 | 149 | 189/641 (29%) |
| [W4](#w4-mercados-e-tesouraria) | Mercados e tesouraria | 66 | 8 | 263 | 263/641 (41%) |
| [W5](#w5-macroeconomia) | Macroeconomia | 37 | 7 | 167 | 307/641 (47%) |
| [W6](#w6-socioeconomia-e-politicas-publicas) | Socioeconomia e políticas públicas | 34 | 9 | 175 | 350/641 (54%) |
| [W7](#w7-plataformas-i-dados-e-mlops) | Plataformas I: dados e MLOps | 39 | 2 | 125 | 391/641 (60%) |
| [W8](#w8-plataformas-ii-llmops-dataops-e-atendimento) | Plataformas II: LLMOps, DataOps e atendimento | 63 | 3 | 203 | 457/641 (71%) |
| [W9](#w9-plataformas-iii-ia-financeira-e-auditoria) | Plataformas III: IA financeira e auditoria | 23 | 4 | 112 | 484/641 (75%) |
| [W10](#w10-outros-dominios) | Outros domínios | 31 | 6 | 145 | 521/641 (81%) |
| [W11](#w11-cobertura-dados-e-ml-classico) | Cobertura: dados e ML clássico | 49 | 0 | 111 | 570/641 (88%) |
| [W12](#w12-cobertura-deep-learning-e-ia) | Cobertura: deep learning e IA | 38 | 0 | 109 | 608/641 (94%) |
| [W13](#w13-cobertura-auditoria-e-dominio) | Cobertura: auditoria e domínio | 22 | 0 | 62 | 630/641 (98%) |
| [W14](#w14-cobertura-ciencias-generativas) | Cobertura: ciências generativas | 11 | 0 | 32 | 641/641 (100%) |
| **Total** | | **587** | **54** | **2100** | |

**Pontos** medem esforço relativo, não horas: receita L1 = 1, L2 = 2, L3 = 3, L4 = 4; projeto integrador = 8. O P1.01 serve de referência para o projeto.

## 3. Ritmo e prazo

O prazo depende do ritmo, e ele só é conhecido depois da onda 0. Por isso a tabela abaixo é um cenário, não uma previsão: **meça os pontos concluídos por mês na W0 e substitua o ritmo.**

| Ritmo (pontos/mês) | Prazo total | Prazo até o fim da W10 (todos os projetos) |
|---:|---:|---:|
| 20 (≈ 7 receitas L3) | 8,8 anos (105 meses) | 7,4 anos (89 meses) |
| 40 (≈ 13 receitas L3) | 4,4 anos (52 meses) | 3,7 anos (45 meses) |
| 80 (≈ 27 receitas L3) | 2,2 anos (26 meses) | 1,9 anos (22 meses) |

Como referência de escala, 2100 pontos são uma obra de muitos meses mesmo no ritmo mais alto. Se isso for demais, as duas saídas honestas são cortar escopo (parar após a W10 e tratar as ondas de cobertura como opcionais) ou reduzir a profundidade das receitas de L1 e L2. Essa escolha é sua e vale decidir depois de medir o ritmo.

## 4. Regras do roadmap

- **Fim de onda:** nada da onda seguinte começa em definitivo antes do critério de saída da atual. Pode-se adiantar rascunhos.
- **Replanejar a cada onda:** ao fechar uma onda, medir o ritmo real, rever prioridades e rodar `make roadmap`.
- **Mudança de prioridade:** edite `PROJECT_WAVES` ou `COVERAGE_WAVES` em `tools/roadmap.py`. O `--check` garante que nenhum item some ou se repete.
- **Revisões periódicas** (SPEC §12) continuam valendo para o que já está pronto e competem por tempo com a escrita nova.

## 5. Ondas

### W0 · Piloto fechado

Escrever as receitas que o P1.01 já cita, para os links do piloto levarem a conteúdo. **22 receitas e 1 projeto, 61 pontos.**

**Critério de saída:** As 22 receitas passam no `make check`, cumprem a Definição de Pronto (SPEC §9) e todos os links do P1.01 resolvem. Anotar o tempo real gasto por receita: ele calibra o prazo de todas as ondas seguintes.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 1 | C2.06 | L3 | Features de agregação e relacionais | citada por P1.01 |
| 2 | D1.03 | L2 | Escolher métricas | citada por P1.01 |
| 3 | D1.07 | L2 | Ajuste de threshold e decisão sob custo | citada por P1.01 |
| 4 | D1.06 | L3 | Calibração de probabilidades | citada por P1.01 |
| 5 | D2.14 | L4 | Deep learning tabular SOTA | citada por P1.01 |
| 6 | G1.02 | L2 | API de inferência online | citada por P1.01 |
| 7 | G1.04 | L2 | Containerização | citada por P1.01 |
| 8 | G2.03 | L2 | Registro de modelos | citada por P1.01 |
| 9 | G3.02 | L3 | Detectar data drift e concept drift | citada por P1.01 |
| 10 | H3.01 | L2 | Interpretabilidade de modelos | citada por P1.01 |
| 11 | H3.04 | L3 | Equidade e viés algorítmico | citada por P1.01 |
| 12 | M2.02 | L2 | Protocolo de validação | citada por P1.01 |
| 13 | M2.03 | L2 | Métricas e alinhamento com o negócio | citada por P1.01 |
| 14 | M2.06 | L2 | Explicabilidade e documentação | citada por P1.01 |
| 15 | M2.07 | L2 | Reprodutibilidade | citada por P1.01 |
| 16 | M2.05 | L3 | Fairness | citada por P1.01 |
| 17 | M2.10 | L3 | Monitoramento e operação pós-deploy | citada por P1.01 |
| 18 | N1.01 | L1 | Scorecard de concessão com WoE/IV | citada por P1.01 |
| 19 | N1.02 | L2 | Scorecard com GBM e explicabilidade regulatória | citada por P1.01 |
| 20 | N1.12 | L2 | Validação de modelos de risco (backtesting, estabilidade) | citada por P1.01 |
| 21 | N1.03 | L3 | Inferência de rejeitados | citada por P1.01 |
| 22 | N6.04 | L3 | Gestão de risco de modelos no setor financeiro | citada por P1.01 |
| 23 | P1.01 | — | Motor de concessão de crédito E2E: scorecard → GBM → decisão → monitoramento | piloto (já concluído) |

### W1 · Núcleo transversal

Parte A inteira e toda receita usada por 4+ projetos. **60 receitas e 0 projetos, 159 pontos.**

**Critério de saída:** Núcleo `done`. Nenhum projeto das ondas seguintes precisa reescrever uma técnica do núcleo.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 24 | A1.01 | L1 | Configurar ambiente Python reprodutível | fundação (Parte A) |
| 25 | A1.02 | L1 | Configurar GPU local e em nuvem | fundação (Parte A) |
| 26 | A1.03 | L1 | Estruturar um repositório de projeto DS/ML | fundação (Parte A) |
| 27 | A1.04 | L2 | Versionar código, dados e modelos | fundação (Parte A) |
| 28 | A1.05 | L2 | Garantir determinismo e seeds | fundação (Parte A) |
| 29 | A1.06 | L2 | Qualidade de código e testes para ML | fundação (Parte A) |
| 30 | A1.07 | L2 | Notebooks em produção | fundação (Parte A) |
| 31 | A1.08 | L3 | Profiling de código e uso de recursos | fundação (Parte A) |
| 32 | A1.09 | L3 | Computação eficiente em Python (dados) | fundação (Parte A) |
| 33 | A2.01 | L1 | Carregar e inspecionar dados tabulares | fundação (Parte A) |
| 34 | A2.03 | L1 | Tipos de dados, datas, texto e encoding | fundação (Parte A) |
| 35 | A2.04 | L1 | Estatística descritiva e inferência básica | fundação (Parte A) |
| 36 | A2.02 | L2 | Escolher formato de arquivo | fundação (Parte A) |
| 37 | A2.05 | L2 | Probabilidade e simulação (Monte Carlo, bootstrap) | fundação (Parte A) |
| 38 | A2.07 | L2 | Álgebra linear e otimização na prática | fundação (Parte A) |
| 39 | A2.06 | L3 | Inferência bayesiana prática | fundação (Parte A) |
| 40 | B5.01 | L1 | Agendar um pipeline simples | usada por 4 projetos |
| 41 | B5.10 | L4 | Plataforma de dados self-service | usada por 4 projetos |
| 42 | C2.08 | L3 | Features geográficas | usada por 4 projetos |
| 43 | D4.01 | L1 | Previsão univariada baseline | usada por 4 projetos |
| 44 | D4.02 | L2 | Previsão com ML | usada por 4 projetos |
| 45 | D4.03 | L2 | Previsão com bibliotecas dedicadas | usada por 4 projetos |
| 46 | D4.10 | L2 | Backtesting e avaliação em séries | usada por 5 projetos |
| 47 | D4.04 | L3 | Previsão com deep learning | usada por 5 projetos |
| 48 | D4.06 | L3 | Previsão hierárquica e reconciliação | usada por 5 projetos |
| 49 | D4.07 | L3 | Previsão probabilística | usada por 7 projetos |
| 50 | D4.08 | L3 | Demanda intermitente | usada por 4 projetos |
| 51 | D4.09 | L3 | Previsão multivariada e com regressores exógenos | usada por 5 projetos |
| 52 | D4.11 | L3 | Previsão de demanda E2E (varejo) | usada por 4 projetos |
| 53 | D4.12 | L3 | Mudanças estruturais e change point | usada por 4 projetos |
| 54 | D4.05 | L4 | Foundation models para séries | usada por 6 projetos |
| 55 | E2.06 | L3 | OCR e documentos | usada por 5 projetos |
| 56 | E2.09 | L4 | Vídeo (classificação, ação, tracking) | usada por 4 projetos |
| 57 | F2.01 | L2 | RAG básico E2E | usada por 4 projetos |
| 58 | F2.02 | L2 | Estratégias de chunking | usada por 4 projetos |
| 59 | F2.03 | L2 | Escolher embeddings | usada por 4 projetos |
| 60 | F2.04 | L3 | Busca híbrida e reranking | usada por 4 projetos |
| 61 | F2.05 | L3 | Query transformation | usada por 4 projetos |
| 62 | F2.06 | L3 | RAG sobre dados estruturados (text-to-SQL) | usada por 5 projetos |
| 63 | F2.07 | L3 | RAG sobre documentos complexos (PDF, tabelas, imagens) | usada por 4 projetos |
| 64 | F2.10 | L3 | Avaliação de RAG | usada por 4 projetos |
| 65 | F2.08 | L4 | GraphRAG e knowledge graphs | usada por 4 projetos |
| 66 | F2.09 | L4 | RAG agentico e multi-hop | usada por 4 projetos |
| 67 | F2.11 | L4 | RAG em produção: atualização, ACL, multi-tenant | usada por 4 projetos |
| 68 | F2.12 | L4 | Memória de longo prazo para agentes e assistentes | usada por 4 projetos |
| 69 | F6.01 | L2 | Construir um conjunto de avaliação (golden set) | usada por 6 projetos |
| 70 | F6.02 | L3 | LLM-as-a-judge | usada por 7 projetos |
| 71 | F6.03 | L3 | Frameworks de eval | usada por 6 projetos |
| 72 | F6.05 | L3 | Observabilidade e tracing de LLM | usada por 6 projetos |
| 73 | F6.06 | L3 | Guardrails e validação de saída | usada por 6 projetos |
| 74 | F6.09 | L3 | Alucinação: detecção e mitigação | usada por 6 projetos |
| 75 | F6.10 | L3 | Vieses, equidade e IA responsável em LLMs | usada por 6 projetos |
| 76 | F6.11 | L3 | Testes de regressão contínuos de prompts e modelos | usada por 6 projetos |
| 77 | F6.12 | L3 | Privacidade, PII e conformidade em apps de IA | usada por 6 projetos |
| 78 | F6.13 | L3 | Feedback de usuários e melhoria contínua | usada por 6 projetos |
| 79 | F6.04 | L4 | Avaliação de agentes | usada por 6 projetos |
| 80 | F6.07 | L4 | Prompt injection e segurança de agentes | usada por 7 projetos |
| 81 | F6.08 | L4 | Red teaming e testes adversariais | usada por 6 projetos |
| 82 | G1.03 | L2 | Inferência em lote | usada por 4 projetos |
| 83 | G1.10 | L3 | Inferência em borda/mobile | usada por 4 projetos |

### W2 · Crédito

Fechar a vertical de crédito e risco de crédito (P1.02–P1.10). **55 receitas e 9 projetos, 227 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 84 | D2.13 | L3 | Survival analysis e churn | puxada por P1.02 |
| 85 | N1.04 | L3 | Modelos PD, LGD e EAD | puxada por P1.02 |
| 86 | N1.05 | L4 | Perda esperada IFRS 9 / CPC 48 / Resolução CMN 4.966 | puxada por P1.02 |
| 87 | N1.14 | L4 | Testes de estresse de crédito | puxada por P1.02 |
| 88 | N4.01 | L1 | Dados macroeconômicos brasileiros | puxada por P1.02 |
| 89 | P1.02 | — | Modelos PD/LGD/EAD e perda esperada IFRS 9 com cenários macro | projeto integrador |
| 90 | B2.08 | L3 | Processamento de dados geoespaciais | puxada por P1.03 |
| 91 | D2.08 | L3 | Regressão quantílica e intervalos de predição | puxada por P1.03 |
| 92 | N1.09 | L3 | Avaliação automática de imóveis (AVM) para garantias | puxada por P1.03 |
| 93 | N1.10 | L3 | Crédito com garantia (home equity, auto) | puxada por P1.03 |
| 94 | N5.11 | L3 | Mercado imobiliário e acessibilidade habitacional | puxada por P1.03 |
| 95 | P1.03 | — | AVM de imóveis para crédito com garantia | projeto integrador |
| 96 | D6.06 | L3 | Pesquisa operacional + ML | puxada por P1.04 |
| 97 | H1.01 | L2 | Teste A/B do zero | puxada por P1.04 |
| 98 | H1.02 | L3 | Problemas comuns em experimentos | puxada por P1.04 |
| 99 | H1.03 | L3 | Redução de variância (CUPED) | puxada por P1.04 |
| 100 | H1.04 | L3 | Testes sequenciais e bayesianos | puxada por P1.04 |
| 101 | H1.05 | L4 | Experimentos em marketplaces e redes | puxada por P1.04 |
| 102 | H2.01 | L3 | Inferência causal com dados observacionais | puxada por P1.04 |
| 103 | H2.03 | L3 | Uplift modeling | puxada por P1.04 |
| 104 | L1.04 | L3 | Estimar efeitos causais com deep learning | puxada por P1.04 |
| 105 | N1.07 | L4 | Precificação baseada em risco e elasticidade | puxada por P1.04 |
| 106 | P1.04 | — | Precificação de crédito baseada em risco com elasticidade causal | projeto integrador |
| 107 | D5.07 | L3 | Bandits e exploração | puxada por P1.05 |
| 108 | N1.08 | L3 | Cobrança e recuperação | puxada por P1.05 |
| 109 | P1.05 | — | Cobrança inteligente: survival, uplift e otimização da régua | projeto integrador |
| 110 | C2.09 | L3 | Features de grafo | puxada por P1.06 |
| 111 | N1.11 | L3 | Crédito para PMEs com dados alternativos | puxada por P1.06 |
| 112 | N2.06 | L1 | Categorização de transações | puxada por P1.06 |
| 113 | N6.01 | L3 | Integração com Open Finance Brasil | puxada por P1.06 |
| 114 | P1.06 | — | Crédito PME com Open Finance e dados alternativos | projeto integrador |
| 115 | F1.04 | L2 | Saídas estruturadas | puxada por P1.07 |
| 116 | F3.12 | L3 | Automação de documentos e backoffice | puxada por P1.07 |
| 117 | M4.01 | L2 | Escolha de modelos e arquitetura da solução | puxada por P1.07 |
| 118 | M4.02 | L2 | Prompts e system prompts | puxada por P1.07 |
| 119 | M4.03 | L3 | Pipelines RAG | puxada por P1.07 |
| 120 | M4.04 | L3 | Cobertura e qualidade dos evals | puxada por P1.07 |
| 121 | M4.06 | L3 | Alucinação e factualidade | puxada por P1.07 |
| 122 | M4.07 | L3 | Fluxo de dados e privacidade em apps LLM | puxada por P1.07 |
| 123 | M4.09 | L3 | Conformidade regulatória de sistemas de IA | puxada por P1.07 |
| 124 | M4.05 | L4 | Segurança de aplicações LLM | puxada por P1.07 |
| 125 | M4.08 | L4 | Fine-tuning e dados de instrução | puxada por P1.07 |
| 126 | N6.06 | L3 | Uso de IA generativa em instituições financeiras | puxada por P1.07 |
| 127 | P1.07 | — | Underwriting assistido por LLM: documentos → parecer → auditoria | projeto integrador |
| 128 | C1.03 | L2 | Dashboards e data apps | puxada por P1.08 |
| 129 | N1.13 | L3 | Early warning e monitoramento de carteira | puxada por P1.08 |
| 130 | P1.08 | — | Early warning e monitoramento de carteira por safras | projeto integrador |
| 131 | M0.01 | L1 | Metodologia de auditoria técnica | puxada por P1.09 |
| 132 | M0.04 | L1 | Relatório de auditoria e plano de remediação | puxada por P1.09 |
| 133 | M0.02 | L2 | Frameworks e normas de referência | puxada por P1.09 |
| 134 | M0.03 | L2 | Matriz de riscos e severidade de achados | puxada por P1.09 |
| 135 | M0.05 | L3 | Modelos de maturidade e scorecards | puxada por P1.09 |
| 136 | M0.06 | L3 | Auditoria assistida por LLMs e agentes | puxada por P1.09 |
| 137 | M0.07 | L4 | Auditoria contínua (audit-as-code, policy-as-code) | puxada por P1.09 |
| 138 | M2.01 | L2 | Dados de treino | puxada por P1.09 |
| 139 | M2.08 | L2 | Código e testes de ML | puxada por P1.09 |
| 140 | M2.04 | L3 | Robustez e estabilidade | puxada por P1.09 |
| 141 | M2.09 | L3 | Validação independente (model risk management) | puxada por P1.09 |
| 142 | M2.11 | L4 | Auditoria caixa-preta | puxada por P1.09 |
| 143 | N5.10 | L3 | Inclusão financeira e fairness no acesso a crédito | puxada por P1.09 |
| 144 | P1.09 | — | Auditoria completa de um modelo de crédito | projeto integrador |
| 145 | N4.02 | L2 | Econometria de séries temporais | puxada por P1.10 |
| 146 | N4.04 | L3 | Previsão de inflação | puxada por P1.10 |
| 147 | P1.10 | — | Stress testing de carteira com modelos satélite | projeto integrador |

### W3 · Fraude, PLD/AML e compliance

Fechar a vertical de fraude e conformidade (P2). **37 receitas e 5 projetos, 149 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 148 | B3.01 | L2 | Primeiro pipeline de streaming | puxada por P2.01 |
| 149 | B3.02 | L3 | Processar streams com estado e janelas | puxada por P2.01 |
| 150 | B3.03 | L3 | Semânticas de entrega (at-least/exactly-once) | puxada por P2.01 |
| 151 | B3.04 | L3 | Late data, watermarks e reordenação | puxada por P2.01 |
| 152 | B3.05 | L3 | Schema registry e evolução de schemas | puxada por P2.01 |
| 153 | B3.07 | L3 | Analytics em tempo real (OLAP streaming) | puxada por P2.01 |
| 154 | B3.06 | L4 | Feature computation em tempo real | puxada por P2.01 |
| 155 | B3.08 | L4 | Streaming para inferência de ML | puxada por P2.01 |
| 156 | C2.11 | L4 | Feature store | puxada por P2.01 |
| 157 | D3.08 | L3 | Detecção de fraude | puxada por P2.01 |
| 158 | G1.01 | L1 | Empacotar um modelo | puxada por P2.01 |
| 159 | G1.05 | L3 | Deploy em Kubernetes | puxada por P2.01 |
| 160 | G1.06 | L3 | Deploy serverless de modelos | puxada por P2.01 |
| 161 | G1.07 | L3 | Plataformas gerenciadas | puxada por P2.01 |
| 162 | G1.08 | L3 | Estratégias de release | puxada por P2.01 |
| 163 | G1.09 | L3 | Otimização de latência e throughput | puxada por P2.01 |
| 164 | G1.11 | L4 | Serving de múltiplos modelos | puxada por P2.01 |
| 165 | G3.01 | L2 | Monitorar performance e saúde do serviço | puxada por P2.01 |
| 166 | G3.04 | L3 | Loops de feedback e rotulagem tardia | puxada por P2.01 |
| 167 | G3.05 | L3 | Resposta a incidentes de ML | puxada por P2.01 |
| 168 | G3.06 | L3 | Monitoramento de custos de ML | puxada por P2.01 |
| 169 | G3.07 | L3 | Monitoramento de LLMs em produção | puxada por P2.01 |
| 170 | G3.03 | L4 | Monitoramento sem rótulos | puxada por P2.01 |
| 171 | N2.01 | L2 | Fraude de transação (cartão, Pix) | puxada por P2.01 |
| 172 | P2.01 | — | Antifraude de transações em tempo real (cartão, Pix) | projeto integrador |
| 173 | B2.09 | L3 | Processamento de grafos | puxada por P2.02 |
| 174 | D6.01 | L3 | Aprendizado em grafos | puxada por P2.02 |
| 175 | N2.04 | L3 | PLD/AML com grafos | puxada por P2.02 |
| 176 | N2.05 | L3 | Redução de falsos positivos em alertas AML | puxada por P2.02 |
| 177 | P2.02 | — | PLD/AML com grafos e GNNs | projeto integrador |
| 178 | F1.09 | L2 | Multimodal com LLMs (imagem, PDF, áudio) | puxada por P2.03 |
| 179 | N2.02 | L3 | Fraude de aplicação e identidade sintética | puxada por P2.03 |
| 180 | N2.03 | L4 | Fraude documental e deepfake no onboarding | puxada por P2.03 |
| 181 | P2.03 | — | Onboarding seguro: KYC, fraude documental e deepfake | projeto integrador |
| 182 | B1.08 | L3 | Ingestão de dados não estruturados em escala (PDF, imagem, áudio, vídeo) | puxada por P2.04 |
| 183 | N2.07 | L3 | RegTech: interpretação de normas com LLM | puxada por P2.04 |
| 184 | P2.04 | — | Assistente regulatório RAG (BCB, CVM, ANPD) | projeto integrador |
| 185 | E3.01 | L1 | Classificação de texto | puxada por P2.05 |
| 186 | E4.02 | L3 | Reconhecimento de fala (ASR) | puxada por P2.05 |
| 187 | F7.04 | L3 | Classificação e triagem em escala com LLM | puxada por P2.05 |
| 188 | N2.08 | L3 | Monitoramento de conduta e comunicações | puxada por P2.05 |
| 189 | P2.05 | — | Monitoramento de conduta: ouvidoria, reclamações e chamadas | projeto integrador |

### W4 · Mercados e tesouraria

Dados de mercado, portfólio, risco de mercado e sinais de texto (P3). **66 receitas e 8 projetos, 263 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 190 | B1.01 | L1 | Ler dados de APIs REST/GraphQL | puxada por P3.01 |
| 191 | B1.03 | L1 | Ingestão de bancos relacionais (full load) | puxada por P3.01 |
| 192 | B1.06 | L1 | Ingestão de arquivos em lote (S3/GCS/ADLS/SFTP) | puxada por P3.01 |
| 193 | B1.02 | L2 | Web scraping responsável | puxada por P3.01 |
| 194 | B1.04 | L2 | Ingestão incremental | puxada por P3.01 |
| 195 | B1.07 | L2 | Ingestão de dados semiestruturados e aninhados | puxada por P3.01 |
| 196 | B1.09 | L2 | Conectores SaaS e ELT gerenciado vs custom | puxada por P3.01 |
| 197 | B1.05 | L3 | CDC (Change Data Capture) | puxada por P3.01 |
| 198 | B1.10 | L3 | Ingestão de dados de IoT e telemetria | puxada por P3.01 |
| 199 | B4.05 | L3 | Data lake e lakehouse | puxada por P3.01 |
| 200 | B5.02 | L2 | DAGs robustos: retries, idempotência, backfill | puxada por P3.01 |
| 201 | B5.04 | L2 | Testes e contratos de dados | puxada por P3.01 |
| 202 | B5.03 | L3 | Orquestração baseada em assets e eventos | puxada por P3.01 |
| 203 | B5.05 | L3 | Observabilidade de dados | puxada por P3.01 |
| 204 | B5.06 | L3 | Linhagem e documentação de dados | puxada por P3.01 |
| 205 | B5.07 | L3 | Governança, PII, LGPD/GDPR | puxada por P3.01 |
| 206 | B5.08 | L3 | CI/CD para pipelines de dados | puxada por P3.01 |
| 207 | B5.09 | L3 | Infraestrutura como código para dados | puxada por P3.01 |
| 208 | B5.11 | L4 | Migração de plataformas de dados | puxada por P3.01 |
| 209 | N3.01 | L1 | Dados de mercado e ajustes corporativos | puxada por P3.01 |
| 210 | N3.02 | L3 | Backtesting sem vieses | puxada por P3.01 |
| 211 | P3.01 | — | Pipeline de dados de mercado + backtesting sem vieses | projeto integrador |
| 212 | D1.08 | L3 | Comparar modelos com rigor estatístico | puxada por P3.02 |
| 213 | N3.03 | L2 | Previsão de volatilidade | puxada por P3.02 |
| 214 | N3.04 | L2 | Otimização de portfólio | puxada por P3.02 |
| 215 | N3.10 | L3 | Fatores e alphas | puxada por P3.02 |
| 216 | P3.02 | — | Gestão de portfólio E2E: retorno, risco, otimização | projeto integrador |
| 217 | N3.05 | L3 | Risco de mercado: VaR e Expected Shortfall | puxada por P3.03 |
| 218 | N3.06 | L3 | Curva de juros | puxada por P3.03 |
| 219 | P3.03 | — | Risco de mercado: VaR/ES com backtesting regulatório | projeto integrador |
| 220 | E5.01 | L3 | Implementar Transformer do zero | puxada por P3.04 |
| 221 | E5.02 | L3 | Treino com mixed precision | puxada por P3.04 |
| 222 | E5.03 | L3 | Treino distribuído de dados (DDP) | puxada por P3.04 |
| 223 | E5.05 | L3 | Otimização de memória | puxada por P3.04 |
| 224 | E5.06 | L3 | Otimização de throughput de dados | puxada por P3.04 |
| 225 | E5.11 | L3 | Compressão: quantização, poda, destilação | puxada por P3.04 |
| 226 | E5.04 | L4 | Paralelismo de modelo, pipeline e tensor | puxada por P3.04 |
| 227 | E5.07 | L4 | Compilação e kernels | puxada por P3.04 |
| 228 | E5.08 | L4 | Treino em TPUs e clusters | puxada por P3.04 |
| 229 | E5.09 | L4 | Scaling laws e planejamento de compute | puxada por P3.04 |
| 230 | E5.10 | L4 | Arquiteturas alternativas ao Transformer | puxada por P3.04 |
| 231 | E5.12 | L4 | Tolerância a falhas e checkpointing | puxada por P3.04 |
| 232 | L5.03 | L3 | Physics-Informed Neural Networks (PINNs) | puxada por P3.04 |
| 233 | L5.04 | L4 | Neural operators | puxada por P3.04 |
| 234 | N3.07 | L4 | Precificação de derivativos com ML | puxada por P3.04 |
| 235 | P3.04 | — | Precificação de derivativos com PINNs e neural SDEs | projeto integrador |
| 236 | N3.09 | L3 | NLP financeiro | puxada por P3.05 |
| 237 | P3.05 | — | Sinais a partir de texto: notícias, fatos relevantes, resultados | projeto integrador |
| 238 | F3.01 | L2 | Tool use | puxada por P3.06 |
| 239 | F3.02 | L2 | Primeiro agente (loop ReAct) | puxada por P3.06 |
| 240 | F3.03 | L3 | Model Context Protocol (MCP) | puxada por P3.06 |
| 241 | F3.04 | L3 | Workflows vs agentes autônomos | puxada por P3.06 |
| 242 | F3.07 | L3 | Humano no loop e aprovações | puxada por P3.06 |
| 243 | F3.11 | L3 | Agentes para dados (analista de dados / SQL / BI) | puxada por P3.06 |
| 244 | F3.05 | L4 | Sistemas multiagente | puxada por P3.06 |
| 245 | F3.06 | L4 | Agentes de código e uso de computador | puxada por P3.06 |
| 246 | F3.08 | L4 | Estado, persistência e execução durável | puxada por P3.06 |
| 247 | F3.09 | L4 | Planejamento, reflexão e auto-correção | puxada por P3.06 |
| 248 | F3.10 | L4 | Confiabilidade de agentes | puxada por P3.06 |
| 249 | F7.10 | L4 | Pesquisa profunda (deep research agents) | puxada por P3.06 |
| 250 | P3.06 | — | Agente de equity research com fontes citadas | projeto integrador |
| 251 | D6.05 | L3 | Aprendizado por reforço clássico | puxada por P3.07 |
| 252 | L2.14 | L3 | Calibrar modelos epidemiológicos e baseados em agentes | puxada por P3.07 |
| 253 | L4.04 | L3 | Arquitetura de generative agents | puxada por P3.07 |
| 254 | L4.05 | L3 | Frameworks de simulação com LLM | puxada por P3.07 |
| 255 | L4.07 | L3 | Populações sintéticas ("silicon samples") e seus limites | puxada por P3.07 |
| 256 | L4.09 | L3 | Medir emergência e propriedades macro | puxada por P3.07 |
| 257 | L4.06 | L4 | Simulação social e de mercado com LLMs | puxada por P3.07 |
| 258 | L4.08 | L4 | ABMs híbridos regras + LLM para escala e custo | puxada por P3.07 |
| 259 | L4.10 | L4 | Calibrar e validar simulações multiagente | puxada por P3.07 |
| 260 | N3.11 | L4 | Microestrutura e livro de ofertas | puxada por P3.07 |
| 261 | P3.07 | — | Simulação de mercado e livro de ofertas com agentes | projeto integrador |
| 262 | N3.12 | L3 | Liquidez, ALM e fluxo de caixa | puxada por P3.08 |
| 263 | P3.08 | — | Tesouraria: previsão de fluxo de caixa e liquidez | projeto integrador |

### W5 · Macroeconomia

Nowcasting, inflação, política monetária e risco sistêmico (P4). **37 receitas e 7 projetos, 167 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 264 | N4.03 | L3 | Nowcasting de atividade | puxada por P4.01 |
| 265 | P4.01 | — | Nowcasting do PIB/IBC-Br com dados mistos | projeto integrador |
| 266 | P4.02 | — | Previsão de IPCA: econometria × ML × foundation models | projeto integrador |
| 267 | E3.02 | L1 | Análise de sentimento | puxada por P4.03 |
| 268 | E3.03 | L2 | NER e extração de informação | puxada por P4.03 |
| 269 | E3.04 | L2 | Similaridade semântica e busca | puxada por P4.03 |
| 270 | E3.05 | L2 | Sumarização | puxada por P4.03 |
| 271 | E3.06 | L3 | Tradução automática | puxada por P4.03 |
| 272 | E3.07 | L3 | QA extrativo e generativo | puxada por P4.03 |
| 273 | E3.08 | L3 | Classificação multilíngue e PT-BR | puxada por P4.03 |
| 274 | E3.10 | L3 | Tokenização | puxada por P4.03 |
| 275 | E3.11 | L3 | Moderação de conteúdo e toxicidade | puxada por P4.03 |
| 276 | E3.09 | L4 | Pré-treino de modelo de linguagem de domínio | puxada por P4.03 |
| 277 | E3.12 | L4 | Texto em escala: dedup e filtragem de corpus | puxada por P4.03 |
| 278 | N4.05 | L3 | Análise de comunicação de bancos centrais | puxada por P4.03 |
| 279 | P4.03 | — | Monitor de comunicação do Copom com LLMs | projeto integrador |
| 280 | L2.04 | L3 | Neural Posterior Estimation (NPE) | puxada por P4.04 |
| 281 | L2.05 | L3 | Neural Likelihood e Ratio Estimation (NLE, NRE) | puxada por P4.04 |
| 282 | L2.07 | L3 | Aprender estatísticas-resumo | puxada por P4.04 |
| 283 | L2.06 | L4 | SBI com difusão e flow matching | puxada por P4.04 |
| 284 | L2.08 | L4 | Validar SBI | puxada por P4.04 |
| 285 | N4.06 | L4 | Modelos DSGE e calibração | puxada por P4.04 |
| 286 | N4.07 | L4 | Macro baseada em agentes | puxada por P4.04 |
| 287 | P4.04 | — | Calibração de modelo macro (DSGE ou ABM) com SBI | projeto integrador |
| 288 | L3.09 | L3 | Síntese de grafos preservando estrutura | puxada por P4.05 |
| 289 | L4.03 | L2 | Dinâmica de redes, difusão e contágio | puxada por P4.05 |
| 290 | N4.08 | L4 | Risco sistêmico e contágio em redes financeiras | puxada por P4.05 |
| 291 | P4.05 | — | Risco sistêmico e contágio em redes financeiras | projeto integrador |
| 292 | E2.01 | L1 | Classificação de imagens | puxada por P4.06 |
| 293 | E2.02 | L2 | Transfer learning e fine-tuning | puxada por P4.06 |
| 294 | E2.03 | L2 | Data augmentation de imagens | puxada por P4.06 |
| 295 | E2.04 | L3 | Detecção de objetos | puxada por P4.06 |
| 296 | E2.05 | L3 | Segmentação semântica/instância | puxada por P4.06 |
| 297 | E2.07 | L3 | Detecção de defeitos industriais | puxada por P4.06 |
| 298 | E2.11 | L3 | Busca visual e similaridade | puxada por P4.06 |
| 299 | E2.13 | L3 | Few-shot e zero-shot em visão | puxada por P4.06 |
| 300 | E2.14 | L3 | Visão em dispositivos de borda | puxada por P4.06 |
| 301 | E2.08 | L4 | Imagens médicas | puxada por P4.06 |
| 302 | E2.10 | L4 | Estimativa de pose, profundidade e 3D | puxada por P4.06 |
| 303 | E2.12 | L4 | Modelos generativos de imagem | puxada por P4.06 |
| 304 | N4.09 | L3 | Indicadores alternativos e de alta frequência | puxada por P4.06 |
| 305 | P4.06 | — | Indicadores alternativos de atividade econômica | projeto integrador |
| 306 | N4.10 | L3 | Previsão de câmbio e juros | puxada por P4.07 |
| 307 | P4.07 | — | Previsão de câmbio e curva de juros | projeto integrador |

### W6 · Socioeconomia e políticas públicas

Avaliação de impacto, pobreza, microssimulação e mercado de trabalho (P5). **34 receitas e 9 projetos, 175 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 308 | H2.02 | L3 | Quasi-experimentos | puxada por P5.01 |
| 309 | L1.11 | L3 | Sensibilidade a confundimento não observado | puxada por P5.01 |
| 310 | N5.02 | L2 | Análise de pesquisas com desenho amostral complexo | puxada por P5.01 |
| 311 | N5.06 | L3 | Avaliação de impacto de programas sociais | puxada por P5.01 |
| 312 | P5.01 | — | Avaliação de impacto de programa de transferência de renda | projeto integrador |
| 313 | N5.03 | L2 | Desigualdade e pobreza | puxada por P5.02 |
| 314 | N5.05 | L3 | Estimação para pequenas áreas | puxada por P5.02 |
| 315 | P5.02 | — | Mapa de pobreza com satélite + censo (pequenas áreas) | projeto integrador |
| 316 | N5.01 | L1 | Microdados socioeconômicos | puxada por P5.03 |
| 317 | N5.07 | L4 | Microssimulação tributária e de transferências | puxada por P5.03 |
| 318 | P5.03 | — | Microssimulação de reforma tributária | projeto integrador |
| 319 | L1.15 | L4 | Gêmeos digitais causais | puxada por P5.04 |
| 320 | L4.01 | L1 | Fundamentos de sistemas complexos adaptativos | puxada por P5.04 |
| 321 | L4.02 | L2 | Modelagem baseada em agentes clássica | puxada por P5.04 |
| 322 | L4.12 | L3 | Teoria dos jogos computacional e design de mecanismos | puxada por P5.04 |
| 323 | L4.14 | L3 | Riscos, vieses e ética em simulações com LLM | puxada por P5.04 |
| 324 | L4.11 | L4 | Aprendizado por reforço multiagente | puxada por P5.04 |
| 325 | L4.13 | L4 | Gêmeos digitais de organizações e políticas públicas | puxada por P5.04 |
| 326 | L4.15 | L4 | Infraestrutura para simulações massivas | puxada por P5.04 |
| 327 | P5.04 | — | Simulação de políticas com generative agents | projeto integrador |
| 328 | N5.08 | L2 | Mercado de trabalho e emprego | puxada por P5.05 |
| 329 | N5.04 | L3 | Decomposição de diferenciais salariais | puxada por P5.05 |
| 330 | P5.05 | — | Mercado de trabalho: previsão de emprego e desigualdade salarial | projeto integrador |
| 331 | D3.02 | L2 | Segmentação de clientes | puxada por P5.06 |
| 332 | N5.09 | L3 | Endividamento e saúde financeira das famílias | puxada por P5.06 |
| 333 | P5.06 | — | Superendividamento das famílias: diagnóstico e alerta precoce | projeto integrador |
| 334 | L1.14 | L4 | Fairness causal e contrafactual | puxada por P5.07 |
| 335 | P5.07 | — | Inclusão financeira e equidade no acesso a crédito | projeto integrador |
| 336 | P5.08 | — | Habitação: índices de preço e acessibilidade | projeto integrador |
| 337 | H2.04 | L4 | Descoberta causal | puxada por P5.09 |
| 338 | H2.05 | L4 | Mix de marketing (MMM) e incrementalidade | puxada por P5.09 |
| 339 | L1.01 | L2 | Modelos causais estruturais (SCM) do zero | puxada por P5.09 |
| 340 | L1.08 | L2 | Explicações contrafactuais acionáveis | puxada por P5.09 |
| 341 | L1.02 | L3 | Elicitar DAGs com especialistas e LLMs | puxada por P5.09 |
| 342 | L1.03 | L3 | Descoberta causal híbrida (conhecimento + dados) | puxada por P5.09 |
| 343 | L1.06 | L3 | Inferência contrafactual (abdução, ação, predição) | puxada por P5.09 |
| 344 | L1.09 | L3 | Contrafactuais com LLMs: geração, avaliação e limites | puxada por P5.09 |
| 345 | L1.12 | L3 | Causalidade em séries temporais e sistemas dinâmicos | puxada por P5.09 |
| 346 | L1.05 | L4 | Programação probabilística causal | puxada por P5.09 |
| 347 | L1.07 | L4 | Modelos generativos contrafactuais (deep SCM) | puxada por P5.09 |
| 348 | L1.10 | L4 | Aprendizado de representações causais | puxada por P5.09 |
| 349 | L1.13 | L4 | Avaliação contrafactual de políticas e decisões | puxada por P5.09 |
| 350 | P5.09 | — | Avaliação contrafactual de política econômica | projeto integrador |

### W7 · Plataformas I: dados e MLOps

Lakehouse com Open Finance e plataforma de MLOps com gestão de risco de modelos (P6.01–P6.02). **39 receitas e 2 projetos, 125 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 351 | B2.01 | L1 | ETL local pequeno | puxada por P6.01 |
| 352 | B2.02 | L2 | Transformações SQL versionadas | puxada por P6.01 |
| 353 | B2.07 | L2 | Limpeza de dados textuais e endereços | puxada por P6.01 |
| 354 | B2.03 | L3 | Processamento distribuído batch | puxada por P6.01 |
| 355 | B2.04 | L3 | Joins, janelas e agregações em escala | puxada por P6.01 |
| 356 | B2.06 | L3 | Deduplicação e entity resolution | puxada por P6.01 |
| 357 | B2.05 | L4 | Otimização de jobs Spark | puxada por P6.01 |
| 358 | B2.10 | L4 | Pipelines de dados para texto/imagem/áudio em escala | puxada por P6.01 |
| 359 | B4.01 | L1 | Escolher o tipo de banco | puxada por P6.01 |
| 360 | B4.02 | L1 | Modelagem relacional e normalização | puxada por P6.01 |
| 361 | B4.03 | L2 | Modelagem dimensional | puxada por P6.01 |
| 362 | B4.04 | L2 | Data warehouse na nuvem | puxada por P6.01 |
| 363 | B4.06 | L3 | Catálogos e metastore | puxada por P6.01 |
| 364 | B4.07 | L3 | Particionamento, clustering e indexação | puxada por P6.01 |
| 365 | B4.08 | L3 | Otimizar PostgreSQL para analytics | puxada por P6.01 |
| 366 | B4.09 | L3 | Banco de séries temporais | puxada por P6.01 |
| 367 | B4.10 | L3 | Banco de grafos | puxada por P6.01 |
| 368 | B4.11 | L3 | Banco vetorial | puxada por P6.01 |
| 369 | B4.13 | L3 | Estratégia de custo em dados (FinOps) | puxada por P6.01 |
| 370 | B4.12 | L4 | Arquitetura (Lambda, Kappa, Medallion, Data Mesh, Data Fabric) | puxada por P6.01 |
| 371 | I1.01 | L2 | Escolher cloud e serviços de dados/ML | puxada por P6.01 |
| 372 | I1.09 | L2 | Infraestrutura local (homelab / workstation) | puxada por P6.01 |
| 373 | I1.02 | L3 | Kubernetes para dados e ML | puxada por P6.01 |
| 374 | I1.03 | L3 | Computação distribuída com Ray | puxada por P6.01 |
| 375 | I1.05 | L3 | Otimização de custo de GPU | puxada por P6.01 |
| 376 | I1.06 | L3 | Segurança de dados e modelos | puxada por P6.01 |
| 377 | I1.08 | L3 | Observabilidade full-stack | puxada por P6.01 |
| 378 | I1.10 | L3 | Sustentabilidade e eficiência energética | puxada por P6.01 |
| 379 | I1.04 | L4 | Redes, GPUs e interconexão | puxada por P6.01 |
| 380 | I1.07 | L4 | Segurança da cadeia de suprimentos de ML | puxada por P6.01 |
| 381 | N6.02 | L2 | Modelagem de dados bancários | puxada por P6.01 |
| 382 | P6.01 | — | Plataforma de dados de uma financeira (lakehouse + Open Finance) | projeto integrador |
| 383 | G2.01 | L2 | Pipeline de treino reprodutível | puxada por P6.02 |
| 384 | G2.02 | L3 | Orquestração de ML | puxada por P6.02 |
| 385 | G2.04 | L3 | CI/CD/CT para ML | puxada por P6.02 |
| 386 | G2.05 | L3 | Retreino automático e gatilhos | puxada por P6.02 |
| 387 | G2.06 | L3 | Níveis de maturidade MLOps | puxada por P6.02 |
| 388 | G2.07 | L3 | Governança de modelos e documentação | puxada por P6.02 |
| 389 | G2.09 | L3 | Reprodutibilidade de modelos e auditoria | puxada por P6.02 |
| 390 | G2.08 | L4 | Plataforma interna de ML | puxada por P6.02 |
| 391 | P6.02 | — | Plataforma de MLOps com gestão de risco de modelos | projeto integrador |

### W8 · Plataformas II: LLMOps, DataOps e atendimento

LLMOps regulado, DataOps e agente de atendimento com auditoria (P6.03–P6.05). **63 receitas e 3 projetos, 203 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 392 | J1.01 | L1 | Versionar prompts como código | puxada por P6.03 |
| 393 | J1.02 | L2 | Gerenciar configurações de LLM | puxada por P6.03 |
| 394 | J1.03 | L2 | Ambientes dev/staging/prod para apps de LLM | puxada por P6.03 |
| 395 | J1.04 | L3 | Migrar de modelo ou de provedor | puxada por P6.03 |
| 396 | J1.05 | L3 | Reduzir dependência de provedor (lock-in) | puxada por P6.03 |
| 397 | J1.06 | L4 | Ciclo de vida de modelos fine-tuned e adapters | puxada por P6.03 |
| 398 | J2.01 | L2 | Testes unitários e de contrato em chamadas de LLM | puxada por P6.03 |
| 399 | J2.02 | L3 | Evals no CI como gate de deploy | puxada por P6.03 |
| 400 | J2.03 | L3 | Lidar com não determinismo e testes instáveis | puxada por P6.03 |
| 401 | J2.04 | L3 | Release progressivo de prompts e modelos | puxada por P6.03 |
| 402 | J2.05 | L3 | Testes de carga e limites de taxa | puxada por P6.03 |
| 403 | J3.01 | L2 | Tracing de chamadas, cadeias e agentes | puxada por P6.03 |
| 404 | J3.02 | L2 | Métricas operacionais | puxada por P6.03 |
| 405 | J3.03 | L3 | Avaliação online de qualidade | puxada por P6.03 |
| 406 | J3.04 | L3 | FinOps de LLM: atribuição e controle de custo | puxada por P6.03 |
| 407 | J3.05 | L3 | Cache semântico e de respostas | puxada por P6.03 |
| 408 | J3.06 | L3 | Degradação e falha de provedores | puxada por P6.03 |
| 409 | J3.07 | L4 | Mineração de falhas em logs de produção | puxada por P6.03 |
| 410 | J4.01 | L3 | Curar logs de produção em datasets | puxada por P6.03 |
| 411 | J4.02 | L3 | Do log ao eval: golden set crescente | puxada por P6.03 |
| 412 | J4.04 | L3 | Consentimento, retenção e direito ao esquecimento | puxada por P6.03 |
| 413 | J4.03 | L4 | Do log ao fine-tune: destilação contínua | puxada por P6.03 |
| 414 | J5.01 | L2 | Segredos e chaves de API | puxada por P6.03 |
| 415 | J5.02 | L3 | Catálogo de modelos aprovados e políticas de uso | puxada por P6.03 |
| 416 | J5.03 | L3 | Guardrails em produção e combate a abuso | puxada por P6.03 |
| 417 | J5.06 | L3 | Maturidade LLMOps e roadmap | puxada por P6.03 |
| 418 | J5.04 | L4 | Operação multi-tenant | puxada por P6.03 |
| 419 | J5.05 | L4 | AgentOps: operar agentes em produção | puxada por P6.03 |
| 420 | P6.03 | — | Plataforma LLMOps em ambiente regulado | projeto integrador |
| 421 | K1.01 | L1 | Princípios DataOps e mapa de fluxo de valor | puxada por P6.04 |
| 422 | K1.02 | L2 | Métricas de DataOps | puxada por P6.04 |
| 423 | K1.03 | L2 | Estratégia de ambientes para dados | puxada por P6.04 |
| 424 | K1.04 | L3 | Branching de dados ("Git para dados") | puxada por P6.04 |
| 425 | K1.05 | L3 | Dados de teste | puxada por P6.04 |
| 426 | K2.01 | L1 | Lint e padronização de SQL e código de dados | puxada por P6.04 |
| 427 | K2.02 | L2 | Pirâmide de testes de dados | puxada por P6.04 |
| 428 | K2.07 | L2 | Migrações de bancos e dados | puxada por P6.04 |
| 429 | K2.03 | L3 | Data diff e análise de impacto em PRs | puxada por P6.04 |
| 430 | K2.04 | L3 | CI incremental (slim CI, state-aware) | puxada por P6.04 |
| 431 | K2.05 | L3 | Write-Audit-Publish (WAP) | puxada por P6.04 |
| 432 | K2.06 | L3 | Mudanças de schema e contratos | puxada por P6.04 |
| 433 | K3.01 | L2 | SLAs, SLOs e SLIs de dados | puxada por P6.04 |
| 434 | K3.03 | L2 | Alertas acionáveis e roteamento por dono | puxada por P6.04 |
| 435 | K3.02 | L3 | Detecção automática de anomalias em tabelas | puxada por P6.04 |
| 436 | K3.04 | L3 | Resposta a incidentes e post-mortems | puxada por P6.04 |
| 437 | K3.05 | L3 | Reprocessamento e backfill seguros | puxada por P6.04 |
| 438 | K3.06 | L3 | Backup, DR e continuidade | puxada por P6.04 |
| 439 | K4.01 | L2 | Ownership e catálogo de produtos de dados | puxada por P6.04 |
| 440 | K4.02 | L3 | Golden paths e templates de pipelines | puxada por P6.04 |
| 441 | K4.04 | L3 | FinOps integrado ao DataOps | puxada por P6.04 |
| 442 | K4.05 | L3 | Maturidade DataOps e roadmap de adoção | puxada por P6.04 |
| 443 | K4.03 | L4 | Platform engineering para dados | puxada por P6.04 |
| 444 | N6.03 | L3 | Dados regulatórios e reporte | puxada por P6.04 |
| 445 | P6.04 | — | Transformação DataOps de um time de dados financeiro | projeto integrador |
| 446 | F7.09 | L3 | Automação de atendimento ao cliente | puxada por P6.05 |
| 447 | M5.01 | L2 | Inventário de ferramentas e permissões | puxada por P6.05 |
| 448 | M5.02 | L3 | Níveis de autonomia e supervisão humana | puxada por P6.05 |
| 449 | M5.04 | L3 | Servidores MCP e integrações | puxada por P6.05 |
| 450 | M5.05 | L3 | Trajetórias e logs | puxada por P6.05 |
| 451 | M5.09 | L3 | Confiabilidade e taxa de sucesso | puxada por P6.05 |
| 452 | M5.10 | L3 | Governança e responsabilização | puxada por P6.05 |
| 453 | M5.03 | L4 | Modelagem de ameaças de agentes | puxada por P6.05 |
| 454 | M5.06 | L4 | Sandboxing e isolamento | puxada por P6.05 |
| 455 | M5.07 | L4 | Testes de falha e caos | puxada por P6.05 |
| 456 | M5.08 | L4 | Sistemas multiagente | puxada por P6.05 |
| 457 | P6.05 | — | Agente de atendimento bancário com ferramentas e auditoria | projeto integrador |

### W9 · Plataformas III: IA financeira e auditoria

Dados sintéticos, LLM financeiro em PT-BR, analista com IA e auditoria agêntica (P6.06–P6.09). **23 receitas e 4 projetos, 112 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 458 | L3.04 | L3 | Síntese relacional multitabela | puxada por P6.06 |
| 459 | L3.10 | L4 | Síntese de grafos temporais e redes dinâmicas | puxada por P6.06 |
| 460 | L3.13 | L4 | Dados sintéticos com privacidade diferencial | puxada por P6.06 |
| 461 | N6.05 | L3 | LGPD e sigilo bancário em projetos de dados | puxada por P6.06 |
| 462 | P6.06 | — | Dados sintéticos bancários preservando topologia da rede de transações | projeto integrador |
| 463 | F4.01 | L2 | Decidir: prompt vs RAG vs fine-tuning | puxada por P6.07 |
| 464 | F4.02 | L3 | Fine-tuning supervisionado (SFT) | puxada por P6.07 |
| 465 | F4.03 | L3 | PEFT: LoRA, QLoRA, DoRA, adapters | puxada por P6.07 |
| 466 | F4.06 | L3 | Construir datasets de instrução | puxada por P6.07 |
| 467 | F4.08 | L3 | Fine-tuning de embeddings e rerankers | puxada por P6.07 |
| 468 | F4.04 | L4 | Alinhamento por preferência | puxada por P6.07 |
| 469 | F4.05 | L4 | RL para raciocínio (RLVR/GRPO) | puxada por P6.07 |
| 470 | F4.07 | L4 | Destilação de LLMs | puxada por P6.07 |
| 471 | F4.09 | L4 | Fine-tuning multimodal | puxada por P6.07 |
| 472 | F4.10 | L4 | Mesclagem de modelos | puxada por P6.07 |
| 473 | F4.11 | L4 | Pré-treino de LLM pequeno do zero | puxada por P6.07 |
| 474 | F4.12 | L4 | Esquecimento catastrófico e avaliação pós-fine-tuning | puxada por P6.07 |
| 475 | F5.01 | L3 | Servir LLM em produção | puxada por P6.07 |
| 476 | F5.03 | L3 | Dimensionar GPU e custo por token | puxada por P6.07 |
| 477 | F5.04 | L3 | Gateway de LLM, roteamento e fallback | puxada por P6.07 |
| 478 | F5.07 | L3 | Servir com decodificação restrita | puxada por P6.07 |
| 479 | F5.02 | L4 | Otimizações de inferência | puxada por P6.07 |
| 480 | F5.05 | L4 | Autoscaling e filas para inferência | puxada por P6.07 |
| 481 | F5.06 | L4 | Inferência em borda e dispositivo | puxada por P6.07 |
| 482 | P6.07 | — | LLM financeiro em PT-BR: fine-tuning, avaliação e serving | projeto integrador |
| 483 | P6.08 | — | Analista financeiro com IA (text-to-SQL + relatórios) | projeto integrador |
| 484 | P6.09 | — | Auditoria de sistema agêntico em instituição financeira | projeto integrador |

### W10 · Outros domínios

Amplitude técnica fora de finanças (P7). **31 receitas e 6 projetos, 145 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 485 | P7.01 | — | Previsão de demanda no varejo | projeto integrador |
| 486 | D5.01 | L1 | Recomendação baseada em popularidade/conteúdo | puxada por P7.02 |
| 487 | D5.02 | L2 | Filtragem colaborativa | puxada por P7.02 |
| 488 | D5.03 | L3 | Two-tower e retrieval | puxada por P7.02 |
| 489 | D5.04 | L3 | Ranking (learning to rank) | puxada por P7.02 |
| 490 | D5.06 | L3 | Cold start | puxada por P7.02 |
| 491 | D5.05 | L4 | Sequential | puxada por P7.02 |
| 492 | D5.08 | L4 | Avaliação offline vs online, off-policy | puxada por P7.02 |
| 493 | D5.09 | L4 | Arquitetura E2E de recomendação (retrieval → ranking → re-ranking) | puxada por P7.02 |
| 494 | D5.10 | L4 | Recomendação com LLMs | puxada por P7.02 |
| 495 | P7.02 | — | Sistema de recomendação de produtos (next best offer) | projeto integrador |
| 496 | P7.03 | — | Inspeção visual industrial | projeto integrador |
| 497 | L5.01 | L1 | Espectro caixa-branca, cinza e preta | puxada por P7.04 |
| 498 | L5.02 | L2 | Ajustar EDOs e modelos mecanísticos a dados | puxada por P7.04 |
| 499 | L5.09 | L2 | Modelos grey-box com correção de resíduo | puxada por P7.04 |
| 500 | L5.06 | L3 | Descoberta de equações | puxada por P7.04 |
| 501 | L5.08 | L3 | Assimilação de dados | puxada por P7.04 |
| 502 | L5.12 | L3 | Incerteza epistêmica vs aleatória | puxada por P7.04 |
| 503 | L5.13 | L3 | Integrar conhecimento de domínio | puxada por P7.04 |
| 504 | L5.05 | L4 | Universal Differential Equations e neural ODEs híbridas | puxada por P7.04 |
| 505 | L5.07 | L4 | Restrições físicas e simetrias em redes | puxada por P7.04 |
| 506 | L5.10 | L4 | Gêmeos digitais físicos | puxada por P7.04 |
| 507 | L5.11 | L4 | Modelos de fundação científicos | puxada por P7.04 |
| 508 | L5.14 | L4 | Validação, extrapolação e confiança epistêmica | puxada por P7.04 |
| 509 | L5.15 | L4 | Otimização e controle com modelos híbridos | puxada por P7.04 |
| 510 | P7.04 | — | Gêmeo digital híbrido física + ML | projeto integrador |
| 511 | L2.01 | L2 | Calibração bayesiana clássica com MCMC | puxada por P7.05 |
| 512 | L2.03 | L2 | Approximate Bayesian Computation (ABC) | puxada por P7.05 |
| 513 | L2.02 | L3 | Workflow bayesiano completo | puxada por P7.05 |
| 514 | L2.10 | L3 | Emuladores e surrogates de simuladores caros | puxada por P7.05 |
| 515 | L2.13 | L3 | Otimização bayesiana para calibração | puxada por P7.05 |
| 516 | L2.15 | L3 | Quantificação de incerteza ponta a ponta | puxada por P7.05 |
| 517 | L2.09 | L4 | Robustez a simuladores mal especificados | puxada por P7.05 |
| 518 | L2.11 | L4 | Calibração de modelos computacionais com discrepância | puxada por P7.05 |
| 519 | L2.12 | L4 | Design ótimo de experimentos bayesiano | puxada por P7.05 |
| 520 | P7.05 | — | Calibração SBI de modelo epidemiológico | projeto integrador |
| 521 | P7.06 | — | Treinar um LLM pequeno do zero | projeto integrador |

### W11 · Cobertura: dados e ML clássico

Receitas de A–K que nenhum projeto exige. **49 receitas e 0 projetos, 111 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 522 | C1.01 | L1 | EDA tabular completa | cobertura (nenhum projeto exige) |
| 523 | C1.02 | L1 | Visualização estática e interativa | cobertura (nenhum projeto exige) |
| 524 | C1.04 | L1 | Detectar e tratar valores ausentes | cobertura (nenhum projeto exige) |
| 525 | C1.05 | L2 | Detectar e tratar outliers | cobertura (nenhum projeto exige) |
| 526 | C1.06 | L2 | Análise de correlação e dependência | cobertura (nenhum projeto exige) |
| 527 | C1.07 | L2 | EDA de texto | cobertura (nenhum projeto exige) |
| 528 | C1.08 | L2 | EDA de imagens | cobertura (nenhum projeto exige) |
| 529 | C1.09 | L2 | EDA de séries temporais | cobertura (nenhum projeto exige) |
| 530 | C1.10 | L2 | Redução de dimensionalidade e visualização | cobertura (nenhum projeto exige) |
| 531 | C1.11 | L3 | Detectar data leakage | cobertura (nenhum projeto exige) |
| 532 | C1.12 | L3 | Data-centric AI: encontrar erros de rótulo | cobertura (nenhum projeto exige) |
| 533 | C2.01 | L1 | Codificar variáveis categóricas | cobertura (nenhum projeto exige) |
| 534 | C2.02 | L1 | Escalonar e transformar numéricas | cobertura (nenhum projeto exige) |
| 535 | C2.03 | L2 | Features de data e tempo | cobertura (nenhum projeto exige) |
| 536 | C2.04 | L2 | Features de texto clássicas | cobertura (nenhum projeto exige) |
| 537 | C2.05 | L2 | Features a partir de embeddings | cobertura (nenhum projeto exige) |
| 538 | C2.07 | L2 | Seleção de features | cobertura (nenhum projeto exige) |
| 539 | C2.10 | L2 | Pipelines de features sem leakage | cobertura (nenhum projeto exige) |
| 540 | C2.12 | L3 | Geração automática de features (AutoFE) | cobertura (nenhum projeto exige) |
| 541 | D1.01 | L1 | Primeiro modelo end-to-end (baseline) | cobertura (nenhum projeto exige) |
| 542 | D1.04 | L1 | Overfitting, underfitting, curvas de aprendizado | cobertura (nenhum projeto exige) |
| 543 | D1.02 | L2 | Estratégia de validação | cobertura (nenhum projeto exige) |
| 544 | D1.05 | L2 | Ajuste de hiperparâmetros | cobertura (nenhum projeto exige) |
| 545 | D1.09 | L2 | AutoML | cobertura (nenhum projeto exige) |
| 546 | D1.10 | L3 | Ensembles: bagging, boosting, stacking, blending | cobertura (nenhum projeto exige) |
| 547 | D2.01 | L1 | Classificação binária | cobertura (nenhum projeto exige) |
| 548 | D2.03 | L1 | Regressão | cobertura (nenhum projeto exige) |
| 549 | D2.02 | L2 | Classificação multiclasse e multirrótulo | cobertura (nenhum projeto exige) |
| 550 | D2.04 | L2 | Dados desbalanceados | cobertura (nenhum projeto exige) |
| 551 | D2.05 | L3 | Poucos dados tabulares | cobertura (nenhum projeto exige) |
| 552 | D2.06 | L3 | Muitos dados tabulares (escala) | cobertura (nenhum projeto exige) |
| 553 | D2.07 | L3 | Dados mistos e alta cardinalidade | cobertura (nenhum projeto exige) |
| 554 | D2.09 | L3 | Modelos monotônicos e interpretáveis por desenho | cobertura (nenhum projeto exige) |
| 555 | D2.10 | L3 | Aprendizado semi-supervisionado | cobertura (nenhum projeto exige) |
| 556 | D2.11 | L3 | Aprendizado ativo e rotulagem eficiente | cobertura (nenhum projeto exige) |
| 557 | D2.12 | L3 | Weak supervision | cobertura (nenhum projeto exige) |
| 558 | D2.15 | L4 | Domain shift e covariate shift | cobertura (nenhum projeto exige) |
| 559 | D3.01 | L1 | Clusterização | cobertura (nenhum projeto exige) |
| 560 | D3.03 | L2 | Detecção de anomalias tabular | cobertura (nenhum projeto exige) |
| 561 | D3.05 | L2 | Regras de associação | cobertura (nenhum projeto exige) |
| 562 | D3.06 | L2 | Modelagem de tópicos | cobertura (nenhum projeto exige) |
| 563 | D3.04 | L3 | Detecção de anomalias em séries | cobertura (nenhum projeto exige) |
| 564 | D3.07 | L4 | Aprendizado de representações | cobertura (nenhum projeto exige) |
| 565 | D6.02 | L3 | Previsão espaço-temporal | cobertura (nenhum projeto exige) |
| 566 | D6.04 | L3 | Geração de dados sintéticos tabulares | cobertura (nenhum projeto exige) |
| 567 | D6.03 | L4 | Dados com privacidade (DP, federated) | cobertura (nenhum projeto exige) |
| 568 | H3.05 | L2 | Explicações para stakeholders | cobertura (nenhum projeto exige) |
| 569 | H3.02 | L3 | Interpretabilidade de deep learning | cobertura (nenhum projeto exige) |
| 570 | H3.03 | L4 | Interpretabilidade mecanicista de LLMs | cobertura (nenhum projeto exige) |

### W12 · Cobertura: deep learning e IA

Receitas de E e F que nenhum projeto exige. **38 receitas e 0 projetos, 109 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 571 | E1.01 | L1 | Rede neural do zero | cobertura (nenhum projeto exige) |
| 572 | E1.02 | L2 | Loop de treino robusto | cobertura (nenhum projeto exige) |
| 573 | E1.03 | L2 | Otimizadores e schedulers | cobertura (nenhum projeto exige) |
| 574 | E1.04 | L2 | Regularização | cobertura (nenhum projeto exige) |
| 575 | E1.07 | L2 | Rastreamento de experimentos | cobertura (nenhum projeto exige) |
| 576 | E1.08 | L2 | Escolha de framework | cobertura (nenhum projeto exige) |
| 577 | E1.05 | L3 | Inicialização e estabilidade numérica | cobertura (nenhum projeto exige) |
| 578 | E1.06 | L3 | Debug de treino | cobertura (nenhum projeto exige) |
| 579 | E4.01 | L2 | Classificação de áudio | cobertura (nenhum projeto exige) |
| 580 | E4.03 | L3 | Síntese de fala (TTS) | cobertura (nenhum projeto exige) |
| 581 | E4.04 | L3 | Diarização e separação | cobertura (nenhum projeto exige) |
| 582 | E4.05 | L4 | Agentes de voz em tempo real | cobertura (nenhum projeto exige) |
| 583 | E4.06 | L4 | Modelos visão-linguagem | cobertura (nenhum projeto exige) |
| 584 | E4.07 | L4 | Busca e RAG multimodal | cobertura (nenhum projeto exige) |
| 585 | E4.08 | L4 | Geração de música/áudio | cobertura (nenhum projeto exige) |
| 586 | E6.01 | L2 | Autoencoders e VAEs | cobertura (nenhum projeto exige) |
| 587 | E6.02 | L3 | GANs | cobertura (nenhum projeto exige) |
| 588 | E6.03 | L4 | Modelos de difusão do zero | cobertura (nenhum projeto exige) |
| 589 | E6.04 | L4 | Aprendizado por reforço profundo | cobertura (nenhum projeto exige) |
| 590 | E6.05 | L4 | Meta-learning, few-shot, continual learning | cobertura (nenhum projeto exige) |
| 591 | E6.06 | L4 | Neural ODEs, PINNs, ML científico | cobertura (nenhum projeto exige) |
| 592 | E6.07 | L4 | Incerteza em deep learning | cobertura (nenhum projeto exige) |
| 593 | E6.08 | L4 | Robustez e ataques adversariais | cobertura (nenhum projeto exige) |
| 594 | F1.01 | L1 | Primeira chamada a um LLM | cobertura (nenhum projeto exige) |
| 595 | F1.03 | L1 | Prompt engineering sistemático | cobertura (nenhum projeto exige) |
| 596 | F1.02 | L2 | Escolher modelo (qualidade/custo/latência) | cobertura (nenhum projeto exige) |
| 597 | F1.05 | L2 | Streaming, async e concorrência | cobertura (nenhum projeto exige) |
| 598 | F1.10 | L2 | Rodar LLMs locais | cobertura (nenhum projeto exige) |
| 599 | F1.06 | L3 | Gerenciar contexto longo | cobertura (nenhum projeto exige) |
| 600 | F1.07 | L3 | Prompt caching e otimização de custo | cobertura (nenhum projeto exige) |
| 601 | F1.08 | L3 | Raciocínio e modelos "thinking" | cobertura (nenhum projeto exige) |
| 602 | F7.01 | L2 | Chatbot conversacional com memória | cobertura (nenhum projeto exige) |
| 603 | F7.02 | L3 | Assistente de busca sobre base de conhecimento | cobertura (nenhum projeto exige) |
| 604 | F7.03 | L3 | Extração estruturada de documentos | cobertura (nenhum projeto exige) |
| 605 | F7.05 | L3 | Geração de conteúdo com controle de qualidade | cobertura (nenhum projeto exige) |
| 606 | F7.08 | L3 | Análise de dados conversacional | cobertura (nenhum projeto exige) |
| 607 | F7.06 | L4 | Copiloto de código interno | cobertura (nenhum projeto exige) |
| 608 | F7.07 | L4 | Assistente de voz | cobertura (nenhum projeto exige) |

### W13 · Cobertura: auditoria e domínio

Receitas de M e N que nenhum projeto exige. **22 receitas e 0 projetos, 62 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 609 | M1.01 | L2 | Arquitetura de dados | cobertura (nenhum projeto exige) |
| 610 | M1.02 | L2 | Qualidade de dados por dimensão | cobertura (nenhum projeto exige) |
| 611 | M1.08 | L2 | Custo e eficiência | cobertura (nenhum projeto exige) |
| 612 | M1.09 | L2 | Código SQL, dbt e Spark | cobertura (nenhum projeto exige) |
| 613 | M1.03 | L3 | Pipelines e orquestração | cobertura (nenhum projeto exige) |
| 614 | M1.04 | L3 | Modelagem e camada semântica | cobertura (nenhum projeto exige) |
| 615 | M1.05 | L3 | Linhagem e rastreabilidade | cobertura (nenhum projeto exige) |
| 616 | M1.06 | L3 | Segurança e controle de acesso | cobertura (nenhum projeto exige) |
| 617 | M1.07 | L3 | Privacidade e conformidade LGPD/GDPR | cobertura (nenhum projeto exige) |
| 618 | M1.10 | L3 | Confiabilidade, DR e SLAs | cobertura (nenhum projeto exige) |
| 619 | M1.11 | L4 | Due diligence técnica de plataforma de dados | cobertura (nenhum projeto exige) |
| 620 | M3.01 | L2 | Pipeline de dados e augmentations | cobertura (nenhum projeto exige) |
| 621 | M3.08 | L2 | Licenças de pesos e dados | cobertura (nenhum projeto exige) |
| 622 | M3.09 | L2 | Eficiência computacional e energia | cobertura (nenhum projeto exige) |
| 623 | M3.02 | L3 | Dinâmica de treino | cobertura (nenhum projeto exige) |
| 624 | M3.03 | L3 | Robustez adversarial e fora de distribuição | cobertura (nenhum projeto exige) |
| 625 | M3.04 | L3 | Calibração e incerteza | cobertura (nenhum projeto exige) |
| 626 | M3.07 | L3 | Efeitos de compressão | cobertura (nenhum projeto exige) |
| 627 | M3.05 | L4 | Privacidade e memorização | cobertura (nenhum projeto exige) |
| 628 | M3.06 | L4 | Backdoors, envenenamento e integridade de pesos | cobertura (nenhum projeto exige) |
| 629 | N1.06 | L2 | Behavior score e gestão de limites | cobertura (nenhum projeto exige) |
| 630 | N3.08 | L4 | Deep hedging e RL em finanças | cobertura (nenhum projeto exige) |

### W14 · Cobertura: ciências generativas

Receitas de L (fronteira) que nenhum projeto exige. **11 receitas e 0 projetos, 32 pontos.**

**Critério de saída:** Todas as receitas e projetos da onda em `done` (SPEC §9), resultados `full` versionados, `make check` verde e links dos projetos resolvidos.

| Ordem | ID | Nível | Título | Motivo |
|---:|---|---|---|---|
| 631 | L3.01 | L1 | Fundamentos: fidelidade, utilidade e privacidade | cobertura (nenhum projeto exige) |
| 632 | L3.02 | L2 | Síntese tabular condicional e controlada | cobertura (nenhum projeto exige) |
| 633 | L3.05 | L2 | Síntese com LLMs | cobertura (nenhum projeto exige) |
| 634 | L3.03 | L3 | Síntese de séries temporais | cobertura (nenhum projeto exige) |
| 635 | L3.06 | L3 | Análise topológica de dados (TDA) | cobertura (nenhum projeto exige) |
| 636 | L3.12 | L3 | Síntese guiada por restrições lógicas e físicas | cobertura (nenhum projeto exige) |
| 637 | L3.14 | L3 | Cenários raros e stress testing sintético | cobertura (nenhum projeto exige) |
| 638 | L3.15 | L3 | Governança de dados sintéticos | cobertura (nenhum projeto exige) |
| 639 | L3.07 | L4 | Métricas topológicas para dados sintéticos | cobertura (nenhum projeto exige) |
| 640 | L3.08 | L4 | Geração com perdas topológicas | cobertura (nenhum projeto exige) |
| 641 | L3.11 | L4 | Preservar dinâmica: atratores, invariantes, Lyapunov | cobertura (nenhum projeto exige) |

## 6. Como regenerar

```bash
make roadmap     # reescreve ROADMAP.md e config/roadmap.yml
make check       # inclui `roadmap.py --check`
```
