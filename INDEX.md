# Cookbook de Ciência de Dados, ML, Deep Learning, Engenharia de Dados e AI Engineering
# Cookbook of Data Science, ML, Deep Learning, Data Engineering & AI Engineering

> Índice mestre v0.1 / Master index v0.1
> Organização por **problema**, não por ferramenta. Cada problema é uma "receita-mãe" que explora todas as stacks viáveis e todas as variáveis de decisão.
> Organized by **problem**, not by tool. Each problem is a "parent recipe" exploring every viable stack and every decision variable.

---

## 0. Como ler este índice / How to read this index

**Nível / Level**
- 🟢 **L1 Introdutório / Introductory**: primeira vez fazendo; dataset pequeno, uma máquina.
- 🟡 **L2 Intermediário / Intermediate**: prática de projeto real; escala média, boas práticas.
- 🟠 **L3 Avançado / Advanced**: produção, escala, trade-offs finos.
- 🔴 **L4 SOTA / Especialista**: fronteira de pesquisa e engenharia; técnicas recentes, otimização extrema.

**Cada problema vira uma receita-mãe com esta anatomia / Each problem becomes a parent recipe with this anatomy**

1. **Problema e contexto** / Problem and context: quando aparece, métrica de sucesso.
2. **Mapa de decisão** / Decision map: árvore "se X então Y" para escolher a stack.
3. **Stacks candidatas** / Candidate stacks: cada uma com *pros, contras, casos de uso, custo, maturidade, curva de aprendizado*.
4. **Passo a passo por stack** / Step-by-step per stack: código executável (um notebook por stack).
5. **Eixos de variação** / Variation axes: cada variável relevante explorada (hiperparâmetro, tamanho de dados, formato, arquitetura, hardware, custo) com efeito medido.
6. **Benchmark comparativo** / Comparative benchmark: mesma tarefa, mesmos dados, todas as stacks.
7. **Validação** / Validation: como saber que está certo.
8. **Armadilhas e falhas comuns** / Pitfalls and failure modes.
9. **Do protótipo à produção** / From prototype to production.
10. **Referências** / References (papers, docs, versões pinadas).

**Colunas das tabelas / Table columns**: `ID | Problema / Problem | Nível | Stacks e eixos principais a explorar`

---

## PARTE A: Fundações / Foundations

### A1. Ambiente, reprodutibilidade e ferramentas / Environment, reproducibility, tooling
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| A1.01 | Configurar ambiente Python reprodutível / Reproducible Python environment | 🟢 | venv, conda/mamba, poetry, uv, pip-tools, Docker, devcontainers, Nix |
| A1.02 | Configurar GPU local e em nuvem / GPU setup local and cloud | 🟢 | CUDA/cuDNN, ROCm, Apple MPS, Colab, Kaggle, Lambda, RunPod, Vast.ai, SageMaker, Vertex, Azure ML |
| A1.03 | Estruturar um repositório de projeto DS/ML / Project repo structure | 🟢 | cookiecutter-data-science, Kedro, estrutura monorepo vs polyrepo |
| A1.04 | Versionar código, dados e modelos / Version code, data, models | 🟡 | Git, Git LFS, DVC, lakeFS, DagsHub, Hugging Face Hub, W&B Artifacts |
| A1.05 | Garantir determinismo e seeds / Determinism and seeds | 🟡 | seeds, flags determinísticas por framework, fontes de não-determinismo em GPU |
| A1.06 | Qualidade de código e testes para ML / Code quality and testing for ML | 🟡 | pytest, hypothesis, ruff, mypy, pre-commit, testes de dados, testes de modelo |
| A1.07 | Notebooks em produção / Notebooks to production | 🟡 | Jupyter, JupyterLab, Marimo, papermill, nbdev, Quarto, conversão para scripts/pipelines |
| A1.08 | Profiling de código e uso de recursos / Profiling code and resources | 🟠 | cProfile, py-spy, scalene, line_profiler, memray, PyTorch Profiler, Nsight |
| A1.09 | Computação eficiente em Python (dados) / Efficient data computing in Python | 🟠 | NumPy vetorização, Numba, Cython, Rust (PyO3), Polars, multiprocessing, Dask, Ray |

### A2. Fundamentos de dados e estatística aplicada / Data and applied statistics foundations
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| A2.01 | Carregar e inspecionar dados tabulares / Load and inspect tabular data | 🟢 | pandas, Polars, DuckDB, PyArrow, Modin, Vaex (comparar memória/velocidade) |
| A2.02 | Escolher formato de arquivo / Choose file format | 🟡 | CSV, JSON/NDJSON, Parquet, ORC, Avro, Feather/Arrow IPC, HDF5, Zarr (compressão, schema, leitura parcial) |
| A2.03 | Tipos de dados, datas, texto e encoding / Types, dates, text, encoding | 🟢 | tipos pandas/Arrow, timezone, Unicode, categorical |
| A2.04 | Estatística descritiva e inferência básica / Descriptive stats and basic inference | 🟢 | scipy, statsmodels, pingouin; testes paramétricos vs não paramétricos |
| A2.05 | Probabilidade e simulação (Monte Carlo, bootstrap) / Probability and simulation | 🟡 | NumPy, SciPy, PyMC, resampling |
| A2.06 | Inferência bayesiana prática / Practical Bayesian inference | 🟠 | PyMC, Stan, NumPyro, Turing, brms; MCMC vs VI vs Laplace |
| A2.07 | Álgebra linear e otimização na prática / Applied linear algebra and optimization | 🟡 | NumPy, SciPy, CVXPY, JAX, autodiff; SGD, Adam, L-BFGS |

---

## PARTE B: Engenharia de Dados / Data Engineering

### B1. Ingestão / Ingestion
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| B1.01 | Ler dados de APIs REST/GraphQL / Ingest from REST/GraphQL APIs | 🟢 | requests, httpx, aiohttp; paginação, rate limit, retry, backoff |
| B1.02 | Web scraping responsável / Responsible web scraping | 🟡 | BeautifulSoup, Scrapy, Playwright, Selenium; robots.txt, legalidade, anti-bot |
| B1.03 | Ingestão de bancos relacionais (full load) / Relational DB full load | 🟢 | SQLAlchemy, ConnectorX, pandas, Spark JDBC |
| B1.04 | Ingestão incremental / Incremental ingestion | 🟡 | watermark, timestamp, hash diff, Airbyte, Fivetran, Meltano, dlt |
| B1.05 | CDC (Change Data Capture) | 🟠 | Debezium, Kafka Connect, AWS DMS, Datastream, Fivetran, log-based vs trigger-based |
| B1.06 | Ingestão de arquivos em lote (S3/GCS/ADLS/SFTP) / Batch file ingestion | 🟢 | boto3, gcsfs, fsspec, Auto Loader, Glue, Dataflow |
| B1.07 | Ingestão de dados semiestruturados e aninhados / Semi-structured nested data | 🟡 | JSON/XML, explode, flatten, schema evolution, variant types |
| B1.08 | Ingestão de dados não estruturados em escala (PDF, imagem, áudio, vídeo) / Unstructured ingestion | 🟠 | Unstructured, Docling, Tika, Textract, Document AI, ffmpeg, OCR (Tesseract, PaddleOCR, VLMs) |
| B1.09 | Conectores SaaS e ELT gerenciado vs custom / Managed vs custom ELT | 🟡 | Airbyte, Fivetran, Stitch, dlt, scripts próprios (custo vs manutenção) |
| B1.10 | Ingestão de dados de IoT e telemetria / IoT and telemetry ingestion | 🟠 | MQTT, AWS IoT, Azure IoT Hub, Kafka, TimescaleDB, InfluxDB |

### B2. Transformação e processamento / Transformation and processing
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| B2.01 | ETL local pequeno / Small local ETL | 🟢 | pandas, Polars, DuckDB, SQL puro |
| B2.02 | Transformações SQL versionadas / Versioned SQL transformations | 🟡 | dbt, SQLMesh, Dataform; modelos incrementais, snapshots, testes |
| B2.03 | Processamento distribuído batch / Distributed batch | 🟠 | Spark (PySpark, Scala), Dask, Ray Data, Flink batch, Trino, BigQuery, Snowflake |
| B2.04 | Joins, janelas e agregações em escala / Joins, windows, aggregations at scale | 🟠 | broadcast, sort-merge, bucketing, skew handling, salting |
| B2.05 | Otimização de jobs Spark / Spark job tuning | 🔴 | partições, shuffle, AQE, memória, formatos, Photon, Velox, Gluten |
| B2.06 | Deduplicação e entity resolution / Deduplication and entity resolution | 🟠 | regras, fuzzy (RapidFuzz), Splink, dedupe, embeddings + ANN, LLM-assisted |
| B2.07 | Limpeza de dados textuais e endereços / Text and address cleaning | 🟡 | regex, libpostal, spaCy, LLMs para normalização |
| B2.08 | Processamento de dados geoespaciais / Geospatial processing | 🟠 | GeoPandas, Shapely, H3, S2, PostGIS, Sedona, DuckDB spatial, raster (rasterio, xarray) |
| B2.09 | Processamento de grafos / Graph processing | 🟠 | NetworkX, igraph, GraphFrames, Neo4j, TigerGraph, cuGraph |
| B2.10 | Pipelines de dados para texto/imagem/áudio em escala / Large-scale unstructured pipelines | 🔴 | Ray Data, Spark + GPU, Dataflow, Daft, WebDataset, Mosaic Streaming |

### B3. Streaming e tempo real / Streaming and real time
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| B3.01 | Primeiro pipeline de streaming / First streaming pipeline | 🟡 | Kafka, Redpanda, Pulsar, Kinesis, Pub/Sub, Event Hubs |
| B3.02 | Processar streams com estado e janelas / Stateful stream processing | 🟠 | Flink, Spark Structured Streaming, Kafka Streams, Beam, Bytewax, Materialize, RisingWave |
| B3.03 | Semânticas de entrega (at-least/exactly-once) / Delivery semantics | 🟠 | idempotência, transações Kafka, checkpoints, outbox pattern |
| B3.04 | Late data, watermarks e reordenação / Late data and watermarks | 🟠 | Flink, Beam, Spark; event time vs processing time |
| B3.05 | Schema registry e evolução de schemas / Schema registry and evolution | 🟠 | Avro, Protobuf, JSON Schema, Confluent SR, Apicurio |
| B3.06 | Feature computation em tempo real / Real-time features | 🔴 | Flink, Feast, Tecton, Hopsworks, Redis, Materialize |
| B3.07 | Analytics em tempo real (OLAP streaming) / Real-time OLAP | 🟠 | ClickHouse, Druid, Pinot, Rockset-like, DuckDB, Materialize |
| B3.08 | Streaming para inferência de ML / Streaming ML inference | 🔴 | Flink + ONNX/Triton, Kafka + microservices, Ray Serve |

### B4. Armazenamento, modelagem e lakehouse / Storage, modeling, lakehouse
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| B4.01 | Escolher o tipo de banco / Choose database type | 🟢 | relacional, document, key-value, colunar, grafo, vetorial, time series, NewSQL (decision tree) |
| B4.02 | Modelagem relacional e normalização / Relational modeling | 🟢 | 3NF, índices, constraints, PostgreSQL, MySQL |
| B4.03 | Modelagem dimensional / Dimensional modeling | 🟡 | Kimball, star/snowflake, SCD tipos 1–6, Data Vault 2.0, One Big Table |
| B4.04 | Data warehouse na nuvem / Cloud data warehouse | 🟡 | BigQuery, Snowflake, Redshift, Synapse, Databricks SQL, ClickHouse Cloud |
| B4.05 | Data lake e lakehouse / Data lake and lakehouse | 🟠 | Delta Lake, Iceberg, Hudi, Paimon; ACID, time travel, compaction, catálogos |
| B4.06 | Catálogos e metastore / Catalogs and metastore | 🟠 | Unity Catalog, Glue, Polaris, Nessie, Hive Metastore, DataHub, OpenMetadata |
| B4.07 | Particionamento, clustering e indexação / Partitioning, clustering, indexing | 🟠 | partition pruning, z-order, liquid clustering, bloom filters, índices |
| B4.08 | Otimizar PostgreSQL para analytics / Tune PostgreSQL for analytics | 🟠 | EXPLAIN, índices, particionamento, pgvector, TimescaleDB, Citus |
| B4.09 | Banco de séries temporais / Time-series database | 🟠 | TimescaleDB, InfluxDB, QuestDB, ClickHouse, Prometheus |
| B4.10 | Banco de grafos / Graph database | 🟠 | Neo4j, Memgraph, Neptune, TigerGraph, Cypher/Gremlin/GQL |
| B4.11 | Banco vetorial / Vector database | 🟠 | pgvector, Qdrant, Weaviate, Milvus, Pinecone, Chroma, FAISS, LanceDB, OpenSearch; índices HNSW/IVF/PQ/DiskANN |
| B4.12 | Arquitetura (Lambda, Kappa, Medallion, Data Mesh, Data Fabric) / Architecture patterns | 🔴 | trade-offs, quando usar cada um |
| B4.13 | Estratégia de custo em dados (FinOps) / Data FinOps | 🟠 | compressão, tiering, spot, slots/reservas, auditoria de queries |

### B5. Orquestração, qualidade, governança e observabilidade / Orchestration, quality, governance, observability
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| B5.01 | Agendar um pipeline simples / Schedule a simple pipeline | 🟢 | cron, Airflow, Prefect, Dagster, Mage, Kestra, Step Functions, Cloud Composer |
| B5.02 | DAGs robustos: retries, idempotência, backfill / Robust DAGs | 🟡 | Airflow, Dagster (assets), Prefect, Temporal |
| B5.03 | Orquestração baseada em assets e eventos / Asset and event-driven orchestration | 🟠 | Dagster, Airflow datasets, Argo Events |
| B5.04 | Testes e contratos de dados / Data tests and contracts | 🟡 | Great Expectations, Soda, dbt tests, Pandera, Pydantic, data contracts |
| B5.05 | Observabilidade de dados / Data observability | 🟠 | Monte Carlo, Elementary, OpenLineage, Marquez, Datadog |
| B5.06 | Linhagem e documentação de dados / Lineage and documentation | 🟠 | OpenLineage, DataHub, OpenMetadata, dbt docs, Amundsen |
| B5.07 | Governança, PII, LGPD/GDPR / Governance, PII, privacy law | 🟠 | classificação, mascaramento, tokenização, RBAC/ABAC, Presidio, row/column-level security |
| B5.08 | CI/CD para pipelines de dados / CI/CD for data pipelines | 🟠 | GitHub Actions, GitLab CI, dbt slim CI, ambientes efêmeros |
| B5.09 | Infraestrutura como código para dados / IaC for data platforms | 🟠 | Terraform, Pulumi, CDK, Crossplane |
| B5.10 | Plataforma de dados self-service / Self-service data platform | 🔴 | Data Mesh, produtos de dados, semantic layer (dbt SL, Cube, MetricFlow) |
| B5.11 | Migração de plataformas de dados / Data platform migration | 🔴 | estratégia strangler, validação de paridade, dual-run |

