import numpy as np
import pandas as pd

from sdg_mapping.utils.misc_utils import camel_to_snake, fetch

def sdg_index_file_path(year):

    fname = f'{year}_sdg_index.xlsx'
    return f'{project_dir}/data/raw/sdg_index/{fname}'

def fetch_index(year, fout=None):
    url = None
    if year == 2019:
        url = 'https://sdsna.github.io/2019GlobalIndex/2019GlobalIndexResults.xlsx'

    if fout is None:
        fout = sdg_index_file_path(year)

    if not os.path.isdir(os.path.dirname(fout)):
        os.makedirs(os.path.dirname(fout))

    return fetch(url, fout)

def read_workbook(data_sheet_name, data_path):
    df = pd.read_excel(open(f'{data_path}', 'rb'),
              sheet_name=data_sheet_name)

    return df

def parse_2019_sdg_index(dataset, sheet_name, path):

    with open(f'{project_dir}/data/aux/sdg_index_mappings.json', 'r') as f:
        maps = json.load(f)

    trend_map = maps['trend_map']
    achievement_map = maps['achievement_map']

    sdg_index_19_df = dataset.drop([0]).reset_index(drop=True)

    trend_columns = [i for i in sdg_index_19_df.columns if 'Trend' in i]
    dashboard_columns = [i for i in sdg_index_19_df.columns if (('Dashboard' in i) and ('Goal' in i))]


    for j in trend_columns:
        sdg_index_19_df[j] = sdg_index_19_df[j].map(trend_map)
    for j in dashboard_columns:
        sdg_index_19_df[j] = sdg_index_19_df[j].map(achievement_map)

    return sdg_index_19_df

def load_sdg_index(year=None,):


    fin = sdg_index_file_path(year)
    df = read_workbook(sheet_name, fin)
    df = parse_2019_sdg_index(df)

    return df



    # https://sdsna.github.io/2019GlobalIndex/2019GlobalIndexResults.xlsx
    # https://github.com/sdsna/2018GlobalIndex/raw/master/2018GlobalIndexResults.xlsx
    # https://github.com/sdsna/2017GlobalIndex/blob/master/2017GlobalIndexResults.xlsx
