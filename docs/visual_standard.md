# 🎨 Padrão Visual — Tech Challenge Fase 3

Padrão único aplicado a gráficos, tabelas, relatório, deck e diagrama.

> **Onde isto vira código:** as regras de gráfico abaixo estão implementadas nos helpers do notebook
> `src/notebooks/05_gold_analytics.ipynb` (paleta, formatação PT-BR, grid, molduras, margens e faixa
> de rodapé). Reexecutar o notebook regenera os 15 PNGs de `consumption/charts/` já dentro do padrão —
> não há edição manual de imagem em nenhuma etapa.

## Paleta institucional

| Cor | Hex | Uso |
|---|---|---|
| Azul institucional | `#1F3864` | Série principal, cabeçalho de tabelas, títulos de seção |
| Azul médio | `#2E5395` | Segunda série, subtítulos |
| Azul claro | `#7BA7D7` | Terceira série, edição mais antiga em séries temporais |
| Laranja destaque | `#E8710A` | Contraste, realce, caixa "Implicação para o cliente" |
| Cinza neutro | `#8C8C8C` | Contexto histórico (2019–2022), categoria residual |
| Cinza claro | `#F2F2F2` | Zebra de tabelas, fundo |

## Regras semânticas

- Série única e rankings: azul institucional.
- Comparação de dois grupos: azul institucional + laranja.
- Estado praticado × desejado: cinza neutro (o que **é**) + azul institucional (o que **se quer**) —
  o cinza evita sugerir que o modelo atual seja o "errado"; o contraste já comunica a lacuna.
- Séries de três edições: gradiente claro → médio → institucional (transmite progressão temporal).
- Categoria nova, sem série comparável (ex.: `Especialista/Staff+`, criada em 2025/26): laranja de
  destaque, para deixar explícito que não há histórico atrás dela.
- Contexto histórico: cinza neutro.
- **Vermelho e verde não são usados em categorias neutras**, para não sugerir juízo de valor.
- **Exceção declarada:** o diagrama de arquitetura mantém as cores oficiais AWS nos serviços
  (verde S3, roxo Glue, vermelho IAM), por convenção de mercado reconhecida por avaliadores.

## Formatação de gráficos

- Figura 10 × 5,2 pol a 200 dpi; fonte sem serifa; título 12 pt em negrito.
- Grid apenas no eixo de valor, transparência 25%, atrás das barras.
- Molduras superior e direita removidas.
- Margem de 20–30% reservada no eixo de valor: rótulos nunca são cortados.
- Faixa fixa reservada ao rodapé: fonte, edição e n nunca colidem com o eixo.
- **Números em PT-BR**: vírgula decimal e ponto de milhar (R$ 18.001 · 24,0%).
- Todo gráfico traz fonte, edição e n amostral no rodapé.

## Formatação de tabelas

- Cabeçalho `#1F3864` com texto branco em negrito; zebra `#F2F2F2`; bordas cinza.
- Primeira coluna alinhada à esquerda. Colunas curtas — números, classificações, prazos
  (`Alta`, `0–90 dias`) — centralizadas, com o cabeçalho centralizado junto. Colunas de texto
  corrido permanecem à esquerda: centralizar frase longa prejudica a leitura.
- Corpo 9 pt. Legenda numerada acima da tabela, com campo automático de numeração
  (`SEQ Tabela` no Word — precisa ser atualizado com F9 antes de exportar o PDF).

## Cores funcionais do material executivo

Além da paleta principal, o deck usa variações declaradas — todas derivadas dela:

| Cor | Hex | Uso | Por quê |
|---|---|---|---|
| Laranja escuro | `#C4610A` · `#A34D00` | Texto do *eyebrow* e do rótulo "Implicação para o cliente" | O `#E8710A` puro não tem contraste suficiente em texto pequeno |
| Laranja claro | `#FFF3E0` | Fundo da caixa "Implicação para o cliente" | Realce sem competir com o gráfico ao lado |
| Vermelho / âmbar | `#B02A20` · `#9A6B00` | Prioridade **Alta** / **Média** na matriz de recomendações | **Exceção declarada** à regra "sem vermelho/verde": aqui a categoria *é* um juízo de valor (urgência), e não uma categoria neutra |
| Escala de cinzas | `#1A1A1A` → `#777777` | Corpo, subtítulo, legenda de figura, rodapé | Hierarquia tipográfica: quanto mais claro, mais acessório |
