from bokeh.io import show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import Slider, Dropdown
from bokeh.layouts import widgetbox, column, row
import render_map

global start_year
global end_year
global festival
global year
global world_map

start_year = 1932
end_year = 2019
year = start_year
world_map = None

#
# def dropdown_handler(attr, old, new):
#     print("Dropdown: ", old, " to ", new)
#     global festival
#     festival = new
#     global world_map
#     world_map = render_map.plot_data(year)


def year_handler(attr, old, new):
    global year
    year = new
    global world_map
    world_map = render_map.plot_data(year)

output_file("film-festivals.html")
slider = Slider(start=start_year, end=end_year, value=start_year, step=1, title="Year")
slider.on_change("value", year_handler)
# show(slider)

festival_list = [("Cannes", "cannes"), ("Berlin", "berlin"), ("Venice", "venice")]
# festival_dropdown = Dropdown(label="Festival", button_type="primary", menu=festival_list)
# festival_dropdown.on_change("value", dropdown_handler)
# show(festival_dropdown)
world_map = render_map.plot_data(year)
# layout = column(row(widgetbox(festival_dropdown), widgetbox(slider)), world_map)
layout = column(row(widgetbox(slider)), world_map)
curdoc().add_root(layout)
show(layout)