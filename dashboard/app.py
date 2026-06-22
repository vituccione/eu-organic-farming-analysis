import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from folium import Map, GeoJson, GeoJsonTooltip
from urllib.request import urlopen
import json
from streamlit_folium import st_folium
from branca.element import Template, MacroElement

# Set page configuration
st.set_page_config(
    page_title="Modern Farming Dashboard",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded")
    
# Add custom CSS styling
st.markdown("""
<style>

/* Customize slider number */
div.stSlider > div[data-baseweb="slider"] > div > div > div > div {
    font-weight: bold;
    font-size: 20px;
}

/* Adjust padding for block container */
[data-testid="stMainBlockContainer"] {
    padding-top: 2rem;
}   

/* Adjust padding for sidebar container */
[data-testid="stSidebarHeader"] {
    padding: 0rem;
}   

/* Style the sidebar title */
[data-testid="stSidebar"] h1 {
    color: #4CAF50;
    font-weight: bold;
}
            
/* Adjust the width of the sidebar */
[data-testid="stSidebar"] {
    width: 360px !important;
}

/* Adjust spacing and alignment for vertical blocks */
[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# Generate choropleth map
def generate_choropleth(df, unit):
    fig = px.choropleth(
        df,
        color='value',
        locations='map_code',
        animation_frame='year',
        hover_name='state_name',
        hover_data={'map_code': False},
        color_continuous_scale=px.colors.sequential.Greens,
        labels={'value': unit, 'year': 'Year', 'cmef_code': 'Indicator'}
    )
    
    fig.update_layout(
        geo=dict(
            projection=go.layout.geo.Projection(type='natural earth'),
            projection_scale=5,
            center={'lat': 52, 'lon': 15},
            showframe=False,
            showcoastlines=True,
            coastlinewidth=0.3,
            showcountries=True,
            countrywidth=0.3,
            bgcolor='#0e1117'
        ),
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
    )
    
    fig.update_traces(marker_line_color='black', marker_line_width=0.5)
    return fig

# Generate growth rate chart
def generate_growth_chart(df, selected_year):
    df = df.sort_values(by=['state_name', 'year'])
    df['previous_value'] = df.groupby('state_name')['value'].shift(1)
    df['growth_rate'] = ((df['value'] - df['previous_value']) / df['previous_value']) * 100

    df['growth_rate'] = df['growth_rate'].replace([float('inf'), -float('inf')], None)
    df['growth_rate'] = df['growth_rate'].fillna(0)

    df_year = df[df['year'] == selected_year]

    if selected_year == df['year'].min():
        fig = go.Figure()
        fig.add_annotation(
            text=f"Year-on-year growth rates are unavailable for {selected_year}.<br>Select the next year to view growth rates.",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color="#FFD700"),
        )
        fig.update_layout(
            title={
                'text': f"Year-on-Year Growth Rate in {selected_year}",
                'font': {'size': 20},
                'x': 0.5,
                'xanchor': 'center',
            },
            xaxis_title="Country",
            yaxis_title="Growth Rate (%)",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            template="plotly_dark",
        )
        return fig

    sorted_states = sorted(df_year['state_name'].unique())

    fig = px.bar(
        df_year,
        x='state_name',
        y='growth_rate',
        title=f"Year-on-Year Growth Rate in {selected_year}",
        labels={'growth_rate': "Growth Rate (%)", 'state_name': 'Country'},
        category_orders={'state_name': sorted_states},
        hover_data={'state_name': False, 'growth_rate': ':.2f'},
        hover_name='state_name',
    )

    fig.update_traces(marker=dict(
        color=df_year['growth_rate'],
        colorscale=[
            [0.0, 'rgb(239, 83, 80)'],
            [0.5, 'rgb(139, 195, 74)'],
            [1.0, 'rgb(76, 175, 80)']
        ],
        colorbar=dict(
            title="%",
            thickness=10
        )
    ))
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Growth Rate (%)",
        title={
            'text': fig.layout.title.text,
            'font': {'size': 20},
            'x': 0.5,
            'xanchor': 'center',
        }
    )
    return fig

# Generate cumulative contribution chart
def generate_cumulative_chart(df, selected_year):
    df_cumulative = df[df['year'] <= selected_year].copy()

    df_cumulative = df_cumulative.groupby('state_name', as_index=False)['value'].sum()

    total_value = df_cumulative['value'].sum()
    df_cumulative['contribution'] = (df_cumulative['value'] / total_value) * 100

    min_contribution = df_cumulative['contribution'].min()
    max_contribution = df_cumulative['contribution'].max()
    df_cumulative['normalized_contribution'] = (
        (df_cumulative['contribution'] - min_contribution) /
        (max_contribution - min_contribution)
    )

    color_scale = px.colors.sequential.Greens
    num_colors = len(color_scale)
    df_cumulative['color'] = df_cumulative['normalized_contribution'].apply(
        lambda x: color_scale[int(x * (num_colors - 1))]
    )

    df_cumulative['text_label'] = df_cumulative.apply(
        lambda row: row['state_name'] if row['contribution'] > 5 else '', axis=1
    )

    fig = px.pie(
        df_cumulative,
        values='contribution',
        names='state_name',
        labels={'contribution': 'Contribution'},
        title=f"Cumulative Contribution by {selected_year}",
        hover_data={'state_name': False},
        hover_name='state_name',
    )
    fig.update_traces(
        textinfo='label+percent',
        text=df_cumulative['text_label'],
        textposition='inside',
        insidetextorientation='radial',
        pull=[0.1 if value > 5 else 0 for value in df_cumulative['contribution']],
        marker=dict(colors=df_cumulative['color'])
    )
    fig.update_layout(
        showlegend=True,
        title={
            'text': fig.layout.title.text,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20},
        },
        font=dict(size=16),
        height=550,
        width=550
    )

    return fig

# Render a detailed table
def render_table(df, selected_year, unit):
    st.markdown(f"##### Top Countries in {selected_year}")

    df_sorted = df.sort_values(by="value", ascending=False)

    st.dataframe(
        df_sorted,
        use_container_width=True,
        column_order=["state_name", "value"],
        hide_index=True,
        column_config={
            "state_name": st.column_config.TextColumn("Country"),
            "value": st.column_config.ProgressColumn(
                unit,
                format="%f",
                min_value=0,
                max_value=df_sorted["value"].max(),
            ), 
        },
        width=None,
    )
    
# Generate map with clustering results
def generate_cluster_map(df_clusters, europe_geojson):
    
    columns_labels = {
        'tot_area': 'Organic Area (ha)',
        'share_area': 'Organic Share (%)',
        'tot_cap': 'CAP Support (€)',
        'tot_sentiment': 'Sentiment Score',
        'annual_growth': 'Annual Growth (%)',
        'cluster': 'Cluster'
    }

    df_clusters['cluster'] = df_clusters['cluster'].astype(str)
    country_data = df_clusters.rename(columns=columns_labels).set_index('state_name').to_dict(orient='index')

    for feature in europe_geojson['features']:
        country = feature['properties']['NAME']
        details = country_data.get(country, {})
        tooltip_text = f"<b>{country}</b><br>" + "<br>".join(
            [f"{k}: {v:,.2f}" if isinstance(v, (int, float)) else f"{k}: {v}" for k, v in details.items()]
        ) if details else "No Data Available"
        feature['properties']['tooltip'] = tooltip_text

    def style_function(feature):
        cluster_colors = {'1': 'red', '2': 'blue', '3': 'green'}
        cluster = country_data.get(feature['properties']['NAME'], {}).get('Cluster', 'N/A')
        color = cluster_colors.get(cluster, 'gray')
        return {
            'fillColor': color,
            'color': 'black',
            'weight': 1.2,
            'fillOpacity': 0.4,
        }

    def highlight_function(feature):
        cluster_colors = {'1': 'red', '2': 'blue', '3': 'green'}
        cluster = country_data.get(feature['properties']['NAME'], {}).get('Cluster', 'N/A')
        color = cluster_colors.get(cluster, 'gray')
        return {
            'fillColor': color,
            'color': 'white',
            'weight': 2,
            'fillOpacity': 0.6
        }
    
    black_sea_tiles = "https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.png"
    attr="alidade_satellite"

    m = create_cluster_map(black_sea_tiles, attr)

    GeoJson(
        europe_geojson,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=GeoJsonTooltip(fields=["tooltip"], aliases=[""], localize=True)
    ).add_to(m)

    legend_html = """
    {% macro html(this, kwargs) %}
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 150px;
        height: 120px;
        background-color: rgba(255, 255, 255, 0.8);
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
        box-shadow: 3px 3px 5px rgba(0,0,0,0.4);
        color: black;
    ">
        <b>Legend</b><br>
        <i style="background:rgba(255, 0, 0, 0.5); width:15px; height:15px; display:inline-block;"></i> Cluster 1<br>
        <i style="background:rgba(0, 0, 255, 0.5); width:15px; height:15px; display:inline-block;"></i> Cluster 2<br>
        <i style="background:rgba(0, 128, 0, 0.5); width:15px; height:15px; display:inline-block;"></i> Cluster 3<br>
        <i style="background:rgba(128, 128, 128, 0.5); width:15px; height:15px; display:inline-block;"></i> No Data <br>
    </div>
    {% endmacro %}
    """

    macro = MacroElement()
    macro._template = Template(legend_html)
    m.get_root().add_child(macro)

    return m

# Add about section in the sidebar
def add_info_section_sidebar(selected_tab):
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Info ℹ️")
    if selected_tab == "CMEF Indicators":
        st.sidebar.write('''
            - Data Source: [Agri-food Data Portal](https://agridata.ec.europa.eu/extensions/DataPortal/home.html)
            - :green[**CMEF Indicators**]: Key information on CAP implementation, its results and its impacts
            - :green[**Dynamic Map**]: Select an indicator and slide year to view trends across countries
            - :orange[**Note**]: Map reflects source data availability; some years may be missing for some countries
        ''')
       
        with st.sidebar.expander("About missing data", expanded=False):
            st.markdown('''
            - France has experienced delays in making payments for the organic measure in 2015 and 2016
            - The Netherlands does not support organic farming through the EAFRD but relies on national funds
            - For Malta, the support target for the entire programming period 2014–2020 is low (28 hectares), and the measure has not yet been launched
            - In Italy, support for organic farming was low in 2015 because most of the Regional Development Programs were approved in the second half of 2015, leaving insufficient time to launch the organic farming measure
            - In Sweden, the share of organic area granted support is low because EU funding is provided only for conversion, not for the maintenance of organic farming
            - Similarly, in Romania, Bulgaria, and Spain, the share of organic area granted support is around 50%, as some regions only finance conversion
            
            Source: [Organic production - Infopage](https://agridata.ec.europa.eu/Qlik_Downloads/Organic-Production-sources.htm)
            ''')

    elif selected_tab == "Clustering Results":
        st.sidebar.write('''
            - Data Source: Internal Analysis (Processed Clustering Data)
            - :green[**Clustering Results**]: Visualizes country groupings based on shared characteristics
            - :green[**Interactive Map**]: Hover over countries for more info
            - :orange[**Note**]: Data aggregated over multiple years
        ''')

        with st.sidebar.expander("Clusters meaning",expanded=False):
            st.markdown('''
            | Cluster | Summary |
            |---------|---------|
            | :red[**Cluster 1**] | High growth rates, small organic areas, and low CAP funding. Represents emerging or fast-growing regions with minimal resources |
            | :blue[**Cluster 2**] | Largest organic areas, highest CAP funding, and strong public sentiment. Likely established agricultural regions with strong financial and public support |
            | :green[**Cluster 3**] | Low growth rates, moderate organic areas, and mid-level CAP funding. Represents stable but slower-growing regions with limited public sentiment |
            ''')

@st.cache_data
def load_data(filepath):
    return pd.read_csv(filepath)
@st.cache_data
def prepare_cmef_map_data(cmef_data, selected_code):
    df_map = cmef_data[cmef_data['cmef_code'] == selected_code]
    return df_map

@st.cache_resource
def load_geojson(geojson_url):
    with urlopen(geojson_url) as response:
        return json.load(response)
@st.cache_resource
def create_cluster_map(tiles, attr):
    return Map(location=[50, 15], zoom_start=5, tiles=tiles, attr=attr)

def main():
    # Configuration variables
    DATA_PATH = {
        "CMEF": "data/df_clean_indicators.csv",
        "CLUSTERING": "data/df_unscaled.csv"
    }
    GEOJSON_URL = "https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson"
    DASHBOARD_TITLE = "Modern Farming Dashboard 🌾"

    INDICATOR_TITLES = {
        'CMEF': 'Common Monitoring and Evaluation Framework',
        'CTX_SEC_19_1c': 'Total agricultural area under organic farming in hectares',
        'CTX_SEC_19_2': 'Share of agricultural area under organic farming',
        'OIR_01a_2.11': 'Total public expenditure (EU funds + national co-financing)',
        'OIR_01b_2.11': 'EU-funded public expenditure only',
        'OIR_06_1.2': 'Physical area supported under CAP measures for organic farming'
    }

    # Load datasets
    cmef_data = load_data(DATA_PATH["CMEF"])
    clustering_data = load_data(DATA_PATH["CLUSTERING"])

    # Prepare CMEF indicators
    cmef_data.sort_values(by=['year'], ascending=True, inplace=True)
    code_list = sorted(cmef_data['cmef_code'].unique())


    # Set up dashboard layout
    st.sidebar.title(DASHBOARD_TITLE)
    tabs = st.sidebar.radio("Select Tab", ["CMEF Indicators", "Clustering Results"], label_visibility='collapsed')
    add_info_section_sidebar(tabs)

    if tabs == "CMEF Indicators":
        display_cmef_tab(cmef_data, code_list, INDICATOR_TITLES)

    elif tabs == "Clustering Results":
        display_clustering_tab(clustering_data, GEOJSON_URL)

def display_cmef_tab(cmef_data, code_list, indicator_titles):
    st.markdown("""
    <div style="text-align: center; font-size: 24px; font-weight: bold;">
        CMEF (Common Monitoring and Evaluation Framework) Indicators Dynamic Map
    </div>
    """, unsafe_allow_html=True)

    select_col1, select_col2 = st.columns((1, 7), gap="medium")

    with select_col1:
        st.write("Select an indicator:")

    with select_col2:
        selected_code = st.selectbox(
            "Select an Indicator",
            label_visibility='collapsed',
            options=code_list,
            format_func=lambda code: f"{code} - {indicator_titles.get(code, 'Unknown Indicator')}",
            index=0
        )

    df_map = prepare_cmef_map_data(cmef_data, selected_code)

    unit = df_map['unit'].unique()[0] if not df_map['unit'].isnull().all() else "Unit"

    available_years = sorted(df_map['year'].unique())
    min_year = int(min(available_years))
    max_year = int(max(available_years))

    selected_year = st.slider(
        "Select a Year",
        label_visibility='collapsed',
        min_value=min_year,
        max_value=max_year,
        value=min_year
    )

    df_year_filtered = df_map[df_map['year'] == selected_year]

    map_col1, map_col2 = st.columns((3, 1), gap="medium")

    with map_col1:
        choropleth_fig = generate_choropleth(df_year_filtered, unit)
        st.plotly_chart(choropleth_fig, use_container_width=True)

    with map_col2:
        render_table(df_year_filtered, selected_year, unit)

    plot_col1, plot_col2 = st.columns(2)

    with plot_col1:
        bar_fig = generate_growth_chart(df_map, selected_year)
        st.plotly_chart(bar_fig, use_container_width=True)

    with plot_col2:
        line_fig = generate_cumulative_chart(df_map, selected_year)
        st.plotly_chart(line_fig, use_container_width=True)

def display_clustering_tab(clustering_data, geojson_url):
    st.markdown("""
    <div style="text-align: center; font-size: 24px; font-weight: bold;">
        Clustering Results Interactive Map
    </div>
    """, unsafe_allow_html=True)

    europe_geojson = load_geojson(geojson_url)
    cluster_map = generate_cluster_map(clustering_data, europe_geojson)
    # Add custom CSS for map frame auto resize
    st.markdown("""
        <style>
        iframe {
            width: 100%;
            min-height: 400px; /* Minimum height for smaller screens */
            height: calc(100vh - 200px); /* Full viewport height minus 50px padding */
            border: none;
        }
        </style>
        """, unsafe_allow_html=True)

    st.components.v1.html(cluster_map.get_root().render(), height=0, scrolling=False)


if __name__ == "__main__":
    main()
