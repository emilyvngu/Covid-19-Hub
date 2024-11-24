# Testing world_map
import geoviews as gv
from geoviews import opts
import pandas as pd
import geoviews.tile_sources as gvts


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

world_map_plot = world_map(data_json)