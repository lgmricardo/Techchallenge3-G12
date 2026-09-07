# Guia de Coleta de Evidências — Tech Challenge Fase 3
**AWS Academy Learner Lab · prints E01 a E08**

Grupo: Efraim Oliveira · Érica Tarsis · Ricardo Moraes · Rodrigo Bernardino · Thiago Galvão

> **Regra dos prints:** capture sempre a janela inteira do navegador (não só um trecho).
> A URL do Console AWS deve aparecer na barra de endereços de cada print.
> **macOS:** `Cmd + Shift + 4`, depois barra de espaço + clique na janela → salva automático na Área de Trabalho.
> **Windows:** `Win + Shift + S` → recorte de janela → copiar → colar no Paint e salvar.

---

## Pré-requisitos antes de começar

Antes de tirar qualquer print, confirme que:

- [ ] `~/.aws/credentials` está preenchido com as **3 chaves** do Lab (access key, secret, session token)
- [ ] `aws sts get-caller-identity` retorna JSON sem erro (mostra Account e Arn com `LabRole`)
- [ ] Os 6 CSVs estão em `datalake/bronze/ano=YYYY/state_of_data_YYYY.csv` localmente
- [ ] Os dois arquivos de Job estão prontos: `src/jobs/job_01_bronze_to_silver.py` e `src/jobs/job_02_silver_to_gold.py`

---

## E01 — Learner Lab funcionando + Console us-east-1

**Requisito:** R2 (ambiente AWS demonstrado)
**Arquivos:** `evidence/E01a_vocareum_lab_ativo.png` (Vocareum) + `evidence/E01b_console_us_east_1.png` (Console us-east-1)

### O que fazer

1. Acesse `awsacademy.instructure.com` → faça login → abra o curso **AWS Academy Learner Lab**.
2. Menu lateral **Modules** → clique em **Launch AWS Academy Learner Lab**.
3. Na tela do **Vocareum** (painel azul), clique em **Start Lab** e aguarde o círculo ao lado de **AWS** ficar **verde**.
4. Com o círculo verde visível e o timer rodando (ex: `04:00:00` no topo), tire o print **desta tela** antes de clicar em AWS.

   **O que deve aparecer no print:**
   - Botão **AWS** com círculo **verde** ao lado
   - Timer com tempo restante (ex: `03:58:42`)
   - Budget atual (ex: `$ 50.00 / $ 50.00` ou quanto restar)
   - Cabeçalho do Vocareum com o nome do Lab

5. Clique no link **AWS** (com círculo verde) → o Console AWS abre em nova aba.
6. No Console, confira o canto superior direito: deve mostrar **N. Virginia** (ou `us-east-1`). Se mostrar outra região, clique e selecione **US East (N. Virginia)**.
7. Tire um segundo print do **Console AWS** mostrando:

   **O que deve aparecer no print:**
   - Barra de endereços: `https://us-east-1.console.aws.amazon.com/console/home?region=us-east-1`
   - Canto superior direito: **N. Virginia** visível
   - Painel principal do Console (os ícones dos serviços)

> **Dica:** junte os dois prints em um único arquivo (Vocareum + Console) ou entregue separados como `E01a` e `E01b`.

---

## E02 — Bucket S3 com Block Public Access ativado

**Requisito:** Segurança 8.1 (SSE-S3 + Block Public Access)
**Arquivo:** `evidence/E02_bucket_block_public_access.png`

### O que fazer

#### Criar o bucket (se ainda não existe)

1. No Console AWS, barra de busca → digite **S3** → clique no serviço.
2. Clique em **Create bucket**.
3. Preencha:
   - **Bucket name:** `stateofdata-g12-<suasiniciais>` (ex: `stateofdata-g12-rm`). Tudo minúsculo, sem acento, sem espaço. O nome é único globalmente — se der "already exists", acrescente um número aleatório.
   - **AWS Region:** `us-east-1`
