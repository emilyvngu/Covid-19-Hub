from statistics import correlation

import pandas as pd
import numpy as np
import panel as pn
import plotly.express as px
import holoviews as hv
import geoviews as gv
import geoviews.tile_sources as gvts
from geoviews import opts
from holoviews import opts
import geopandas as gpd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests
import json
import param
import folium
from folium import Map, Marker
from folium.plugins import MarkerCluster


# Initialize panel and extensions
hv.extension('bokeh')
pn.extension('plotly')
gv.extension('bokeh')

# global data
global_data = {'total_cases':500, 'total_deaths':100, 'total_recovered':200, 'total_active':200}

# country-specific data
countries = ["USA", "India", "Brazil", "Russia", "France", "Japan"]
country_total_case_data = {'US':{'total_cases':900, 'total_deaths':100, 'total_recovered':200, 'total_active':200},
            'India':{'total_cases':800, 'total_deaths':100, 'total_recovered':200, 'total_active':200},
            'Italy':{'total_cases':700, 'total_deaths':100, 'total_recovered':200, 'total_active':200}}
df = pd.DataFrame(country_total_case_data)

world_map_data = [
    {'country': 'USA', 'lon': -95.7129, 'lat': 37.0902, 'case_death_ratio': 0.05},
    {'country': 'India', 'lon': 78.9629, 'lat': 20.5937, 'case_death_ratio': 0.03},
    {'country': 'Brazil', 'lon': -51.9253, 'lat': -14.2350, 'case_death_ratio': 0.06},
    {'country': 'Russia', 'lon': 105.3188, 'lat': 61.5240, 'case_death_ratio': 0.02},
    {'country': 'France', 'lon': 2.2137, 'lat': 46.6034, 'case_death_ratio': 0.04},
    {'country': 'Australia', 'lon': 133.7751, 'lat': -25.2744, 'case_death_ratio': 0.01}
]

country_data = pd.DataFrame({
    "USA": [900, 100, 200, 200],
    "India": [800, 100, 200, 200],
    "Brazil": [700, 80, 190, 200],
    "Russia": [600, 90, 210, 190],
}, index=["Total Cases", "Total Deaths", "Total Recovered", "Total Active"]).T


# Widgets

country_selector = pn.widgets.Select(name='Select Country', options=df.columns.tolist(), width=280)

# Callback Functions

def other_global_stats():
    stats_md = f"""
    ### Global Statistics
    - **Total Cases:** {global_data['total_cases']:,}
    - **Total Deaths:** {global_data['total_deaths']:,}
    - **Total Recovered:** {global_data['total_recovered']:,}
    - **Total Active:** {global_data['total_active']:,}
    """
    return pn.pane.Markdown(stats_md, width=300, style={"padding": "10px", "font-size": "14px"})

@pn.depends(country=country_selector.param.value)
def country_stats(country):
    if not country:
        return pn.pane.Markdown("### Select a country to view its statistics.", width=300)

    country_data = df[country]
    stats_md = f"""
    ### {country} Statistics
    - **Cases:** {country_data['total_cases']:,}
    - **Deaths:** {country_data['total_deaths']:,}
    - **Recovered:** {country_data['total_recovered']:,}
    - **Active:** {country_data['total_active']:,}
    """
    return pn.pane.Markdown(stats_md, width=300, style={"padding": "10px", "font-size": "14px"})

def create_global_pie_chart():
    global_df = pd.DataFrame({
        'Category': ['Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active'],
        'Count': list(global_data.values())
    })
    fig = px.pie(
        global_df,
        names='Category',
        values='Count',
        title='Global COVID-19 Statistics'
    )
    # Update layout to make the chart smaller
    fig.update_layout(
        width=310,  # Adjust width
        height=310,  # Adjust height
        #margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=12  # Optional: reduce font size
    )
    return pn.pane.Plotly(fig)

@pn.depends(country=country_selector.param.value)
def create_country_pie_chart(country):
    if country not in country_total_case_data:
        return pn.pane.Markdown("### Select a valid country")
    country_data = country_total_case_data[country]
    country_df = pd.DataFrame({
        'Category': ['Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active'],
        'Count': list(country_data.values())
    })
    fig = px.pie(
        country_df,
        names='Category',
        values='Count',
        title=f"{country} COVID-19 Statistics"
    )
    # Update layout to make the chart smaller
    fig.update_layout(
        width=310,  # Adjust width
        height=310,  # Adjust height
        #margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=12  # Optional: reduce font size
    )
    return pn.pane.Plotly(fig)

