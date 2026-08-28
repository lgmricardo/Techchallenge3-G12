# 🧭 Guia AWS Passo a Passo — Tech Challenge Fase 3
**Do acesso à conta até as evidências anexadas na entrega · escrito para quem nunca usou AWS**

Grupo: Efraim Oliveira · Érica Tarsis · Ricardo Moraes · Rodrigo Bernardino · Thiago Galvão
Pré-requisitos: pacote `tech_challenge_fase3_pipeline.zip` (scripts em `src/jobs/`, queries no notebook 04) e os 6 CSVs da pesquisa.

> **Regra de ouro:** siga as partes na ordem. Cada parte termina com um ✅ *checkpoint* (o que você deve estar vendo) e uma 📸 *evidência* (print para a entrega). Se o checkpoint não bater, pare e avise no grupo — não improvise.

---

## PARTE 0 — Acesso à conta (AWS Academy Learner Lab)

No AWS Academy **não se cria conta AWS própria nem se cadastra cartão**. A FIAP envia um convite para um laboratório pronto.

1. Procure no e-mail institucional o convite **"AWS Academy Learner Lab"** (remetente AWS Academy/Instructure). Olhe também o spam.
2. Clique em **Get Started** e crie sua senha na plataforma Canvas (`awsacademy.instructure.com`).
3. Faça login no Canvas → **Dashboard** → abra o curso **AWS Academy Learner Lab**.
4. Menu lateral **Modules** → clique em **Launch AWS Academy Learner Lab** → aceite os termos (só na 1ª vez).
5. Na tela do laboratório (Vocareum), clique em **Start Lab** e aguarde o círculo ao lado da palavra **AWS** ficar **verde** (1–3 min).
6. Clique no link **AWS** (com o círculo verde) → o Console AWS abre em nova aba, já logado.
7. No canto superior direito do Console, confira a região: **N. Virginia (us-east-1)**. **Não mude a região** — o LabRole só funciona bem nela.

**Coisas importantes do Learner Lab:**
- ⏱️ A sessão dura ~4 horas (timer no topo). Pode clicar **Start Lab** de novo quantas vezes precisar.
- 💰 Há um orçamento de créditos (ex.: US$ 50) mostrado ao lado do timer. **Se zerar, a conta bloqueia sem volta.** Nosso projeto consome centavos se seguirmos este guia (S3 + 2 jobs pequenos + Athena).
- 💾 Quando a sessão expira, **nada do S3/Glue é apagado** — só a sessão fecha.
- 🔚 Ao terminar o dia, clique em **End Lab**.

✅ **Checkpoint:** Console AWS aberto, região us-east-1, timer rodando.
📸 **Evidência E01:** print da tela do Learner Lab/Vocareum (timer + budget) com a sessão ativa. *(Requisito R2)*

---

## PARTE 1 — Criar o bucket S3 e subir os CSVs (camada Bronze)

1. Na barra de busca do Console, digite **S3** → abra o serviço → **Create bucket**.
2. **Bucket name:** `stateofdata-fiap-grupo-<seunome>` (tudo minúsculo, sem espaço/acento; o nome é único no mundo — se der erro "already exists", acrescente números).
3. Region: **us-east-1**.
4. **Block Public Access:** deixe **TODAS as caixas marcadas** (padrão). Não desmarque nada.
5. **Default encryption:** deixe **SSE-S3** (padrão, já vem habilitado).
6. Clique **Create bucket**.
7. Entre no bucket → **Create folder** → nome `datalake` → dentro dela crie `bronze` → dentro de `bronze`, crie **6 pastas**, exatamente com estes nomes:
   `ano=2019` · `ano=2021` · `ano=2022` · `ano=2023` · `ano=2024` · `ano=2025`
8. **Renomeie os CSVs no seu computador ANTES do upload** — o Job 1 procura exatamente este padrão:

| Pasta no S3 | Nome exato do arquivo |
|---|---|
| `ano=2019/` | `state_of_data_2019.csv` |
| `ano=2021/` | `state_of_data_2021.csv` |
| `ano=2022/` | `state_of_data_2022.csv` |
| `ano=2023/` | `state_of_data_2023.csv` |
| `ano=2024/` | `state_of_data_2024.csv` |
| `ano=2025/` | `state_of_data_2025.csv` |

9. Entre em cada pasta `ano=YYYY` → **Upload** → **Add files** → selecione o CSV correspondente → **Upload** (aguarde a barra verde "Succeeded").

✅ **Checkpoint:** 6 pastas, cada uma com 1 CSV com o nome exato da tabela acima.
📸 **Evidências:** **E02** — aba *Permissions* do bucket mostrando **Block public access: On** *(segurança 8.1)*; **E03** — listagem de `datalake/bronze/` com as 6 pastas e arquivos *(R1 e R3)*.

