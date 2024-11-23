import pandas as pd
import numpy as np
import panel as pn
import plotly.express as px
import holoviews as hv
import geoviews as gv
from holoviews import opts

# Initialize panel and extensions
hv.extension('bokeh')
pn.extension()

# global data
global_data = {'total_cases':500, 'total_deaths':100, 'total_recovered':200, 'total_active':200}

# country-specific data
countries = ["USA", "India", "Brazil", "Russia", "France", "Japan"]
country_total_case_data = {'US':{'total_cases':900, 'total_deaths':100, 'total_recovered':200, 'total_active':200},
            'India':{'total_cases':800, 'total_deaths':100, 'total_recovered':200, 'total_active':200},
            'Italy':{'total_cases':700, 'total_deaths':100, 'total_recovered':200, 'total_active':200}}
df = pd.DataFrame(country_total_case_data)

# Widgets

country_selector = pn.widgets.Select(name='Select Country', options=df.columns.tolist(), width=280)
chart_width = pn.widgets.IntSlider(name='Chart Width', start=400, end=1200, step=100, value=600)
chart_height = pn.widgets.IntSlider(name='Chart Height', start=300, end=800, step=100, value=400)


# Callback Functions
def global_stats():
    stats_card = pn.Card(
        pn.Column(
            pn.pane.Markdown(f"**Total Cases:** {global_data['total_cases']:,}"),
            pn.pane.Markdown(f"**Total Deaths:** {global_data['total_deaths']:,}"),
            pn.pane.Markdown(f"**Total Recovered:** {global_data['total_recovered']:,}"),
            pn.pane.Markdown(f"**Total Active:** {global_data['total_active']:,}")
        ),
        title="Global Statistics",
        width=300
    )
    return stats_card


@pn.depends(country=country_selector.param.value)
def country_stats(country):
    if not country:
        return "Select a country to view its statistics."
    country_data = df[country]
    return pn.Card(
        pn.Column(
            f"**Cases:** {country_data['total_cases']:,}",
            f"**Deaths:** {country_data['total_deaths']:,}",
            f"**Recovered:** {country_data['total_recovered']:,}",
            f"**Active:** {country_data['total_active']:,}"
        ),
        title=f"{country} Statistics",
        width=300
    )

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
    return pn.pane.Plotly(fig, width=400, height=400)

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
    return pn.pane.Plotly(fig, width=400, height=400)

def create_line_chart():
    time = pd.date_range(start='2020-01-01', periods=50, freq='M')
    cases = np.random.randint(100000, 1000000, 50)
    deaths = np.random.randint(1000, 10000, 50)
    recovered = np.random.randint(50000, 100000, 50)

    df_trends = pd.DataFrame({'Date': time, 'Cases': cases, 'Deaths': deaths, 'Recovered': recovered})
    fig = px.line(df_trends, x='Date', y=['Cases', 'Deaths', 'Recovered'],
                  labels={'value': 'Count', 'variable': 'Metric'},
                  title='COVID-19 Trends Over Time')
    return pn.pane.Plotly(fig)

def get_theme():
    """
    Determines the current theme of the application (light or dark).
    Parameters:
        None
    Returns:
        str: 'dark' if dark mode is active, otherwise 'default'.
    """
    args = pn.state.session_args
    if "theme" in args and args["theme"][0] == b"dark":
        return "dark"
    return "default"

# Sidebar Cards
search_card = pn.Card(
    pn.Column(country_selector),
    title="Country Selector",
    width=320,
    collapsed=False
)

chart_settings_card = pn.Card(
    pn.Column(chart_width, chart_height),
    title="Chart Settings",
    width=320,
    collapsed=True
)

# Layout
layout = pn.template.FastListTemplate(
    title="COVID Insight Dashboard",
    theme_toggle=True,
    sidebar=[
        """global_stats(),
        search_card,
        pn.Spacer(height=50),
        country_stats"""
        #chart_settings_card
    ],
    main=[
        pn.Tabs(
            ("Global vs. Country Comparison", pn.Column(
                pn.Row(
                    pn.Card(country_selector, title="Country Selector", width=300),
                    global_stats(),  # Global stats card
                    country_stats  # Country stats card
                ),
                pn.Row(
                    create_global_pie_chart,  # Global pie chart
                    create_country_pie_chart  # Country-specific pie chart
                )
            )),
            ("Graphs", pn.Column(
                pn.Row(
                    create_line_chart()
                ),
                pn.Row(
                    'kk'
                )
            ))
        )
    ],
    header_background='#343a40'
).servable()

layout.show()