def create_line_chart():
    time = pd.date_range(start='2020-01-01', periods=50, freq='M')
    cases = np.random.randint(100000, 1000000, 50)
    deaths = np.random.randint(1000, 10000, 50)
    recovered = np.random.randint(50000, 100000, 50)

    df_trends = pd.DataFrame({'Date': time, 'Cases': cases, 'Deaths': deaths, 'Recovered': recovered})
    fig = px.line(df_trends, x='Date', y=['Cases', 'Deaths', 'Recovered'],
                  labels={'value': 'Count', 'variable': 'Metric'},
                  title='COVID-19 Trends Over Time',
                  height=350)
    return pn.pane.Plotly(fig)


def world_map(data_json):
    data = pd.DataFrame(data_json)
    points = gv.Points(data, ['lon', 'lat'], ['case_death_ratio', 'country'])
    map_plot = points.opts(
        opts.Points(
            size=15,
            tools=['hover'],
            color='case_death_ratio',
            cmap='YlOrBr',
            width=800,
            height=500
        )
    )
    # Use CartoDark basemap
    basemap = gvts.CartoDark
    return basemap * map_plot

def correlation_heatmap(data):
    correlation_matrix = data.corr()

    # Create the Plotly heatmap
    fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        color_continuous_scale="Viridis",
        title="Interactive Correlation Heatmap: COVID-19 Statistics",
        labels={"color": "Correlation"}
    )
    fig.update_layout(
        width=500, height=310,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return pn.pane.Plotly(fig, config={"displayModeBar": False})

def generate_static_map():
    # Use a public GeoJSON source for world countries
    geojson_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
    response = requests.get(geojson_url)
    geojson_data = response.json()

    # Convert GeoJSON to GeoDataFrame
    world = gpd.GeoDataFrame.from_features(geojson_data["features"])

    # Custom points
    world_map_data = [
        {'country': 'USA', 'lon': -95.7129, 'lat': 37.0902},
        {'country': 'India', 'lon': 78.9629, 'lat': 20.5937},
        {'country': 'Brazil', 'lon': -51.9253, 'lat': -14.2350},
    ]
    gdf = gpd.GeoDataFrame(world_map_data, geometry=gpd.points_from_xy(
        [item['lon'] for item in world_map_data],
        [item['lat'] for item in world_map_data]
    ))

    # Plot the map
    fig, ax = plt.subplots(figsize=(10, 6))
    world.plot(ax=ax, color='lightgrey', edgecolor='black')
    gdf.plot(ax=ax, color='red', markersize=50)
    plt.title("Static World Map with Points")
    plt.tight_layout()

    # Save the figure to a buffer
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Encode the image in base64
    base64_img = base64.b64encode(buf.read()).decode('utf-8')
    img_html = f"<img src='data:image/png;base64,{base64_img}'/>"
    return pn.pane.HTML(img_html, width=800, height=500)

def generate_interactive_map():
    # Define the map center and zoom level
    map_center = [0, 0]  # Center on the equator
    world_map = Map(location=map_center, zoom_start=2, tiles='CartoDB positron')

    # Custom points
    world_map_data = [
        {'country': 'USA', 'lon': -95.7129, 'lat': 37.0902},
        {'country': 'India', 'lon': 78.9629, 'lat': 20.5937},
        {'country': 'Brazil', 'lon': -51.9253, 'lat': -14.2350},
    ]

    # Add markers with a marker cluster for better scalability
    marker_cluster = MarkerCluster().add_to(world_map)
    for data in world_map_data:
        Marker(location=[data['lat'], data['lon']],
               popup=f"{data['country']}").add_to(marker_cluster)

    # Convert the map to HTML
    return pn.pane.HTML(world_map._repr_html_(), width=800, height=500)

# Sidebar Cards
search_card = pn.Card(
    pn.Column(country_selector),
    title="Country Selector",
    width=320,
    collapsed=False
)

static_map_card = pn.Card(
    generate_static_map(),
    title="Static World Map",
    width=900
)

heatmap_card = pn.Card(
    correlation_heatmap(country_data),
    title="Correlation Heatmap",
    width=650
)

# Layout
layout = pn.template.FastListTemplate(
    title="COVID Insight Hub",
    theme_toggle=True,  # Enable toggle for switching themes
    sidebar=[
        other_global_stats(),  # Global stats card
        pn.Card(country_selector, title="Country Selector", width=300),
        country_stats  # Country stats card
        #chart_settings_card
    ],
    main=[
        pn.Tabs(
            ("Global vs. Country Comparison", pn.Column(
                pn.Row(
                    create_global_pie_chart,  # Global pie chart
                    correlation_heatmap(country_data)
                ),
                pn.Row(
                    create_country_pie_chart,  # Country-specific pie chart
                    create_line_chart(),
                )
            )),
            ("Map", pn.Column(
                pn.Row(
                ),
                pn.Row(
                    #world_map(world_map_data),  # Pass JSON data to the world_map function
                    static_map_card,
                    generate_interactive_map()
                )
            ))
        )
    ],
    header_background='#343a40',
).servable()

layout.show()