4. **Block Public Access settings for this bucket:** deixe TODAS as 4 caixas marcadas (padrão). Não desmarque nenhuma.
5. **Default encryption:** deixe `Server-side encryption with Amazon S3 managed keys (SSE-S3)` — já vem assim por padrão no Academy.
6. Clique **Create bucket** → aguarde a mensagem verde de sucesso.

#### Tirar o print E02

1. Na listagem de buckets do S3, clique no nome do bucket que você criou.
2. Clique na aba **Permissions** (segunda ou terceira aba, ao lado de Objects e Properties).
3. Role a página até a seção **Block public access (bucket settings)**.
4. Verifique que aparece **Block all public access: On** (em verde ou com checkmark).

   **O que deve aparecer no print:**
   - URL com `https://s3.console.aws.amazon.com/s3/buckets/<nome-do-bucket>?tab=permissions`
   - Nome do bucket visível no cabeçalho da página
   - Seção **Block public access** com status **On** claramente visível
   - Opcionalmente: seção **Default encryption** logo abaixo, mostrando **SSE-S3**

> Se quiser capturar SSE-S3 também, role um pouco mais para baixo e tire um print maior. Não é obrigatório, mas reforça o requisito.

---

## E03 — Bronze: 6 CSVs no S3 com nomes corretos

**Requisito:** R1 (dados ingeridos) e R3 (estrutura Medallion)
**Arquivo:** `evidence/E03_s3_bronze_6_edicoes.png`

### O que fazer

#### Criar as pastas e fazer o upload

1. Dentro do bucket, clique em **Create folder** → nome: `datalake` → **Create folder**.
2. Entre em `datalake/` → **Create folder** → nome: `bronze` → **Create folder**.
3. Entre em `bronze/` → crie as 6 pastas abaixo (uma por vez, clicando em Create folder):

   | Pasta a criar |
   |---|
   | `ano=2019` |
   | `ano=2021` |
   | `ano=2022` |
   | `ano=2023` |
   | `ano=2024` |
   | `ano=2025` |

4. Entre em **`ano=2019/`** → clique em **Upload** → **Add files** → selecione `state_of_data_2019.csv` → **Upload**. Aguarde a barra verde "Upload succeeded".
5. Repita para cada pasta, usando o CSV correspondente:

   | Pasta | Arquivo |
   |---|---|
   | `ano=2019/` | `state_of_data_2019.csv` |
   | `ano=2021/` | `state_of_data_2021.csv` |
   | `ano=2022/` | `state_of_data_2022.csv` |
   | `ano=2023/` | `state_of_data_2023.csv` |
   | `ano=2024/` | `state_of_data_2024.csv` |
   | `ano=2025/` | `state_of_data_2025.csv` |

#### Tirar o print E03

1. Navegue até `s3://<seu-bucket>/datalake/bronze/` clicando nas pastas pelo Console.
2. Você deve ver as 6 pastas `ano=YYYY` listadas.

   **O que deve aparecer no print:**
   - URL: `https://s3.console.aws.amazon.com/s3/buckets/<bucket>?prefix=datalake/bronze/`
   - As 6 pastas `ano=2019`, `ano=2021`, `ano=2022`, `ano=2023`, `ano=2024`, `ano=2025` visíveis
   - Cabeçalho mostrando o caminho: `<bucket> > datalake > bronze`

3. Opcional (reforça R1): entre em uma das pastas (ex: `ano=2025/`) e tire um print adicional mostrando o arquivo `state_of_data_2025.csv` com o tamanho em MB — isso confirma que não está vazio.

> **Atenção:** os nomes das pastas precisam ser exatamente `ano=2019` (com sinal de igual, sem espaço). O Job 1 usa esse padrão para extrair a coluna `ano` automaticamente via particionamento Hive.

---

## E04 — Glue Job 1 criado e com execução Succeeded

