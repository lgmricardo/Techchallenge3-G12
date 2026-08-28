# -*- coding: utf-8 -*-
"""Lógica compartilhada do board — carga de dados e construção dos gráficos Plotly.

Sem nenhuma chamada `st.*`: usado tanto pelo app interativo (board.py) quanto pelo
exportador estático (export_pdf.py), para as duas ferramentas nunca divergirem sobre
como cada gráfico é calculado a partir da camada Gold.
"""
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

BASE = Path(__file__).resolve().parents[2]
GOLD = BASE / "datalake" / "gold" / "csv"
ASSETS = Path(__file__).resolve().parent / "assets"

# ---------------------------------------------------------------------------
# Paleta institucional (mesma do relatório e do material executivo)
# ---------------------------------------------------------------------------
AZUL = "#1F3864"
AZUL_MED = "#2E5395"
AZUL_CLARO = "#7BA7D7"
LARANJA = "#E8710A"
CINZA = "#8C8C8C"
CINZA_TXT = "#666666"
BG_CARD = "#F7F8FA"
SERIE = [AZUL_CLARO, AZUL_MED, AZUL]

ROTULO_ANO = {2019: "2019", 2021: "2021", 2022: "2022", 2023: "2023", 2024: "2024", 2025: "2025/26"}
ROTULOS_ORDEM = list(ROTULO_ANO.values())  # força eixo categórico em ordem cronológica (não numérica)
NIVEIS = ["Júnior", "Pleno", "Sênior", "Especialista/Staff+"]
UF_REGIAO = {  # código IBGE de cada UF (properties.codigo_ibg no GeoJSON de fronteiras) -> macrorregião
    "11": "Norte", "12": "Norte", "13": "Norte", "14": "Norte", "15": "Norte", "16": "Norte", "17": "Norte",
    "21": "Nordeste", "22": "Nordeste", "23": "Nordeste", "24": "Nordeste", "25": "Nordeste",
    "26": "Nordeste", "27": "Nordeste", "28": "Nordeste", "29": "Nordeste",
    "31": "Sudeste", "32": "Sudeste", "33": "Sudeste", "35": "Sudeste",
    "41": "Sul", "42": "Sul", "43": "Sul",
    "50": "Centro-oeste", "51": "Centro-oeste", "52": "Centro-oeste", "53": "Centro-oeste",
}
ANOS_NUCLEO = [2023, 2024, 2025]
PLOT_CFG = dict(displayModeBar=False)


def ler(nome):
    return pd.read_csv(GOLD / f"{nome}.csv")


def geojson_uf():
    with open(ASSETS / "brasil_uf.geojson", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Gauge genérico (usado 6x: Tab 1 e Tab 3)
# ---------------------------------------------------------------------------
def fig_gauge(value, title, ref=None, max_v=100, suffix="%"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta" if ref is not None else "gauge+number",
        value=value,
        number={"suffix": suffix, "font": {"size": 30, "color": AZUL}},
        delta={"reference": ref, "increasing": {"color": LARANJA}, "decreasing": {"color": "#B02A20"},
               "font": {"size": 13}} if ref is not None else None,
        gauge={
            "axis": {"range": [0, max_v], "tickfont": {"size": 9}},
            "bar": {"color": AZUL, "thickness": 0.75},
            "bgcolor": "white",
            "steps": [{"range": [0, max_v * 0.5], "color": "#EFEFEF"},
                      {"range": [max_v * 0.5, max_v], "color": "#E2E8F0"}],
            "threshold": {"line": {"color": LARANJA, "width": 3}, "thickness": 0.85, "value": value},
        },
        title={"text": title, "font": {"size": 13, "color": CINZA_TXT}},
    ))
    fig.update_layout(height=210, margin=dict(l=25, r=25, t=45, b=10), paper_bgcolor="rgba(0,0,0,0)")
    return fig


