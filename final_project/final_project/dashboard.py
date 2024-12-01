from statistics import correlation
import pandas as pd
import numpy as np
import panel as pn
import plotly.express as px
import holoviews as hv
import geoviews as gv
import geoviews.tile_sources as gvts
from holoviews import opts

# Initialize panel and extensions
hv.extension('bokeh')
pn.extension('plotly')
gv.extension('bokeh')

# Data:

# global data
global_json = {'total_cases':500, 'total_deaths':100, 'total_recovered':200, 'total_active':200}
# global_json = get_total_cases()

#____________________________________________________________________________________
# country-specific data
# country_totals_json = get_total_cases_by_country()
# (not needed) countries = ["USA", "India", "Brazil", "Russia", "France", "Japan"]
country_totals_json = {'US':{'total_cases':900, 'total_deaths':100, 'total_recovered':200, 'total_active':200},
            'India':{'total_cases':800, 'total_deaths':100, 'total_recovered':200, 'total_active':200},
            'Italy':{'total_cases':700, 'total_deaths':100, 'total_recovered':200, 'total_active':200}}
country_totals_df = pd.DataFrame(country_totals_json)

#____________________________________________________________________________________
# Data with each country's location and case-death ratio
# world_map_json = get_case_fatality_ratio()
world_map_json = [
    {'country': 'USA', 'lon': -95.7129, 'lat': 37.0902, 'case_death_ratio': 0.05},
    {'country': 'India', 'lon': 78.9629, 'lat': 20.5937, 'case_death_ratio': 0.03},
    {'country': 'Brazil', 'lon': -51.9253, 'lat': -14.2350, 'case_death_ratio': 0.06},
    {'country': 'Russia', 'lon': 105.3188, 'lat': 61.5240, 'case_death_ratio': 0.02},
    {'country': 'France', 'lon': 2.2137, 'lat': 46.6034, 'case_death_ratio': 0.04},
    {'country': 'Australia', 'lon': 133.7751, 'lat': -25.2744, 'case_death_ratio': 0.01}
]
world_map_df = pd.DataFrame(world_map_json)
world_map_df_sorted = world_map_df.sort_values(by='case_death_ratio', ascending=False)

#____________________________________________________________________________________
# Data of total cases, deaths, and recovered over time:
# trend_json = get_total_cases_over_time()
# trends_df = pd.DataFrame(trend_json)

time = pd.date_range(start='2020-01-01', periods=50, freq='M')
cases = np.random.randint(100000, 1000000, 50)
deaths = np.random.randint(1000, 10000, 50)
recovered = np.random.randint(50000, 100000, 50)

trends_df = pd.DataFrame({'Date': time, 'Cases': cases, 'Deaths': deaths, 'Recovered': recovered})

#____________________________________________________________________________________
country_heat_data = pd.DataFrame({
    "USA": [900, 100, 200, 200],
    "India": [800, 100, 200, 200],
    "Brazil": [700, 80, 190, 200],
    "Russia": [600, 90, 210, 190],
}, index=["Total Cases", "Total Deaths", "Total Recovered", "Total Active"]).T

#____________________________________________________________________________________
# Countries with its corresponding case_death_ratio - Needed for country_selector widget:
options = {row['country']: f"{row['case_death_ratio']:.2%}" for _, row in world_map_df.iterrows()}

# Widgets:

# For selecting a specific country:
country_selector = pn.widgets.Select(name='Select Country', options=country_totals_df.columns.tolist(), width=280)
# Search bar widget to search for news - NEWS API
search_bar = pn.widgets.TextInput(
    name="Search News",
    placeholder="Enter search term (e.g., COVID, Vaccine)...",
    width=305
)

# Callback Functions:

def other_global_stats():
    """ Function to display the global statistics
    """
    stats_md = f"""
    ### Global Statistics
    - **Total Cases:** {global_json['total_cases']:,}
    - **Total Deaths:** {global_json['total_deaths']:,}
    - **Total Recovered:** {global_json['total_recovered']:,}
    - **Total Active:** {global_json['total_active']:,}
    """
    return pn.pane.Markdown(stats_md, width=300, style={"padding": "10px", "font-size": "14px"})


@pn.depends(country=country_selector.param.value)
def country_stats(country):
    """ Function to display a selected country's statistics:
        The country is selected through the country_selector widget
    """
    if not country:
        return pn.pane.Markdown("### Select a country to view its statistics.", width=300)

    country_data = country_totals_df[country]
    stats_md = f"""
    ### {country} Statistics
    - **Total Cases:** {country_data['total_cases']:,}
    - **Total Deaths:** {country_data['total_deaths']:,}
    - **Total Recovered:** {country_data['total_recovered']:,}
    - **Total Active:** {country_data['total_active']:,}
    """
    return pn.pane.Markdown(stats_md, width=300, style={"padding": "10px", "font-size": "14px"})


def create_global_pie_chart():
    """ Generates the global pie chart using the global statistics
    """
    global_df = pd.DataFrame({
        'Category': ['Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active'],
        'Count': list(global_json.values())
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
        height=320,  # Adjust height
        #margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=12  # Optional: reduce font size
    )
    return pn.pane.Plotly(fig)


@pn.depends(country=country_selector.param.value)
def create_country_pie_chart(country):
    """ Generates the pie chart using selected country's statistics
        Country is selected through country_selector widget
    """
    country_data = country_totals_json[country]
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
        height=320,  # Adjust height
        #margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=12  # Optional: reduce font size
    )
    return pn.pane.Plotly(fig)