**Requisito:** R4 (ETL PySpark documentado) e R7 (execução demonstrada)
**Arquivos:** `evidence/E04a_glue_job1_script.png` (script) + `evidence/E04b_glue_job1_succeeded.png` (execução Succeeded)

### O que fazer

#### Criar o Job 1

1. No Console AWS, barra de busca → **Glue** → clique no serviço.
2. Menu lateral esquerdo: **ETL jobs** → clique em **Script editor**.
3. Em "Engine", selecione **Spark**. Em "Options", selecione **"Start fresh"** → clique **Create script**.
4. A aba do editor de script abre com um código de exemplo. **Selecione tudo** (Ctrl+A ou Cmd+A) e **delete**.
5. Abra o arquivo `src/jobs/job_01_bronze_to_silver.py` no VS Code ou outro editor, **selecione todo o conteúdo** (Cmd+A) e **copie** (Cmd+C).
6. Volte ao Console do Glue e **cole** (Cmd+V) no editor. O script inteiro deve aparecer.
7. Clique na aba **Job details** (ao lado da aba "Script").
8. Preencha os campos:

   | Campo | Valor |
   |---|---|
   | **Name** | `job_01_bronze_to_silver` |
   | **IAM Role** | `LabRole` (selecionar na lista dropdown — nunca criar role nova) |
   | **Glue version** | `Glue 4.0` (Spark 3.3, Python 3) |
   | **Worker type** | `G.1X` |
   | **Requested number of workers** | `2` |
   | **Job timeout (minutes)** | `30` |

9. Role para baixo até encontrar a seção **Job parameters**. Clique em **Add new parameter**:
   - **Key:** `--BUCKET`
   - **Value:** `stateofdata-g12-<suasiniciais>` (só o nome do bucket, **sem** `s3://` e **sem** barra final)

10. Clique em **Save** (botão no canto superior direito). Aguarde a confirmação "Job saved successfully".
11. Clique em **Run** → aguarde. A aba **Runs** aparece automaticamente.

#### Acompanhar a execução

- O status inicial é **Running** (ícone laranja girando).
- Leva de **5 a 12 minutos** dependendo do tamanho dos CSVs.
- Se quiser ver os logs em tempo real: na linha da execução, clique nos três pontinhos → **View logs** → abre o CloudWatch.
- Aguarde o status mudar para **Succeeded** (ícone verde com checkmark).

#### Tirar o print E04

O ideal é **um único print** que mostre as duas coisas: o script aberto e a execução com Succeeded. Para isso:

**Opção A (um print):**
1. Abra o Glue Job `job_01_bronze_to_silver`.
2. Clique na aba **Script** para mostrar o código.
3. Sem sair da aba Script, abra a aba **Runs** em uma nova aba do navegador (clique com botão direito → abrir em nova aba).
4. Tire um print de cada aba separada.

**Opção B (dois prints, E04a e E04b):**
- Print 1 — aba **Script**: mostra o código `job_01_bronze_to_silver` aberto no editor Glue.
- Print 2 — aba **Runs**: mostra a linha de execução com status **Succeeded**.

**O que deve aparecer no print da aba Runs:**
- URL: `https://us-east-1.console.aws.amazon.com/glue/home?region=us-east-1#/v2/etl-configuration/jobs/runs/...`
- Nome do Job: `job_01_bronze_to_silver`
- Status: **Succeeded** (texto verde)
- Data/hora de início e fim da execução visíveis
- Tempo de duração (ex: `7 min 32 s`)

> **Se o job falhar:** clique na linha da execução → botão **Output logs** (ou **Error logs**) → leia a última mensagem. As causas mais comuns são: (1) `--BUCKET` digitado errado ou com `s3://`; (2) nome do CSV diferente do esperado; (3) sessão do Lab expirou — faça Start Lab de novo e clique Run novamente.

---

## E05 — Glue Job 2 com execução Succeeded