---

## PARTE C: Análise de Dados e Feature Engineering / Data Analysis and Feature Engineering

### C1. Análise exploratória e visualização / EDA and visualization
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| C1.01 | EDA tabular completa / Full tabular EDA | 🟢 | pandas, ydata-profiling, sweetviz, Polars, DuckDB |
| C1.02 | Visualização estática e interativa / Static and interactive viz | 🟢 | matplotlib, seaborn, plotly, altair, plotnine, bokeh, hvplot |
| C1.03 | Dashboards e data apps / Dashboards and data apps | 🟡 | Streamlit, Gradio, Dash, Panel, Shiny, Evidence, Metabase, Superset, Power BI, Looker |
| C1.04 | Detectar e tratar valores ausentes / Missing values | 🟢 | MCAR/MAR/MNAR, imputação simples, KNN, MICE, modelos, indicadores |
| C1.05 | Detectar e tratar outliers / Outliers | 🟡 | IQR, z-score, Isolation Forest, robust scaling, winsorização |
| C1.06 | Análise de correlação e dependência / Correlation and dependence | 🟡 | Pearson, Spearman, MI, distance correlation, SHAP interactions |
| C1.07 | EDA de texto / Text EDA | 🟡 | frequências, n-gramas, tópicos, embeddings + UMAP |
| C1.08 | EDA de imagens / Image EDA | 🟡 | distribuição de tamanhos, classes, duplicatas, FiftyOne, CleanVision |
| C1.09 | EDA de séries temporais / Time series EDA | 🟡 | decomposição, ACF/PACF, sazonalidade, estacionariedade |
| C1.10 | Redução de dimensionalidade e visualização / Dimensionality reduction | 🟡 | PCA, t-SNE, UMAP, PaCMAP, autoencoders |
| C1.11 | Detectar data leakage / Detect leakage | 🟠 | leakage temporal, de alvo, de grupo; auditoria sistemática |
| C1.12 | Data-centric AI: encontrar erros de rótulo / Find label errors | 🟠 | cleanlab, confident learning, FiftyOne, Argilla |

### C2. Feature engineering
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| C2.01 | Codificar variáveis categóricas / Encode categoricals | 🟢 | one-hot, ordinal, target, CatBoost, hashing, embeddings aprendidos, leave-one-out |
| C2.02 | Escalonar e transformar numéricas / Scale and transform numerics | 🟢 | standard, minmax, robust, quantile, Box-Cox, Yeo-Johnson, log |
| C2.03 | Features de data e tempo / Date and time features | 🟡 | calendário, cíclicas (sin/cos), lags, rolling, feriados, Fourier |
| C2.04 | Features de texto clássicas / Classical text features | 🟡 | BoW, TF-IDF, hashing, n-gramas, char-level |
| C2.05 | Features a partir de embeddings / Embedding-based features | 🟡 | sentence-transformers, OpenAI/Cohere/Voyage/Gemini embeddings, CLIP |
| C2.06 | Features de agregação e relacionais / Aggregation and relational features | 🟠 | Featuretools, SQL, window functions, deep feature synthesis |
| C2.07 | Seleção de features / Feature selection | 🟡 | filter, wrapper, embedded, Boruta, SHAP, permutation, L1 |
| C2.08 | Features geográficas / Geo features | 🟠 | H3, distâncias, POIs, raster, OSM |
| C2.09 | Features de grafo / Graph features | 🟠 | centralidades, node2vec, GNN embeddings |
| C2.10 | Pipelines de features sem leakage / Leak-free feature pipelines | 🟡 | sklearn Pipeline, ColumnTransformer, feature-engine |
| C2.11 | Feature store | 🔴 | Feast, Tecton, Hopsworks, Databricks FS, SageMaker FS, Vertex FS; consistência online/offline, point-in-time join |
| C2.12 | Geração automática de features (AutoFE) / Automated feature engineering | 🟠 | Featuretools, AutoGluon, LLM-assisted FE |

---

## PARTE D: Machine Learning Clássico / Classical Machine Learning

### D1. Fundamentos de modelagem / Modeling fundamentals
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| D1.01 | Primeiro modelo end-to-end (baseline) / First end-to-end model | 🟢 | scikit-learn; dummy baseline, regressão logística/linear |
| D1.02 | Estratégia de validação / Validation strategy | 🟡 | hold-out, k-fold, stratified, group, time-series split, nested CV, purged CV |
| D1.03 | Escolher métricas / Choose metrics | 🟡 | classificação, regressão, ranking, calibração, métricas de negócio, custos assimétricos |
| D1.04 | Overfitting, underfitting, curvas de aprendizado / Over/underfitting, learning curves | 🟢 | regularização, bias-variance, early stopping |
| D1.05 | Ajuste de hiperparâmetros / Hyperparameter tuning | 🟡 | grid, random, Optuna, Hyperopt, Ray Tune, SMAC, Hyperband/ASHA, BO |
| D1.06 | Calibração de probabilidades / Probability calibration | 🟠 | Platt, isotônica, temperature scaling, conformal prediction |
| D1.07 | Ajuste de threshold e decisão sob custo / Thresholding and cost-sensitive decisions | 🟡 | curvas PR/ROC, custo esperado, otimização de lucro |
| D1.08 | Comparar modelos com rigor estatístico / Statistically sound model comparison | 🟠 | testes pareados, bootstrap, McNemar, Nadeau-Bengio, Bayesian comparison |
| D1.09 | AutoML | 🟡 | AutoGluon, FLAML, H2O, auto-sklearn, TPOT, Vertex AutoML, SageMaker Autopilot |
| D1.10 | Ensembles: bagging, boosting, stacking, blending / Ensembles | 🟠 | RF, ExtraTrees, XGBoost, LightGBM, CatBoost, stacking, hill climbing |

### D2. Aprendizado supervisionado tabular / Tabular supervised learning
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| D2.01 | Classificação binária / Binary classification | 🟢 | LR, árvores, RF, GBM (XGB/LGBM/CatBoost), SVM, KNN, TabPFN, TabM/FT-Transformer |
| D2.02 | Classificação multiclasse e multirrótulo / Multiclass and multilabel | 🟡 | OvR/OvO, classifier chains, métricas macro/micro |
| D2.03 | Regressão / Regression | 🟢 | linear, Ridge/Lasso/Elastic, GBM, GAM, NN, quantile regression |
| D2.04 | Dados desbalanceados / Imbalanced data | 🟡 | pesos, SMOTE e variantes, undersampling, focal loss, threshold, métricas |
| D2.05 | Poucos dados tabulares / Small tabular data | 🟠 | regularização, TabPFN, bayesiano, data augmentation, transfer |
| D2.06 | Muitos dados tabulares (escala) / Large tabular data | 🟠 | LightGBM/XGBoost distribuído, GPU (cuML, RAPIDS), Dask, Spark MLlib |
| D2.07 | Dados mistos e alta cardinalidade / Mixed data, high cardinality | 🟠 | CatBoost, embeddings, target encoding com CV |
| D2.08 | Regressão quantílica e intervalos de predição / Quantile and prediction intervals | 🟠 | quantile GBM, conformal, NGBoost, bayesiano |
| D2.09 | Modelos monotônicos e interpretáveis por desenho / Monotonic and inherently interpretable | 🟠 | EBM (InterpretML), GAM, regras, constraints monotônicas em GBM |
| D2.10 | Aprendizado semi-supervisionado / Semi-supervised | 🟠 | pseudo-labeling, label propagation, FixMatch-tabular |
| D2.11 | Aprendizado ativo e rotulagem eficiente / Active learning | 🟠 | uncertainty sampling, query-by-committee, modAL, Argilla, Label Studio |
| D2.12 | Weak supervision | 🟠 | Snorkel, labeling functions, LLM como rotulador |
| D2.13 | Survival analysis e churn | 🟠 | lifelines, scikit-survival, DeepSurv, GBM survival |
| D2.14 | Deep learning tabular SOTA / Tabular deep learning SOTA | 🔴 | FT-Transformer, TabM, TabPFN v2, SAINT, foundation models tabulares; quando vencem GBMs |
| D2.15 | Domain shift e covariate shift / Distribution shift | 🔴 | importance weighting, adversarial validation, DRO, domain adaptation |

### D3. Aprendizado não supervisionado / Unsupervised learning
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| D3.01 | Clusterização / Clustering | 🟢 | k-means, GMM, DBSCAN, HDBSCAN, hierárquico, spectral; métricas internas |
| D3.02 | Segmentação de clientes / Customer segmentation | 🟡 | RFM, k-means, embeddings, LCA |
| D3.03 | Detecção de anomalias tabular / Tabular anomaly detection | 🟡 | Isolation Forest, LOF, OCSVM, autoencoder, PyOD, ECOD |
| D3.04 | Detecção de anomalias em séries / Time-series anomaly detection | 🟠 | STL + resíduos, Prophet, Matrix Profile, LSTM-AE, Anomaly Transformer, TimesFM/Chronos |
| D3.05 | Regras de associação / Association rules | 🟡 | Apriori, FP-Growth, mlxtend |
| D3.06 | Modelagem de tópicos / Topic modeling | 🟡 | LDA, NMF, BERTopic, Top2Vec |
| D3.07 | Aprendizado de representações / Representation learning | 🔴 | autoencoders, VAE, contrastive (SimCLR, CLIP-style), SSL (DINOv2, MAE) |
| D3.08 | Detecção de fraude / Fraud detection | 🟠 | GBM, grafos (GNN), anomalias, regras híbridas, streaming, feedback loop |

### D4. Séries temporais e previsão / Time series and forecasting
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| D4.01 | Previsão univariada baseline / Univariate forecasting baseline | 🟢 | naive, sazonal naive, média móvel, ETS, ARIMA/SARIMA |
| D4.02 | Previsão com ML / Forecasting with ML | 🟡 | LightGBM com lags, sktime, skforecast, mlforecast, direct vs recursive vs multi-output |
| D4.03 | Previsão com bibliotecas dedicadas / Dedicated forecasting libs | 🟡 | Prophet, NeuralProphet, statsforecast, Darts, GluonTS |
| D4.04 | Previsão com deep learning / Deep learning forecasting | 🟠 | N-BEATS, N-HiTS, TFT, DeepAR, PatchTST, iTransformer, TimesNet |
| D4.05 | Foundation models para séries / Time-series foundation models | 🔴 | TimesFM, Chronos(-Bolt), Moirai, Lag-Llama, TimeGPT, MOMENT; zero-shot vs fine-tune |
| D4.06 | Previsão hierárquica e reconciliação / Hierarchical forecasting | 🟠 | MinT, bottom-up, top-down, hierarchicalforecast |
| D4.07 | Previsão probabilística / Probabilistic forecasting | 🟠 | quantis, conformal, DeepAR, bayesiano, CRPS |
| D4.08 | Demanda intermitente / Intermittent demand | 🟠 | Croston, SBA, TSB, ADIDA |
| D4.09 | Previsão multivariada e com regressores exógenos / Multivariate and exogenous | 🟠 | VAR, VARMAX, TFT, ML com features exógenas |
| D4.10 | Backtesting e avaliação em séries / Backtesting | 🟡 | rolling origin, expanding window, MASE, sMAPE, WQL |
| D4.11 | Previsão de demanda E2E (varejo) / Retail demand forecasting E2E | 🟠 | hierarquia, promoções, canibalização, estoque, M5 |
| D4.12 | Mudanças estruturais e change point / Structural breaks | 🟠 | ruptures, BOCPD, CUSUM |

### D5. Sistemas de recomendação e ranking / Recommender systems and ranking
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| D5.01 | Recomendação baseada em popularidade/conteúdo / Popularity and content-based | 🟢 | TF-IDF, embeddings, similaridade |
| D5.02 | Filtragem colaborativa / Collaborative filtering | 🟡 | KNN, SVD, ALS (implicit), LightFM, Surprise |
| D5.03 | Two-tower e retrieval / Two-tower retrieval | 🟠 | TensorFlow Recommenders, TorchRec, FAISS/ScaNN |
| D5.04 | Ranking (learning to rank) | 🟠 | LambdaMART (LightGBM/XGBoost), RankNet, cross-encoders, métricas NDCG/MAP |
| D5.05 | Sequential / session-based | 🔴 | GRU4Rec, SASRec, BERT4Rec, Transformers4Rec, HSTU |
| D5.06 | Cold start | 🟠 | conteúdo, bandits, meta-learning, LLM-based |
| D5.07 | Bandits e exploração / Bandits and exploration | 🟠 | ε-greedy, UCB, Thompson, contextual bandits (Vowpal Wabbit) |
| D5.08 | Avaliação offline vs online, off-policy / Offline vs online, off-policy eval | 🔴 | IPS, DR, replay, interleaving, A/B |
| D5.09 | Arquitetura E2E de recomendação (retrieval → ranking → re-ranking) / E2E recsys architecture | 🔴 | feature store, vector DB, serving de baixa latência, diversidade e fairness |
| D5.10 | Recomendação com LLMs / LLM-based recommendation | 🔴 | LLM como ranker, embeddings, geração de explicações, semantic IDs |

### D6. Dados especiais / Special data settings
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| D6.01 | Aprendizado em grafos / Graph learning | 🟠 | node2vec, GCN, GAT, GraphSAGE, PyG, DGL, graph transformers |
| D6.02 | Previsão espaço-temporal / Spatiotemporal | 🟠 | ConvLSTM, ST-GNN, Graph WaveNet |
| D6.03 | Dados com privacidade (DP, federated) / Privacy-preserving ML | 🔴 | differential privacy (Opacus, TF Privacy), federated (Flower, FedML), SMPC, dados sintéticos |
| D6.04 | Geração de dados sintéticos tabulares / Synthetic tabular data | 🟠 | SDV, CTGAN, TabDDPM, copulas, LLM-based; avaliação de fidelidade e privacidade |
| D6.05 | Aprendizado por reforço clássico / Classic reinforcement learning | 🟠 | Gymnasium, Stable-Baselines3, DQN, PPO, SAC |
| D6.06 | Pesquisa operacional + ML / Operations research + ML | 🟠 | OR-Tools, Pyomo, Gurobi, HiGHS; previsão → otimização |

---

## PARTE E: Deep Learning

