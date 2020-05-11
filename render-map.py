# Citations: https://towardsdatascience.com/a-complete-guide-to-an-interactive-geographical-map-using-python-f4c5197e23e0

import geopandas as gpd
import json
import pandas as pd
import numpy as np
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, ColumnDataSource
from bokeh.models import HoverTool, Dropdown

shapefile = 'ne_110m_admin_0_countries.shp'


def plot_data(festival, year):
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    # Rename columns
    gdf.columns = ['country', 'country_code', 'geometry']

    # Read data to json.
    gdf_json = json.loads(gdf.to_json())
    # Convert to String like object.
    grid = json.dumps(gdf_json)

    datafile1 = './data/' + festival + '_best_actor.csv'
    # Read csv file using pandas
    df1 = pd.read_csv(datafile1, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df1 = df1.loc[df1['Year'] == year]

    datafile2 = './data/' + festival + '_best_actress.csv'
    df2 = pd.read_csv(datafile1, sep=',', names=['Year', 'Actress', 'Countries'], skiprows=1)
    df2 = df2.loc[df2['Year'] == year]

    datafile3 = './data/' + festival + '_best_director.csv'
    df3 = pd.read_csv(datafile1, sep=',', names=['Year', 'Director', 'Countries'], skiprows=1)
    df3 = df3.loc[df3['Year'] == year]

    datafile4 = './data/' + festival + '_best_film.csv'
    df4 = pd.read_csv(datafile1, sep=',', names=['Year', 'Director', 'Countries'], skiprows=1)
    df4 = df4.loc[df4['Year'] == year]

    frames = [df1, df2, df3, df4]
    result = pd.concat(frames)

    countryfile = './data/country_geocodes.csv'
    cf = pd.read_csv(countryfile, sep=',', names=['Country', 'Latitude', 'Longitude'], skiprows=1)
    print (result)
    print (cf)
    points = pd.merge(result, cf, left_on='Year', right_on='Country', how='left')

    geosource = GeoJSONDataSource(geojson=grid)
    pointsource = ColumnDataSource(points)

    # Create figure object.
    p = figure(title='Worldwide Film Festival Awards', plot_height=600, plot_width=1050)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    # Add patch renderer to figure.
    patch = p.patches('xs', 'ys', source=geosource, fill_color='#fff7bc',
                      line_color='black', line_width=0.35, fill_alpha=1,
                      hover_fill_color="#fec44f")

    p.add_tools(HoverTool(tooltips=[('Year', '@Year'), ('Best Actor', '@Actor'), ('Best Actress', '@Actress'),
                                    ('Best Director', '@Director'), ('Country', '@Country')], renderers=[patch]))

    show(p)

if __name__ == "__main__":
    # output_file("film-festivals.html")
    # filters_list = [("Festival", "festival")]
    # filter_dropdown = Dropdown(label="Filter By", button_type="primary", menu=filters_list)
    # show(filter_dropdown)
    plot_data("cannes")