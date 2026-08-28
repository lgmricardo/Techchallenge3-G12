# -*- coding: utf-8 -*-
"""Board analítico interativo — State of Data Brasil (Tech Challenge Fase 3).

Peça separada de consumption/streamlit_app/ (que replica os 15 PNGs estáticos): este board
constrói visualizações NOVAS e interativas — gauges, mapa coroplético do Brasil, sunburst,
funil, heatmap, radar e dumbbell — direto da camada Gold (datalake/gold/csv/), sem
reprocessar nada e sem inventar nenhum número. A lógica de dados/gráficos vive em charts.py,
compartilhada com export_pdf.py para as duas ferramentas nunca divergirem.

Rodar:
    streamlit run consumption/streamlit_dashboard/board.py
"""
import streamlit as st

import charts as c

st.set_page_config(page_title="State of Data Brasil — Board", page_icon="📊", layout="wide",
                    initial_sidebar_state="expanded")

# ---------------------------------------------------------------------------
# CSS — cards de KPI, tipografia, remoção de paddings default do Streamlit
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
  .block-container {{ padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1400px; }}
  h1, h2, h3 {{ color: {c.AZUL}; }}
  .stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
  .stTabs [data-baseweb="tab"] {{
      background-color: {c.BG_CARD}; border-radius: 8px 8px 0 0; padding: 10px 18px;
      font-weight: 600; color: {c.CINZA_TXT};
  }}
  .stTabs [aria-selected="true"] {{ background-color: {c.AZUL} !important; color: white !important; }}
  .kpi-card {{
      background: linear-gradient(135deg, {c.AZUL} 0%, {c.AZUL_MED} 100%); border-radius: 12px;
      padding: 16px 20px; color: white; text-align: left; box-shadow: 0 2px 8px rgba(31,56,100,.25);
  }}
  .kpi-card .kpi-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: .06em; opacity: .85; }}
  .kpi-card .kpi-value {{ font-size: 30px; font-weight: 800; line-height: 1.25; }}
  .kpi-card .kpi-delta {{ font-size: 12px; color: #FFD9B0; margin-top: 2px; }}
  .section-note {{ color: {c.CINZA_TXT}; font-size: 12.5px; font-style: italic; margin-top: -6px; }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def ler(nome):
    return c.ler(nome)


@st.cache_data
def geojson_uf():
    return c.geojson_uf()


st.sidebar.title("📊 State of Data Brasil")
st.sidebar.caption("Board analítico · Tech Challenge Fase 3")
st.sidebar.markdown("---")
ano_foco = st.sidebar.selectbox("Edição em foco (visões instantâneas)", c.ANOS_NUCLEO,
                                 index=2, format_func=lambda a: c.ROTULO_ANO[a])
st.sidebar.caption("Gráficos de série temporal sempre mostram todas as edições disponíveis; "
                    "esta seleção afeta apenas as visões de um único ano (gauges, mapa, radar, heatmap...).")
st.sidebar.markdown("---")
st.sidebar.caption("22.686 respostas · 6 edições (2019–2025/26) · 21 tabelas Gold · "
                    "fonte: `datalake/gold/csv/`. Nenhum dado é reprocessado aqui.")

st.title("O Mercado Brasileiro de Dados — Board Interativo")
st.caption("State of Data Brasil (Data Hackers/Bain) · pipeline AWS Medallion · "
           f"visões instantâneas calibradas para **{c.ROTULO_ANO[ano_foco]}**")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Visão Geral", "💰 Remuneração & Carreira", "👥 Diversidade & Liderança",
    "🤖 Tecnologia & IA", "🌎 Geografia & Trabalho",
])

# ===========================================================================
# TAB 1 · VISÃO GERAL
# ===========================================================================
with tab1:
    tec = ler("gold_technologies")
    genai = ler("gold_genai_usage")
    mercado = ler("gold_market_pulse")

    py = tec[(tec.categoria == "linguagem") & (tec.tecnologia == "Python")].set_index("ano").pct
    aws = tec[(tec.categoria == "cloud") & (tec.tecnologia == "AWS")].set_index("ano").pct
    emp = genai[genai.modalidade == "Empresa paga"].set_index("ano").pct
    sat = mercado.set_index("ano").pct_satisfeitos

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.plotly_chart(c.fig_gauge(py[ano_foco], "Adoção de Python", ref=py[min(py.index)]),
                         use_container_width=True, config=c.PLOT_CFG)
    with c2:
        st.plotly_chart(c.fig_gauge(aws[ano_foco], "AWS entre provedores cloud", ref=aws[min(aws.index)]),
                         use_container_width=True, config=c.PLOT_CFG)
    with c3:
        st.plotly_chart(c.fig_gauge(emp[ano_foco], "GenAI paga pela empresa", ref=emp[min(emp.index)]),
                         use_container_width=True, config=c.PLOT_CFG)
    with c4:
        st.plotly_chart(c.fig_gauge(sat[ano_foco], "Satisfação com a empresa", ref=sat[min(sat.index)]),
                         use_container_width=True, config=c.PLOT_CFG)

    st.markdown("---")
    colA, colB = st.columns([1.3, 1])
    with colA:
        st.plotly_chart(c.fig_volumetria(ler("gold_respondents")),
                         use_container_width=True, config=c.PLOT_CFG)
    with colB:
        st.plotly_chart(c.fig_sunburst_tech(tec, ano_foco), use_container_width=True, config=c.PLOT_CFG)
    st.caption("Fonte: gold_respondents.csv · gold_technologies.csv")

# ===========================================================================
# TAB 2 · REMUNERAÇÃO & CARREIRA
# ===========================================================================
with tab2:
    sal_sen = ler("gold_salary_by_seniority")
    sal_cargo = ler("gold_salary_by_role")
    criterios = ler("gold_job_criteria")

    colA, colB = st.columns([1.1, 1])
    with colA:
        st.plotly_chart(c.fig_escada_salarial(sal_sen), use_container_width=True, config=c.PLOT_CFG)
    with colB:
        st.plotly_chart(c.fig_premio_cargo(sal_cargo, ano_foco), use_container_width=True, config=c.PLOT_CFG)

    st.plotly_chart(c.fig_funil_criterios(criterios, ano_foco), use_container_width=True, config=c.PLOT_CFG)
    st.caption("Fonte: gold_salary_by_seniority.csv · gold_salary_by_role.csv · gold_job_criteria.csv")

# ===========================================================================
# TAB 3 · DIVERSIDADE & LIDERANÇA
# ===========================================================================
with tab3:
    gen_sal = ler("gold_gender_seniority_salary")
    gen_lead = ler("gold_gender_leadership")
    gen_role = ler("gold_gender_role_seniority")

    colA, colB = st.columns([1, 1.1])
    with colA:
        st.plotly_chart(c.fig_dumbbell_gap(gen_sal, ano_foco), use_container_width=True, config=c.PLOT_CFG)
    with colB:
        st.plotly_chart(c.fig_heatmap_genero_cargo(gen_role, ano_foco),
                         use_container_width=True, config=c.PLOT_CFG)

    c1, c2 = st.columns(2)
    d = gen_lead[gen_lead.ano == ano_foco].set_index("genero").pct_gestores
    with c1:
        st.plotly_chart(c.fig_gauge(d.get("Feminino", 0), "% mulheres em posição de gestão"),
                         use_container_width=True, config=c.PLOT_CFG)
    with c2:
        st.plotly_chart(c.fig_gauge(d.get("Masculino", 0), "% homens em posição de gestão"),
                         use_container_width=True, config=c.PLOT_CFG)
    st.caption("Fonte: gold_gender_seniority_salary.csv · gold_gender_role_seniority.csv · gold_gender_leadership.csv")

# ===========================================================================
# TAB 4 · TECNOLOGIA & IA
# ===========================================================================
with tab4:
    tec = ler("gold_technologies")
    ia = ler("gold_ai_priority")
    genai_sen = ler("gold_genai_usage_by_seniority")

    colA, colB = st.columns(2)
    with colA:
        st.plotly_chart(c.fig_linguagens_series(tec), use_container_width=True, config=c.PLOT_CFG)
    with colB:
        st.plotly_chart(c.fig_cloud_series(tec), use_container_width=True, config=c.PLOT_CFG)

    colC, colD = st.columns([1, 1.1])
    with colC:
        st.plotly_chart(c.fig_ia_prioridade(ia), use_container_width=True, config=c.PLOT_CFG)
    with colD:
        st.plotly_chart(c.fig_genai_por_nivel(genai_sen, ano_foco), use_container_width=True, config=c.PLOT_CFG)
    st.caption("Fonte: gold_technologies.csv · gold_ai_priority.csv · gold_genai_usage_by_seniority.csv")

# ===========================================================================
# TAB 5 · GEOGRAFIA & MODELO DE TRABALHO
# ===========================================================================
with tab5:
    reg = ler("gold_regions")
    work = ler("gold_work_model")

    colA, colB = st.columns([1.2, 1])
    with colA:
        st.plotly_chart(c.fig_mapa_regioes(reg, ano_foco, geojson_uf()),
                         use_container_width=True, config=c.PLOT_CFG)
    with colB:
        st.plotly_chart(c.fig_radar_modelo_trabalho(work, ano_foco),
                         use_container_width=True, config=c.PLOT_CFG)
    st.caption("Fonte: gold_regions.csv · gold_work_model.csv · malha de UFs: click_that_hood/Code for America "
               "(fronteiras estaduais do Brasil). Cor por macrorregião — os estados de uma mesma região "
               "compartilham o mesmo valor.")
