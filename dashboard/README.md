# Dashboard

An interactive **Streamlit** dashboard summarising the organic-farming analysis with
**Plotly** charts and **Folium** choropleth maps of the EU.

## Run it

```bash
# from this directory
pip install -r requirements.txt
streamlit run app.py
```

The app reads its prepared data from `data/` (relative to this folder):

- `data/df_clean_indicators.csv` — cleaned indicators for the EDA dynamic map.
- `data/df_unscaled.csv` — country features for the clustering map.

## Features

- **EDA dynamic map** — organic-farming area / share across EU countries.
- **Clusters dynamic map** — country groupings from the K-Means / hierarchical clustering.
- Interactive Plotly visualisations with country- and year-level filtering.

> The dashboard fetches a Europe GeoJSON and map tiles at runtime, so an internet connection is
> required on first load.