### E1. Fundamentos / Foundations
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| E1.01 | Rede neural do zero / Neural net from scratch | 🟢 | NumPy, depois PyTorch, TensorFlow/Keras, JAX/Flax; autodiff |
| E1.02 | Loop de treino robusto / Robust training loop | 🟡 | PyTorch puro, Lightning, Keras, Accelerate, fastai, Hugging Face Trainer |
| E1.03 | Otimizadores e schedulers / Optimizers and schedulers | 🟡 | SGD, Adam/AdamW, Lion, Sophia, Muon, Shampoo; warmup, cosine, OneCycle |
| E1.04 | Regularização / Regularization | 🟡 | dropout, weight decay, BN/LN/GN, augmentation, label smoothing, mixup |
| E1.05 | Inicialização e estabilidade numérica / Initialization and numerical stability | 🟠 | Xavier/He, gradient clipping, mixed precision, loss scaling |
| E1.06 | Debug de treino / Debugging training | 🟠 | overfit num batch, gradient checks, NaN hunting, ativações, TensorBoard/W&B |
| E1.07 | Rastreamento de experimentos / Experiment tracking | 🟡 | MLflow, W&B, Neptune, Comet, TensorBoard, Aim, ClearML |
| E1.08 | Escolha de framework / Framework choice | 🟡 | PyTorch, TensorFlow, JAX, MLX, ONNX; critérios |

### E2. Visão computacional / Computer vision
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| E2.01 | Classificação de imagens / Image classification | 🟢 | CNN simples, ResNet, EfficientNet, ConvNeXt, ViT, DINOv2/SigLIP + linear probe |
| E2.02 | Transfer learning e fine-tuning / Transfer learning and fine-tuning | 🟡 | congelar vs descongelar, LR discriminativo, timm, torchvision, HF |
| E2.03 | Data augmentation de imagens / Image augmentation | 🟡 | Albumentations, torchvision v2, Kornia, RandAugment, CutMix, geração sintética |
| E2.04 | Detecção de objetos / Object detection | 🟠 | YOLO (v8–v12), RT-DETR, Faster R-CNN, DETR, Detectron2, MMDetection, Grounding DINO |
| E2.05 | Segmentação semântica/instância / Segmentation | 🟠 | U-Net, DeepLab, Mask R-CNN, SegFormer, SAM/SAM2, Mask2Former |
| E2.06 | OCR e documentos / OCR and document understanding | 🟠 | Tesseract, PaddleOCR, TrOCR, LayoutLM, Donut, VLMs (Qwen-VL, Gemini, Claude) |
| E2.07 | Detecção de defeitos industriais / Industrial defect detection | 🟠 | PatchCore, anomalib, autoencoder, few-shot |
| E2.08 | Imagens médicas / Medical imaging | 🔴 | MONAI, nnU-Net, DICOM, validação regulatória, incerteza |
| E2.09 | Vídeo (classificação, ação, tracking) / Video | 🔴 | SlowFast, VideoMAE, TimeSformer, ByteTrack, DeepSORT, SAM2 |
| E2.10 | Estimativa de pose, profundidade e 3D / Pose, depth and 3D | 🔴 | MediaPipe, ViTPose, Depth Anything, NeRF, 3D Gaussian Splatting |
| E2.11 | Busca visual e similaridade / Visual search | 🟠 | CLIP/SigLIP + FAISS/vector DB, metric learning |
| E2.12 | Modelos generativos de imagem / Generative image models | 🔴 | GAN, VAE, difusão (Stable Diffusion, SDXL, Flux), ControlNet, LoRA, DreamBooth, avaliação (FID, CLIP score) |
| E2.13 | Few-shot e zero-shot em visão / Few/zero-shot vision | 🟠 | CLIP, SAM, DINOv2, VLMs, prompting visual |
| E2.14 | Visão em dispositivos de borda / Edge vision | 🟠 | TFLite, ONNX Runtime, TensorRT, CoreML, OpenVINO, quantização |

### E3. NLP clássico e Transformers / NLP and Transformers
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| E3.01 | Classificação de texto / Text classification | 🟢 | TF-IDF + LR, fastText, BERT/DeBERTa fine-tune, SetFit, embeddings + LR, LLM zero/few-shot |
| E3.02 | Análise de sentimento / Sentiment analysis | 🟢 | VADER, modelos HF, fine-tune, LLM |
| E3.03 | NER e extração de informação / NER and information extraction | 🟡 | spaCy, Flair, BERT-NER, GLiNER, LLM com saída estruturada |
| E3.04 | Similaridade semântica e busca / Semantic similarity and search | 🟡 | BM25, sentence-transformers, bi-encoders, cross-encoders, híbrido |
| E3.05 | Sumarização / Summarization | 🟡 | extrativa, T5/BART/PEGASUS, LLMs; avaliação (ROUGE, BERTScore, LLM-judge) |
| E3.06 | Tradução automática / Machine translation | 🟠 | MarianMT, NLLB, M2M, LLMs, avaliação (COMET, BLEU) |
| E3.07 | QA extrativo e generativo / Extractive and generative QA | 🟠 | BERT-QA, FiD, LLM + RAG |
| E3.08 | Classificação multilíngue e PT-BR / Multilingual and PT-BR NLP | 🟠 | BERTimbau, XLM-R, mDeBERTa, Sabiá, LLMs multilíngues; avaliação em português |
| E3.09 | Pré-treino de modelo de linguagem de domínio / Domain-adaptive pretraining | 🔴 | continued pretraining, tokenizer customizado, MLM vs CLM |
| E3.10 | Tokenização / Tokenization | 🟠 | BPE, WordPiece, Unigram, tiktoken, SentencePiece, byte-level |
| E3.11 | Moderação de conteúdo e toxicidade / Content moderation | 🟠 | classificadores, LLM-as-classifier, listas, humanos no loop |
| E3.12 | Texto em escala: dedup e filtragem de corpus / Corpus dedup and filtering | 🔴 | MinHash/LSH, fuzzy dedup, quality classifiers, datatrove, NeMo Curator |

### E4. Áudio, fala e multimodal / Audio, speech and multimodal
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| E4.01 | Classificação de áudio / Audio classification | 🟡 | librosa, espectrogramas, CNN, AST, BEATs, YAMNet |
| E4.02 | Reconhecimento de fala (ASR) / Speech recognition | 🟠 | Whisper (faster-whisper, WhisperX), wav2vec2, NeMo, Deepgram, Google/Azure/AWS STT |
| E4.03 | Síntese de fala (TTS) / Text to speech | 🟠 | Coqui, Piper, XTTS, ElevenLabs, OpenAI TTS, F5-TTS |
| E4.04 | Diarização e separação / Diarization and separation | 🟠 | pyannote, Demucs, NeMo |
| E4.05 | Agentes de voz em tempo real / Real-time voice agents | 🔴 | WebRTC, LiveKit, Pipecat, APIs realtime; latência, barge-in, VAD |
| E4.06 | Modelos visão-linguagem / Vision-language models | 🔴 | CLIP, BLIP, LLaVA, Qwen-VL, PaliGemma, Gemini, Claude; fine-tuning |
| E4.07 | Busca e RAG multimodal / Multimodal search and RAG | 🔴 | ColPali, CLIP, embeddings multimodais |
| E4.08 | Geração de música/áudio / Music and audio generation | 🔴 | MusicGen, AudioLDM, Stable Audio |

### E5. Arquiteturas e treino em escala / Architectures and large-scale training
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| E5.01 | Implementar Transformer do zero / Transformer from scratch | 🟠 | PyTorch, JAX; atenção, posicional (RoPE, ALiBi), KV cache |
| E5.02 | Treino com mixed precision / Mixed-precision training | 🟠 | fp16, bf16, fp8, AMP, Transformer Engine |
| E5.03 | Treino distribuído de dados (DDP) / Data-parallel training | 🟠 | DDP, FSDP, DeepSpeed ZeRO, Horovod, Accelerate |
| E5.04 | Paralelismo de modelo, pipeline e tensor / Model, pipeline, tensor parallelism | 🔴 | Megatron-LM, DeepSpeed, torchtitan, JAX pjit/sharding, NeMo |
| E5.05 | Otimização de memória / Memory optimization | 🟠 | gradient checkpointing, accumulation, offload, 8-bit optimizers, FlashAttention |
| E5.06 | Otimização de throughput de dados / Data loader throughput | 🟠 | DataLoader tuning, WebDataset, Mosaic Streaming, DALI, FFCV |
| E5.07 | Compilação e kernels / Compilers and kernels | 🔴 | torch.compile, XLA, Triton, CUDA, CUTLASS, TensorRT |
| E5.08 | Treino em TPUs e clusters / TPU and cluster training | 🔴 | JAX/Flax, MaxText, SLURM, Kubernetes, Ray Train, SkyPilot |
| E5.09 | Scaling laws e planejamento de compute / Scaling laws and compute planning | 🔴 | Chinchilla, estimativa de FLOPs, orçamento, curvas |
| E5.10 | Arquiteturas alternativas ao Transformer / Alternative architectures | 🔴 | Mamba/SSM, RWKV, MoE, híbridos, linear attention |
| E5.11 | Compressão: quantização, poda, destilação / Compression | 🟠 | PTQ, QAT, GPTQ, AWQ, GGUF, bitsandbytes, pruning, knowledge distillation |
| E5.12 | Tolerância a falhas e checkpointing / Fault tolerance and checkpointing | 🔴 | checkpoint assíncrono, elastic training, spot |

### E6. Geração e outros paradigmas / Generative and other paradigms
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| E6.01 | Autoencoders e VAEs | 🟡 | PyTorch, Keras; espaço latente, β-VAE |
| E6.02 | GANs | 🟠 | DCGAN, StyleGAN, WGAN-GP; estabilidade |
| E6.03 | Modelos de difusão do zero / Diffusion from scratch | 🔴 | DDPM, DDIM, flow matching, diffusers, classifier-free guidance |
| E6.04 | Aprendizado por reforço profundo / Deep RL | 🔴 | PPO, SAC, DQN, Dreamer, RLlib, CleanRL |
| E6.05 | Meta-learning, few-shot, continual learning | 🔴 | MAML, prototypical, EWC, replay |
| E6.06 | Neural ODEs, PINNs, ML científico / Scientific ML | 🔴 | torchdiffeq, DeepXDE, neural operators (FNO) |
| E6.07 | Incerteza em deep learning / Uncertainty in deep learning | 🔴 | MC Dropout, deep ensembles, Laplace, evidential, conformal |
| E6.08 | Robustez e ataques adversariais / Robustness and adversarial attacks | 🔴 | FGSM, PGD, adversarial training, certified robustness |

---

## PARTE F: AI Engineering (LLMs e sistemas de IA) / AI Engineering (LLMs and AI systems)

### F1. Fundamentos de uso de LLMs / LLM usage fundamentals
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| F1.01 | Primeira chamada a um LLM / First LLM call | 🟢 | APIs Anthropic, OpenAI, Google, Mistral, Cohere; SDKs oficiais |
| F1.02 | Escolher modelo (qualidade/custo/latência) / Choose a model | 🟡 | proprietários vs open-weights, tamanhos, tabelas de decisão, benchmarks próprios |
| F1.03 | Prompt engineering sistemático / Systematic prompt engineering | 🟢 | zero/few-shot, CoT, XML/estrutura, papéis, exemplos, iteração com evals |
| F1.04 | Saídas estruturadas / Structured outputs | 🟡 | JSON schema, tool use, Pydantic, Instructor, Outlines, grammars, constrained decoding |
| F1.05 | Streaming, async e concorrência / Streaming, async, concurrency | 🟡 | SSE, asyncio, semáforos, rate limit, retries |
| F1.06 | Gerenciar contexto longo / Long-context management | 🟠 | janela, truncamento, resumo hierárquico, context caching, compactação |
| F1.07 | Prompt caching e otimização de custo / Prompt caching and cost optimization | 🟠 | cache de prefixo, batch APIs, roteamento de modelos, modelos menores, destilação |
| F1.08 | Raciocínio e modelos "thinking" / Reasoning models | 🟠 | orçamento de raciocínio, quando usar, custo/latência |
| F1.09 | Multimodal com LLMs (imagem, PDF, áudio) / Multimodal with LLMs | 🟡 | visão em APIs, extração de documentos, limites |
| F1.10 | Rodar LLMs locais / Run local LLMs | 🟡 | Ollama, llama.cpp, LM Studio, MLX, vLLM, GGUF; quantização |

### F2. RAG e conhecimento / RAG and knowledge
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| F2.01 | RAG básico E2E / Basic RAG E2E | 🟡 | loader → chunk → embed → vector DB → retrieve → generate; LangChain, LlamaIndex, Haystack, código próprio |
| F2.02 | Estratégias de chunking / Chunking strategies | 🟡 | tamanho fixo, recursivo, semântico, por estrutura, late chunking, parent-child, contextual retrieval |
| F2.03 | Escolher embeddings / Choose embeddings | 🟡 | OpenAI, Cohere, Voyage, Gemini, BGE, E5, Jina, Nomic, Matryoshka; avaliação no próprio domínio (MTEB, PT-BR) |
| F2.04 | Busca híbrida e reranking / Hybrid search and reranking | 🟠 | BM25 + densa, RRF, cross-encoders, Cohere Rerank, ColBERT |
| F2.05 | Query transformation | 🟠 | rewriting, HyDE, multi-query, decomposição, step-back |
| F2.06 | RAG sobre dados estruturados (text-to-SQL) / Text-to-SQL | 🟠 | schema linking, semantic layer, validação, guardrails de execução |
| F2.07 | RAG sobre documentos complexos (PDF, tabelas, imagens) / Complex-document RAG | 🟠 | Docling, Unstructured, ColPali, parsers com VLM |
| F2.08 | GraphRAG e knowledge graphs | 🔴 | Neo4j, Microsoft GraphRAG, LightRAG, extração de entidades por LLM |
| F2.09 | RAG agentico e multi-hop / Agentic and multi-hop RAG | 🔴 | self-RAG, CRAG, loops de recuperação, planejamento |
| F2.10 | Avaliação de RAG / RAG evaluation | 🟠 | recall@k, faithfulness, answer relevance, RAGAS, TruLens, LLM-judge, golden sets |
| F2.11 | RAG em produção: atualização, ACL, multi-tenant / Production RAG | 🔴 | indexação incremental, permissões por documento, citações, observabilidade |
| F2.12 | Memória de longo prazo para agentes e assistentes / Long-term memory | 🔴 | memória episódica/semântica, mem0, Letta, resumos, vetor + grafo |