def create_line_chart():
    """ Generates line chart of total cases, deaths, and recovered over time
    """
    fig = px.line(trends_df, x='Date', y=['Cases', 'Deaths', 'Recovered'],
                  labels={'value': 'Count', 'variable': 'Metric'},
                  title='COVID-19 Trends Over Time',
                  height=350)
    return pn.pane.Plotly(fig)


def correlation_heatmap(data):
    """ Generates heatmap to visualize the correlations among key
        COVID-19 statistics: cases, deaths, recoveries, and active cases.
    """
    correlation_matrix = data.corr()

    fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        color_continuous_scale="Viridis",
        title="Correlation Heatmap: COVID-19 Statistics",
        labels={"color": "Correlation"}
    )
    fig.update_layout(
        width=500, height=320,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return pn.pane.Plotly(fig, config={"displayModeBar": False})

def generate_case_fatality_map():
    """ Generates interactive world map which has points of
        countries using their longitude and latitude coordinates,
        while using color to show the intensity of the corresponding country's
        case_death_ratio
    """
    fig = px.scatter_geo(
        world_map_df,
        lat="lat",
        lon="lon",
        #text="country",  # Display country name on hover
        size="case_death_ratio",  # Size represents the case_death_ratio
        color="case_death_ratio",  # Color intensity represents case_death_ratio
        color_continuous_scale="Reds",  # Red for alarming ratios
        title="World Map: Case Fatality Ratios",
        projection="natural earth",
        labels={"case_death_ratio": "Case Fatality Ratio"},
        template="plotly_white"
    )
    fig.update_traces(marker=dict(sizemode='area', sizeref=0.01, line=dict(width=0.5, color="black")))
    fig.update_geos(
        showcountries=True, countrycolor="LightGrey",
        showcoastlines=True, coastlinecolor="LightBlue",
        showland=True, landcolor="LightGreen",
        showocean=True, oceancolor="LightBlue"
    )
    return pn.pane.Plotly(fig, width=800, height=500)

def create_ranking_box(data, height=400, width=220):
    """ Generates a scrollable ranking box for the given data.
    """
    # Create styled ranking cards
    ranking_items = [
        pn.pane.Markdown(
            f"""
            <div style="padding: 10px; text-align: center; border: 1px solid #ccc; 
            background-color: #f0f0f0; border-radius: 5px;">
                <b>{row['country']}</b><br>
                Fatality Rate: {row['case_death_ratio']:.2%}
            </div>
            """,
            width=200
        )
        for index, row in data.iterrows()
    ]

    # Create the scrollable ranking box
    ranking_box = pn.Column(
        *ranking_items,
        scroll=True,  # Enable scrolling
        height=height,  # Set height for the scrollable box
        width=width,  # Width of the box
        background="#58a3c6"  # Blue-green background matching your mockup
    )

    # Add a title to the ranking box
    ranking_layout = pn.Column(
        pn.pane.Markdown("<h3 style='text-align: center; color: white;'>Ranking</h3>", width=width),
        ranking_box,
        background="#58a3c6",  # Background for the entire ranking column
        margin=0,
        align="center"
    )

    return ranking_layout

#search_bar.param.watch(display_news, "value")

# Create a container for news articles
news_container = pn.Column(scroll=True, height=400, width=400)

# Initial news fetch
#display_news()

# Sidebar Cards:

# Layout to select a specific country
search_card = pn.Card(
    pn.Column(country_selector),
    title="Country Selector",
    width=320,
    collapsed=False
)

# Layout for the news section
news_section = pn.Column(
    pn.pane.Markdown("## COVID-19 Related News"),
    search_bar,
    news_container,
    background="#f9f9f9",  # Light grey background for the section
    width=400
)

# Layout:
layout = pn.template.FastListTemplate(
    title="COVID Insight Hub",
    sidebar=[
        other_global_stats(),  # Global stats card
        pn.Card(country_selector, title="Country Selector", width=300),
        country_stats,  # Country stats card
        news_section
    ],
    main=[
        pn.Tabs(
            ("COVID-19 Statistics Overview", pn.Column( # Tab 1
                pn.Row(
                    create_global_pie_chart,  # Global pie chart
                    correlation_heatmap(country_heat_data) # Heatmap
                ),
                pn.Row(
                    create_country_pie_chart,  # Country-specific pie chart
                    create_line_chart(), # Line chart
                )
            )),
            ("Case-Fatality Ratio Map", pn.Column( # Tab 2
                pn.Row(
                    pn.Column(generate_case_fatality_map(), sizing_mode="stretch_width"),  # World map
                            create_ranking_box(world_map_df, height=441, width=210), # Ranking of ratio on right
                )
            ))
        )
    ],
    header_background="#2c2c2c",  # Dark grey for header
    accent_base_color="#f5f5f5",  # White accents
    header_color="#ffffff",  # White text for header
    background="#1e1e1e",  # Blackish background
    theme_toggle=True
).servable()

layout.show()