**Requisito:** R4 e R7
**Arquivos:** `evidence/E05a_glue_job2_script.png` (script) + `evidence/E05b_glue_job2_succeeded.png` (execução Succeeded)

### O que fazer

> **Execute somente depois do Job 1 ter status Succeeded no E04.**

1. Repita os mesmos passos do E04, mas usando o arquivo `src/jobs/job_02_silver_to_gold.py`.
2. Configurações idênticas ao Job 1, exceto o **Name**: `job_02_silver_to_gold`.
3. O parâmetro `--BUCKET` é o **mesmo bucket** do Job 1.
4. Clique em **Save** → **Run** → aguarde **Succeeded** (pode demorar 8–15 minutos — este job grava 21 tabelas agregadas).

#### Tirar o print E05

**O que deve aparecer:**
- URL no Console Glue
- Nome do Job: `job_02_silver_to_gold`
- Status: **Succeeded** (verde)
- Data/hora e duração da execução visíveis

---

## E06 — S3 com camadas Silver e Gold geradas (Parquet)

**Requisito:** R5 (camadas Medallion no S3)
**Arquivos:** `evidence/E06a_s3_silver.png` + `evidence/E06b_s3_gold.png`

### O que fazer

Após os dois jobs com Succeeded, navegue no S3 para confirmar que as camadas foram criadas.

#### Verificar Silver

1. Console AWS → S3 → seu bucket → `datalake/` → `silver/`.
2. Devem existir duas pastas: `silver_core/` e `silver_serie_longa/`.
3. Entre em `silver_core/` → deve haver subpastas `ano=2023/`, `ano=2024/`, `ano=2025/` (núcleo = P1, só as 3 edições recentes) com arquivos `.parquet` dentro. Já `silver_serie_longa/` tem as 6 partições (`ano=2019` a `ano=2025`).

#### Verificar Gold

1. Volte para `datalake/` → `gold/`.
2. Devem existir pastas para as 21 tabelas: `gold_respondents/`, `gold_roles/`, `gold_seniority/`, etc.
3. Também deve existir `gold/csv/` com os CSVs das tabelas agregadas.

#### Tirar os prints E06

Tire **dois prints** (ou um print largo mostrando os dois):

**Print E06a — Silver:**
- Navegue até `s3://<bucket>/datalake/silver/`
- **O que deve aparecer:** as pastas `silver_core` e `silver_serie_longa` listadas, com o caminho `<bucket> > datalake > silver` visível no breadcrumb

**Print E06b — Gold:**
- Navegue até `s3://<bucket>/datalake/gold/`
- **O que deve aparecer:** as 20 pastas `gold_*` listadas (role a tela para mostrar o máximo possível), com o caminho `<bucket> > datalake > gold` visível

> Se não aparecer a pasta `silver/` ou `gold/` no S3, o job falhou silenciosamente. Verifique os logs do job no CloudWatch (aba Runs → Output logs).

---

## E07 — Glue Data Catalog com database e tabelas

**Requisito:** R4 (catálogo de dados demonstrado)
**Arquivo:** `evidence/E07_glue_catalog_tabelas.png`

Há duas formas de catalogar: **Crawler** (mais simples) ou **DDL manual no Athena**. Escolha uma.

---

### Opção A — Crawler (recomendada para quem usa Console)

1. No Console AWS → **Glue** → menu lateral → **Crawlers** → **Create crawler**.
2. **Crawler name:** `crawler_state_of_data` → Next.
3. **Add a data source** → S3 → no campo "S3 path" → `s3://<seu-bucket>/datalake/silver/` → **Add an S3 data source**.
4. Clique novamente em **Add a data source** → `s3://<seu-bucket>/datalake/gold/` → **Add an S3 data source**. → Next.
5. **IAM Role:** selecione **LabRole** na lista → Next.
6. **Target database** → clique em **Add database** → nome: `stateofdata` → **Create database** → selecione `stateofdata` na lista → Next.
7. **Crawler schedule:** deixe **On demand** → Next → **Create crawler**.
8. Na listagem de Crawlers, selecione `crawler_state_of_data` → clique **Run** → aguarde o status mudar para **Completed** (2–5 min).
9. Após Completed, vá em Glue → **Tables** (menu lateral, sob "Data Catalog") → filtre por database `stateofdata`.