### F3. Agentes e sistemas compostos / Agents and compound systems
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| F3.01 | Tool use / function calling | 🟡 | APIs nativas, definição de schemas, paralelismo, tratamento de erro |
| F3.02 | Primeiro agente (loop ReAct) / First agent | 🟡 | código puro, LangGraph, Claude Agent SDK, OpenAI Agents SDK, PydanticAI, smolagents, CrewAI |
| F3.03 | Model Context Protocol (MCP) | 🟠 | servidores e clientes MCP, segurança, descoberta de ferramentas |
| F3.04 | Workflows vs agentes autônomos / Workflows vs autonomous agents | 🟠 | prompt chaining, roteamento, paralelização, orquestrador-trabalhadores, avaliador-otimizador |
| F3.05 | Sistemas multiagente / Multi-agent systems | 🔴 | supervisor, handoff, debate, paralelismo, custo e confiabilidade |
| F3.06 | Agentes de código e uso de computador / Coding and computer-use agents | 🔴 | sandboxes, Claude Code-style, browser/computer use, avaliação (SWE-bench) |
| F3.07 | Humano no loop e aprovações / Human-in-the-loop | 🟠 | interrupções, checkpoints, filas de revisão |
| F3.08 | Estado, persistência e execução durável / State and durable execution | 🔴 | LangGraph checkpointers, Temporal, Inngest, filas |
| F3.09 | Planejamento, reflexão e auto-correção / Planning, reflection, self-correction | 🔴 | plan-and-execute, reflexion, verificadores |
| F3.10 | Confiabilidade de agentes / Agent reliability | 🔴 | limites de passos, orçamentos, detecção de loops, fallback, idempotência de ferramentas |
| F3.11 | Agentes para dados (analista de dados / SQL / BI) / Data agents | 🟠 | text-to-SQL + código, notebooks, semantic layer, governança |
| F3.12 | Automação de documentos e backoffice / Document and back-office automation | 🟠 | extração → validação → ação; filas, auditoria |

### F4. Adaptação de modelos / Model adaptation
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| F4.01 | Decidir: prompt vs RAG vs fine-tuning / Decide between prompting, RAG, fine-tuning | 🟡 | árvore de decisão, custo, dados necessários |
| F4.02 | Fine-tuning supervisionado (SFT) / Supervised fine-tuning | 🟠 | Hugging Face TRL, Axolotl, Unsloth, LLaMA-Factory, torchtune, APIs gerenciadas |
| F4.03 | PEFT: LoRA, QLoRA, DoRA, adapters | 🟠 | PEFT, Unsloth; rank, alvo de módulos, LR, quantização |
| F4.04 | Alinhamento por preferência / Preference alignment | 🔴 | RLHF, DPO, IPO, KTO, ORPO, SimPO, reward models |
| F4.05 | RL para raciocínio (RLVR/GRPO) / RL for reasoning | 🔴 | GRPO, PPO, verificadores, TRL, veRL, OpenRLHF |
| F4.06 | Construir datasets de instrução / Build instruction datasets | 🟠 | dados sintéticos (self-instruct, Evol-Instruct), curadoria, deduplicação, qualidade, anotação humana |
| F4.07 | Destilação de LLMs / LLM distillation | 🔴 | logits, dados gerados por professor, rejection sampling |
| F4.08 | Fine-tuning de embeddings e rerankers / Fine-tune embeddings and rerankers | 🟠 | sentence-transformers, hard negatives, MNRL, dados sintéticos |
| F4.09 | Fine-tuning multimodal / Multimodal fine-tuning | 🔴 | VLMs, LoRA em visão-linguagem |
| F4.10 | Mesclagem de modelos / Model merging | 🔴 | TIES, DARE, SLERP, mergekit |
| F4.11 | Pré-treino de LLM pequeno do zero / Pretrain a small LLM from scratch | 🔴 | nanoGPT, Megatron, torchtitan; dados, tokenizer, scaling |
| F4.12 | Esquecimento catastrófico e avaliação pós-fine-tuning / Catastrophic forgetting and post-FT eval | 🔴 | mistura de dados, regularização, regressão de capacidades |

### F5. Serving e inferência / Serving and inference
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| F5.01 | Servir LLM em produção / Serve an LLM | 🟠 | vLLM, SGLang, TGI, TensorRT-LLM, llama.cpp, Ollama, Triton, NIM |
| F5.02 | Otimizações de inferência / Inference optimizations | 🔴 | continuous batching, PagedAttention, KV cache, prefix caching, speculative decoding, quantização |
| F5.03 | Dimensionar GPU e custo por token / GPU sizing and cost per token | 🟠 | VRAM, throughput, latência (TTFT/ITL), A100/H100/L4/B200, spot |
| F5.04 | Gateway de LLM, roteamento e fallback / LLM gateway, routing, fallback | 🟠 | LiteLLM, Portkey, OpenRouter, Kong, cache semântico |
| F5.05 | Autoscaling e filas para inferência / Autoscaling and queues | 🔴 | KServe, Ray Serve, Modal, Kubernetes, KEDA |
| F5.06 | Inferência em borda e dispositivo / On-device inference | 🔴 | llama.cpp, MLC, ExecuTorch, CoreML, WebGPU/Transformers.js |
| F5.07 | Servir com decodificação restrita / Constrained decoding serving | 🟠 | Outlines, XGrammar, guidance |

### F6. Avaliação, qualidade e segurança de IA / Evaluation, quality and AI safety
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| F6.01 | Construir um conjunto de avaliação (golden set) / Build an eval set | 🟡 | curadoria, casos de borda, dados sintéticos, anotação |
| F6.02 | LLM-as-a-judge | 🟠 | rubricas, pairwise, viés de posição/tamanho, calibração com humanos |
| F6.03 | Frameworks de eval / Eval frameworks | 🟠 | promptfoo, DeepEval, Inspect, Braintrust, LangSmith, Phoenix, lm-eval-harness, OpenAI Evals |
| F6.04 | Avaliação de agentes / Agent evaluation | 🔴 | trajetórias, sucesso de tarefa, custo, ambientes simulados |
| F6.05 | Observabilidade e tracing de LLM / LLM observability | 🟠 | OpenTelemetry, Langfuse, LangSmith, Phoenix, Helicone, Datadog |
| F6.06 | Guardrails e validação de saída / Guardrails and output validation | 🟠 | Guardrails AI, NeMo Guardrails, Llama Guard, classificadores, regras |
| F6.07 | Prompt injection e segurança de agentes / Prompt injection and agent security | 🔴 | isolamento, privilégios mínimos, filtros, red teaming, OWASP LLM Top 10 |
| F6.08 | Red teaming e testes adversariais / Red teaming | 🔴 | garak, PyRIT, promptfoo, jailbreaks, automação |
| F6.09 | Alucinação: detecção e mitigação / Hallucination detection and mitigation | 🟠 | grounding, citações, verificação, auto-consistência |
| F6.10 | Vieses, equidade e IA responsável em LLMs / Bias, fairness, responsible AI | 🟠 | benchmarks (BBQ), auditoria, model cards |
| F6.11 | Testes de regressão contínuos de prompts e modelos / Continuous regression testing | 🟠 | CI com evals, versionamento de prompts, canários |
| F6.12 | Privacidade, PII e conformidade em apps de IA / Privacy, PII and compliance | 🟠 | redação, retenção zero, residência de dados, LGPD, EU AI Act |
| F6.13 | Feedback de usuários e melhoria contínua / User feedback and continuous improvement | 🟠 | thumbs, logs → datasets de eval/FT, active learning |

### F7. Aplicações de IA (produtos) / AI product applications
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| F7.01 | Chatbot conversacional com memória / Conversational chatbot | 🟡 | histórico, resumo, persistência, UI (Streamlit, Gradio, Chainlit, Next.js) |
| F7.02 | Assistente de busca sobre base de conhecimento / Knowledge-base assistant | 🟠 | RAG + citações + permissões |
| F7.03 | Extração estruturada de documentos / Structured document extraction | 🟠 | VLM/LLM + schema + validação + revisão humana |
| F7.04 | Classificação e triagem em escala com LLM / LLM classification at scale | 🟠 | batch APIs, cascatas (modelo pequeno → grande), custo |
| F7.05 | Geração de conteúdo com controle de qualidade / Content generation with QA | 🟠 | templates, verificadores, estilo, humano no loop |
| F7.06 | Copiloto de código interno / Internal code copilot | 🔴 | RAG sobre repositórios, agentes, testes automáticos |
| F7.07 | Assistente de voz / Voice assistant | 🔴 | ASR + LLM + TTS ou modelos realtime |
| F7.08 | Análise de dados conversacional / Conversational analytics | 🟠 | text-to-SQL, gráficos, semantic layer |
| F7.09 | Automação de atendimento ao cliente / Customer support automation | 🟠 | RAG + ferramentas + handoff humano + métricas (CSAT, resolução) |
| F7.10 | Pesquisa profunda (deep research agents) / Deep research agents | 🔴 | busca web, planejamento, subagentes, síntese com citações |

---

## PARTE G: MLOps e Produção / MLOps and Production

### G1. Empacotamento, deploy e serving / Packaging, deployment, serving
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| G1.01 | Empacotar um modelo / Package a model | 🟢 | pickle/joblib (riscos), ONNX, TorchScript, SavedModel, MLflow Models, BentoML |
| G1.02 | API de inferência online / Online inference API | 🟡 | FastAPI, Flask, BentoML, Ray Serve, KServe, Seldon, TorchServe, Triton |
| G1.03 | Inferência em lote / Batch inference | 🟡 | Spark, Ray, SageMaker Batch, Vertex Batch, Airflow |
| G1.04 | Containerização / Containerization | 🟡 | Docker multi-stage, imagens leves, GPU, segurança |
| G1.05 | Deploy em Kubernetes / Kubernetes deploy | 🟠 | Helm, KServe, HPA/KEDA, GPU scheduling, Kubeflow |
| G1.06 | Deploy serverless de modelos / Serverless deploy | 🟠 | Lambda, Cloud Run, Modal, Replicate, SageMaker Serverless; cold start |
| G1.07 | Plataformas gerenciadas / Managed platforms | 🟠 | SageMaker, Vertex AI, Azure ML, Databricks Mosaic AI; lock-in vs velocidade |
| G1.08 | Estratégias de release / Release strategies | 🟠 | shadow, canary, blue-green, A/B, champion-challenger |
| G1.09 | Otimização de latência e throughput / Latency and throughput optimization | 🟠 | ONNX Runtime, TensorRT, batching dinâmico, quantização, cache |
| G1.10 | Inferência em borda/mobile / Edge and mobile | 🟠 | TFLite, CoreML, ExecuTorch, ONNX, OpenVINO |
| G1.11 | Serving de múltiplos modelos / Multi-model serving | 🔴 | Triton, Ray Serve, multi-tenancy, model mesh |

### G2. Pipelines, CI/CD e governança de modelos / Pipelines, CI/CD, model governance
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| G2.01 | Pipeline de treino reprodutível / Reproducible training pipeline | 🟡 | DVC, Kedro, ZenML, Metaflow, Prefect, Dagster |
| G2.02 | Orquestração de ML / ML orchestration | 🟠 | Kubeflow, Airflow, Argo, Flyte, Vertex Pipelines, SageMaker Pipelines |
| G2.03 | Registro de modelos / Model registry | 🟡 | MLflow, W&B, SageMaker, Vertex, Hugging Face Hub |
| G2.04 | CI/CD/CT para ML / CI/CD/CT for ML | 🟠 | GitHub Actions, testes de dados/modelo, gates de qualidade, retreino contínuo |
| G2.05 | Retreino automático e gatilhos / Automated retraining and triggers | 🟠 | agenda, drift, degradação de métrica |
| G2.06 | Níveis de maturidade MLOps / MLOps maturity levels | 🟠 | mapa 0–3, arquitetura por nível |
| G2.07 | Governança de modelos e documentação / Model governance and documentation | 🟠 | model cards, datasheets, auditoria, SR 11-7, EU AI Act |
| G2.08 | Plataforma interna de ML / Internal ML platform | 🔴 | build vs buy, arquitetura, SLAs, multi-time |
| G2.09 | Reprodutibilidade de modelos e auditoria / Model reproducibility and audit | 🟠 | lineage dados → código → modelo, ambientes congelados |

### G3. Monitoramento e operação / Monitoring and operations
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| G3.01 | Monitorar performance e saúde do serviço / Service health monitoring | 🟡 | Prometheus, Grafana, OpenTelemetry, Datadog, alertas, SLOs |
| G3.02 | Detectar data drift e concept drift / Drift detection | 🟠 | Evidently, NannyML, WhyLabs, Alibi Detect; PSI, KS, MMD, performance estimada sem rótulo |
| G3.03 | Monitoramento sem rótulos / Monitoring without labels | 🔴 | CBPE, proxies, shadow models |
| G3.04 | Loops de feedback e rotulagem tardia / Feedback loops and delayed labels | 🟠 | amostragem, active learning, viés de seleção |
| G3.05 | Resposta a incidentes de ML / ML incident response | 🟠 | runbooks, rollback, post-mortems |
| G3.06 | Monitoramento de custos de ML / ML cost monitoring | 🟠 | tags, atribuição, custo por predição, GPU utilization |
| G3.07 | Monitoramento de LLMs em produção / LLM production monitoring | 🟠 | latência, tokens, qualidade, drift de prompts, custo, segurança |

---

## PARTE H: Estatística Avançada, Inferência Causal e Experimentação / Advanced Statistics, Causal Inference, Experimentation

| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| H1.01 | Teste A/B do zero / A/B testing from scratch | 🟡 | poder amostral, MDE, testes de proporção/média, SRM, duração |
| H1.02 | Problemas comuns em experimentos / Common experiment pitfalls | 🟠 | peeking, múltiplas comparações, efeitos de novidade, interferência |
| H1.03 | Redução de variância (CUPED) / Variance reduction | 🟠 | CUPED, estratificação, regressão ajustada |
| H1.04 | Testes sequenciais e bayesianos / Sequential and Bayesian testing | 🟠 | mSPRT, always-valid p-values, bayesian A/B, bandits |
| H1.05 | Experimentos em marketplaces e redes / Network and marketplace experiments | 🔴 | switchback, cluster randomization |
| H2.01 | Inferência causal com dados observacionais / Observational causal inference | 🟠 | DAGs, matching, IPW, doubly robust, DoWhy, EconML, CausalML |
| H2.02 | Quasi-experimentos / Quasi-experiments | 🟠 | diff-in-diff, RDD, IV, controle sintético, CausalImpact |
| H2.03 | Uplift modeling | 🟠 | T/S/X-learner, causal forests, métricas Qini |
| H2.04 | Descoberta causal / Causal discovery | 🔴 | PC, GES, NOTEARS, LiNGAM |
| H2.05 | Mix de marketing (MMM) e incrementalidade / Marketing mix modeling | 🔴 | Meridian, PyMC-Marketing, Robyn, geo-experiments |
| H3.01 | Interpretabilidade de modelos / Model interpretability | 🟡 | SHAP, LIME, PDP/ICE, permutation importance, counterfactuals |
| H3.02 | Interpretabilidade de deep learning / Deep learning interpretability | 🟠 | Grad-CAM, Integrated Gradients, attention, Captum |
| H3.03 | Interpretabilidade mecanicista de LLMs / Mechanistic interpretability | 🔴 | TransformerLens, SAEs, probing, activation patching |
| H3.04 | Equidade e viés algorítmico / Fairness and algorithmic bias | 🟠 | Fairlearn, AIF360, métricas de grupo, mitigação pré/in/pós-processamento |
| H3.05 | Explicações para stakeholders / Explaining to stakeholders | 🟡 | storytelling, tradução técnico → negócio |

---