# ---------------------------------------------------------------------------
# TAB 1 · VISÃO GERAL
# ---------------------------------------------------------------------------
def fig_volumetria(resp):
    d = resp.sort_values("ano").copy()
    d["rotulo"] = d.ano.map(ROTULO_ANO)
    d["grupo"] = d.ano.apply(lambda a: "Núcleo obrigatório" if a >= 2023 else "Contexto histórico")
    fig = px.bar(d, x="rotulo", y="n", color="grupo", category_orders={"rotulo": ROTULOS_ORDEM},
                 color_discrete_map={"Núcleo obrigatório": AZUL, "Contexto histórico": CINZA},
                 text="n", labels={"rotulo": "", "n": "Respondentes", "grupo": ""})
    fig.update_xaxes(type="category")
    fig.update_traces(texttemplate="%{text:,.0f}".replace(",", "."), textposition="outside")
    fig.update_layout(height=380, legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       title="Volumetria por edição")
    return fig


def fig_sunburst_tech(tec, ano_foco):
    d = tec[tec.ano == ano_foco].copy()
    fig = px.sunburst(d, path=["categoria", "tecnologia"], values="usuarios", color="categoria",
                       color_discrete_map={"linguagem": AZUL, "cloud": LARANJA, "bi": AZUL_CLARO})
    fig.update_traces(textinfo="label+percent parent")
    fig.update_layout(height=380, margin=dict(l=0, r=0, t=40, b=0),
                       title=f"Mapa de tecnologias — {ROTULO_ANO[ano_foco]}")
    return fig


# ---------------------------------------------------------------------------
# TAB 2 · REMUNERAÇÃO & CARREIRA
# ---------------------------------------------------------------------------
def fig_escada_salarial(sal_sen):
    d = sal_sen.copy()
    d["rotulo"] = d.ano.map(ROTULO_ANO)
    fig = px.line(d, x="rotulo", y="salario_mediano_pm", color="nivel", markers=True,
                   category_orders={"nivel": NIVEIS, "rotulo": ROTULOS_ORDEM},
                   color_discrete_sequence=[AZUL_CLARO, AZUL_MED, AZUL, LARANJA],
                   labels={"rotulo": "", "salario_mediano_pm": "R$/mês (mediana)", "nivel": ""})
    fig.update_xaxes(type="category")
    fig.update_traces(line=dict(width=3), marker=dict(size=9))
    fig.update_layout(height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                       title="Escada salarial por senioridade")
    return fig


def fig_premio_cargo(sal_cargo, ano_foco):
    d = sal_cargo[(sal_cargo.ano == ano_foco) & (sal_cargo.n >= 30)].nlargest(9, "salario_mediano_pm")
    d = d.sort_values("salario_mediano_pm")
    fig = px.bar(d, x="salario_mediano_pm", y="cargo_grupo", orientation="h", text="salario_mediano_pm",
                 labels={"salario_mediano_pm": "R$/mês", "cargo_grupo": ""})
    fig.update_traces(marker_color=AZUL, texttemplate="R$ %{text:,.0f}".replace(",", "."),
                       textposition="outside")
    fig.update_xaxes(range=[0, d.salario_mediano_pm.max() * 1.22])
    fig.update_layout(height=400, margin=dict(r=40), paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)", title=f"Prêmio por cargo (n≥30) — {ROTULO_ANO[ano_foco]}")
    return fig


def fig_funil_criterios(criterios, ano_foco):
    d = criterios[criterios.ano == ano_foco].sort_values("pct", ascending=False)
    fig = go.Figure(go.Funnel(
        y=d.criterio, x=d.pct, textinfo="value+percent initial",
        marker={"color": [LARANJA if i < 2 else AZUL for i in range(len(d))]},
    ))
    fig.update_layout(height=430, title=f"Critérios decisivos na escolha de onde trabalhar — {ROTULO_ANO[ano_foco]}",
                       paper_bgcolor="rgba(0,0,0,0)")
    return fig


