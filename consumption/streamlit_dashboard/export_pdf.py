# -*- coding: utf-8 -*-
"""Exporta um snapshot do board (board.py) como PDF — uma página por aba, usando os
mesmos gráficos de charts.py (compartilhado com o app interativo), para nunca divergir
do que o board mostra. Como o board tem um seletor de edição, o snapshot fixa
ano_foco = 2025 ("2025/26", a edição-núcleo mais recente e o default do app).

Rodar:
    python consumption/streamlit_dashboard/export_pdf.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import charts as c  # noqa: E402
from fpdf import FPDF  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "board_state_of_data_brasil.pdf"
IMG_DIR = HERE / "_pdf_tmp"
IMG_DIR.mkdir(exist_ok=True)

ANO_FOCO = 2025  # "2025/26" — mesma edição-núcleo mais recente usada como default no app

AZUL = (0x1F, 0x38, 0x64)
LARANJA = (0xC4, 0x61, 0x0A)
CINZA = (0x66, 0x66, 0x66)

PAGE_W, PAGE_H = 297, 210
MARGIN = 14
CONTENT_W = PAGE_W - 2 * MARGIN

pdf = FPDF(orientation="L", unit="mm", format="A4")
pdf.set_auto_page_break(False)

FONTDIR = "/System/Library/Fonts/Supplemental"
pdf.add_font("Arial", "", f"{FONTDIR}/Arial.ttf")
pdf.add_font("Arial", "B", f"{FONTDIR}/Arial Bold.ttf")
pdf.add_font("Arial", "I", f"{FONTDIR}/Arial Italic.ttf")


def save(fig, name, width=850, height=480, scale=2):
    path = IMG_DIR / f"{name}.png"
    fig.write_image(str(path), width=width, height=height, scale=scale)
    return path


def place(path, x, y, max_w, max_h, center=False):
    with Image.open(path) as im:
        iw, ih = im.size
    w, h = max_w, max_w * ih / iw
    if h > max_h:
        h = max_h
        w = max_h * iw / ih
    if center:
        x = x + (max_w - w) / 2
    pdf.image(str(path), x=x, y=y, w=w, h=h)
    return w, h


def header(titulo, fonte_txt):
    pdf.add_page()
    pdf.set_font("Arial", "B", 9)
    pdf.set_text_color(*LARANJA)
    pdf.set_xy(MARGIN, 10)
    pdf.cell(0, 6, "BOARD ANALITICO - STATE OF DATA BRASIL - TECH CHALLENGE FASE 3")
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(*AZUL)
    pdf.set_xy(MARGIN, 17)
    pdf.cell(0, 9, titulo)
    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(*CINZA)
    pdf.set_xy(MARGIN, 191)
    pdf.multi_cell(CONTENT_W, 4.2, fonte_txt)


# ---------------------------------------------------------------------------
# Capa
# ---------------------------------------------------------------------------
pdf.add_page()
pdf.set_font("Arial", "B", 10)
pdf.set_text_color(*LARANJA)
pdf.set_xy(MARGIN, 30)
pdf.cell(0, 8, "TECH CHALLENGE FASE 3 - BOARD ANALITICO INTERATIVO (STREAMLIT + PLOTLY)")
pdf.set_font("Arial", "B", 26)
pdf.set_text_color(*AZUL)
pdf.set_xy(MARGIN, 45)
pdf.multi_cell(CONTENT_W, 12, "O Mercado Brasileiro de Dados")
pdf.set_font("Arial", "", 13)
pdf.set_text_color(*CINZA)
pdf.set_xy(MARGIN, 75)
pdf.multi_cell(CONTENT_W, 7,
                "State of Data Brasil (Data Hackers/Bain) - pipeline AWS Medallion\n"
                "Snapshot exportado de consumption/streamlit_dashboard/board.py")
pdf.set_font("Arial", "", 10)
pdf.set_xy(MARGIN, 97)
pdf.multi_cell(CONTENT_W, 6,
                "22.686 respostas - 6 edicoes (2019-2025/26) - 21 tabelas Gold - fonte: datalake/gold/csv/\n"
                "Visoes instantaneas (gauges, mapa, radar, heatmap) calibradas para a edicao 2025/26\n"
                "Graficos de serie temporal mostram todas as edicoes disponiveis, nao apenas o snapshot\n\n"
                "Paginas: 1) Visao Geral  2) Remuneracao & Carreira  3) Diversidade & Lideranca  "
                "4) Tecnologia & IA  5) Geografia & Trabalho")

# ---------------------------------------------------------------------------
# Tab 1 - Visao Geral
# ---------------------------------------------------------------------------
tec = c.ler("gold_technologies")
genai = c.ler("gold_genai_usage")
mercado = c.ler("gold_market_pulse")
resp = c.ler("gold_respondents")

py = tec[(tec.categoria == "linguagem") & (tec.tecnologia == "Python")].set_index("ano").pct
aws = tec[(tec.categoria == "cloud") & (tec.tecnologia == "AWS")].set_index("ano").pct
emp = genai[genai.modalidade == "Empresa paga"].set_index("ano").pct
sat = mercado.set_index("ano").pct_satisfeitos

header("1. Visao Geral", "Fonte: gold_respondents.csv - gold_technologies.csv - "
                          "gold_genai_usage.csv - gold_market_pulse.csv")
gauges1 = [
    save(c.fig_gauge(py[ANO_FOCO], "Adocao de Python", ref=py[min(py.index)]), "g1a", 420, 300),
    save(c.fig_gauge(aws[ANO_FOCO], "AWS entre provedores cloud", ref=aws[min(aws.index)]), "g1b", 420, 300),
    save(c.fig_gauge(emp[ANO_FOCO], "GenAI paga pela empresa", ref=emp[min(emp.index)]), "g1c", 420, 300),
    save(c.fig_gauge(sat[ANO_FOCO], "Satisfacao com a empresa", ref=sat[min(sat.index)]), "g1d", 420, 300),
]
gw = (CONTENT_W - 3 * 6) / 4
for i, gpath in enumerate(gauges1):
    place(gpath, MARGIN + i * (gw + 6), 33, gw, 46)

volum = save(c.fig_volumetria(resp), "volumetria", 850, 480)
sunb = save(c.fig_sunburst_tech(tec, ANO_FOCO), "sunburst", 700, 600)
place(volum, MARGIN, 85, 155, 100)
place(sunb, MARGIN + 155 + 8, 85, CONTENT_W - 155 - 8, 100, center=True)

# ---------------------------------------------------------------------------
# Tab 2 - Remuneracao & Carreira
# ---------------------------------------------------------------------------
sal_sen = c.ler("gold_salary_by_seniority")
sal_cargo = c.ler("gold_salary_by_role")
criterios = c.ler("gold_job_criteria")

header("2. Remuneracao & Carreira", "Fonte: gold_salary_by_seniority.csv - "
                                     "gold_salary_by_role.csv - gold_job_criteria.csv")
escada = save(c.fig_escada_salarial(sal_sen), "escada", 850, 480)
premio = save(c.fig_premio_cargo(sal_cargo, ANO_FOCO), "premio", 850, 480)
place(escada, MARGIN, 33, 131, 78)
place(premio, MARGIN + 131 + 8, 33, CONTENT_W - 131 - 8, 78, center=True)

funil = save(c.fig_funil_criterios(criterios, ANO_FOCO), "funil", 1000, 560)
place(funil, MARGIN, 116, CONTENT_W, 74, center=True)

# ---------------------------------------------------------------------------
# Tab 3 - Diversidade & Lideranca
# ---------------------------------------------------------------------------
gen_sal = c.ler("gold_gender_seniority_salary")
gen_lead = c.ler("gold_gender_leadership")
gen_role = c.ler("gold_gender_role_seniority")

header("3. Diversidade & Lideranca", "Fonte: gold_gender_seniority_salary.csv - "
                                      "gold_gender_role_seniority.csv - gold_gender_leadership.csv")
dumbbell = save(c.fig_dumbbell_gap(gen_sal, ANO_FOCO), "dumbbell", 800, 480)
heatmap = save(c.fig_heatmap_genero_cargo(gen_role, ANO_FOCO), "heatmap", 800, 480)
place(dumbbell, MARGIN, 33, 128, 92)
place(heatmap, MARGIN + 128 + 8, 33, CONTENT_W - 128 - 8, 92, center=True)

d_lead = gen_lead[gen_lead.ano == ANO_FOCO].set_index("genero").pct_gestores
g3a = save(c.fig_gauge(d_lead.get("Feminino", 0), "% mulheres em posicao de gestao"), "g3a", 420, 300)
g3b = save(c.fig_gauge(d_lead.get("Masculino", 0), "% homens em posicao de gestao"), "g3b", 420, 300)
gw3 = (CONTENT_W - 8) / 2
place(g3a, MARGIN, 130, gw3, 56, center=True)
place(g3b, MARGIN + gw3 + 8, 130, gw3, 56, center=True)

# ---------------------------------------------------------------------------
# Tab 4 - Tecnologia & IA
# ---------------------------------------------------------------------------
ia = c.ler("gold_ai_priority")
genai_sen = c.ler("gold_genai_usage_by_seniority")

header("4. Tecnologia & IA", "Fonte: gold_technologies.csv - gold_ai_priority.csv - "
                              "gold_genai_usage_by_seniority.csv")
lingu = save(c.fig_linguagens_series(tec), "lingu", 850, 480)
cloud = save(c.fig_cloud_series(tec), "cloud", 850, 480)
place(lingu, MARGIN, 33, 130, 78)
place(cloud, MARGIN + 130 + 8, 33, CONTENT_W - 130 - 8, 78, center=True)

ia_p = save(c.fig_ia_prioridade(ia), "ia_p", 850, 520)
genai_n = save(c.fig_genai_por_nivel(genai_sen, ANO_FOCO), "genai_n", 850, 480)
place(ia_p, MARGIN, 118, 128, 70)
place(genai_n, MARGIN + 128 + 8, 118, CONTENT_W - 128 - 8, 70, center=True)

# ---------------------------------------------------------------------------
# Tab 5 - Geografia & Trabalho
# ---------------------------------------------------------------------------
reg = c.ler("gold_regions")
work = c.ler("gold_work_model")

header("5. Geografia & Trabalho", "Fonte: gold_regions.csv - gold_work_model.csv - malha de UFs: "
                                   "click_that_hood/Code for America. Cor por macrorregiao - os "
                                   "estados de uma mesma regiao compartilham o mesmo valor.")
mapa = save(c.fig_mapa_regioes(reg, ANO_FOCO, c.geojson_uf()), "mapa", 800, 640)
radar = save(c.fig_radar_modelo_trabalho(work, ANO_FOCO), "radar", 700, 640)
place(mapa, MARGIN, 33, 152, 152, center=True)
place(radar, MARGIN + 152 + 8, 33, CONTENT_W - 152 - 8, 152, center=True)

# ---------------------------------------------------------------------------
pdf.output(str(OUT))
print("SALVO:", OUT, f"({len(pdf.pages)} paginas)")

for f in IMG_DIR.glob("*.png"):
    f.unlink()
IMG_DIR.rmdir()