#### Tirar o print E07 (via Crawler)

**O que deve aparecer:**
- URL: `https://us-east-1.console.aws.amazon.com/glue/home?region=us-east-1#/v2/data-catalog/tables`
- Database selecionado: `stateofdata`
- Lista de tabelas incluindo `silver_core`, `silver_serie_longa` e as tabelas `gold_*` (pelo menos 10 tabelas visíveis)

---

### Opção B — DDL manual no Athena (se preferir não usar Crawler)

1. Console AWS → **Athena** → **Query editor**.
2. **Antes da primeira query:** clique em **Settings** (ícone de engrenagem) → **Manage** → em "Query result location" coloque `s3://<seu-bucket>/athena-results/` → **Save**. Isso é obrigatório, senão o Athena dá erro.
3. Na área de query, cole e execute cada bloco abaixo **em sequência** (um de cada vez, clicando em Run):

**Bloco 1 — Criar database:**
```sql
CREATE DATABASE IF NOT EXISTS stateofdata;
```

**Bloco 2 — Tabela silver_core** (cole o DDL completo de `src/notebooks/04_athena_queries.ipynb` — primeira célula, `CREATE EXTERNAL TABLE stateofdata.silver_core`):
```sql
-- Cole aqui o CREATE EXTERNAL TABLE stateofdata.silver_core (...)
-- disponível em src/notebooks/04_athena_queries.ipynb
```

**Bloco 3 — Registrar partições:**
```sql
MSCK REPAIR TABLE stateofdata.silver_core;
```

**Bloco 4 — Tabela silver_serie_longa** (também em `src/notebooks/04_athena_queries.ipynb`).

4. Após executar o DDL, tire o print do Glue Data Catalog em Glue → **Databases** → clique em `stateofdata` → veja as tabelas listadas.

#### Tirar o print E07 (via DDL)

**O que deve aparecer:**
- Tela de **Databases** do Glue Data Catalog mostrando `stateofdata` com a contagem de tabelas
- **Ou:** aba do Athena com o banco `stateofdata` selecionado e as tabelas visíveis no painel esquerdo

---

## E08 — 7 Queries no Athena (Q1 a Q7)

**Requisito:** R6 (perguntas respondidas com dados reais)
**Arquivos:** `evidence/E08_athena_q1.png` até `evidence/E08_athena_q7.png` (7 prints)

### Configuração única (fazer uma vez)

1. Console AWS → **Athena** → **Query editor**.
2. Se ainda não configurou: clique em **Settings** → **Manage** → defina `s3://<seu-bucket>/athena-results/` como output location → **Save**.
3. No painel esquerdo, em **Database**, selecione **`stateofdata`**.

### Para cada query: cole, execute, tire o print

O print de cada query deve mostrar **na mesma tela:** o SQL digitado + o resultado da tabela + o database `stateofdata` selecionado à esquerda.

---

#### Q1 — Estrutura do mercado (top cargos por edição)

Cole no editor:
```sql
SELECT ano, cargo_grupo, n, pct
FROM (
    SELECT ano, cargo_grupo, COUNT(*) AS n,
           ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY ano), 1) AS pct,
           ROW_NUMBER() OVER (PARTITION BY ano ORDER BY COUNT(*) DESC) AS rk
    FROM stateofdata.silver_core
    WHERE cargo_grupo IS NOT NULL
    GROUP BY ano, cargo_grupo
) t
WHERE rk <= 5
ORDER BY ano, rk;
```

Clique **Run query** → aguarde "Completed" → tire o print.