---

## PARTE 2 — Criar e rodar os 2 Glue Jobs (ETL PySpark)

### 2.1. Job 1 — Bronze → Silver
1. Busque **Glue** no Console → menu **ETL jobs** → **Script editor** → engine **Spark** → **Create script** (opção "Start fresh").
2. Apague o conteúdo de exemplo e **cole o arquivo inteiro** `src/jobs/job_01_bronze_to_silver.py` do pacote.
3. Aba **Job details** — preencha exatamente:
   - **Name:** `job_01_bronze_to_silver`
   - **IAM Role:** `LabRole` (selecione na lista — nunca crie role nova)
   - **Glue version:** 4.0 · **Language:** Python 3
   - **Worker type:** `G.1X` · **Requested number of workers:** `2`
   - **Job timeout:** `30` minutos
   - Em **Job parameters** → **Add new parameter**:
     - Key: `--BUCKET`  ·  Value: `stateofdata-fiap-grupo-<seunome>` (só o nome, **sem** `s3://`)
4. **Save** → **Run** → acompanhe na aba **Runs** até o status **Succeeded** (5–10 min).
5. Se der **Failed:** clique na execução → **Output logs** (CloudWatch) → leia a última linha de erro. Causas comuns: nome do CSV diferente da tabela da Parte 1; parâmetro `--BUCKET` com `s3://` ou com erro de digitação; região errada.

### 2.2. Job 2 — Silver → Gold
Repita os passos com o arquivo `src/jobs/job_02_silver_to_gold.py`, nome `job_02_silver_to_gold` e o **mesmo parâmetro** `--BUCKET`. Rode **somente depois** do Job 1 dar Succeeded.

✅ **Checkpoint:** no S3 apareceram `datalake/silver/` (pastas `silver_core` e `silver_serie_longa` com arquivos `.parquet`) e `datalake/gold/` (20 pastas de tabelas + `csv/`).
📸 **Evidências:** **E04a/E04b** — script do Job 1 aberto + aba Runs com **Succeeded** *(R4 e R7)*; **E05a/E05b** — Job 2 **Succeeded** *(R4 e R7)*; **E06a/E06b** — S3 mostrando silver e gold com Parquet *(R5)*.

---

## PARTE 3 — Catalogar as tabelas (Glue Data Catalog)

Escolha **UMA** das opções (a A é a mais simples para júnior):

**Opção A — Crawler (recomendada):**
1. Glue → **Crawlers** → **Create crawler** → Name: `crawler_state_of_data`.
2. **Add a data source** → S3 → `s3://<seu-bucket>/datalake/silver/` → Add. Repita adicionando `s3://<seu-bucket>/datalake/gold/`.
3. IAM Role: **LabRole**.
4. **Target database:** Add database → nome `stateofdata`.
5. Schedule: **On demand** → Create → selecione o crawler → **Run**. Aguarde "Completed".
6. Confira em Glue → **Tables**: devem aparecer `silver_core`, `silver_serie_longa` e as tabelas `gold_*`.

**Opção B — DDL manual:** no Athena, execute o bloco SQL do início do **notebook 04** (`CREATE DATABASE stateofdata`, `CREATE EXTERNAL TABLE ...` e `MSCK REPAIR TABLE` — este último registra as partições `ano=YYYY`).

✅ **Checkpoint:** database `stateofdata` com as tabelas listadas.
📸 **Evidência E07:** tela do Glue Data Catalog com o database e as tabelas *(R4)*.

---

## PARTE 4 — Consultas no Athena

1. Busque **Athena** → **Query editor**.
2. **Antes da 1ª query:** aba **Settings** → **Manage** → **Query result location:** `s3://<seu-bucket>/athena-results/` → Save. (Sem isso o Athena dá erro "output location not provided".)
3. À esquerda, selecione **Database: `stateofdata`**.
4. Abra o **notebook 04** do pacote e copie as queries **Q1 a Q7**, uma por vez → **Run**. Cada uma responde a uma pergunta de negócio do PDF.
5. Confirme que os números batem com os resultados do notebook (mesma base ⇒ mesmos números).

✅ **Checkpoint:** as 7 queries executam com status Completed e retornam tabelas.
📸 **Evidência E08:** um print por query (Q1…Q7) mostrando **SQL + resultado + database `stateofdata`** na mesma tela *(R6)*.

---

## PARTE 5 — Gráficos (opcional no Lab)

