# 🎓 Roteiro de Arguição — Tech Challenge Fase 3
**Respostas preparadas para as perguntas mais prováveis da banca**

Grupo: Efraim Oliveira · Érica Tarsis · Ricardo Moraes · Rodrigo Bernardino · Thiago Galvão

> **Como usar:** cada bloco traz a pergunta esperada, a resposta curta (o que dizer em 20–30 segundos)
> e a evidência de apoio (onde está no material, caso peçam para mostrar). Responda a curta primeiro;
> só aprofunde se houver follow-up.

---

## 1. "Por que os salários terminam em 1? R$ 14.001, R$ 18.001…"

**Resposta curta:** porque a pesquisa não coleta salário exato — coleta faixas. Aplicamos a premissa P3:
o ponto médio de cada faixa. A faixa de R$ 12.001 a R$ 16.000 tem ponto médio R$ 14.000,50, que
arredondamos para R$ 14.001. O "1" é resíduo aritmético da regra, não um valor observado.

**Se aprofundarem:** por isso vários grupos exibem exatamente a mesma mediana — o conjunto de valores
possíveis é discreto. Três grupos empatarem em R$ 14.001 não é coincidência suspeita: é a granularidade
do instrumento. É como medir altura com régua marcada a cada 10 cm.

**Evidência:** Tabela 4 (premissa P3) · Seção 6.1 · Tabela 10.

---

## 2. "Por que não há testes de hipótese ou intervalos de confiança?"

**Resposta curta:** foi decisão metodológica declarada, não omissão. A amostra é por conveniência —
divulgada em comunidade online, sem desenho probabilístico nem pesos amostrais. Intervalos de confiança
e testes de significância pressupõem amostragem probabilística; aplicá-los aqui produziria números com
aparência de rigor, mas sem validade inferencial para o universo de profissionais do país.

**O que fizemos em substituição:** declaramos o *n* de cada recorte, destacamos apenas diferenças de
magnitude expressiva e consistentes entre edições, e tratamos toda leitura como "entre os respondentes".

**Evidência:** Seção 2.6 (nota metodológica) · Seção 13.2 (limitações).

---

## 3. "Vocês compararam salário por cargo sem controlar senioridade — isso não enviesa?"

**Resposta curta:** essa foi exatamente a verificação que fizemos, e o resultado está na Seção 6.3.
A composição varia muito: 35,3% de sênior+ em BI contra 65,1% em ML/AI Engineer. Fixando o nível
Sênior, a hierarquia de três patamares se mantém — logo o efeito de cargo é real, não artefato.

**O ponto forte:** o controle também nos fez **corrigir** uma conclusão. Na visão agregada, Ciência de
Dados parecia valer menos que Engenharia; controlando por senioridade, as duas são idênticas em todos
os níveis. A diferença bruta vinha só da composição. E descobrimos que a mediana agregada
**subestima** o ML/AI Engineer, que atinge cerca de R$ 27.500 no nível Especialista/Staff+.

**Evidência:** Seção 6.3 · Tabela 11 · Seção 13.4 (linha 1).

---

## 4. "Por que a amostra caiu de 5.217 para 3.495 em 2025/26? Isso invalida a comparação?"

**Resposta curta:** a variação reflete adesão à pesquisa, não o tamanho do mercado. Por isso o relatório
inteiro trabalha com proporções e nunca com valores absolutos entre edições — e todo gráfico declara o
*n* correspondente.

**Se aprofundarem:** a queda afeta a precisão das estimativas em recortes pequenos, e por isso adotamos
corte de n ≥ 30 nos gráficos por grupo — premissa P8, justificada na Seção 2.6. Está registrado
também como risco na Tabela 19 e nas limitações da Seção 13.2.

**Evidência:** Seção 5.1 · Figura 2 · Tabela 19 (linha "Queda de volumetria").

---

## 5. "Como garantem que nenhum dado se perdeu no pipeline?"

**Resposta curta:** por asserções automáticas de reconciliação ao final de cada Glue Job. As 22.686
linhas ingeridas na camada Bronze correspondem exatamente às linhas gravadas na Silver, edição por
edição — zero registros descartados. Se a contagem divergir, o job falha.

**Evidência:** Tabela 7 (reconciliação) · Tabela 8 (métricas do pipeline).

---

## 6. "Como compararam edições com esquemas de colunas diferentes?"

**Resposta curta:** com um de-para versionado de cerca de 60 variáveis por edição, aplicado no Glue Job 1.
A edição 2023 usa cabeçalhos em tupla; 2024 e 2025/26 usam notação hierárquica; e os códigos mudam de
posição entre anos — a coluna de AWS, por exemplo, é 4.e.1 em 2025/26, 4.h.1 em 2024 e P4_h_2 em 2023.
Nenhuma comparação é feita antes da harmonização.

**Evidência:** Seção 2.2 · Tabela 3 · `src/config/column_mapping.json`.

---

## 7. "Por que incluíram 2019, 2021 e 2022 se o enunciado pede as três últimas?"

**Resposta curta:** as três últimas edições (2023, 2024 e 2025/26) são o núcleo obrigatório de toda a
análise. As anteriores entram apenas como série histórica em três indicadores de longo prazo — gênero,
linguagens e cloud — onde a tendência de década agrega valor. A decisão está registrada como premissa P1.

**Evidência:** Tabela 2 · Tabela 4 (P1) · Figuras 7, 9 e 10.

---

## 8. "Vocês usaram Spark de verdade ou só pandas?"

