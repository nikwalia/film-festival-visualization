from bokeh.io import show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import Slider, Dropdown
from bokeh.layouts import widgetbox, column, row
import render_map

if __name__ == "__main__":
    output_file("film-festivals.html")
    start_year = 1920
    end_year = 2020
    slider = Slider(start=start_year, end=end_year, value=start_year, step=1, title="Year")
    # show(slider)

    festival_list = [("Cannes", "cannes"), ("Berlin", "berlin"), ("Venice", "venice")]
    festival_dropdown = Dropdown(label="Festival", button_type="primary", menu=festival_list)
    # show(festival_dropdown)
    
    layout = row(widgetbox(festival_dropdown), widgetbox(slider))
    curdoc().add_root(layout)
    show(layout)