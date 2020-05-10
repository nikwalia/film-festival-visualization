import pandas as pd
import os


def find_year_data(year):
    all_files = os.listdir('data')
    year_data = {}
    for file in all_files:
        df = pd.read_csv('data/' + file, delimiter='\t', index_col=None)
        festival_name = file.split('_')[0]
        award_category = file.split('_')[2].split('.')[0]
        matches = df[df['Year'] == year]
        if festival_name not in year_data.keys():
            year_data[festival_name] = {}
        year_data[festival_name][award_category] = matches

    return year_data


if __name__ == "__main__":
    dat = find_year_data(1980)
    print(dat)