## PARTE I: Plataformas, Infraestrutura, Custo e Segurança / Platforms, Infrastructure, Cost and Security

| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| I1.01 | Escolher cloud e serviços de dados/ML / Choose cloud and services | 🟡 | AWS vs GCP vs Azure vs on-prem vs neoclouds; matriz de decisão |
| I1.02 | Kubernetes para dados e ML / Kubernetes for data and ML | 🟠 | operadores, GPU, Ray on K8s, Spark on K8s, Karpenter |
| I1.03 | Computação distribuída com Ray / Distributed compute with Ray | 🟠 | Ray Core, Data, Train, Tune, Serve |
| I1.04 | Redes, GPUs e interconexão / Networking and GPU interconnect | 🔴 | NVLink, InfiniBand, NCCL, topologia |
| I1.05 | Otimização de custo de GPU / GPU cost optimization | 🟠 | spot, reservas, MIG, time-slicing, right-sizing, neoclouds |
| I1.06 | Segurança de dados e modelos / Data and model security | 🟠 | IAM, segredos, criptografia, VPC, supply chain (pickle, safetensors) |
| I1.07 | Segurança da cadeia de suprimentos de ML / ML supply chain security | 🔴 | assinatura de modelos, SBOM, scanning de pesos |
| I1.08 | Observabilidade full-stack / Full-stack observability | 🟠 | OpenTelemetry, Prometheus, Grafana, Loki, Tempo |
| I1.09 | Infraestrutura local (homelab / workstation) / Local infrastructure | 🟡 | escolha de GPU, VRAM, refrigeração, orçamento |
| I1.10 | Sustentabilidade e eficiência energética / Sustainability and energy efficiency | 🟠 | CodeCarbon, medição de pegada, eficiência de modelos |

---

## PARTE J: LLMOps

> Opera aplicações de LLM e agentes no dia a dia: versionamento, CI/CD, observabilidade, custo, ciclo de dados e governança. Complementa F5 (serving) e F6 (avaliação).
> Day-to-day operation of LLM apps and agents. Complements F5 (serving) and F6 (evaluation).

### J1. Ciclo de vida de prompts, configurações e modelos / Prompt, config and model lifecycle
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| J1.01 | Versionar prompts como código / Prompts as code | 🟢 | Git + templates (Jinja), prompt registries (Langfuse, LangSmith, MLflow Prompt Registry, PromptLayer, Agenta); acoplar prompt + modelo + parâmetros |
| J1.02 | Gerenciar configurações de LLM / LLM configuration management | 🟡 | Hydra, Pydantic Settings, feature flags (LaunchDarkly, Unleash, Flagsmith), config imutável por release |
| J1.03 | Ambientes dev/staging/prod para apps de LLM / Dev, staging, prod environments | 🟡 | chaves por ambiente, mocks de LLM, gravação e replay (VCR), dados sintéticos |
| J1.04 | Migrar de modelo ou de provedor / Model upgrade and provider migration | 🟠 | evals de regressão, shadow traffic, adaptação de prompts entre famílias, deprecações |
| J1.05 | Reduzir dependência de provedor (lock-in) / Provider lock-in mitigation | 🟠 | camadas de abstração (LiteLLM, Vercel AI SDK), multi-provider, fallback para open-weights |
| J1.06 | Ciclo de vida de modelos fine-tuned e adapters / Fine-tuned model and adapter lifecycle | 🔴 | registry de LoRAs, multi-LoRA serving (vLLM, LoRAX), linhagem dados → adapter, retreino |

### J2. CI/CD e testes para aplicações de LLM / CI/CD and testing for LLM apps
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| J2.01 | Testes unitários e de contrato em chamadas de LLM / Unit and contract tests | 🟡 | pytest, mocks, asserts de schema; testes determinísticos vs estatísticos |
| J2.02 | Evals no CI como gate de deploy / Evals as CI deploy gates | 🟠 | promptfoo, DeepEval, Inspect, Braintrust; limiares, significância, custo do CI |
| J2.03 | Lidar com não determinismo e testes instáveis / Non-determinism and flaky tests | 🟠 | múltiplas amostras, pass@k e pass^k, intervalos de confiança |
| J2.04 | Release progressivo de prompts e modelos / Progressive release | 🟠 | canary, A/B, feature flags, rollback automático por métrica |
| J2.05 | Testes de carga e limites de taxa / Load and rate-limit testing | 🟠 | Locust, k6; RPM/TPM, backpressure, filas |

### J3. Observabilidade, custo e desempenho / Observability, cost and performance
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| J3.01 | Tracing de chamadas, cadeias e agentes / Tracing calls, chains, agents | 🟡 | OpenTelemetry (convenções GenAI), Langfuse, Phoenix, LangSmith, Weave, Opik |
| J3.02 | Métricas operacionais / Operational metrics | 🟡 | TTFT, latência, tokens, taxa de erro, cache hit; Prometheus, Grafana, SLOs |
| J3.03 | Avaliação online de qualidade / Online quality evaluation | 🟠 | LLM-judge amostral, feedback explícito e implícito, drift de entradas via embeddings |
| J3.04 | FinOps de LLM: atribuição e controle de custo / LLM FinOps | 🟠 | custo por feature, usuário e tenant; orçamentos, quotas, alertas, roteamento por custo |
| J3.05 | Cache semântico e de respostas / Semantic and response caching | 🟠 | Redis, GPTCache; limiar de similaridade, invalidação, riscos de resposta errada |
| J3.06 | Degradação e falha de provedores / Provider degradation and outages | 🟠 | health checks, circuit breakers, failover entre provedores |
| J3.07 | Mineração de falhas em logs de produção / Failure mining from production logs | 🔴 | clustering de conversas, taxonomia de erros, triagem assistida por LLM |

### J4. Ciclo de dados e melhoria contínua (data flywheel) / Data flywheel
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| J4.01 | Curar logs de produção em datasets / Curate production logs into datasets | 🟠 | remoção de PII, amostragem, anotação (Argilla, Label Studio) |
| J4.02 | Do log ao eval: golden set crescente / Logs to evals | 🟠 | seleção de casos difíceis, rotulagem, versionamento de datasets |
| J4.03 | Do log ao fine-tune: destilação contínua / Logs to fine-tuning | 🔴 | filtragem por qualidade, retreino, reavaliação, controle de regressão |
| J4.04 | Consentimento, retenção e direito ao esquecimento / Consent, retention, erasure | 🟠 | LGPD/GDPR, políticas de retenção, remoção de dados de datasets derivados |

### J5. Governança e segurança operacional / Operational governance and security
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| J5.01 | Segredos e chaves de API / Secrets and API keys | 🟡 | Vault, Secrets Manager, rotação, chaves por ambiente e por serviço |
| J5.02 | Catálogo de modelos aprovados e políticas de uso / Approved model catalog and policies | 🟠 | AI gateway com políticas, allowlists, avaliações de fornecedores |
| J5.03 | Guardrails em produção e combate a abuso / Production guardrails and abuse | 🟠 | rate limit por usuário, detecção de jailbreak, moderação |
| J5.04 | Operação multi-tenant / Multi-tenant operation | 🔴 | isolamento de dados e contexto, limites e custos por tenant |
| J5.05 | AgentOps: operar agentes em produção / Operating agents in production | 🔴 | replay de trajetórias, sandboxes, orçamentos, kill switch, versionamento de ferramentas e MCP |
| J5.06 | Maturidade LLMOps e roadmap / LLMOps maturity and roadmap | 🟠 | níveis 0–4, priorização de capacidades |

---

## PARTE K: DataOps

> Práticas de engenharia, automação e operação que tornam pipelines de dados rápidos, confiáveis e seguros de mudar. Complementa B5.
> Engineering, automation and operations practices that make data pipelines fast, reliable and safe to change. Complements B5.

### K1. Princípios e fundações / Principles and foundations
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| K1.01 | Princípios DataOps e mapa de fluxo de valor / DataOps principles and value stream | 🟢 | manifesto DataOps, lean, value stream mapping |
| K1.02 | Métricas de DataOps / DataOps metrics | 🟡 | lead time, frequência de deploy, MTTR, taxa de falha de mudança, data downtime |
| K1.03 | Estratégia de ambientes para dados / Data environment strategy | 🟡 | schemas por desenvolvedor, zero-copy clones (Snowflake, BigQuery, Databricks) |
| K1.04 | Branching de dados ("Git para dados") / Data branching | 🟠 | lakeFS, Nessie, branches e tags do Iceberg, clones Delta, Dolt |
| K1.05 | Dados de teste / Test data management | 🟠 | amostragem, subsetting, mascaramento, sintéticos (↔ L3), fixtures |

### K2. CI/CD e testes / CI/CD and testing
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| K2.01 | Lint e padronização de SQL e código de dados / Lint and style | 🟢 | sqlfluff, ruff, pre-commit, convenções de nomes |
| K2.02 | Pirâmide de testes de dados / Data testing pyramid | 🟡 | unit tests (dbt, SQLMesh), integração, regressão, testes em produção |
| K2.03 | Data diff e análise de impacto em PRs / Data diff and impact review | 🟠 | data-diff, Recce, Datafold, SQLMesh plan, linhagem por coluna |
| K2.04 | CI incremental (slim CI, state-aware) / Incremental CI | 🟠 | dbt defer e state:modified, SQLMesh virtual environments, ambientes efêmeros |
| K2.05 | Write-Audit-Publish (WAP) | 🟠 | branches Iceberg/Delta, tabelas blue-green, swaps atômicos |
| K2.06 | Mudanças de schema e contratos / Schema changes and contracts | 🟠 | data contracts, detecção de breaking changes, schema registry |
| K2.07 | Migrações de bancos e dados / Database and data migrations | 🟡 | Alembic, Flyway, Liquibase, Atlas |

### K3. Confiabilidade, observabilidade e incidentes / Reliability, observability, incidents
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| K3.01 | SLAs, SLOs e SLIs de dados / Data SLAs, SLOs, SLIs | 🟡 | frescor, volume, schema, qualidade |
| K3.02 | Detecção automática de anomalias em tabelas / Automated table anomaly detection | 🟠 | Elementary, Soda, Monte Carlo, métodos estatísticos próprios |
| K3.03 | Alertas acionáveis e roteamento por dono / Actionable alerting and ownership | 🟡 | ownership, PagerDuty, Opsgenie, Slack, redução de ruído |
| K3.04 | Resposta a incidentes e post-mortems / Incident response and post-mortems | 🟠 | runbooks, causa raiz via linhagem, cultura blameless |
| K3.05 | Reprocessamento e backfill seguros / Safe reprocessing and backfill | 🟠 | idempotência, time travel, reprocessamento por partição |
| K3.06 | Backup, DR e continuidade / Backup, DR, continuity | 🟠 | RPO/RTO, replicação entre regiões, testes de restauração |

### K4. Organização, colaboração e plataforma / Organization, collaboration, platform
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| K4.01 | Ownership e catálogo de produtos de dados / Ownership and data product catalog | 🟡 | DataHub, OpenMetadata, metadados de dono e SLA |
| K4.02 | Golden paths e templates de pipelines / Golden paths and templates | 🟠 | Backstage, cookiecutters, pacotes dbt |
| K4.03 | Platform engineering para dados / Data platform engineering | 🔴 | plataforma interna (IDP), abstrações, autoatendimento |
| K4.04 | FinOps integrado ao DataOps / FinOps in DataOps | 🟠 | custo por pipeline e produto, chargeback e showback |
| K4.05 | Maturidade DataOps e roadmap de adoção / DataOps maturity and adoption | 🟠 | diagnóstico, priorização, gestão da mudança |

---

## PARTE L: Ciências Generativas + Ciência de Dados / Generative Sciences + Data Science

> Fronteira entre modelos generativos, simulação, causalidade e conhecimento científico. Expande e aprofunda A2.06, D6.04, E6.06 e H2 (↔ indica referência cruzada).
> Frontier where generative models, simulation, causality and scientific knowledge meet. Expands A2.06, D6.04, E6.06 and H2 (↔ marks cross-references).

### L1. Modelagem Causal Híbrida e Inferência Contrafactual / Hybrid Causal Modeling and Counterfactual Inference
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| L1.01 | Modelos causais estruturais (SCM) do zero / Structural causal models from scratch | 🟡 | DAGs, do-calculus, critérios backdoor e frontdoor; pgmpy, DoWhy, y0 |
| L1.02 | Elicitar DAGs com especialistas e LLMs / DAG elicitation with experts and LLMs | 🟠 | LLM como prior de grafo, combinação com descoberta causal, testes de independência condicional |
| L1.03 | Descoberta causal híbrida (conhecimento + dados) / Hybrid causal discovery | 🟠 | causal-learn, gCastle, restrições de conhecimento, NOTEARS, DAG-GNN |
| L1.04 | Estimar efeitos causais com deep learning / Deep causal effect estimation | 🟠 | TARNet, CFRNet, DragonNet, CEVAE, causal transformers; EconML, CausalML |
| L1.05 | Programação probabilística causal / Causal probabilistic programming | 🔴 | Pyro + ChiRho, NumPyro; intervenções e contrafactuais em modelos generativos |
| L1.06 | Inferência contrafactual (abdução, ação, predição) / Counterfactual inference | 🟠 | SCMs com ruído aditivo, identificabilidade de contrafactuais, limites |
| L1.07 | Modelos generativos contrafactuais (deep SCM) / Deep counterfactual generative models | 🔴 | normalizing flows, VAEs, difusão (Diff-SCM); contrafactuais em imagem e texto |
| L1.08 | Explicações contrafactuais acionáveis / Actionable counterfactual explanations | 🟡 | DiCE, Alibi, recourse algorítmico, restrições de plausibilidade |
| L1.09 | Contrafactuais com LLMs: geração, avaliação e limites / LLM counterfactuals | 🟠 | counterfactual data augmentation, consistência causal de LLMs |
| L1.10 | Aprendizado de representações causais / Causal representation learning | 🔴 | latentes causais, iVAE, identificabilidade |
| L1.11 | Sensibilidade a confundimento não observado / Sensitivity to unobserved confounding | 🟠 | sensemakr, E-values, bounds parciais |
| L1.12 | Causalidade em séries temporais e sistemas dinâmicos / Time-series and dynamical causality | 🟠 | Granger, PCMCI (Tigramite), convergent cross mapping, transfer entropy |
| L1.13 | Avaliação contrafactual de políticas e decisões / Counterfactual policy evaluation | 🔴 | dynamic treatment regimes, off-policy evaluation, causal RL |
| L1.14 | Fairness causal e contrafactual / Causal and counterfactual fairness | 🔴 | counterfactual fairness, efeitos por caminho (path-specific) |
| L1.15 | Gêmeos digitais causais / Causal digital twins | 🔴 | SCM + simulador, análise what-if de intervenções (↔ L4.13, L5.10) |