**O que deve aparecer no print E08_athena_q1.png:**
- Database `stateofdata` selecionado à esquerda
- O SQL da Q1 visível no editor
- Tabela de resultados com colunas: `ano`, `cargo_grupo`, `n`, `pct`
- Status **Completed** e tempo de execução visíveis
- Pelo menos 5 linhas de resultado visíveis

---

#### Q2 — Escada salarial (mediana por senioridade)

```sql
WITH ranked AS (
    SELECT ano, nivel, salario_pm,
           ROW_NUMBER() OVER (PARTITION BY ano, nivel ORDER BY salario_pm) AS rn,
           COUNT(*) OVER (PARTITION BY ano, nivel) AS cnt
    FROM stateofdata.silver_core
    WHERE salario_pm IS NOT NULL AND nivel IS NOT NULL
)
SELECT ano, nivel, MAX(cnt) AS n,
       ROUND(AVG(salario_pm), 0) AS salario_mediano_pm
FROM ranked
WHERE rn IN (CAST((cnt+1)/2 AS INTEGER), CAST((cnt+2)/2 AS INTEGER))
GROUP BY ano, nivel
ORDER BY ano, salario_mediano_pm;
```

> **Atenção — não use `APPROX_PERCENTILE(salario_pm, 0.5)` aqui.** O Athena (Trino) usa um T-digest de
> baixa precisão por padrão, que pode divergir da mediana real quando `salario_pm` tem muitos valores
> repetidos (é o ponto médio de faixas salariais, não um valor contínuo) — ex.: para 2023×Sênior ele
> retornava R$ 11.498 em vez dos R$ 10.001 corretos, mesmo com `n` idêntico (1.419), uma diferença de
> aproximação e não de filtro. O PySpark (`percentile_approx` do Job 2, `04_athena_queries.ipynb`) usa
> precisão muito maior por padrão e não tem esse problema. A query acima calcula a mediana exata via
> `ROW_NUMBER`, batendo com o `gold_salary_by_seniority.csv` e o relatório em todas as células.

**O que deve aparecer no print E08_athena_q2.png:**
- Colunas: `ano`, `nivel`, `n`, `salario_mediano_pm`
- Resultados mostrando variação de salário por senioridade ao longo dos anos
- Valores batendo com `gold_salary_by_seniority.csv` (ex.: 2023×Sênior = 10001, não 11498)

---

#### Q3 — Gap salarial de gênero (controlado por senioridade, 2025)

```sql
WITH ranked AS (
    SELECT nivel, genero, salario_pm,
           ROW_NUMBER() OVER (PARTITION BY nivel, genero ORDER BY salario_pm) AS rn,
           COUNT(*) OVER (PARTITION BY nivel, genero) AS cnt
    FROM stateofdata.silver_core
    WHERE ano = '2025'
      AND salario_pm IS NOT NULL
      AND nivel IS NOT NULL
      AND genero IN ('Masculino', 'Feminino')
),
sal AS (
    SELECT nivel, genero, MAX(cnt) AS n,
           ROUND(AVG(salario_pm), 0) AS mediana
    FROM ranked
    WHERE rn IN (CAST((cnt+1)/2 AS INTEGER), CAST((cnt+2)/2 AS INTEGER))
    GROUP BY nivel, genero
)
SELECT f.nivel,
       f.mediana AS mediana_feminino,
       m.mediana AS mediana_masculino,
       ROUND(100.0 * (f.mediana - m.mediana) / m.mediana, 1) AS gap_pct,
       f.n AS n_feminino, m.n AS n_masculino
FROM sal f
JOIN sal m ON f.nivel = m.nivel AND f.genero = 'Feminino' AND m.genero = 'Masculino'
ORDER BY m.mediana DESC;
```

