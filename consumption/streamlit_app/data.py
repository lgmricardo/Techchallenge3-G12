# -*- coding: utf-8 -*-
"""Estrutura compartilhada dos 15 gráficos, usada por app.py e por export_pdf.py.
Mantida à parte para as duas ferramentas nunca divergirem sobre quais gráficos existem."""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
GOLD = BASE / "datalake" / "gold" / "csv"
CHARTS = BASE / "consumption" / "charts"

# Cada entrada: (título, arquivo PNG, figura no relatório, tabela Gold fonte, filtro_col, filtro_val)
PERGUNTAS = {
    "Contexto — Volumetria": [
        ("Respondentes por edição", "G01_respondents_by_edition.png", "Figura 2",
         "gold_respondents", None, None),
    ],
    "1. Estrutura do mercado": [
        ("Perfis profissionais — participação por cargo (2025/26)", "G02_roles_2025.png", "Figura 3",
         "gold_roles", None, None),
        ("Senioridade por edição", "G03_seniority_by_year.png", "Figura 4",
         "gold_seniority", None, None),
    ],
    "2. Perfis valorizados e remuneração": [
        ("Salário mediano por senioridade", "G04_salary_by_seniority.png", "Figura 5",
         "gold_salary_by_seniority", None, None),
        ("Salário mediano por grupo de cargo (2025/26)", "G05_salary_by_role_2025.png", "Figura 6",
         "gold_salary_by_role", None, None),
    ],
    "3. Diversidade de gênero": [
        ("Participação feminina — série histórica", "G06_female_participation.png", "Figura 7",
         "gold_gender_participation", None, None),
        ("Gap de gênero controlado por senioridade (2025/26)", "G07_gender_gap_by_seniority.png", "Figura 8",
         "gold_gender_seniority_salary", None, None),
    ],
    "4. Tecnologias com maior adoção": [
        ("Adoção de linguagens no trabalho", "G08_languages_series.png", "Figura 9",
         "gold_technologies", "categoria", "linguagem"),
        ("Adoção de provedores de cloud", "G09_cloud_providers_series.png", "Figura 10",
         "gold_technologies", "categoria", "cloud"),
        ("Ferramentas de BI (2025/26)", "G10_bi_tools_2025.png", "Figura 11",
         "gold_technologies", "categoria", "bi"),
    ],
    "5. Adoção de IA": [
        ("IA generativa como prioridade da empresa", "G11_ai_priority.png", "Figura 12",
         "gold_ai_priority", None, None),
        ("Uso individual de GenAI e Copilots", "G12_genai_usage.png", "Figura 13",
         "gold_genai_usage", None, None),
    ],
    "6. Regiões e modelos de trabalho": [
        ("Distribuição regional e salário médio (2025/26)", "G13_regions_2025.png", "Figura 14",
         "gold_regions", None, None),
        ("Modelo de trabalho: praticado versus desejado (2025/26)", "G14_work_model.png", "Figura 15",
         "gold_work_model", None, None),
    ],
    "7. Oportunidades e desafios": [
        ("Critérios decisivos na escolha de onde trabalhar (2025/26)", "G15_job_criteria.png", "Figura 16",
         "gold_job_criteria", None, None),
    ],
}