### L2. Calibração Bayesiana e Simulation-Based Inference (SBI) / Bayesian Calibration and SBI
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| L2.01 | Calibração bayesiana clássica com MCMC / Classic Bayesian calibration with MCMC | 🟡 | PyMC, Stan, NumPyro; priors, diagnósticos (R-hat, ESS, divergências), ArviZ |
| L2.02 | Workflow bayesiano completo / Full Bayesian workflow | 🟠 | prior e posterior predictive checks, LOO, WAIC, stacking de modelos |
| L2.03 | Approximate Bayesian Computation (ABC) | 🟡 | rejeição, SMC-ABC; pyabc, ELFI; estatísticas-resumo, distâncias, tolerância |
| L2.04 | Neural Posterior Estimation (NPE) | 🟠 | sbi, BayesFlow, LAMPE; normalizing flows, inferência amortizada |
| L2.05 | Neural Likelihood e Ratio Estimation (NLE, NRE) | 🟠 | sbi, swyft; sequencial vs amortizado |
| L2.06 | SBI com difusão e flow matching / SBI with diffusion and flow matching | 🔴 | score-based posterior estimation, FMPE, Simformer |
| L2.07 | Aprender estatísticas-resumo / Learned summary statistics | 🟠 | embedding networks, DeepSets, transformers |
| L2.08 | Validar SBI / Validating SBI | 🔴 | simulation-based calibration (SBC), cobertura, TARP |
| L2.09 | Robustez a simuladores mal especificados / Robustness to simulator misspecification | 🔴 | robust NPE, detecção de OOD, generalized Bayes |
| L2.10 | Emuladores e surrogates de simuladores caros / Emulators and surrogates | 🟠 | processos gaussianos (GPyTorch, GPflow), emuladores neurais, polynomial chaos |
| L2.11 | Calibração de modelos computacionais com discrepância / Computer model calibration with discrepancy | 🔴 | Kennedy–O'Hagan, history matching |
| L2.12 | Design ótimo de experimentos bayesiano / Bayesian optimal experimental design | 🔴 | expected information gain, BOED amortizado, Pyro OED |
| L2.13 | Otimização bayesiana para calibração / Bayesian optimization for calibration | 🟠 | BoTorch, Ax, scikit-optimize |
| L2.14 | Calibrar modelos epidemiológicos e baseados em agentes / Calibrating epidemic and agent-based models | 🟠 | SEIR, ABMs (Mesa) + sbi (↔ L4.10) |
| L2.15 | Quantificação de incerteza ponta a ponta / End-to-end uncertainty quantification | 🟠 | propagação de incerteza, sensibilidade global (SALib, índices de Sobol) |

### L3. Síntese Controlada de Dados e Preservação de Topologia Dinâmica / Controlled Data Synthesis and Dynamic Topology Preservation
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| L3.01 | Fundamentos: fidelidade, utilidade e privacidade / Fidelity, utility, privacy | 🟢 | SDV, SDMetrics, synthcity; train-synthetic-test-real (TSTR) |
| L3.02 | Síntese tabular condicional e controlada / Conditional tabular synthesis | 🟡 | CTGAN, TVAE, TabDDPM, cópulas; condicionamento e restrições de negócio |
| L3.03 | Síntese de séries temporais / Time-series synthesis | 🟠 | TimeGAN, Diffusion-TS; preservar autocorrelação, sazonalidade e regimes |
| L3.04 | Síntese relacional multitabela / Relational multi-table synthesis | 🟠 | HMA (SDV), integridade referencial, cardinalidades |
| L3.05 | Síntese com LLMs / LLM-based synthesis | 🟡 | prompting estruturado, diversidade, colapso de modo, deduplicação |
| L3.06 | Análise topológica de dados (TDA) / Topological data analysis | 🟠 | homologia persistente, Mapper; giotto-tda, GUDHI, ripser, KeplerMapper |
| L3.07 | Métricas topológicas para dados sintéticos / Topological metrics for synthetic data | 🔴 | distâncias bottleneck e Wasserstein entre diagramas, persistence landscapes |
| L3.08 | Geração com perdas topológicas / Topology-preserving generation | 🔴 | perdas de persistência diferenciáveis, regularização topológica em VAEs, GANs e difusão |
| L3.09 | Síntese de grafos preservando estrutura / Structure-preserving graph synthesis | 🟠 | ER, BA, SBM, GraphRNN, DiGress; distribuição de graus, motifs, comunidades |
| L3.10 | Síntese de grafos temporais e redes dinâmicas / Temporal graph synthesis | 🔴 | TagGen, TG-GAN, difusão temporal; evolução de comunidades e motivos temporais |
| L3.11 | Preservar dinâmica: atratores, invariantes, Lyapunov / Preserving dynamics | 🔴 | embedding de Takens, reservoir computing, neural ODEs, métricas de sistemas dinâmicos |
| L3.12 | Síntese guiada por restrições lógicas e físicas / Constraint-aware synthesis | 🟠 | rejection sampling, guidance em difusão, programas probabilísticos |
| L3.13 | Dados sintéticos com privacidade diferencial / Differentially private synthesis | 🔴 | DP-CTGAN, PATE-GAN, AIM, MST; validação por ataques de inferência de membro |
| L3.14 | Cenários raros e stress testing sintético / Rare scenarios and stress testing | 🟠 | eventos de cauda, choques simulados, oversampling de raridades |
| L3.15 | Governança de dados sintéticos / Synthetic data governance | 🟠 | rotulagem, linhagem, riscos de contaminação de treino e eval |

### L4. Sistemas Complexos Adaptativos Aumentados por LLMs e Multiagentes (Generative Agents) / LLM-Augmented Complex Adaptive Systems
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| L4.01 | Fundamentos de sistemas complexos adaptativos / Complex adaptive systems foundations | 🟢 | emergência, feedback, não linearidade, autômatos celulares |
| L4.02 | Modelagem baseada em agentes clássica / Classic agent-based modeling | 🟡 | Mesa, NetLogo, AgentPy, Repast; regras, scheduling, espaço, redes |
| L4.03 | Dinâmica de redes, difusão e contágio / Network dynamics, diffusion, contagion | 🟡 | NetworkX, SIR em redes, dinâmica de opinião, cascatas |
| L4.04 | Arquitetura de generative agents / Generative agent architecture | 🟠 | memória, reflexão, planejamento; recuperação por recência, importância e relevância |
| L4.05 | Frameworks de simulação com LLM / LLM simulation frameworks | 🟠 | Concordia, AgentSociety, OASIS, AgentTorch, CAMEL; comparação |
| L4.06 | Simulação social e de mercado com LLMs / Social and market simulation | 🔴 | difusão de opinião, adoção de produtos, precificação, negociação |
| L4.07 | Populações sintéticas ("silicon samples") e seus limites / Silicon samples and their limits | 🟠 | personas, vieses, validade frente a pesquisas reais |
| L4.08 | ABMs híbridos regras + LLM para escala e custo / Hybrid rule + LLM ABMs | 🔴 | LLM só em decisões-chave, agentes arquetípicos, cache, modelos pequenos |
| L4.09 | Medir emergência e propriedades macro / Measuring emergence | 🟠 | parâmetros de ordem, entropia, informação mútua, análise das redes resultantes |
| L4.10 | Calibrar e validar simulações multiagente / Calibrating and validating multi-agent simulations | 🔴 | SBI (↔ L2.14), pattern-oriented modeling, reprodutibilidade |
| L4.11 | Aprendizado por reforço multiagente / Multi-agent RL | 🔴 | PettingZoo, RLlib, MAPPO; cooperação e competição |
| L4.12 | Teoria dos jogos computacional e design de mecanismos / Computational game theory | 🟠 | OpenSpiel, equilíbrios, LLMs como jogadores |
| L4.13 | Gêmeos digitais de organizações e políticas públicas / Organizational and policy digital twins | 🔴 | what-if de políticas, intervenções contrafactuais (↔ L1.15) |
| L4.14 | Riscos, vieses e ética em simulações com LLM / Risks and ethics of LLM simulations | 🟠 | homogeneização, estereótipos, sobreinterpretação, transparência |
| L4.15 | Infraestrutura para simulações massivas / Infrastructure for massive simulations | 🔴 | Ray, vLLM, batching de inferência, milhares de agentes |

### L5. Physics-Informed Data Science e Modelos Híbridos Epistêmicos / Physics-Informed DS and Epistemic Hybrid Models
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| L5.01 | Espectro caixa-branca, cinza e preta / White, grey, black-box spectrum | 🟢 | modelos mecanísticos vs orientados a dados, critérios de escolha |
| L5.02 | Ajustar EDOs e modelos mecanísticos a dados / Fitting ODEs and mechanistic models | 🟡 | SciPy, lmfit, PyMC ODE, Diffrax; identificabilidade de parâmetros |
| L5.03 | Physics-Informed Neural Networks (PINNs) | 🟠 | DeepXDE, PhysicsNeMo, PyTorch e JAX puros; perdas de resíduo, balanceamento, falhas comuns |
| L5.04 | Neural operators | 🔴 | FNO, DeepONet, neuraloperator; generalização entre condições |
| L5.05 | Universal Differential Equations e neural ODEs híbridas / UDEs and hybrid neural ODEs | 🔴 | SciML (Julia), torchdiffeq, Diffrax; aprender o termo desconhecido |
| L5.06 | Descoberta de equações / Equation discovery | 🟠 | SINDy (PySINDy), regressão simbólica (PySR) |
| L5.07 | Restrições físicas e simetrias em redes / Physical constraints and equivariance | 🔴 | leis de conservação, redes hamiltonianas e lagrangianas, equivariância (e3nn) |
| L5.08 | Assimilação de dados / Data assimilation | 🟠 | Kalman, EKF, UKF, EnKF, filtros de partículas, 4D-Var; filterpy, DAPPER |
| L5.09 | Modelos grey-box com correção de resíduo / Residual hybrid models | 🟡 | mecanístico + ML no resíduo; arranjos em série e em paralelo |
| L5.10 | Gêmeos digitais físicos / Physical digital twins | 🔴 | sensores + modelo + assimilação + ML, atualização contínua |
| L5.11 | Modelos de fundação científicos / Scientific foundation models | 🔴 | GraphCast, Aurora, modelos de materiais e proteínas; uso e fine-tuning |
| L5.12 | Incerteza epistêmica vs aleatória / Epistemic vs aleatoric uncertainty | 🟠 | ensembles, abordagem bayesiana, discrepância de modelo (↔ L2.11) |
| L5.13 | Integrar conhecimento de domínio / Knowledge-guided ML | 🟠 | priors informativos, features físicas, grafos de conhecimento, regras |
| L5.14 | Validação, extrapolação e confiança epistêmica / Validation, extrapolation, epistemic trust | 🔴 | testes fora do domínio, verificação de invariantes, critérios de aceitação |
| L5.15 | Otimização e controle com modelos híbridos / Optimization and control with hybrid models | 🔴 | MPC com modelos aprendidos, otimização de processos |

---

## PARTE M: Auditoria Técnica / Technical Auditing

> Como avaliar sistemas existentes de forma independente, com evidências, critérios e plano de remediação. Cobre sistemas de dados, ML, deep learning, arquiteturas de IA e sistemas agênticos.
> How to independently assess existing systems with evidence, criteria and remediation plans.

### M0. Fundamentos e metodologia / Foundations and methodology
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| M0.01 | Metodologia de auditoria técnica / Technical audit methodology | 🟢 | escopo, critérios, coleta de evidências, amostragem, entrevistas |
| M0.02 | Frameworks e normas de referência / Reference frameworks and standards | 🟡 | NIST AI RMF e perfil GenAI (AI 600-1), ISO/IEC 42001, 23894, 5259, 25012, DAMA-DMBOK, COBIT, EU AI Act, LGPD, PL 2338/2023, SR 11-7 |
| M0.03 | Matriz de riscos e severidade de achados / Risk matrix and finding severity | 🟡 | probabilidade × impacto, priorização |
| M0.04 | Relatório de auditoria e plano de remediação / Audit report and remediation plan | 🟢 | templates, rastreabilidade de evidências, follow-up |
| M0.05 | Modelos de maturidade e scorecards / Maturity models and scorecards | 🟠 | escalas, pesos, comparação entre times e sistemas |
| M0.06 | Auditoria assistida por LLMs e agentes / LLM-assisted auditing | 🟠 | revisão de código, documentação e logs; verificação humana dos achados |
| M0.07 | Auditoria contínua (audit-as-code, policy-as-code) / Continuous auditing | 🔴 | OPA, checks em CI, dashboards de conformidade |

### M1. Auditoria de sistemas de dados / Data systems audit
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| M1.01 | Arquitetura de dados / Data architecture | 🟡 | aderência a padrões, acoplamento, escalabilidade, pontos únicos de falha |
| M1.02 | Qualidade de dados por dimensão / Data quality by dimension | 🟡 | completude, unicidade, validade, consistência, atualidade, acurácia; profiling |
| M1.03 | Pipelines e orquestração / Pipelines and orchestration | 🟠 | idempotência, retries, backfill, dependências, tratamento de erro |
| M1.04 | Modelagem e camada semântica / Modeling and semantic layer | 🟠 | modelos dimensionais, definições de métricas, lógica duplicada |
| M1.05 | Linhagem e rastreabilidade / Lineage and traceability | 🟠 | OpenLineage, lacunas, linhagem por coluna |
| M1.06 | Segurança e controle de acesso / Security and access control | 🟠 | IAM, privilégios excessivos, segredos, criptografia, logs de acesso |
| M1.07 | Privacidade e conformidade LGPD/GDPR / Privacy and compliance | 🟠 | inventário de PII, bases legais, retenção, mascaramento |
| M1.08 | Custo e eficiência / Cost and efficiency | 🟡 | queries caras, storage órfão, compute ocioso |
| M1.09 | Código SQL, dbt e Spark / SQL, dbt, Spark code | 🟡 | sqlfluff, revisão, cobertura de testes, anti-padrões |
| M1.10 | Confiabilidade, DR e SLAs / Reliability, DR, SLAs | 🟠 | cumprimento de SLAs, testes de restauração |
| M1.11 | Due diligence técnica de plataforma de dados / Data platform technical due diligence | 🔴 | M&A, avaliação de fornecedores, dívida técnica |