**Resposta curta:** todo o processamento — ingestão, harmonização e agregações — é PySpark, executado em
dois Glue Jobs. Pandas e Matplotlib aparecem apenas na etapa final de visualização, sobre os agregados
já reduzidos da camada Gold, que têm poucas dezenas de linhas.

**Evidência:** `src/jobs/job_01_bronze_to_silver.py` e `src/jobs/job_02_silver_to_gold.py` · notebooks 02, 03 e 05.

---

## 9. "Qual a recomendação mais importante para o cliente?"

**Resposta curta:** governar o uso de IA generativa agora. Em dois anos, a modalidade "empresa paga a
ferramenta" saltou de 6,4% para 42,4% — o uso migrou do gratuito e não governado para o corporativo
licenciado. Para um banco regulado, publicar a política de uso e fornecer ferramenta oficial é
simultaneamente ganho de produtividade e mitigação de risco de vazamento. É custo baixo e efeito imediato.

**Evidência:** Seção 9.2 · Tabela 14 · Seção 12.4 (quick wins de 90 dias).

---

## 10. "O que os dados NÃO permitem afirmar?"

**Resposta curta:** três coisas. Primeira: não permitem projeção estatística para o universo de
profissionais do Brasil — a amostra é por conveniência. Segunda: não permitem inferência causal; tudo é
correlacional. Terceira: os níveis absolutos de adoção de tecnologia provavelmente estão superestimados,
porque a pesquisa circula em comunidade digitalmente engajada. Por isso confiamos mais nas tendências
direcionais entre edições do que nos níveis absolutos.

**Evidência:** Seção 13.2 (limitações metodológicas).

---

## 11. "Por que a conclusão de cloud usa só a AWS? Não é porque o projeto roda na AWS?"

**Resposta curta:** é o contrário — escolhemos a AWS como referência e, por coerência, construímos o
pipeline nela. A decisão tem três motivos, todos na Seção 8.2. Primeiro, a decisão do cliente é
unívoca: ele precisa eleger uma stack e financiar certificações, não descrever um mercado repartido.
Segundo, a divergência de rótulo de 2023 atinge os três provedores ao mesmo tempo; seguir três séries
triplicaria a incerteza daquele ponto sem mudar a conclusão. Terceiro, a liderança da AWS se apoia na
edição mais recente e não contaminada — 48,3% em 2025/26 —, com a maior amplitude de crescimento da
série (23,3% em 2019).

**Se aprofundarem:** Azure e GCP continuam na Figura 10 como contexto de mercado, mas nenhuma
recomendação da Seção 12 se apoia neles. E testamos se a série estaria quebrada pela mudança de
rótulo: somando as marcações dos três provedores sobre a base válida, a densidade de resposta é
praticamente idêntica — 104,5% em 2023 e 104,3% em 2024. A hipótese de quebra não se confirmou.

**Evidência:** Seção 8.2 · Figura 10 · Tabela 19 (última linha).

---

## 12. "Vocês cortaram os grupos pequenos. Isso não é escolher o que mostrar?"

**Resposta curta:** é premissa declarada — P8 — e é corte de exibição, não de processamento: nenhum
registro sai do pipeline, e os grupos pequenos continuam íntegros na camada Gold. O motivo é medido,
não convencional: como a pesquisa coleta faixas e não valores, a mediana de um grupo pequeno salta
uma faixa inteira quando um único respondente muda. Reamostrando os dados, a mediana de
Estatística/Economia (n = 9) oscila entre R$ 1.500 e R$ 18.000 — sete faixas. Exibir isso ao lado de
um grupo de 599 respondentes comunicaria uma precisão que o dado não tem.

**Se aprofundarem:** o critério afeta 2 dos 12 grupos de cargo de 2025/26 — 25 pessoas, 1,0% da base
— e a região Norte no recorte por senioridade. Todos são nomeados no texto quando ficam de fora.

**Evidência:** Tabela 4 (P8) · Seção 2.6 · `config/versioned_assumptions.md`.

---

## ⚡ Perguntas-relâmpago (resposta de uma linha)

| Pergunta | Resposta |
|---|---|
| Quantas tabelas na camada Gold? | 20 tabelas analíticas, em Parquet e CSV. |
| Por que Medallion? | Bronze imutável garante auditoria; Silver harmoniza; Gold serve consulta rápida. |
| Por que Athena e não Redshift? | Serverless, sem cluster provisionado, custo por consulta — adequado ao volume e ao Lab. |
| Por que mediana e não média? | Robustez à assimetria típica de distribuições salariais. |
| Por que evitaram gráficos de pizza? | Acima de três categorias, a percepção de proporção por ângulo é ruim; usamos barras. |
| Quem é o perfil mais bem pago? | ML/AI Engineer — R$ 18.001 na mediana geral e cerca de R$ 27.500 no topo. |
| Qual o maior desafio dos gestores? | Dividir tempo entre entregas técnicas e gestão (36,3%). |
| A participação feminina melhorou? | Não: pico de 24,8% em 2022, recuo para 22,0% em 2025/26. |

---

## 🎯 Frase de encerramento

> "A vantagem competitiva do cliente não estará em adotar IA — estará em ter dados confiáveis,
> plataforma moderna e gente capaz de capturar valor antes da paridade do mercado. A arquitetura que
> construímos não apenas produziu essas respostas: é o protótipo funcional da plataforma que recomendamos."

*Fonte dos dados: State of Data Brasil — Data Hackers & Bain (Kaggle), edições 2019 a 2025/26.*
