# Data

This project draws on two kinds of data: **official EU organic-farming indicators** and
**public Reddit discussions**.

## Files

### Root `data/` (notebook inputs)

| File | Size | Description | Source |
|------|-----:|-------------|--------|
| `cmef_indicators.csv` | ~222 KB | Organic-farming indicators: organic area, CAP support (M11), public expenditure, organic share of UAA. | **EU CMEF** / **Eurostat** (CAP open data). |
| `reddit_scraped_data.csv` | ~8 MB | ~11,800 Reddit posts mentioning organic farming, with subreddit, country, year, query keyword, title, body, score, upvote ratio, timestamp. | **Reddit** via PRAW. |
| `df_sentiment.csv` | ~4.5 KB | Aggregated sentiment results used by the indicators notebook. | Derived. |

### `dashboard/data/` (prepared dashboard inputs)

| File | Size | Description |
|------|-----:|-------------|
| `df_clean_indicators.csv` | ~205 KB | Cleaned indicator data for the dashboard's EDA map. |
| `df_unscaled.csv` | ~2 KB | Country-level features for the clustering map. |

## Indicator reference (CMEF / Eurostat)

| Code | Name | Unit | Source |
|------|------|------|--------|
| `OIR_06_1.2` | Physical area supported for M11 | supported hectares | CATS |
| `OIR_01a_2.11` | Total public expenditure (EU + national co-financing) | EUR | DOE |
| `OIR_01b_2.11` | Total public expenditure (EU funds) | EUR | DOE |
| `CTX_SEC_19_1c` | Agricultural area under organic farming (certified + in conversion) | ha UAA | Eurostat `org_cropar` |
| `CTX_SEC_19_2` | Share of UAA under organic farming | % total UAA | Eurostat `org_cropar`, `apro_cpsh1` |

Official EU sources:
- Organic production data portal — https://agridata.ec.europa.eu/Qlik_Downloads/Organic-Production-sources.htm
- EU Agri-food Data Portal — https://agridata.ec.europa.eu/extensions/DataPortal/home.html

## Reddit data & ethics

The Reddit dataset contains **public** posts only and is included for academic,
non-commercial reproducibility. No private user information is stored beyond what Reddit
exposes publicly. To re-scrape, register a Reddit app and provide your own `client_id` /
`client_secret` in the marked cell of `02-reddit-sentiment-topics.ipynb` — the placeholders
are intentionally blank, and credentials should **never** be committed.
