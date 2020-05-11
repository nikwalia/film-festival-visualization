from bokeh.io import show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import Slider, Dropdown
from bokeh.layouts import widgetbox, column, row
import render_map

start_year = 1932
end_year = 2019
festival = "Cannes"
year = start_year

def dropdown_handler(attr, old, new):
    festival = new

def year_handler(attr, old, new):
    year = new

if __name__ == "__main__":
    output_file("film-festivals.html")
    slider = Slider(start=start_year, end=end_year, value=year, step=1, title="Year")
    slider.on_change("value", year_handler)
    # show(slider)

    festival_list = [("Cannes", "cannes"), ("Berlin", "berlin"), ("Venice", "venice")]
    festival_dropdown = Dropdown(label=festival, button_type="primary", menu=festival_list)
    festival_dropdown.on_change("value", dropdown_handler)
    # show(festival_dropdown)
    world_map = render_map.plot_data(festival.lower(), year)
    layout = column(row(widgetbox(festival_dropdown), widgetbox(slider)), world_map)
    curdoc().add_root(layout)
    show(layout)