# ---------------------------------------------------------------------------
# TAB 3 · DIVERSIDADE & LIDERANÇA
# ---------------------------------------------------------------------------
def fig_dumbbell_gap(gen_sal, ano_foco):
    d = gen_sal[gen_sal.ano == ano_foco]
    piv = d.pivot(index="nivel", columns="genero", values="salario_mediano_pm").reindex(NIVEIS)
    fig = go.Figure()
    for nivel in NIVEIS:
        if nivel not in piv.index or piv.loc[nivel].isna().any():
            continue
        m, f = piv.loc[nivel, "Masculino"], piv.loc[nivel, "Feminino"]
        fig.add_trace(go.Scatter(x=[f, m], y=[nivel, nivel], mode="lines",
                                  line=dict(color="#D9D9D9", width=6), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=piv["Masculino"], y=piv.index, mode="markers", name="Masculino",
                              marker=dict(color=AZUL, size=16)))
    fig.add_trace(go.Scatter(x=piv["Feminino"], y=piv.index, mode="markers", name="Feminino",
                              marker=dict(color=LARANJA, size=16)))
    fig.update_layout(height=400, title=f"Gap salarial por nível (dumbbell) — {ROTULO_ANO[ano_foco]}",
                       xaxis_title="R$/mês (mediana)", paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.12))
    return fig


def fig_heatmap_genero_cargo(gen_role, ano_foco):
    d = gen_role[(gen_role.ano == ano_foco) & (gen_role.n >= 15)]
    piv = d.pivot_table(index="cargo_grupo", columns="genero", values="salario_mediano_pm")
    piv = piv.dropna().sort_index()
    fig = px.imshow(piv, text_auto=".0f", color_continuous_scale=[[0, "#EAF0FA"], [1, AZUL]],
                     labels=dict(color="R$/mês"), aspect="auto")
    fig.update_layout(height=400, title=f"Salário Sênior por cargo × gênero — {ROTULO_ANO[ano_foco]}",
                       paper_bgcolor="rgba(0,0,0,0)")
    return fig


