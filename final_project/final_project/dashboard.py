import pandas as pd
import panel as pn
import plotly.express as px
import holoviews as hv
import geoviews as gv
import requests

# Initialize panel and extensions
pn.extension('plotly')

# Data:

# Define the base URL
BASE_URL = "http://localhost:9001"

# Access total cases endpoint
response = requests.get(f"{BASE_URL}/total_cases")
if response.status_code == 200:
    country_json = response.json()
    #print("Total Cases:", country_json)
else:
    print("Failed to fetch total cases:", response.status_code)

# Access total cases by country endpoint
response = requests.get(f"{BASE_URL}/total_cases_by_country")
if response.status_code == 200:
    country_totals_json = response.json()
    #print("Total Cases by Country:", country_totals_json)
else:
    print("Failed to fetch total cases by country:", response.status_code)

# Access case fatality ratio endpoint
response = requests.get(f"{BASE_URL}/case_fatality_ratio")
if response.status_code == 200:
    world_map_json = response.json()
    #print("Case Fatality Ratio:", world_map_json)
else:
    print("Failed to fetch case fatality ratio:", response.status_code)

# Access total cases over time endpoint
response = requests.get(f"{BASE_URL}/total_cases_over_time")
if response.status_code == 200:
    trends_df = response.json()
    #print("Total Cases Over Time:", trends_df)
else:
    print("Failed to fetch total cases over time:", response.status_code)

# Access news endpoint
response = requests.get(f"{BASE_URL}/news")
if response.status_code == 200:
    news_data = response.json()
    #print("News:", news_data)
else:
    print("Failed to fetch news:", response.status_code)

#________________________________________________________________________________________________________
# Data:

# global data
# global_json = get_total_cases()
global_json = {}
global_json['total_recovered'] = global_json['total_cases'] - global_json['total_active'] - global_json['total_deaths']

#____________________________________________________________________________________
# country-specific data
# country_totals_json = get_total_cases_by_country()
country_totals_json = {}
country_totals_df = (pd.DataFrame(country_totals_json)/1000).round().astype(int)
country_totals_df.loc['total_recovered'] = (
    country_totals_df.loc['total_cases']
    - country_totals_df.loc['total_active']
    - country_totals_df.loc['total_deaths']
)

#____________________________________________________________________________________
# Data with each country's location and case-death ratio
# world_map_json = get_case_fatality_ratio()
world_map_json = []
world_map_df = pd.DataFrame(world_map_json)
world_map_df_sorted = world_map_df.sort_values(by='case_fatality_ratio', ascending=False)

#____________________________________________________________________________________
# Data of total cases, deaths, and recovered over time:
# trend_json = get_total_cases_over_time()
# trends_df = pd.DataFrame(trend_json)
trends_df = pd.DataFrame({})

#____________________________________________________________________________________
# Heat map data
country_totals_data = {key:list(numbers.values()) for key, numbers in country_totals_json.items()}
country_heat_data = pd.DataFrame(country_totals_data,
                                 index=["Total Cases", "Total Deaths", "Total Recovered", "Total Active"]).T
#____________________________________________________________________________________
news = {}
articles = news["articles"]

#____________________________________________________________________________________
# Widgets:

# For selecting a specific country:
country_selector = pn.widgets.Select(name='Select Country', options=country_totals_df.columns.tolist(), width=280)

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
    return pn.pane.Markdown(stats_md, width=300, styles={"padding": "10px", "font-size": "14px"})


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
    return pn.pane.Markdown(stats_md, width=300, styles={"padding": "10px", "font-size": "14px"})


def create_global_pie_chart():
    """ Generates the global pie chart using the global statistics
    """

    # Filter out 'Total Recovered' if it exists in global_json
    filtered_data = {k: v for k, v in global_json.items() if k != 'total_cases'}

    # Create the DataFrame for the pie chart
    global_df = pd.DataFrame({
        'Category': list(filtered_data.keys()),
        'Count': list(filtered_data.values())
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

    country_data = country_totals_df[country]

    # Filter out the 'total_recovered' row
    filtered_data = country_data[country_data.index != 'total_cases']

    # Create the DataFrame for the pie chart
    country_df = pd.DataFrame({
        'Category': filtered_data.index,
        'Count': filtered_data.values
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
    fig = px.line(trends_df, x='date', y=['total_cases', 'total_deaths', 'total_recovered'],
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
        case_fatality_ratio
    """
    fig = px.scatter_geo(
        world_map_df,
        lat="latitude",
        lon="longitude",
        hover_name="country",  # Display country name on hover
        size="case_fatality_ratio",  # Size represents the case_fatality_ratio
        color="case_fatality_ratio",  # Color intensity represents case_fatality_ratio
        color_continuous_scale="Reds",  # Red for alarming ratios
        title="World Map: Case Fatality Ratios",
        projection="natural earth",
        labels={"case_fatality_ratio": "Case Fatality Ratio"},
        template="plotly_white"
    )
    fig.update_traces(marker=dict(sizemode='area', sizeref=0.1, line=dict(width=0.5, color="black")))
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
                Fatality Rate: {round(row['case_fatality_ratio'], 2)}%
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
        styles = {'background': "#58a3c6"}  # Blue-green background matching your mockup
    )

    # Add a title to the ranking box
    ranking_layout = pn.Column(
        pn.pane.Markdown("<h3 style='text-align: center; color: white;'>Ranking</h3>", width=width),
        ranking_box,
        styles = {'background': "#58a3c6"}, # Background for the entire ranking column
        margin=0,
        align="center"
    )

    return ranking_layout

def create_article_list(articles_data):
    # Create the title as a Markdown pane
    title_pane = pn.pane.Markdown("COVID-19 News Articles",
                                  styles={"margin-bottom": "5px", "font-weight": "bold", "background-color": "lightblue",
                                         "padding": "5px", "border-radius": "5px", "width": "260px", "text-align": "center"})

    # Generate the article list
    article_items = []
    for article in articles_data:
        item = pn.pane.Markdown(
            f"[{article['title']}]({article['link']})",
            styles={"font-size": "14px", "margin-bottom": "10px"}
        )
        article_items.append(item)

    # Combine the title and the article list in a scrollable column
    scrollable_column = pn.Column(title_pane, *article_items, scroll=True, height=300, width=300)
    return scrollable_column

# Layout:
layout = pn.template.FastListTemplate(
    title="COVID Insight Hub",
    sidebar=[
        other_global_stats(),  # Global stats card
        pn.Card(country_selector, title="Country Selector", width=300),
        country_stats,  # Country stats card
        create_article_list(articles)
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
                            create_ranking_box(world_map_df_sorted, height=441, width=210), # Ranking of ratio on right
                )
            ))
        )
    ],
    header_background="#2c2c2c",  # Dark grey for header
    accent_base_color="#f5f5f5",  # White accents
    header_color="#ffffff",  # White text for header
    #theme_toggle=True
).servable()

#layout.show()