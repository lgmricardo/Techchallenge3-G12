# Tech Challenge — Fase 3 | Big Data & Analytics
**State of Data Brasil (Data Hackers/Bain) · AWS Academy Lab · Padrão Medallion**

Grupo: Efraim Oliveira · Érica Tarsis · Ricardo Moraes · Rodrigo Bernardino · Thiago Galvão

---

## 1. O problema de negócio

Uma **instituição financeira de grande porte** pretende expandir sua área de Dados, Analytics e IA
e precisa entender o mercado brasileiro para definir estratégias de **contratação, capacitação e
investimento**. A fonte primária é a pesquisa **State of Data Brasil** (Data Hackers/Bain).

**Pergunta norteadora:** como a evolução do mercado brasileiro de dados — perfil, senioridade,
remuneração, diversidade, tecnologias e adoção de IA — observada nas três últimas edições
(2023, 2024 e 2025/26) deve orientar essas estratégias?

---

## 2. Estratégia da solução (visão geral)

### 2.1. Escopo de dados
| Edições | Papel | Justificativa |
|---|---|---|
| **2023, 2024, 2025/26** | **Núcleo obrigatório** | Exigência do PDF: "3 últimas pesquisas" |
| 2019, 2021, 2022 | Contexto histórico (séries longas: gênero, linguagens, cloud) | Decisão do time: enriquecer tendências sem violar o escopo do PDF |

### 2.2. Arquitetura (Medallion em AWS)
```text
Kaggle (CSVs) ──upload──▶ S3 BRONZE (bruto, imutável, ano=YYYY)
                              │  Glue Job 1 (PySpark): de-para de colunas,
                              │  normalização de categorias, ponto médio salarial
                              ▼
                          S3 SILVER (Parquet)
                          ├── silver_core          (2023–2025/26, 69 colunas harmonizadas)
                          └── silver_serie_longa   (2019–2025/26, colunas mínimas)
                              │  Glue Job 2 (PySpark): agregações por tema
                              ▼
                          S3 GOLD (Parquet + CSV) — 20 tabelas analíticas
                              │  Glue Data Catalog (Crawler ou DDL)
                              ▼
                     Amazon Athena / Glue Notebook (SQL)
                              ▼
                 Notebook 05 (matplotlib) ──▶ 15 gráficos ──▶ Material executivo
```
**Segurança:** bucket privado (Block Public Access), SSE-S3, LabRole (menor privilégio),
partições `ano=YYYY`, Bronze imutável (auditabilidade/linhagem).

### 2.3. Por que essa estratégia
1. **De-para versionado antes de qualquer comparação** — os schemas divergem radicalmente
   entre edições (2023 usa cabeçalhos-tupla `('P1_a ', 'Idade')`; 2024/25 usam `1.a_idade`).
   Comparar sem harmonizar geraria conclusões espúrias. O mapping está em
   `config/column_mapping.json` (evidência de governança).
2. **Bronze imutável** — permite reprocessar tudo do zero (resiliência à expiração da sessão
   do AWS Academy Lab).
3. **Gold pequena e temática** — cada tabela responde a uma pergunta de negócio; Athena
   consulta agregados baratos, e os gráficos consomem CSVs mínimos (`toPandas()` só no fim,
   nunca na base bruta).
4. **Código único, dois ambientes** — os Glue Jobs têm fallback automático: rodam no Glue
   (produção) e localmente (validação), eliminando retrabalho.

---

## 3. Estrutura do repositório

```text
src/
├── README.md                        ← este arquivo
├── notebooks/                       ← ENTREGA 3 (executados, com resultados reais)
│   ├── 01_bronze_ingestion.ipynb    ← Bronze: ingestão + reconciliação de volumetria
│   ├── 02_bronze_to_silver.ipynb    ← de-para, normalizações, premissas P1–P7
│   ├── 03_silver_to_gold.ipynb      ← 20 tabelas Gold × 7 perguntas de negócio
│   ├── 04_athena_queries.ipynb      ← 7 consultas SQL (Athena-ready) + DDL de catalogação
│   └── 05_gold_analytics.ipynb      ← 15 gráficos executivos (com fonte e n)
├── jobs/                            ← REQUISITO R4 (colar no console Glue)
│   ├── job_01_bronze_to_silver.py
│   └── job_02_silver_to_gold.py
└── config/
    ├── column_mapping.json          ← de-para versionado 2019–2025/26
    └── versioned_assumptions.md     ← premissas P1–P7 aprovadas pelo time

../datalake/                         ← bronze/ silver/ gold/ (camadas Medallion; espelha o S3)
../consumption/charts/               ← 15 PNGs prontos para o material executivo
```

**Ordem de execução:** 01 → 02 → 03 → 04 → 05 (cada notebook é idempotente e revalidável).

**Caminhos:** o código usa caminhos relativos à própria pasta (`../../datalake`,
`../../consumption/charts`). Execute os notebooks a partir de `src/notebooks/` e os jobs a partir
de `src/jobs/`; no Glue, o parâmetro `--BUCKET` substitui a base local por `s3://<bucket>/datalake`.

---

## 4. Premissas versionadas (aprovadas pelo grupo)