Os 15 gráficos **já foram gerados e validados** com os dados reais (notebook 05 e `consumption/charts/` do pacote) — o PDF permite ferramenta de visualização a critério do grupo, então **não é preciso gastar créditos aqui**.
Se o grupo quiser evidência extra no Lab: Glue → **Notebooks** → Create (role LabRole), cole células do notebook 05 e rode. ⚠️ Notebook interativo consome créditos por minuto: **pare a sessão do notebook assim que terminar**.

---

## PARTE 6 — Organizar as evidências e anexar na entrega

1. Crie no repositório do grupo a pasta **`evidence/`** e salve os prints com estes nomes:

| Arquivo | O que mostra | Requisito |
|---|---|---|
| `E01a_vocareum_lab_ativo.png` | Timer/budget do Lab (Vocareum) | R2 |
| `E02_bucket_block_public_access.png` | Block Public Access **On** | Segurança 8.1 |
| `E03_s3_bronze_6_edicoes.png` | bronze/ano=YYYY com os 6 CSVs | R1, R3 |
| `E04a_glue_job1_script.png` + `E04b_glue_job1_succeeded.png` | Script + aba Runs (Job 1) | R4, R7 |
| `E05a_glue_job2_script.png` + `E05b_glue_job2_succeeded.png` | Script + Run Succeeded (Job 2) | R4, R7 |
| `E06a_s3_silver.png` + `E06b_s3_gold.png` | Camadas silver e gold no S3 | R5 |
| `E07_glue_catalog_tabelas.png` | Database `stateofdata` + tabelas | R4 |
| `E08_athena_q1.png` … `E08_athena_q7.png` | SQL + resultado de cada query | R6 |

   *Como printar:* Windows `Win+Shift+S` · Mac `Cmd+Shift+4`. Capture a tela inteira (com a URL do console visível).
2. Coloque a pasta `evidence/` **dentro do zip da Entrega 3** (junto de `src/notebooks/`, `src/jobs/`, `src/config/` e `consumption/charts/`).
3. O **material executivo** (`consumption/executive_deck/executive_deck.html`) já referencia a execução na AWS: slide 6 traz a legenda "executada no AWS Academy Lab" e slide 17 (Anexos) lista o bullet "A5 — Evidências de execução na AWS (E01–E08)".
4. Marque na **Matriz 11.0** os requisitos R2, R3, R4, R5, R6 e R7 como ✅ com a referência do arquivo de evidência.

---

## PARTE 7 — Encerramento e higiene de custos

1. Terminou a sessão de trabalho → **End Lab** no Vocareum.
2. Se criou Glue Notebook, **pare/exclua** a sessão dele.
3. Confira o budget restante (topo da tela do Lab).
4. **Depois da nota divulgada:** S3 → selecionar bucket → **Empty** → depois **Delete**.

---

## ⚠️ Tabela Murphy — o que pode dar errado e como resolver

| Problema | Causa provável | Solução |
|---|---|---|
| Sessão expirou no meio do job | Timer de 4h zerou | Start Lab de novo e **rode o job novamente** — os jobs são idempotentes (`mode=overwrite`), nada corrompe |
| Job Failed: "Path does not exist" | Nome/pasta do CSV diferente da tabela da Parte 1 | Corrigir nome no S3 e rodar de novo |
| Job Failed: "Access Denied" | Role errada ou região ≠ us-east-1 | Selecionar **LabRole** e conferir região |
| Job Failed logo no início | `--BUCKET` com `s3://` ou digitado errado | Valor = só o nome do bucket |
| Athena: "No output location provided" | Parte 4 passo 2 pulado | Configurar `athena-results/` |
| Athena não vê as partições `ano=` | Catalogou via DDL sem reparar | Rodar `MSCK REPAIR TABLE` (notebook 04) ou usar o Crawler |
| "Bucket name already exists" | Nome global já usado | Acrescentar sufixo numérico |
| Créditos caindo rápido | Glue Notebook ligado ocioso | Parar notebook; jobs usam no máx. 2 workers G.1X e timeout 30 min |
| Conta bloqueada (budget zerado) | Recursos esquecidos ligados | Prevenção é a única saída: End Lab + Parte 7 sempre |

---

## 👥 Sugestão de divisão (decisão final do grupo)

| Parte | Sugestão de dupla |
|---|---|
| 0–1 (conta + S3) | 1 pessoa executa, 1 confere nomes das pastas/arquivos |
| 2 (Glue Jobs) | 1 pessoa executa, 1 acompanha logs |
| 3–4 (Catálogo + Athena) | 1 pessoa executa, 1 valida números contra o notebook 04 |
| 6 (Evidências) | 1 pessoa consolida prints e atualiza a Matriz 11.0 |

*Fonte dos dados: State of Data Brazil — Data Hackers & Bain (Kaggle). Guia interno do grupo — Tech Challenge FIAP, Fase 3.*
