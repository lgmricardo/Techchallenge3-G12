# Tech Challenge — Fase 3 · Big Data & Analytics na AWS
**POSTECH DTAT · State of Data Brasil (Data Hackers & Bain & Company)**

Pipeline completo de Big Data & Analytics construído na AWS para apoiar uma instituição
financeira de grande porte (cliente simulado) na expansão de sua área de Dados, Analytics e IA,
a partir das seis edições públicas da pesquisa **State of Data Brasil** — 22.686 respostas.

**Grupo:** Efraim Oliveira · Érica Tarsis · Ricardo Moraes · Rodrigo Bernardino · Thiago Galvão

---

## 🎯 Pergunta norteadora

> Como a evolução do mercado brasileiro de dados (perfil profissional, senioridade, remuneração,
> diversidade, tecnologias e adoção de IA), observada nas três últimas edições da pesquisa
> State of Data Brasil, deve orientar as estratégias de **contratação, capacitação e investimento**
> de uma instituição financeira de grande porte?

As sete perguntas de desdobramento do enunciado são respondidas nos blocos analíticos do
Material Executivo (slides 7–13) e nas Seções 5–11 do Relatório Técnico.

---

## 📦 Estrutura do repositório (Medallion Architecture)

O repositório é organizado pelo fluxo do dado — `bronze → silver → gold → consumption` — e não
por tipo de entrega. Cada pasta corresponde a um estágio do pipeline:

```text
Techchallenge3-G12/
├── datalake/                          CAMADAS DE DADOS (espelha o prefixo s3://<bucket>/datalake/)
│   ├── bronze/ano=YYYY/               6 CSVs originais, brutos e imutáveis (versionados — dataset fixo)
│   ├── silver/                        Parquet harmonizado — gerado pelo Job 1
│   └── gold/csv/                      21 tabelas analíticas agregadas (versionadas)
├── src/                               CÓDIGO DO PIPELINE
│   ├── config/                        column_mapping.json + versioned_assumptions.md (P1–P8)
│   ├── jobs/                          job_01_bronze_to_silver.py · job_02_silver_to_gold.py
│   ├── notebooks/                     01_bronze_ingestion … 05_gold_analytics (executados)
│   └── README.md                      documentação técnica do pipeline
├── consumption/                       CAMADA DE CONSUMO (o que a Gold alimenta)
│   ├── charts/                        15 gráficos G01–G15 (PNG), gerados pelo notebook 05
│   ├── executive_deck/                deck executivo em HTML + PPTX + imagens
│   ├── streamlit_app/                 dataviz interativo — replica os 15 gráficos (Streamlit)
│   └── streamlit_dashboard/           board analítico avançado — mapa coroplético, gauges,
│                                       sunburst, funil, heatmap, radar (Streamlit + Plotly)
├── architecture/                      diagrama AWS: .drawio editável + PNG
├── docs/                              relatório técnico, guia AWS, roteiro de arguição, padrão visual
├── evidence/                          prints de execução no AWS Academy Lab (E01–E08)
├── install_requirements.sh            cria/atualiza o venv em .venv e checa a versão do Java
└── requirements.txt                   dependências (núcleo do pipeline + extras opcionais)
```

As três camadas do data lake trazem um `.gitkeep`: a estrutura Medallion é preservada em quem clona
o repositório, enquanto os dados (CSVs brutos, Parquet) ficam fora do versionamento.

**Ambiente local:** `./install_requirements.sh` (o pipeline exige **JDK 8, 11 ou 17** — o PySpark 3.5.1
não funciona em JDK 24+, onde o Security Manager foi removido).

**Mapa entregas × pastas**

| Entrega | Onde está |
|---|---|
| **Entrega 1** — Material executivo | `consumption/executive_deck/` (+ gráficos em `consumption/charts/`) |
| **Entrega 2** — Arquitetura AWS | `architecture/` |
| **Entrega 3** — Código do pipeline | `src/` (notebooks, Glue Jobs, config) |
| Evidência analítica | `datalake/gold/csv/` e `consumption/charts/` |
| Evidência de execução AWS | `evidence/` |
| Documentação | `docs/` |

**Convenção de nomes:** diretórios, arquivos e tabelas em inglês e minúsculos; camadas nomeadas
pelo padrão Medallion; scripts e notebooks nomeados pela transição que executam
(`bronze_to_silver`, `silver_to_gold`); tabelas Gold com prefixo `gold_` + o tema que respondem.
A chave de partição `ano=YYYY` e os nomes de coluna (`ano`, `cargo_grupo`, `salario_mediano_pm`…)
são mantidos em português por serem **contrato de dado**: aparecem no DDL do Athena
(`PARTITIONED BY (ano int)`), no cabeçalho dos CSVs entregues e nos rótulos do relatório técnico.

## 🥇 Camada Gold — 21 tabelas × pergunta de negócio

