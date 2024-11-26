# Testing world_map
import geoviews as gv
from geoviews import opts
import pandas as pd
import geoviews.tile_sources as gvts
import param
import holoviews as hv
import panel as pn

hv.extension('bokeh')
gv.extension('bokeh')


def world_map(data_json):
    # Convert JSON to DataFrame
    data = pd.DataFrame(data_json)

    # Ensure required columns are present
    if not {'country', 'lon', 'lat', 'case_death_ratio'}.issubset(data.columns):
        raise ValueError("JSON data must include 'country', 'lon', 'lat', and 'case_death_ratio' fields.")

    # Create GeoViews Points plot
    points = gv.Points(data, ['lon', 'lat'], ['case_death_ratio', 'country'])

    # Define the map visualization
    map_plot = points.opts(
        opts.Points(
            size=15,
            tools=['hover'],  # Enable hover tooltip
            color='case_death_ratio',  # Color based on the case-death ratio
            cmap='YlOrBr',  # Use a yellow-orange colormap for a similar look
            width=800,
            height=500
        )
    )

    # Add basemap for a background
    basemap = gvts.OSM
    return basemap * map_plot

data_json = [
    {'country': 'USA', 'lon': -95.7129, 'lat': 37.0902, 'case_death_ratio': 0.05},
    {'country': 'India', 'lon': 78.9629, 'lat': 20.5937, 'case_death_ratio': 0.03},
    {'country': 'Brazil', 'lon': -51.9253, 'lat': -14.2350, 'case_death_ratio': 0.06},
    {'country': 'Russia', 'lon': 105.3188, 'lat': 61.5240, 'case_death_ratio': 0.02},
    {'country': 'France', 'lon': 2.2137, 'lat': 46.6034, 'case_death_ratio': 0.04},
    {'country': 'Australia', 'lon': 133.7751, 'lat': -25.2744, 'case_death_ratio': 0.01}
]


class WorldMap(param.Parameterized):
    # Map display options
    opts = dict(width=800, height=500, xaxis=None, yaxis=None, show_grid=False)

    # Tiles (base map)
    tiles = gv.tile_sources.CartoEco.opts(**opts)  # Remove parentheses

    # Extents to control the visible map area
    extents = param.Parameter(default=(-180, -90, 180, 90), precedence=-1)
    tiles.extents = extents.default  # Apply extents to the tiles

    # Dynamic points for country data
    template_df = pd.DataFrame({'country': [], 'lon': [], 'lat': []}, columns=['country', 'lon', 'lat'])
    dfstream = hv.streams.Buffer(template_df, index=False, length=10000)

    points = hv.DynamicMap(hv.Points, streams=[dfstream]).opts(
        size=10, color='blue', fill_alpha=0.5, line_alpha=0.5, tools=['hover']
    )

    def add_country_data(self, data):
        """Add new country data dynamically."""
        self.dfstream.send(pd.DataFrame(data))

    def show_map(self):
        """Combine all map elements into one GeoViews overlay."""
        return self.tiles * self.points


# Instantiate the WorldMap class
world_map_instance = WorldMap()

dynamic_world_map = world_map_instance.show_map()

# Example world map data
world_map_data = [
    {'country': 'USA', 'lon': -95.7129, 'lat': 37.0902},
    {'country': 'India', 'lon': 78.9629, 'lat': 20.5937},
    {'country': 'Brazil', 'lon': -51.9253, 'lat': -14.2350},
]

# Add the data to the map
world_map_instance.add_country_data(world_map_data)

pn.extension()

# Sidebar widgets for customization
chart_width = pn.widgets.IntSlider(name='Chart Width', start=400, end=1200, step=100, value=800)
chart_height = pn.widgets.IntSlider(name='Chart Height', start=300, end=800, step=100, value=500)

# Dynamic Map Card
map_card = pn.Card(
    dynamic_world_map.opts(width=chart_width.value, height=chart_height.value),
    title="World Map",
    width=800
)

# Full Dashboard Layout
layout = pn.template.FastListTemplate(
    title="World Map Dashboard",
    sidebar=[chart_width, chart_height],
    main=[map_card],
    header_background="#343a40"
).servable()

layout.show()