> **Nota:** mesma correção da Q2 — `APPROX_PERCENTILE` usa T-digest impreciso no Trino/Athena
> quando `salario_pm` tem muitos valores repetidos. A query acima calcula a mediana exata via
> `ROW_NUMBER`, por `nivel`+`genero`. Valor esperado (verificado nos microdados): Pleno/Sênior
> mais alto do gap deve bater com mediana_feminino = 10001, mediana_masculino = 14001,
> gap_pct = -28.6.

**O que deve aparecer no print E08_athena_q3.png:**
- Colunas: `nivel`, `mediana_feminino`, `mediana_masculino`, `gap_pct`, `n_feminino`, `n_masculino`
- Valores de gap negativos (salário feminino abaixo do masculino)
- Uma linha com mediana_feminino = 10001, mediana_masculino = 14001, gap_pct = -28.6

> **Nota:** `ano` é catalogado como `varchar` pelo Crawler (vem do particionamento Hive `ano=2025/`). Compare sempre com string (`'2025'`), nunca com inteiro — `WHERE ano = 2025` falha com `TYPE_MISMATCH`.

---

#### Q4 — Tecnologias: evolução de Python, SQL e AWS

```sql
SELECT ano,
       ROUND(100.0 * AVG(CAST(lang_python AS DOUBLE)), 1) AS pct_python,
       ROUND(100.0 * AVG(CAST(lang_sql AS DOUBLE)), 1)    AS pct_sql,
       ROUND(100.0 * AVG(CAST(cloud_aws AS DOUBLE)), 1)   AS pct_aws,
       COUNT(lang_python) AS base_valida
FROM stateofdata.silver_serie_longa
GROUP BY ano
ORDER BY ano;
```

**O que deve aparecer no print E08_athena_q4.png:**
- Tabela `silver_serie_longa` (confirma que a série longa foi catalogada)
- Colunas: `ano`, `pct_python`, `pct_sql`, `pct_aws`, `base_valida`
- 6 linhas (uma por edição: 2019, 2021, 2022, 2023, 2024, 2025)

---

#### Q5 — IA generativa como prioridade (visão dos gestores)

```sql
SELECT ano, prioridade_ia_h, COUNT(*) AS n,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY ano), 1) AS pct
FROM stateofdata.silver_core
WHERE prioridade_ia_h IS NOT NULL
GROUP BY ano, prioridade_ia_h
ORDER BY ano, prioridade_ia_h;
```

**O que deve aparecer no print E08_athena_q5.png:**
- Colunas: `ano`, `prioridade_ia_h`, `n`, `pct`
- Crescimento do percentual "Alta" entre 2023 e 2025

---

#### Q6 — Modelo de trabalho: atual vs ideal (2025)

```sql
SELECT
    COALESCE(a.modelo, i.modelo) AS modelo,
    COALESCE(a.pct_atual, 0) AS pct_atual,
    COALESCE(i.pct_ideal, 0) AS pct_ideal,
    ROUND(COALESCE(i.pct_ideal, 0) - COALESCE(a.pct_atual, 0), 1) AS gap_pp
FROM (
    SELECT modelo_atual_h AS modelo,
           ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_atual
    FROM stateofdata.silver_core
    WHERE ano = '2025' AND modelo_atual_h IS NOT NULL
    GROUP BY modelo_atual_h
) a
FULL JOIN (
    SELECT modelo_ideal_h AS modelo,
           ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_ideal
    FROM stateofdata.silver_core
    WHERE ano = '2025' AND modelo_ideal_h IS NOT NULL
    GROUP BY modelo_ideal_h
) i ON a.modelo = i.modelo
ORDER BY ABS(gap_pp) DESC;
```

**O que deve aparecer no print E08_athena_q6.png:**
- Colunas: `modelo`, `pct_atual`, `pct_ideal`, `gap_pp`
- Gap positivo para "Remoto" (mais desejado do que praticado)

---

#### Q7 — Termômetro do mercado (satisfação, layoff, intenção de troca)