| Pergunta | Tabelas (`datalake/gold/csv/`) |
|---|---|
| 1. Estrutura do mercado | `gold_respondents` · `gold_roles` · `gold_seniority` |
| 2. Perfis valorizados | `gold_salary_by_seniority` · `gold_salary_by_role` · `gold_salary_by_role_seniority` |
| 3. Diversidade de gênero | `gold_gender_participation` · `gold_gender_seniority_salary` · `gold_gender_leadership` · `gold_gender_role_seniority` |
| 4. Tecnologias | `gold_technologies` |
| 5. Adoção de IA | `gold_ai_priority` · `gold_genai_usage` · `gold_genai_usage_by_seniority` |
| 6. Regiões e modelos de trabalho | `gold_regions` · `gold_regions_by_seniority` · `gold_work_model` |
| 7. Oportunidades e desafios | `gold_market_pulse` · `gold_job_change_intent` · `gold_job_criteria` · `gold_manager_challenges` |

`gold_salary_by_role_seniority`, `gold_regions_by_seniority`, `gold_gender_role_seniority` e
`gold_genai_usage_by_seniority` materializam o controle por nível Sênior usado na Seção 6.3/Tabela 11,
na Seção 10.1, na Seção 7.4 (Causa 1 e 2) e na Seção 9.2 do relatório técnico — adicionadas para que
esses números tenham origem rastreável no pipeline (antes eram cálculos ad hoc sem registro em nenhum
notebook).

**Conversão do Material Executivo:** abrir o HTML no navegador → Ctrl+P → salvar como PDF
(layout paisagem); ou abrir no Microsoft Word e salvar como DOCX. As imagens devem permanecer
na mesma pasta do HTML.

**Geração do PDF do Relatório Técnico — atualize os campos antes de exportar.** O DOCX usa campos
do Word para o Sumário, o Índice de Figuras, o Índice de Tabelas e a numeração das legendas
(`SEQ Tabela`/`SEQ Figura`). Enquanto não forem atualizados, os índices saem vazios e a numeração
das legendas fica desatualizada (aparece um "Tabela 11" repetido). Antes de exportar:

1. abrir `docs/technical_report_phase3_v1.docx` no Word;
2. **Ctrl+A** e depois **F9** (no macOS, `fn+F9`) — confirmar "Atualizar índice inteiro" quando perguntado;
3. conferir que Sumário e os dois índices ficaram preenchidos e que as legendas vão de 1 a 20 sem repetição;
4. **Arquivo → Salvar como / Exportar → PDF**, sobrescrevendo `docs/technical_report_phase3_v1.pdf`.

---

## 🏗️ Arquitetura (resumo)

```text
Kaggle (6 CSVs) → S3 BRONZE (ano=YYYY, imutável)
                → Glue Job 1 (PySpark): de-para + harmonização + salário PM → S3 SILVER (Parquet)
                → Glue Job 2 (PySpark): agregações temáticas → S3 GOLD (21 tabelas)
                → Glue Data Catalog → Amazon Athena (Q1–Q7) → CONSUMPTION (gráficos + deck)
```

Controles: SSE-S3 em repouso · Block Public Access · IAM LabRole (menor privilégio) ·
particionamento `ano=YYYY` · LGPD: base anonimizada na origem, uso exclusivamente agregado.

---

## 🔁 Como reproduzir

1. **Dados-fonte:** as seis edições já estão versionadas neste repositório em
   `datalake/bronze/ano=YYYY/` (também disponíveis em https://www.kaggle.com/datahackers/datasets).
   O dataset é fixo para este projeto — não há novas coletas nem atualizações — por isso optamos por
   versionar os ~57 MB de CSVs brutos: garante reprodutibilidade total sem depender de um download
   externo que pode mudar ou sair do ar.
2. **Local:** colocar os CSVs em `datalake/bronze/ano=YYYY/state_of_data_YYYY.csv` e executar os
   notebooks `src/notebooks/01…05` em ordem (PySpark local). Os caminhos são relativos à pasta
   do notebook/script (`../../datalake`), então rode-os de dentro de `src/notebooks/` ou `src/jobs/`.
3. **AWS Academy Lab:** seguir `docs/aws_step_by_step_guide.md` — do acesso ao Learner Lab
   à coleta das evidências E01–E08 (bucket S3, Glue Jobs com parâmetro `--BUCKET`,
   Crawler/DDL e queries no Athena).

Reprodutibilidade garantida por: premissas versionadas (`src/config/versioned_assumptions.md`),
de-para de ~69 colunas por edição (`src/config/column_mapping.json`), jobs idempotentes e asserções de
reconciliação — **22.686 linhas ingeridas na Bronze, 0 descartadas**, todas presentes na `silver_serie_longa`
(as 6 edições). O núcleo analítico `silver_core` (Premissa P1 — só 2023/2024/2025, mais colunas) soma
**14.005 linhas**; os dois totais medem escopos diferentes e não devem ser somados.

---

## 📚 Fontes

- DATA HACKERS; BAIN & COMPANY. *State of Data Brazil* — edições 2019 a 2025/26 (Kaggle).
- Benchmarks de contexto: Bain (IA generativa no Brasil, 2025) · McKinsey (*The State of AI*, 2025) ·
  Databricks (Medallion Architecture) · AWS Builders · Brasscom (Censo de Diversidade TIC 2024–2025).

*Todos os números das análises saem do pipeline sobre os dados oficiais da pesquisa;
fontes externas foram usadas apenas como benchmark.*