### M2. Auditoria de algoritmos de ML / ML algorithms audit
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| M2.01 | Dados de treino / Training data | 🟡 | representatividade, vieses, leakage, qualidade de rótulos, licenças |
| M2.02 | Protocolo de validação / Validation protocol | 🟡 | splits, vazamento temporal e de grupo, tuning no conjunto de teste |
| M2.03 | Métricas e alinhamento com o negócio / Metrics and business alignment | 🟡 | métricas adequadas, custos de erro, thresholds |
| M2.04 | Robustez e estabilidade / Robustness and stability | 🟠 | perturbações, sensibilidade, variância entre seeds e retreinos |
| M2.05 | Fairness | 🟠 | Fairlearn, AIF360; métricas de grupo, interseccionalidade |
| M2.06 | Explicabilidade e documentação / Explainability and documentation | 🟡 | SHAP, model cards, datasheets |
| M2.07 | Reprodutibilidade / Reproducibility | 🟡 | reexecução independente, versões, seeds, ambientes |
| M2.08 | Código e testes de ML / ML code and tests | 🟡 | Giskard, Deepchecks, anti-padrões |
| M2.09 | Validação independente (model risk management) / Independent model validation | 🟠 | SR 11-7, modelos challenger, benchmarking |
| M2.10 | Monitoramento e operação pós-deploy / Post-deployment monitoring | 🟠 | drift, alertas, retreino, rollback |
| M2.11 | Auditoria caixa-preta / Black-box audit | 🔴 | testes por consulta, auditorias externas sem acesso a código ou modelo |

### M3. Auditoria de deep learning / Deep learning audit
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| M3.01 | Pipeline de dados e augmentations / Data pipeline and augmentations | 🟡 | vazamentos, distorções, consistência treino-inferência |
| M3.02 | Dinâmica de treino / Training dynamics | 🟠 | curvas, instabilidades, critérios de escolha de checkpoint |
| M3.03 | Robustez adversarial e fora de distribuição / Adversarial and OOD robustness | 🟠 | ART, Foolbox, TextAttack, benchmarks de shift |
| M3.04 | Calibração e incerteza / Calibration and uncertainty | 🟠 | ECE, diagramas de confiabilidade |
| M3.05 | Privacidade e memorização / Privacy and memorization | 🔴 | membership inference (ML Privacy Meter), extração de dados de treino |
| M3.06 | Backdoors, envenenamento e integridade de pesos / Backdoors, poisoning, weight integrity | 🔴 | detecção de trojans, procedência, safetensors, ModelScan |
| M3.07 | Efeitos de compressão / Compression effects | 🟠 | impacto de quantização e poda em qualidade e fairness |
| M3.08 | Licenças de pesos e dados / Weight and data licensing | 🟡 | compatibilidade de licenças, restrições de uso |
| M3.09 | Eficiência computacional e energia / Compute and energy efficiency | 🟡 | utilização de GPU, pegada de carbono |

### M4. Auditoria de arquiteturas de IA e LLM / AI and LLM architecture audit
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| M4.01 | Escolha de modelos e arquitetura da solução / Model choice and solution architecture | 🟡 | adequação, custo, latência, lock-in |
| M4.02 | Prompts e system prompts / Prompts and system prompts | 🟡 | clareza, conflitos, vazamento de instruções, superfície de injeção |
| M4.03 | Pipelines RAG / RAG pipelines | 🟠 | ingestão, chunking, recuperação, permissões, citações, frescor |
| M4.04 | Cobertura e qualidade dos evals / Eval coverage and quality | 🟠 | representatividade, vieses do juiz, contaminação |
| M4.05 | Segurança de aplicações LLM / LLM application security | 🔴 | OWASP Top 10 para LLM, MITRE ATLAS, red teaming (garak, PyRIT) |
| M4.06 | Alucinação e factualidade / Hallucination and factuality | 🟠 | taxa de alucinação, grounding, verificação |
| M4.07 | Fluxo de dados e privacidade em apps LLM / Data flow and privacy | 🟠 | dados enviados a provedores, retenção, residência |
| M4.08 | Fine-tuning e dados de instrução / Fine-tuning and instruction data | 🔴 | contaminação, licenças, regressões de capacidade |
| M4.09 | Conformidade regulatória de sistemas de IA / Regulatory compliance | 🟠 | classificação de risco (EU AI Act), documentação técnica, transparência |

### M5. Auditoria de sistemas agênticos / Agentic systems audit
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| M5.01 | Inventário de ferramentas e permissões / Tool and permission inventory | 🟡 | mapa de ferramentas, escopos, privilégio mínimo |
| M5.02 | Níveis de autonomia e supervisão humana / Autonomy levels and human oversight | 🟠 | pontos de aprovação, ações irreversíveis |
| M5.03 | Modelagem de ameaças de agentes / Agent threat modeling | 🔴 | injeção indireta, exfiltração, confused deputy; OWASP Agentic, MITRE ATLAS |
| M5.04 | Servidores MCP e integrações / MCP servers and integrations | 🟠 | procedência, permissões, descrições de ferramentas, supply chain |
| M5.05 | Trajetórias e logs / Trajectories and logs | 🟠 | completude dos logs, replay, rastreabilidade de decisões |
| M5.06 | Sandboxing e isolamento / Sandboxing and isolation | 🔴 | containers, rede, sistema de arquivos, credenciais |
| M5.07 | Testes de falha e caos / Failure and chaos testing | 🔴 | ferramentas falhando, entradas adversariais, loops, custo descontrolado |
| M5.08 | Sistemas multiagente / Multi-agent systems | 🔴 | coordenação, propagação de erros, responsabilização |
| M5.09 | Confiabilidade e taxa de sucesso / Reliability and success rate | 🟠 | benchmarks internos, pass^k, variância |
| M5.10 | Governança e responsabilização / Governance and accountability | 🟠 | dono do agente, kill switch, aprovações, trilha de auditoria |

---

## PARTE N: Domínio Finanças, Economia e Socioeconomia / Finance, Economics and Socioeconomics Domain

> Receitas específicas do domínio que sustentam os projetos integradores da Parte P. Contexto brasileiro em primeiro plano (BCB, CVM, Open Finance Brasil, Pix, IBGE), com equivalentes internacionais.
> Domain-specific recipes backing the Part P projects. Brazilian context first, with international equivalents.

### N1. Crédito e risco de crédito / Credit and credit risk
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| N1.01 | Scorecard de concessão com WoE/IV / Application scorecard with WoE/IV | 🟢 | optbinning, scorecardpy, regressão logística, pontos por atributo, PDO |
| N1.02 | Scorecard com GBM e explicabilidade regulatória / GBM scorecards with regulatory explainability | 🟡 | XGBoost/LightGBM monotônicos, EBM, SHAP, reason codes |
| N1.03 | Inferência de rejeitados / Reject inference | 🟠 | parcelamento, augmentation, fuzzy, modelos de seleção (Heckman) |
| N1.04 | Modelos PD, LGD e EAD / PD, LGD, EAD models | 🟠 | PD point-in-time vs through-the-cycle, LGD beta/fracionária, CCF, survival |
| N1.05 | Perda esperada IFRS 9 / CPC 48 / Resolução CMN 4.966 | 🔴 | estágios, SICR, ECL lifetime, cenários macro ponderados |
| N1.06 | Behavior score e gestão de limites / Behavior scoring and limit management | 🟡 | features de comportamento, limites dinâmicos, otimização sob risco |
| N1.07 | Precificação baseada em risco e elasticidade / Risk-based pricing and elasticity | 🔴 | elasticidade causal à taxa (↔ H2, L1), RAROC, otimização de margem |
| N1.08 | Cobrança e recuperação / Collections and recovery | 🟠 | time-to-cure (survival), uplift por ação de cobrança, roll rates, otimização de régua |
| N1.09 | Avaliação automática de imóveis (AVM) para garantias / Automated valuation models for collateral | 🟠 | modelos hedônicos, comparáveis, geo-features (H3), GBM, intervalos de predição, LTV |
| N1.10 | Crédito com garantia (home equity, auto) / Secured lending | 🟠 | LTV dinâmico, risco de garantia, correlação PD × valor da garantia |
| N1.11 | Crédito para PMEs com dados alternativos / SME lending with alternative data | 🟠 | Open Finance, notas fiscais, fluxo de caixa, grafos de relacionamento |
| N1.12 | Validação de modelos de risco (backtesting, estabilidade) / Risk model validation | 🟡 | KS, Gini, PSI, CSI, binomial test, Hosmer-Lemeshow, Traffic Light |
| N1.13 | Early warning e monitoramento de carteira / Early warning and portfolio monitoring | 🟠 | safras (vintage), migração de rating, sinais antecedentes |
| N1.14 | Testes de estresse de crédito / Credit stress testing | 🔴 | modelos satélite macro → PD, cenários, simulação de perdas |

### N2. Fraude, PLD/AML e compliance / Fraud, AML and compliance
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| N2.01 | Fraude de transação (cartão, Pix) / Transaction fraud | 🟡 | features de velocidade, perfis, GBM, regras + ML, custo de falsos positivos |
| N2.02 | Fraude de aplicação e identidade sintética / Application and synthetic identity fraud | 🟠 | consistência cadastral, grafos de identidade, device fingerprint |
| N2.03 | Fraude documental e deepfake no onboarding / Document fraud and deepfakes in onboarding | 🔴 | detecção de adulteração, liveness, detecção de deepfakes, VLMs |
| N2.04 | PLD/AML com grafos / AML with graphs | 🟠 | tipologias, community detection, GNNs, ranking de alertas |
| N2.05 | Redução de falsos positivos em alertas AML / AML alert false-positive reduction | 🟠 | priorização, aprendizado com decisões de analistas, explicabilidade |
| N2.06 | Categorização de transações / Transaction categorization | 🟢 | regras, TF-IDF + LR, embeddings, LLM com taxonomia, MCC |
| N2.07 | RegTech: interpretação de normas com LLM / Regulatory interpretation with LLMs | 🟠 | RAG sobre normas BCB, CVM, ANPD; versionamento de normas, citações |
| N2.08 | Monitoramento de conduta e comunicações / Conduct and communications monitoring | 🟠 | ASR + classificação, reclamações e ouvidoria, Reclame Aqui |

### N3. Mercados, investimentos e tesouraria / Markets, investments and treasury
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| N3.01 | Dados de mercado e ajustes corporativos / Market data and corporate actions | 🟢 | cotações, dividendos, splits; yfinance, B3, CVM, dados de fundos |
| N3.02 | Backtesting sem vieses / Bias-free backtesting | 🟠 | survivorship, look-ahead, purged/embargoed CV, deflated Sharpe; vectorbt, backtrader, zipline-reloaded |
| N3.03 | Previsão de volatilidade / Volatility forecasting | 🟡 | GARCH (arch), volatilidade realizada, HAR, DL, foundation models de séries |
| N3.04 | Otimização de portfólio / Portfolio optimization | 🟡 | Markowitz, risk parity, HRP, Black-Litterman, robusta; PyPortfolioOpt, Riskfolio-Lib, CVXPY |
| N3.05 | Risco de mercado: VaR e Expected Shortfall / Market risk: VaR and ES | 🟠 | histórico, paramétrico, Monte Carlo, cópulas, backtesting de VaR (Kupiec, Christoffersen) |
| N3.06 | Curva de juros / Yield curve modeling | 🟠 | Nelson-Siegel, Svensson, curvas DI e NTN-B, PCA de curva |
| N3.07 | Precificação de derivativos com ML / Derivatives pricing with ML | 🔴 | Black-Scholes, Monte Carlo, PINNs para EDPs (↔ L5.03), neural SDEs, QuantLib |
| N3.08 | Deep hedging e RL em finanças / Deep hedging and RL in finance | 🔴 | deep hedging, execução ótima, armadilhas de RL em mercados |
| N3.09 | NLP financeiro / Financial NLP | 🟠 | sentimento de notícias, fatos relevantes, earnings calls, FinBERT, LLMs |
| N3.10 | Fatores e alphas / Factor investing and alpha research | 🟠 | fatores (valor, momento, qualidade), Fama-French, ML cross-sectional |
| N3.11 | Microestrutura e livro de ofertas / Market microstructure and order books | 🔴 | dados de alta frequência, simulação de LOB, impacto de mercado |
| N3.12 | Liquidez, ALM e fluxo de caixa / Liquidity, ALM and cash-flow forecasting | 🟠 | LCR, NSFR, gaps de descasamento, previsão de saques e captações |

### N4. Macroeconomia e economia aplicada / Macroeconomics and applied economics
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| N4.01 | Dados macroeconômicos brasileiros / Brazilian macro data | 🟢 | BCB SGS, Focus (Olinda), IBGE SIDRA, Ipeadata, FRED; python-bcb, sidrapy |
| N4.02 | Econometria de séries temporais / Time-series econometrics | 🟡 | estacionariedade, cointegração, VAR, VECM, impulso-resposta; statsmodels |
| N4.03 | Nowcasting de atividade / Activity nowcasting | 🟠 | modelos de fatores dinâmicos, MIDAS, bridge equations, ML com dados mistos |
| N4.04 | Previsão de inflação / Inflation forecasting | 🟠 | Phillips, combinação de previsões, ML, foundation models de séries, desagregação por itens |
| N4.05 | Análise de comunicação de bancos centrais / Central bank communication analysis | 🟠 | atas e comunicados do Copom, índices hawkish/dovish, LLMs |
| N4.06 | Modelos DSGE e calibração / DSGE models and calibration | 🔴 | Dynare, estimação bayesiana, SBI (↔ L2) |
| N4.07 | Macro baseada em agentes / Agent-based macroeconomics | 🔴 | ABMs macro, calibração, agentes LLM (↔ L4) |
| N4.08 | Risco sistêmico e contágio em redes financeiras / Systemic risk and network contagion | 🔴 | redes interbancárias, DebtRank, CoVaR, simulação de choques |
| N4.09 | Indicadores alternativos e de alta frequência / Alternative and high-frequency indicators | 🟠 | preços online, luzes noturnas, dados de pagamentos, busca |
| N4.10 | Previsão de câmbio e juros / FX and rates forecasting | 🟠 | modelos estruturais vs ML, avaliação fora da amostra, testes de Diebold-Mariano |

### N5. Socioeconomia e políticas públicas / Socioeconomics and public policy
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| N5.01 | Microdados socioeconômicos / Socioeconomic microdata | 🟢 | PNAD Contínua, Censo, POF, RAIS, CAGED, CadÚnico agregado; Base dos Dados, pesos amostrais |
| N5.02 | Análise de pesquisas com desenho amostral complexo / Complex survey analysis | 🟡 | pesos, estratos, conglomerados; samplics, survey (R) |
| N5.03 | Desigualdade e pobreza / Inequality and poverty | 🟡 | Gini, Theil, Foster-Greer-Thorbecke, curvas de Lorenz, decomposições |
| N5.04 | Decomposição de diferenciais salariais / Wage gap decomposition | 🟠 | Oaxaca-Blinder, RIF regressions, quantílicas |
| N5.05 | Estimação para pequenas áreas / Small area estimation | 🟠 | Fay-Herriot, modelos hierárquicos bayesianos, imagens de satélite + ML |
| N5.06 | Avaliação de impacto de programas sociais / Social program impact evaluation | 🟠 | DiD com múltiplos períodos, RDD, controle sintético (↔ H2, L1) |
| N5.07 | Microssimulação tributária e de transferências / Tax-benefit microsimulation | 🔴 | modelos estáticos e comportamentais, simulação de reformas |
| N5.08 | Mercado de trabalho e emprego / Labor market analytics | 🟡 | previsão de emprego, matching de vagas, transições ocupacionais |
| N5.09 | Endividamento e saúde financeira das famílias / Household debt and financial health | 🟠 | superendividamento, comprometimento de renda, segmentação, early warning |
| N5.10 | Inclusão financeira e fairness no acesso a crédito / Financial inclusion and fair credit access | 🟠 | métricas de acesso, vieses regionais e demográficos (↔ M2.05) |
| N5.11 | Mercado imobiliário e acessibilidade habitacional / Housing markets and affordability | 🟠 | índices de preços (FipeZap, ITBI), repeat sales, hedônicos |

