from bokeh.io import show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, column, row
from bokeh.models import GeoJSONDataSource, ColumnDataSource
from bokeh.models import HoverTool, Slider
from bokeh.palettes import Viridis6 as palette
from bokeh.models import LogColorMapper

import render_map
import json

start_year = 1935
end_year = 2019
year = start_year

# setup initial data
init_dat = render_map.get_data(year)
# Read data to json.
gdf_json = json.loads(init_dat.to_json())
# Convert to String like object.
grid = json.dumps(gdf_json)

geosource = GeoJSONDataSource(geojson=grid)

# map setup
world_map = figure(title='Worldwide Film Festival Awards', plot_height=600, plot_width=1050)
world_map.xgrid.grid_line_color = None
world_map.ygrid.grid_line_color = None
color_mapper = LogColorMapper(palette=palette)

patch = world_map.patches('xs', 'ys', source=geosource, fill_color={'field': 'counts', 'transform': color_mapper},
                          line_color='black', line_width=0.35, fill_alpha=1,
                          hover_fill_color="#fec44f")

# Widgets
world_map.add_tools(HoverTool(tooltips=[(
    'Country', '@country'),
    ('Actor', '@actors'),
    ('Actress', '@actresses'),
    ('Director', '@directors'),
    ('Movie', '@movies'),
    ('Total', '@counts')
], renderers=[patch]))


def year_handler(attr, old, new):
    global year
    year = new
    gdf_json = json.loads(render_map.get_data(year).to_json())
    # Convert to String like object.
    grid = json.dumps(gdf_json)
    # global geosource
    geosource.geojson = grid


output_file("film-festivals.html")

slider = Slider(start=start_year, end=end_year, value=start_year, step=1, title="Year")
slider.on_change("value", year_handler)
layout = column(row(widgetbox(slider)), world_map)
curdoc().add_root(layout)
show(layout)
