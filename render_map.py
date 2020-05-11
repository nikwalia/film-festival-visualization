import geopandas as gpd
import pandas as pd
import numpy as np

shapefile = 'ne_110m_admin_0_countries.shp'

"""
Finds all the data for a given year, along with country shapes
@:param year: the year for which to get the awards
"""


def get_data(year):
    global shapefile
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    # print("In plot_data")
    # Rename columns
    gdf.columns = ['country', 'country_code', 'geometry']

    # ACTOR AWARDS
    datafile1berlin = './data/berlin_best_actor.csv'
    # Read csv file using pandas
    df1berlin = pd.read_csv(datafile1berlin, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df1berlin = df1berlin.loc[df1berlin['Year'] == year]

    datafile1cannes = './data/cannes_best_actor.csv'
    # Read csv file using pandas
    df1cannes = pd.read_csv(datafile1cannes, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df1cannes = df1cannes.loc[df1cannes['Year'] == year]

    datafile1venice = './data/venice_best_actor.csv'
    # Read csv file using pandas
    df1venice = pd.read_csv(datafile1venice, sep=',', names=['Year', 'Actor', 'Countries'], skiprows=1)
    df1venice = df1venice.loc[df1venice['Year'] == year]

    df1 = df1berlin.append(df1cannes, sort=False).append(df1venice, sort=False)

    # ACTRESS AWARDS
    datafile2berlin = './data/berlin_best_actress.csv'
    # Read csv file using pandas
    df2berlin = pd.read_csv(datafile2berlin, sep=',', names=['Year', 'Actress', 'Countries'], skiprows=1)
    df2berlin = df2berlin.loc[df2berlin['Year'] == year]

    datafile2cannes = './data/cannes_best_actress.csv'
    # Read csv file using pandas
    df2cannes = pd.read_csv(datafile2cannes, sep=',', names=['Year', 'Actress', 'Countries'], skiprows=1)
    df2cannes = df2cannes.loc[df2cannes['Year'] == year]

    datafile2venice = './data/venice_best_actress.csv'
    # Read csv file using pandas
    df2venice = pd.read_csv(datafile2venice, sep=',', names=['Year', 'Actress', 'Countries'], skiprows=1)
    df2venice = df2venice.loc[df2venice['Year'] == year]

    df2 = df2berlin.append(df2cannes, sort=False).append(df2venice, sort=False)

    # DIRECTOR AWARDS
    datafile3berlin = './data/berlin_best_director.csv'
    # Read csv file using pandas
    df3berlin = pd.read_csv(datafile3berlin, sep=',', names=['Year', 'Director', 'Countries'], skiprows=1)
    df3berlin = df3berlin.loc[df3berlin['Year'] == year]

    datafile3cannes = './data/cannes_best_director.csv'
    # Read csv file using pandas
    df3cannes = pd.read_csv(datafile3cannes, sep=',', names=['Year', 'Director', 'Countries'], skiprows=1)
    df3cannes = df3cannes.loc[df3cannes['Year'] == year]

    datafile3venice = './data/venice_best_director.csv'
    # Read csv file using pandas
    df3venice = pd.read_csv(datafile3venice, sep=',', names=['Year', 'Director', 'Countries'], skiprows=1)
    df3venice = df3venice.loc[df3venice['Year'] == year]

    df3 = df3berlin.append(df3cannes, sort=False).append(df3venice, sort=False)

    # FILM AWARDS
    datafile4berlin = './data/berlin_best_film.csv'
    # Read csv file using pandas
    df4berlin = pd.read_csv(datafile4berlin, sep=',', names=['Year', 'Movie', 'Countries'], skiprows=1)
    df4berlin = df4berlin.loc[df4berlin['Year'] == year]

    datafile4cannes = './data/cannes_best_film.csv'
    # Read csv file using pandas
    df4cannes = pd.read_csv(datafile4cannes, sep=',', names=['Year', 'Movie', 'Countries'], skiprows=1)
    df4cannes = df4cannes.loc[df4cannes['Year'] == year]

    datafile4venice = './data/venice_best_film.csv'
    # Read csv file using pandas
    df4venice = pd.read_csv(datafile4venice, sep=',', names=['Year', 'Movie', 'Countries'], skiprows=1)
    df4venice = df4venice.loc[df4venice['Year'] == year]

    df4 = df4berlin.append(df4cannes, sort=False).append(df4venice, sort=False)

    frames = [df1, df2, df3, df4]
    result = pd.concat(frames)

    countryfile = './data/country_geocodes.csv'
    cf = pd.read_csv(countryfile, sep=',', names=['Countries', 'Latitude', 'Longitude'], skiprows=1)
    points = pd.merge(result, cf, on="Countries")

    counts = dict((country, 0) for country in gdf['country'])
    actors = dict((country, []) for country in gdf['country'])
    actresses = dict((country, []) for country in gdf['country'])
    directors = dict((country, []) for country in gdf['country'])
    movies = dict((country, []) for country in gdf['country'])

    year_match = points[points['Year'] == year]
    for dat in year_match['Countries']:
        countries = dat.split('|')
        for country in countries:
            counts[country] += 1

    for index, row in year_match.iterrows():
        if not np.isreal(row['Actor']):
            actors[row['Countries']].append(row['Actor'])
        if not np.isreal(row['Actress']):
            actresses[row['Countries']].append(row['Actress'])
        if not np.isreal(row['Director']):
            directors[row['Countries']].append(row['Director'])
        if not np.isreal(row['Movie']):
            movies[row['Countries']].append(row['Movie'])

    gdf['counts'] = counts.values()
    gdf['actors'] = [', '.join(actor_names) for actor_names in actors.values()]
    gdf['actresses'] = [', '.join(actress_names) for actress_names in actresses.values()]
    gdf['directors'] = [', '.join(director_names) for director_names in directors.values()]
    gdf['movies'] = [', '.join(movie_names) for movie_names in movies.values()]

    return gdf