### N6. Dados e regulação do sistema financeiro / Financial system data and regulation
| ID | Problema / Problem | Nv | Stacks e eixos |
|---|---|---|---|
| N6.01 | Integração com Open Finance Brasil / Open Finance Brasil integration | 🟠 | consentimentos, APIs, normalização de dados de contas e transações |
| N6.02 | Modelagem de dados bancários / Banking data modeling | 🟡 | contratos, parcelas, eventos, saldos; snapshots e históricos (SCD) |
| N6.03 | Dados regulatórios e reporte / Regulatory data and reporting | 🟠 | SCR, documentos regulatórios, qualidade e reconciliação |
| N6.04 | Gestão de risco de modelos no setor financeiro / Model risk management in finance | 🟠 | inventário, tiering, validação independente, Res. CMN 4.557, SR 11-7 (↔ M2.09) |
| N6.05 | LGPD e sigilo bancário em projetos de dados / LGPD and banking secrecy | 🟠 | LC 105/2001, bases legais, anonimização, dados sintéticos (↔ L3.13) |
| N6.06 | Uso de IA generativa em instituições financeiras / GenAI in financial institutions | 🟠 | riscos, governança, terceirização de serviços, supervisão |

---

## PARTE P: Projetos End-to-End Integradores / Integrating End-to-End Projects

Cada projeto combina várias receitas-mãe, do dado bruto à produção e monitoramento, em três níveis de profundidade (🟢 versão mínima → 🟠 produção → 🔴 SOTA). Foco principal em **sistemas financeiros, economia e socioeconomia**. A coluna de dados sugere bases públicas para executar o projeto sem dados proprietários.
Each project combines several parent recipes, from raw data to production and monitoring, at three depth tiers. Main focus on **financial systems, economics and socioeconomics**. The data column suggests public datasets.

### P1. Crédito e risco de crédito / Credit and credit risk
| ID | Projeto / Project | Receitas combinadas | Dados públicos sugeridos |
|---|---|---|---|
| P1.01 | Motor de concessão de crédito E2E: scorecard → GBM → decisão → monitoramento / E2E credit decision engine | N1.01–N1.03, N1.12, D1.06, D1.07, G1, G3 | Home Credit Default Risk, Give Me Some Credit, Lending Club |
| P1.02 | Modelos PD/LGD/EAD e perda esperada IFRS 9 com cenários macro / PD-LGD-EAD and IFRS 9 ECL | N1.04, N1.05, N1.14, N4.01, D2.13 | Freddie Mac Single-Family Loan-Level, BCB SGS |
| P1.03 | AVM de imóveis para crédito com garantia / Property AVM for secured lending | N1.09, N1.10, N5.11, C2.08, D2.08, B2.08 | ITBI (Prefeitura de SP), FipeZap, dados geográficos (IBGE, OSM) |
| P1.04 | Precificação de crédito baseada em risco com elasticidade causal / Risk-based pricing with causal elasticity | N1.07, H2.01, H2.03, L1.04, D6.06, H1 | dados simulados + Lending Club |
| P1.05 | Cobrança inteligente: survival, uplift e otimização da régua / Smart collections | N1.08, D2.13, H2.03, D5.07, D6.06 | Home Credit (parcelas), dados simulados |
| P1.06 | Crédito PME com Open Finance e dados alternativos / SME lending with Open Finance | N1.11, N6.01, N2.06, C2.06, C2.09 | dados sintéticos de transações (↔ P6.06) |
| P1.07 | Underwriting assistido por LLM: documentos → parecer → auditoria / LLM-assisted underwriting | F1.04, E2.06, F3.12, F6, M4, N6.06 | documentos sintéticos (holerites, extratos, matrículas) |
| P1.08 | Early warning e monitoramento de carteira por safras / Early warning and vintage monitoring | N1.13, N1.12, G3.02, C1.03 | Freddie Mac, Lending Club |
| P1.09 | Auditoria completa de um modelo de crédito / Full audit of a credit model | M0, M2, N1.12, N6.04, N5.10, H3.04 | Home Credit, Lending Club |
| P1.10 | Stress testing de carteira com modelos satélite / Portfolio stress testing | N1.14, N4.02, N4.04, D4.07 | BCB SGS, Freddie Mac |

### P2. Fraude, PLD/AML e compliance / Fraud, AML and compliance
| ID | Projeto / Project | Receitas combinadas | Dados públicos sugeridos |
|---|---|---|---|
| P2.01 | Antifraude de transações em tempo real (cartão, Pix) / Real-time transaction fraud | N2.01, B3, C2.11, D3.08, G1, G3 | IEEE-CIS Fraud Detection, PaySim, Credit Card Fraud (ULB) |
| P2.02 | PLD/AML com grafos e GNNs / AML with graphs and GNNs | N2.04, N2.05, D6.01, B2.09, H3.01 | IBM AML transactions (sintético), Elliptic |
| P2.03 | Onboarding seguro: KYC, fraude documental e deepfake / Secure onboarding | N2.02, N2.03, E2.06, E2.09, F1.09 | datasets públicos de documentos e deepfakes |
| P2.04 | Assistente regulatório RAG (BCB, CVM, ANPD) / Regulatory RAG assistant | N2.07, F2, F6, B1.08, M4.03 | normativos públicos BCB, CVM, ANPD |
| P2.05 | Monitoramento de conduta: ouvidoria, reclamações e chamadas / Conduct monitoring | N2.08, E4.02, E3.01, F7.04 | Consumidor.gov.br, ranking de reclamações do BCB |

### P3. Mercados, investimentos e tesouraria / Markets, investments and treasury
| ID | Projeto / Project | Receitas combinadas | Dados públicos sugeridos |
|---|---|---|---|
| P3.01 | Pipeline de dados de mercado + backtesting sem vieses / Market data pipeline + bias-free backtesting | N3.01, N3.02, B1, B4.05, B5 | B3, CVM, yfinance |
| P3.02 | Gestão de portfólio E2E: retorno, risco, otimização / E2E portfolio management | N3.03, N3.04, N3.10, D1.08 | B3, Fama-French, Nefin (FEA-USP) |
| P3.03 | Risco de mercado: VaR/ES com backtesting regulatório / Market risk with VaR/ES | N3.05, N3.06, A2.05, D4.07 | B3, curvas de juros (ANBIMA, BCB) |
| P3.04 | Precificação de derivativos com PINNs e neural SDEs / Derivatives pricing with PINNs | N3.07, L5.03, L5.04, E5 | dados sintéticos e opções da B3 |
| P3.05 | Sinais a partir de texto: notícias, fatos relevantes, resultados / Text-based signals | N3.09, E3.01, F1.04, F2, N3.02 | CVM (fatos relevantes, DFP/ITR), notícias |
| P3.06 | Agente de equity research com fontes citadas / Equity research agent | F3, F2, F7.10, N3.09, F6 | CVM, relações com investidores |
| P3.07 | Simulação de mercado e livro de ofertas com agentes / Agent-based market and order book simulation | N3.11, L4.04–L4.10, L2.14, D6.05 | dados de LOB públicos (LOBSTER amostral), sintéticos |
| P3.08 | Tesouraria: previsão de fluxo de caixa e liquidez / Treasury: cash-flow and liquidity forecasting | N3.12, D4.06, D4.07, D4.05 | dados sintéticos, BCB |

### P4. Macroeconomia e economia aplicada / Macroeconomics and applied economics
| ID | Projeto / Project | Receitas combinadas | Dados públicos sugeridos |
|---|---|---|---|
| P4.01 | Nowcasting do PIB/IBC-Br com dados mistos / GDP and IBC-Br nowcasting | N4.01, N4.03, D4.09, B5.01 | BCB SGS, IBGE SIDRA, Ipeadata |
| P4.02 | Previsão de IPCA: econometria × ML × foundation models / IPCA forecasting showdown | N4.04, D4.04, D4.05, D4.10, D1.08 | IBGE SIDRA, Focus |
| P4.03 | Monitor de comunicação do Copom com LLMs / Copom communication monitor | N4.05, E3, F1.04, F6.02 | atas e comunicados do Copom |
| P4.04 | Calibração de modelo macro (DSGE ou ABM) com SBI / Macro model calibration with SBI | N4.06, N4.07, L2.04–L2.08 | BCB SGS, IBGE |
| P4.05 | Risco sistêmico e contágio em redes financeiras / Systemic risk and contagion | N4.08, D6.01, L4.03, L3.09 | dados agregados do BCB, redes sintéticas |
| P4.06 | Indicadores alternativos de atividade econômica / Alternative economic indicators | N4.09, B1.02, E2, C2.08 | luzes noturnas (VIIRS), Google Trends, preços online |
| P4.07 | Previsão de câmbio e curva de juros / FX and yield curve forecasting | N4.10, N3.06, D4, D1.08 | BCB SGS, ANBIMA |

### P5. Socioeconomia e políticas públicas / Socioeconomics and public policy
| ID | Projeto / Project | Receitas combinadas | Dados públicos sugeridos |
|---|---|---|---|
| P5.01 | Avaliação de impacto de programa de transferência de renda / Cash transfer impact evaluation | N5.06, H2.02, L1.11, N5.02 | Portal da Transparência, PNAD Contínua, Base dos Dados |
| P5.02 | Mapa de pobreza com satélite + censo (pequenas áreas) / Poverty mapping with satellite + census | N5.05, E2, N5.03, C2.08 | Censo 2022, Sentinel-2, VIIRS |
| P5.03 | Microssimulação de reforma tributária / Tax reform microsimulation | N5.07, N5.01, N5.03, L4.08 | POF, PNAD Contínua |
| P5.04 | Simulação de políticas com generative agents / Policy simulation with generative agents | L4, L1.15, L2.14, N5.01, L4.14 | PNAD Contínua (para calibrar populações) |
| P5.05 | Mercado de trabalho: previsão de emprego e desigualdade salarial / Labor market forecasting and wage gaps | N5.08, N5.04, D4, N5.02 | RAIS, Novo CAGED, PNAD Contínua |
| P5.06 | Superendividamento das famílias: diagnóstico e alerta precoce / Household over-indebtedness early warning | N5.09, N1.13, D3.02, N2.06 | BCB (endividamento), Serasa agregados, dados sintéticos |
| P5.07 | Inclusão financeira e equidade no acesso a crédito / Financial inclusion and fair credit access | N5.10, M2.05, H3.04, L1.14 | BCB (estatísticas de crédito por região), PNAD |
| P5.08 | Habitação: índices de preço e acessibilidade / Housing price indices and affordability | N5.11, N1.09, C2.08, D4 | ITBI, FipeZap, PNAD |
| P5.09 | Avaliação contrafactual de política econômica / Counterfactual economic policy evaluation | L1, H2, L4.13, N5.06 | Ipeadata, BCB, IBGE |

### P6. Plataformas e operação em instituições financeiras / Platforms and operations in financial institutions
| ID | Projeto / Project | Receitas combinadas | Dados públicos sugeridos |
|---|---|---|---|
| P6.01 | Plataforma de dados de uma financeira (lakehouse + Open Finance) / Lending company data platform | B1–B5, N6.01, N6.02, I1 | dados sintéticos (↔ P6.06) |
| P6.02 | Plataforma de MLOps com gestão de risco de modelos / MLOps with model risk management | G1–G3, N6.04, M2.09, C2.11 | Home Credit, Lending Club |
| P6.03 | Plataforma LLMOps em ambiente regulado / LLMOps in a regulated environment | J1–J5, N6.06, F6, I1.06 | — |
| P6.04 | Transformação DataOps de um time de dados financeiro / DataOps for a financial data team | K1–K4, N6.03, B5 | — |
| P6.05 | Agente de atendimento bancário com ferramentas e auditoria / Banking service agent with audit | F2, F3, F7.09, M5, J5.05 | FAQs públicas, dados sintéticos |
| P6.06 | Dados sintéticos bancários preservando topologia da rede de transações / Topology-preserving synthetic banking data | L3.04, L3.09, L3.10, L3.13, N6.05 | IBM AML, PaySim (como referência) |
| P6.07 | LLM financeiro em PT-BR: fine-tuning, avaliação e serving / PT-BR financial LLM | F4, F5, F6, E3.08, N2.07 | normativos, CVM, textos financeiros públicos |
| P6.08 | Analista financeiro com IA (text-to-SQL + relatórios) / AI financial analyst | F2.06, F3.11, B5.10, F6 | CVM (DFP/ITR), BCB |
| P6.09 | Auditoria de sistema agêntico em instituição financeira / Agentic system audit in a financial institution | M0, M4, M5, N6.06, F6.07 | — |

### P7. Outros domínios (amplitude técnica) / Other domains (technical breadth)
| ID | Projeto / Project | Receitas combinadas | Dados públicos sugeridos |
|---|---|---|---|
| P7.01 | Previsão de demanda no varejo / Retail demand forecasting | D4, B2, G1.03, G3 | M5 (Walmart) |
| P7.02 | Sistema de recomendação de produtos (next best offer) / Product recommender | D5, B4.11, H1 | MovieLens, Santander Product Recommendation |
| P7.03 | Inspeção visual industrial / Industrial visual inspection | E2, E5.11, G1.10 | MVTec AD |
| P7.04 | Gêmeo digital híbrido física + ML / Hybrid physics + ML digital twin | L5, B3, G1 | datasets públicos de sensores |
| P7.05 | Calibração SBI de modelo epidemiológico / SBI calibration of an epidemic model | L2, L4.02 | dados públicos de saúde (DataSUS) |
| P7.06 | Treinar um LLM pequeno do zero / Train a small LLM from scratch | E3.12, E5, F4.11 | corpora abertos em PT-BR |

---

## Estatísticas do índice / Index statistics
- Partes / Parts: **15** (A–N + P)
- Receitas-mãe / Parent recipes: **587**
- Projetos E2E / E2E projects: **54** (48 em finanças, economia e socioeconomia)

## Próximos passos sugeridos / Suggested next steps
1. Revisar o escopo: remover, adicionar e repriorizar receitas e projetos.
2. Fechar o **template de receita** (pt-BR + EN) e o esquema de **metadados** (nível, stacks, versões, custo, hardware).
3. Gerar o esqueleto do repositório (pastas, CI, MkDocs, convenções bilíngues).
4. Produzir uma **receita-piloto** e um **projeto-piloto** (sugestão: P1.01) e validar o formato antes de escalar.
