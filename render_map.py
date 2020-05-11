# Citations: https://towardsdatascience.com/a-complete-guide-to-an-interactive-geographical-map-using-python-f4c5197e23e0

import geopandas as gpd
import json
import pandas as pd
import numpy as np
import bokeh
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, ColumnDataSource
from bokeh.models import HoverTool, Dropdown
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
import math

shapefile = 'ne_110m_admin_0_countries.shp'


def plot_data(festival, year):
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    # Rename columns
    gdf.columns = ['country', 'country_code', 'geometry']

    ## ACTOR AWARDS
    datafile1berlin = './data/berlin_best_actor.csv'
    # Read csv file using pandas
    df1berlin = pd.read_csv(datafile1berlin, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df1berlin = df1berlin.loc[df1berlin['Year'] == year]

    datafile1cannes = './data/cannes_best_actor.csv'
    # Read csv file using pandas
    df1cannes = pd.read_csv(datafile1, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df1cannes = df1cannes.loc[df1cannes['Year'] == year]

    datafile1venice = './data/venice_best_actor.csv'
    # Read csv file using pandas
    df1venice = pd.read_csv(datafile1, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df1venice = df1venice.loc[df1venice['Year'] == year]

    df1 = df1berlin.append(df1cannes, sort=False).append(df1venice, sort=False)

    ## ACTRESS AWARDS
    datafile2berlin = './data/berlin_best_actress.csv'
    # Read csv file using pandas
    df2berlin = pd.read_csv(datafile2berlin, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df2berlin = df2berlin.loc[df2berlin['Year'] == year]

    datafile2cannes = './data/cannes_best_actress.csv'
    # Read csv file using pandas
    df2cannes = pd.read_csv(datafile2cannes, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df2cannes = df2cannes.loc[df2cannes['Year'] == year]

    datafile2venice = './data/venice_best_actress.csv'
    # Read csv file using pandas
    df2venice = pd.read_csv(datafile2venice, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df2venice = df2venice.loc[df2venice['Year'] == year]

    df2 = df2berlin.append(df2cannes, sort=False).append(df2venice, sort=False)

    ## DIRECTOR AWARDS
    datafile3berlin = './data/berlin_best_director.csv'
    # Read csv file using pandas
    df3berlin = pd.read_csv(datafile3berlin, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df3berlin = df3berlin.loc[df3berlin['Year'] == year]

    datafile3cannes = './data/cannes_best_director.csv'
    # Read csv file using pandas
    df3cannes = pd.read_csv(datafile3cannes, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df3cannes = df3cannes.loc[df3cannes['Year'] == year]

    datafile3venice = './data/venice_best_director.csv'
    # Read csv file using pandas
    df3venice = pd.read_csv(datafile3venice, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df3venice = df3venice.loc[df3venice['Year'] == year]

    df3 = df3berlin.append(df3cannes, sort=False).append(df3venice, sort=False)

    ## FILM AWARDS
    datafile4berlin = './data/berlin_best_film.csv'
    # Read csv file using pandas
    df4berlin = pd.read_csv(datafile4berlin, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df4berlin = df4berlin.loc[df4berlin['Year'] == year]

    datafile4cannes = './data/cannes_best_film.csv'
    # Read csv file using pandas
    df4cannes = pd.read_csv(datafile4cannes, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df4cannes = df4cannes.loc[df4cannes['Year'] == year]

    datafile4venice = './data/venice_best_film.csv'
    # Read csv file using pandas
    df4venice = pd.read_csv(datafile4venice, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df4venice = df4venice.loc[df4venice['Year'] == year]

    df4 = df4berlin.append(df4cannes, sort=False).append(df4venice, sort=False)

    frames = [df1, df2, df3, df4]
    result = pd.concat(frames)

    countryfile = './data/country_geocodes.csv'
    cf = pd.read_csv(countryfile, sep=',', names=['Countries', 'Latitude', 'Longitude'], skiprows=1)
    print(result)
    print(cf)
    points = pd.merge(result, cf, on="Countries")
    print(points)

    pointsource = ColumnDataSource(points)

    color_mapper = LogColorMapper(palette=palette)

    counts = dict((country, 0) for country in gdf['country'])

    year_match = points[points['Year'] == year]
    for dat in year_match['Countries']:
        countries = dat.split('|')
        for country in countries:
            counts[country] += 1

    gdf['counts'] = counts.values()

    # Read data to json.
    gdf_json = json.loads(gdf.to_json())
    # Convert to String like object.
    grid = json.dumps(gdf_json)

    geosource = GeoJSONDataSource(geojson=grid)

    # original color: '#fff7bc'
    # Create figure object.
    p = figure(title='Worldwide Film Festival Awards', plot_height=600, plot_width=1050)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    # Add patch renderer to figure.
    patch = p.patches('xs', 'ys', source=geosource, fill_color={'field': 'counts', 'transform': color_mapper},
                      line_color='black', line_width=0.35, fill_alpha=1,
                      hover_fill_color="#fec44f")

    p.add_tools(HoverTool(tooltips=[('Country', '@country'), ('Count', '@counts')], renderers=[patch]))

    return p


if __name__ == "__main__":
    # output_file("film-festivals.html")
    # filters_list = [("Festival", "festival")]
    # filter_dropdown = Dropdown(label="Filter By", button_type="primary", menu=filters_list)
    # show(filter_dropdown)
    plot_data("cannes", 2018)
