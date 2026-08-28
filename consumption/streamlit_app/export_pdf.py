# -*- coding: utf-8 -*-
"""Exporta o resultado do dataviz (app.py) como PDF — uma página por gráfico, mesma
estrutura de data.py (compartilhada com o app), para nunca divergir do que o app mostra.

Rodar:
    python consumption/streamlit_app/export_pdf.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data import PERGUNTAS, GOLD, CHARTS  # noqa: E402
import pandas as pd
from fpdf import FPDF

OUT = Path(__file__).resolve().parent / "dataviz_streamlit.pdf"

AZUL = (0x1F, 0x38, 0x64)
LARANJA = (0xC4, 0x61, 0x0A)
CINZA = (0x66, 0x66, 0x66)

pdf = FPDF(orientation="L", unit="mm", format="A4")
pdf.set_auto_page_break(False)
PAGE_W, PAGE_H = 297, 210
MARGIN = 14

# Fonte TTF com suporte Unicode (em-dash, seta) - as fontes core do fpdf2 (Helvetica etc.) são latin-1 apenas.
FONTDIR = "/System/Library/Fonts/Supplemental"
pdf.add_font("Arial", "", f"{FONTDIR}/Arial.ttf")
pdf.add_font("Arial", "B", f"{FONTDIR}/Arial Bold.ttf")
pdf.add_font("Arial", "I", f"{FONTDIR}/Arial Italic.ttf")

# ---- Capa -------------------------------------------------------------
pdf.add_page()
pdf.set_font("Arial", "B", 10)
pdf.set_text_color(*LARANJA)
pdf.set_xy(MARGIN, 30)
pdf.cell(0, 8, "TECH CHALLENGE FASE 3 - DATAVIZ INTERATIVO (STREAMLIT)")
pdf.set_font("Arial", "B", 26)
pdf.set_text_color(*AZUL)
pdf.set_xy(MARGIN, 45)
pdf.multi_cell(PAGE_W - 2 * MARGIN, 12, "O Mercado Brasileiro de Dados")
pdf.set_font("Arial", "", 13)
pdf.set_text_color(*CINZA)
pdf.set_xy(MARGIN, 75)
pdf.multi_cell(PAGE_W - 2 * MARGIN, 7,
                "State of Data Brasil (Data Hackers/Bain) - pipeline AWS Medallion\n"
                "Resultado exportado de consumption/streamlit_app/app.py")
pdf.set_font("Arial", "", 10)
pdf.set_xy(MARGIN, 95)
pdf.multi_cell(PAGE_W - 2 * MARGIN, 6,
                "22.686 respostas - 6 edicoes (2019-2025/26) - 21 tabelas Gold\n"
                "Graficos identicos ao material executivo (consumption/charts/)")

# ---- Uma pagina por grafico --------------------------------------------
for secao, itens in PERGUNTAS.items():
    for titulo, png, figura, tabela, filtro_col, filtro_val in itens:
        pdf.add_page()
        pdf.set_font("Arial", "B", 9)
        pdf.set_text_color(*LARANJA)
        pdf.set_xy(MARGIN, 10)
        pdf.cell(0, 6, secao.upper())
        pdf.set_font("Arial", "B", 17)
        pdf.set_text_color(*AZUL)
        pdf.set_xy(MARGIN, 17)
        pdf.cell(0, 9, titulo)

        img_path = CHARTS / png
        from PIL import Image
        with Image.open(img_path) as im:
            iw, ih = im.size
        ratio = iw / ih
        max_w = 195
        max_h = 155
        w = max_w
        h = w / ratio
        if h > max_h:
            h = max_h
            w = h * ratio
        img_x = MARGIN
        img_y = 32
        pdf.image(str(img_path), x=img_x, y=img_y, w=w, h=h)

        meta_x = img_x + w + 10
        pdf.set_xy(meta_x, img_y)
        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(*AZUL)
        pdf.multi_cell(PAGE_W - meta_x - MARGIN, 6, f"{figura} do relatorio tecnico")
        pdf.set_xy(meta_x, pdf.get_y() + 3)
        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(*CINZA)
        pdf.multi_cell(PAGE_W - meta_x - MARGIN, 5, f"Fonte: {tabela}.csv")
        if filtro_col:
            pdf.set_xy(meta_x, pdf.get_y() + 2)
            pdf.multi_cell(PAGE_W - meta_x - MARGIN, 5, f"Filtro: {filtro_col} == '{filtro_val}'")

        # tabela de dados (linhas de amostra) abaixo da imagem
        df = pd.read_csv(GOLD / f"{tabela}.csv")
        if filtro_col:
            df = df[df[filtro_col] == filtro_val]
        tbl_y = img_y + h + 6
        pdf.set_xy(MARGIN, tbl_y)
        pdf.set_font("Arial", "B", 8)
        pdf.set_text_color(*CINZA)
        pdf.cell(0, 5, f"Dados ({tabela}.csv, {len(df)} linhas) - amostra:")
        cols = list(df.columns)
        col_w = (PAGE_W - 2 * MARGIN) / len(cols)
        row_y = tbl_y + 6
        pdf.set_xy(MARGIN, row_y)
        pdf.set_font("Arial", "B", 7)
        pdf.set_fill_color(0x1F, 0x38, 0x64)
        pdf.set_text_color(255, 255, 255)
        for c in cols:
            pdf.cell(col_w, 5, str(c), border=0, fill=True)
        pdf.ln(5)
        pdf.set_font("Arial", "", 7)
        pdf.set_text_color(0, 0, 0)
        max_rows = min(len(df), 6)
        for i in range(max_rows):
            pdf.set_x(MARGIN)
            fill = i % 2 == 1
            pdf.set_fill_color(0xF2, 0xF2, 0xF2)
            for c in cols:
                val = df.iloc[i][c]
                txt = f"{val:.1f}" if isinstance(val, float) else str(val)
                pdf.cell(col_w, 5, txt[:22], border=0, fill=fill)
            pdf.ln(5)
        if len(df) > max_rows:
            pdf.set_xy(MARGIN, pdf.get_y() + 1)
            pdf.set_font("Arial", "I", 7)
            pdf.set_text_color(*CINZA)
            pdf.cell(0, 4, f"... e mais {len(df) - max_rows} linha(s). Tabela completa em datalake/gold/csv/{tabela}.csv")

pdf.output(str(OUT))
print("SALVO:", OUT, f"({len(pdf.pages)} paginas)")
