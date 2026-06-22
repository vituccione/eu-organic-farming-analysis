# Organic Farming in the EU — Sentiment, Indicators, Statistics & Clustering

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Made with Jupyter](https://img.shields.io/badge/Jupyter-notebooks-orange.svg)](.)
[![Dashboard: Streamlit](https://img.shields.io/badge/dashboard-Streamlit-red.svg)](dashboard/)

> MSc Data Analytics project (Semester 1) — a multi-method study of **organic farming across
> the European Union**, combining **public-opinion sentiment analysis** of Reddit discussions
> with **official CAP/Eurostat indicators**, **statistical hypothesis testing**, **unsupervised
> clustering**, and an interactive **Streamlit dashboard**.

---

## Overview

The project answers two complementary questions:

1. **What does the public think?** Scraped Reddit discussions are analysed with sentiment models
   and topic modeling to characterise attitudes toward organic farming across EU countries and
   over time.
2. **What do the numbers say?** Official **CMEF** (Common Monitoring and Evaluation Framework)
   and **Eurostat** indicators on organic area, CAP support, and public expenditure are explored,
   tested statistically, and clustered to reveal country groupings.

Findings from both strands are brought together in an interactive dashboard with dynamic maps.

## Two analysis notebooks

| Notebook | Focus | Methods |
|----------|-------|---------|
| [`01-indicators-stats-clustering.ipynb`](01-indicators-stats-clustering.ipynb) | Official organic-farming indicators | EDA · confidence intervals · **hypothesis testing** (paired t-test, Wilcoxon signed-rank, repeated-measures ANOVA, Friedman, OLS) · **clustering** (hierarchical, PCA, K-Means) |
| [`02-reddit-sentiment-topics.ipynb`](02-reddit-sentiment-topics.ipynb) | Public opinion from Reddit | data scraping (PRAW) · **sentiment analysis** (VADER, Naive Bayes, Logistic Regression) · **topic modeling** |

> View the notebooks on
> [nbviewer](https://nbviewer.org/github/vituccione/eu-organic-farming-analysis/tree/main/)
> if GitHub does not render them inline.

## Key findings

- **Positive sentiment dominates** organic-farming discussions and has grown markedly since
  2015, with sharp increases from 2019–2022 — likely driven by policy initiatives and rising
  public awareness.
- **Austria and Denmark** lead in engagement and positive sentiment, while **Ireland and the
  Netherlands** show more balanced sentiment distributions, reflecting regional variation.
- Statistical testing and clustering on CAP/Eurostat indicators reveal distinct country
  groupings in organic area and support levels across the EU.

---

## Interactive dashboard

A **Streamlit** dashboard ([`dashboard/`](dashboard/)) presents the results with **Plotly**
charts and **Folium** choropleth maps (organic-area EDA map and clustering map).

```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

The dashboard reads its prepared data from `dashboard/data/`.

## Getting started (notebooks)

```bash
python -m venv .venv && source .venv/bin/activate
pip install pandas numpy scipy scikit-learn statsmodels matplotlib seaborn \
            nltk vaderSentiment praw plotly folium jupyterlab
jupyter lab
```

Run the notebooks from the repository root (they read CSVs from `data/`). To re-scrape Reddit,
supply your own API credentials in the marked cell of notebook&nbsp;02 — the placeholders are
intentionally left blank.

## Repository structure

```
.
├── 01-indicators-stats-clustering.ipynb   # indicators · stats · clustering
├── 02-reddit-sentiment-topics.ipynb       # scraping · sentiment · topic modeling
├── data/                                   # source datasets (see data/README.md)
├── dashboard/                              # Streamlit app + its prepared data
│   ├── app.py
│   ├── requirements.txt
│   └── data/
├── report/                                 # written report (PDF)
├── LICENSE                                 # MIT (code)
└── README.md
```

## Data

Combines **CMEF/Eurostat** organic-farming indicators (EU CAP open data) with **Reddit**
discussion data collected via PRAW. Full details and a data dictionary are in
[`data/README.md`](data/README.md).

## Report

A written academic report accompanies the analysis — see [`report/`](report/).

## Tech stack

`Python` · `pandas` · `NumPy` · `SciPy` · `scikit-learn` · `statsmodels` · `NLTK` / `VADER` ·
`PRAW` · `Matplotlib` · `seaborn` · `Plotly` · `Folium` · `Streamlit` · `Jupyter`

## Author

**Marco Vitucci** — MSc in Data Analytics.

## License

Code, notebooks, and dashboard are released under the [MIT License](LICENSE). The written report
and its figures are © 2025 Marco Vitucci, all rights reserved. Datasets remain subject to the
terms of their original providers (see [`data/README.md`](data/README.md)). Reddit content
belongs to its respective authors and is included for academic, non-commercial reproducibility.