# ---------------------------------------------------------------------------
# TAB 4 · TECNOLOGIA & IA
# ---------------------------------------------------------------------------
def fig_linguagens_series(tec):
    d = tec[tec.categoria == "linguagem"].copy()
    d["rotulo"] = d.ano.map(ROTULO_ANO)
    fig = px.line(d, x="rotulo", y="pct", color="tecnologia", markers=True,
                   category_orders={"rotulo": ROTULOS_ORDEM},
                   color_discrete_sequence=[AZUL_MED, AZUL, CINZA],
                   labels={"rotulo": "", "pct": "% de uso", "tecnologia": ""})
    fig.update_xaxes(type="category")
    fig.update_traces(line=dict(width=3))
    fig.update_layout(height=340, title="Linguagens — série histórica",
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", yanchor="bottom", y=-0.22))
    return fig


def fig_cloud_series(tec):
    d = tec[tec.categoria == "cloud"].copy()
    d["rotulo"] = d.ano.map(ROTULO_ANO)
    fig = px.line(d, x="rotulo", y="pct", color="tecnologia", markers=True,
                   category_orders={"rotulo": ROTULOS_ORDEM},
                   color_discrete_sequence=[AZUL, AZUL_MED, LARANJA],
                   labels={"rotulo": "", "pct": "% de uso", "tecnologia": ""})
    fig.update_xaxes(type="category")
    fig.update_traces(line=dict(width=3))
    fig.update_layout(height=340, title="Provedores de cloud — série histórica",
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", yanchor="bottom", y=-0.22))
    return fig


def fig_ia_prioridade(ia):
    d = ia.copy()
    d["rotulo"] = d.ano.map(ROTULO_ANO)
    ordem = ["1. Principal prioridade da empresa", "2. Entre as principais (2-4 anos)",
             "3. Iniciativas isoladas, sem foco", "4. Não é prioridade", "5. Não sabe opinar"]
    fig = px.bar(d, x="rotulo", y="pct", color="prioridade_ia_h",
                 category_orders={"prioridade_ia_h": ordem, "rotulo": ROTULOS_ORDEM},
                 color_discrete_sequence=[AZUL, AZUL_MED, AZUL_CLARO, "#D9D9D9", "#B0B0B0"],
                 labels={"rotulo": "", "pct": "% dos gestores", "prioridade_ia_h": ""})
    fig.update_xaxes(type="category")
    fig.update_layout(barmode="stack", height=400, title="IA generativa como prioridade — composição",
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       legend=dict(orientation="h", y=-0.25, font=dict(size=9)))
    return fig


def fig_genai_por_nivel(genai_sen, ano_foco):
    d = genai_sen[(genai_sen.ano == ano_foco) & (genai_sen.modalidade == "Empresa paga")]
    d = d.set_index("nivel").reindex(NIVEIS).reset_index()
    fig = px.bar(d, x="nivel", y="pct", text="pct", color="pct",
                 color_continuous_scale=[[0, AZUL_CLARO], [1, LARANJA]],
                 labels={"nivel": "", "pct": "% que usam GenAI paga pela empresa"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(height=400, showlegend=False, coloraxis_showscale=False,
                       title=f"GenAI paga pela empresa, por nível — {ROTULO_ANO[ano_foco]}",
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


# ---------------------------------------------------------------------------
# TAB 5 · GEOGRAFIA & MODELO DE TRABALHO
# ---------------------------------------------------------------------------
def fig_mapa_regioes(reg, ano_foco, geojson):
    d = reg[reg.ano == ano_foco].set_index("regiao")
    ufs = list(UF_REGIAO.keys())
    regioes = [UF_REGIAO[uf] for uf in ufs]
    salarios = [d.loc[r, "salario_medio_pm"] for r in regioes]
    pcts = [d.loc[r, "pct"] for r in regioes]
    ns = [d.loc[r, "n"] for r in regioes]
    fig = go.Figure(go.Choropleth(
        geojson=geojson, locations=ufs, featureidkey="properties.codigo_ibg",
        z=salarios, customdata=list(zip(regioes, pcts, ns)),
        hovertemplate="<b>%{customdata[0]}</b><br>R$ %{z:,.0f}/mês (salário médio)<br>"
                       "%{customdata[1]:.1f}% dos profissionais<br>n = %{customdata[2]}<extra></extra>",
        colorscale=[[0, AZUL_CLARO], [1, LARANJA]],
        colorbar=dict(title="R$/mês", thickness=14), marker=dict(line=dict(width=1, color="white")),
    ))
    fig.update_geos(projection_type="mercator", lataxis_range=[-35, 6], lonaxis_range=[-75, -33],
                     showland=True, landcolor="#F2F2F2", showcountries=True, countrycolor="#CFCFCF",
                     showcoastlines=False, bgcolor="rgba(0,0,0,0)")
    fig.update_layout(height=460, margin=dict(l=0, r=0, t=45, b=0),
                       title=f"Distribuição regional e salário médio — {ROTULO_ANO[ano_foco]}",
                       paper_bgcolor="rgba(0,0,0,0)")
    return fig


def fig_radar_modelo_trabalho(work, ano_foco):
    d = work[(work.ano == ano_foco) & (work.modelo != "Outro")]
    ordem_mod = ["100% presencial", "Híbrido (dias fixos)", "Híbrido flexível", "100% remoto"]
    atual = d[d.tipo == "Atual"].set_index("modelo").reindex(ordem_mod).pct
    ideal = d[d.tipo == "Ideal"].set_index("modelo").reindex(ordem_mod).pct
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=list(atual) + [atual.iloc[0]], theta=ordem_mod + [ordem_mod[0]],
                                   fill="toself", name="Praticado", line=dict(color=CINZA)))
    fig.add_trace(go.Scatterpolar(r=list(ideal) + [ideal.iloc[0]], theta=ordem_mod + [ordem_mod[0]],
                                   fill="toself", name="Desejado", line=dict(color=LARANJA)))
    fig.update_layout(height=460, title=f"Modelo de trabalho: praticado vs. desejado — {ROTULO_ANO[ano_foco]}",
                       polar=dict(radialaxis=dict(visible=True, range=[0, max(atual.max(), ideal.max()) * 1.15])),
                       legend=dict(orientation="h", y=-0.1), paper_bgcolor="rgba(0,0,0,0)")
    return fig