| # | Premissa | Impacto |
|---|---|---|
| P1 | Núcleo = 2023/24/25-26; históricas só em séries longas | Aderência ao PDF + tendência de 6 edições |
| P2 | Dados anonimizados na origem; análise 100% agregada, sem supressão adicional | Conformidade com uso de base pública |
| P3 | Salário por **ponto médio de faixa**: `(piso+teto)/2`; `Menos de X → X/2`; `Acima de X → X×1,125` | Habilita médias/medianas em R$ |
| P4 | Typo 2025/26 `"a R$ 3000/mês"` corrigido para R$ 30.000 (regra: teto<piso ⇒ teto×10) | 1 registro; documentado |
| P5 | Cargos agrupados em `cargo_grupo` (ex.: DE+Arquiteto juntos, como na edição 2023) | Comparabilidade entre edições |
| P6 | Multirresposta: % sobre **respondentes válidos da questão** | Evita percentuais deflacionados |
| P7 | Booleanos `1/0`, `True/False`, `TRUE/FALSE` (padrão 2024) normalizados | Corrige quebra silenciosa de 2024 |
| P8 | Recortes com **n < 30** não são exibidos (corte de exibição, não de processamento) | Evita mediana instável: com n = 9 ela oscila 7 faixas sob reamostragem. Afeta 1,0% da base; justificativa completa em `config/versioned_assumptions.md` |

**Quebras de série documentadas:** categoria `Especialista/Staff+` só existe em 2025/26;
`cor/raça` e `PCD` inexistem em 2019/2021; questionário de IA generativa nasce em 2023.

---

## 5. Aderência à Matriz 11.0 (controle de nota)

| Req. | Evidência nesta entrega |
|---|---|
| R1 | Bronze com 6 edições, núcleo 2023–2025/26 (`01_bronze_ingestion`) |
| R2 | Jobs/DDL prontos para AWS Academy Lab (prints do console na apresentação) |
| R3 | Convenção `bronze/`, `silver/`, `gold/` com partição `ano=YYYY` (`01_bronze_ingestion`) |
| R4 | `src/jobs/*.py` + DDL/Crawler no notebook 04 |
| R5 | Padrão medallion completo (notebooks 01–03) |
| R6 | 7 consultas SQL Athena-ready executadas (`04_athena_queries`) |
| R7 | PySpark em todo o processamento (notebooks 02–04 e Glue Jobs) |
| R8 | 15 gráficos com fonte, edição e n (`05_gold_analytics`, `../consumption/charts/`) |
| R9 | Diagrama final em `../architecture/` (.drawio editável + PNG); esquema de referência na Seção 2.2 |
| R10 | Gráficos + achados prontos para o material executivo |
| R11 | Este repositório consolidado |
| R12 | Mapeamento tabela Gold × pergunta no cabeçalho do notebook 03 |

---

## 6. Principais achados (números reais do pipeline)

1. **IA saiu do discurso para o orçamento:** "não é prioridade" caiu de 28,8% (2023) para
   11,3% (2025/26); GenAI **paga pela empresa** saltou de 6,4% → 19,3% → **42,4%**.
2. **Prêmio de senioridade cresceu:** mediana Sênior foi de R$ 10 mil (2023) para R$ 14 mil
   (2024–25); novo degrau `Especialista/Staff+` em R$ 18 mil.
3. **Gap de gênero concentra-se no topo:** mediana idêntica em Júnior/Pleno, mas
   **-28,6% no Sênior** e -22,2% no Staff+ (2025/26); participação feminina recuou de 24,8%
   (2022) para 22,0% (2025/26).
4. **Stack dominante:** Python 92% e SQL 84% (2025/26); AWS lidera cloud (48,3%),
   validando a própria stack do projeto.
5. **Modelo de trabalho é risco de retenção:** só **1,9%** desejam 100% presencial, mas
   20,8% estão nesse modelo; híbrido flexível tem o maior gap (+23,5 p.p.).

---

## 7. Riscos e mitigações (Lei de Murphy)

| Risco | Mitigação implementada |
|---|---|
| Sessão do Academy Lab expira | Bronze imutável + jobs idempotentes (`mode=overwrite`) reprocessam tudo |
| Schema divergente entre edições | De-para versionado + `assert` de colunas ausentes no início do job |
| Volumetria adulterada/corrompida | Reconciliação `assert n == VOLUMETRIA_ESPERADA` em todas as camadas |
| Booleanos heterogêneos (2024) | Normalização por `upper()` — bug real encontrado e corrigido |
| Denominador errado em multirresposta | Base = respondentes válidos da questão (P6) em todas as tabelas Gold |
| Viés amostral (comunidade, sem pesos) | Limitação declarada; leitura "entre os respondentes", nunca "no Brasil" |
| Divergência de versão Spark entre Glue e ambiente local | `requirements.txt` fixa `pyspark==3.5.1`, compatível com o Spark 3.3 do Glue 4.0 — código restrito a APIs estáveis presentes em ambas |

---

## 8. Como executar

**Local (validação):** de dentro de `src/jobs/`, `python job_01_bronze_to_silver.py && python job_02_silver_to_gold.py`
ou executar os notebooks 01→05 em ordem.

**AWS Academy Lab:**
1. Criar bucket privado e subir os 6 CSVs em `s3://<bucket>/datalake/bronze/ano=YYYY/`.
2. Criar os 2 Glue Jobs (colar os scripts, role `LabRole`, parâmetro `--BUCKET`).
3. Rodar Job 1 → Job 2; catalogar com Crawler em `datalake/silver` e `datalake/gold`.
4. Executar as queries do notebook 04 no Athena.
5. Gerar os gráficos no Glue Notebook (ou reaproveitar `consumption/charts/`).

---

*Fonte dos dados: State of Data Brazil — Data Hackers & Bain & Company (Kaggle), edições
2019, 2021, 2022, 2023, 2024 e 2025/26. Uso exclusivamente agregado e estatístico.*