```sql
SELECT ano,
       ROUND(100.0 * AVG(CAST(satisfeito AS DOUBLE)), 1)  AS pct_satisfeitos,
       ROUND(100.0 * AVG(CAST(layoff_sim AS DOUBLE)), 1)  AS pct_layoff_sim,
       COUNT(satisfeito) AS n_validos
FROM stateofdata.silver_core
GROUP BY ano
ORDER BY ano;
```

> **Atenção — use `COUNT(satisfeito)`, não `COUNT(*)`.** `satisfeito` só é respondida por quem tem
> vínculo ativo (91,7% do núcleo — Tabela 5 do relatório). `COUNT(*)` conta toda linha do núcleo, inclusive
> quem não respondeu; `COUNT(satisfeito)` conta só quem de fato respondeu, que é o que "n_validos" quer dizer.
> É a mesma query do notebook `04_athena_queries.ipynb` (célula Q7) — mantenha as duas idênticas.

**O que deve aparecer no print E08_athena_q7.png:**
- Colunas: `ano`, `pct_satisfeitos`, `pct_layoff_sim`, `n_validos`
- **3 linhas** (2023, 2024, 2025) — correto por design: `satisfeito` e `layoff_sim` só existem no núcleo `silver_core` (Premissa P1), que cobre apenas essas 3 edições. Não são 6 linhas — isso seria o total da `silver_serie_longa`, que não tem essas colunas.
- Total de `n_validos` = **12.844** (4753 + 4863 + 3228) — os respondentes que de fato responderam
  satisfeito/layoff (91,7% do núcleo de 14.005; ver Tabela 5 do relatório). Não confundir com os 14.005
  do núcleo completo nem com os 22.686 da série longa (ver README).

---

## Checklist final antes de fechar o Lab

Após todos os prints:

- [ ] `evidence/E01a_vocareum_lab_ativo.png` — Vocareum verde
- [ ] `evidence/E01b_console_us_east_1.png` — Console us-east-1
- [ ] `evidence/E02_bucket_block_public_access.png` — Aba Permissions com Block Public Access On
- [ ] `evidence/E03_s3_bronze_6_edicoes.png` — 6 pastas `ano=YYYY` em `bronze/`
- [ ] `evidence/E04a_glue_job1_script.png` + `evidence/E04b_glue_job1_succeeded.png` — Job 1: script e status Succeeded
- [ ] `evidence/E05a_glue_job2_script.png` + `evidence/E05b_glue_job2_succeeded.png` — Job 2: script e status Succeeded
- [ ] `evidence/E06a_s3_silver.png` + `evidence/E06b_s3_gold.png` — Pastas `silver/` e `gold/` no S3
- [ ] `evidence/E07_glue_catalog_tabelas.png` — Database `stateofdata` com tabelas
- [ ] `evidence/E08_athena_q1.png` até `E08_athena_q7.png` — 7 queries com resultados

Após coletar tudo: clique em **End Lab** no Vocareum para encerrar a sessão (os recursos S3/Glue ficam salvos para a próxima sessão — só a sessão fecha).

---

## Onde cada evidência prova cada requisito

| Evidência | Requisito do enunciado | O que demonstra |
|---|---|---|
| E01 | R2 | Pipeline executado no AWS Academy Lab |
| E02 | Segurança 8.1 | Block Public Access + SSE-S3 (dados em repouso protegidos) |
| E03 | R1, R3 | 6 edições ingeridas na camada Bronze particionada por ano |
| E04 | R4, R7 | Job PySpark Bronze→Silver executado com sucesso |
| E05 | R4, R7 | Job PySpark Silver→Gold executado com sucesso |
| E06 | R5 | Camadas Silver (Parquet) e Gold (21 tabelas) geradas no S3 |
| E07 | R4 | Glue Data Catalog com tabelas catalogadas para o Athena |
| E08 | R6 | 7 perguntas de negócio respondidas com queries SQL nos dados reais |

*Guia interno — Tech Challenge Fase 3 · POSTECH DTAT*
