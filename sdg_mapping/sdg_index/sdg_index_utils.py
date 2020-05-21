import numpy as np
import pandas as pd

import sys
import os
import urllib

from sdg_mapping import project_dir

from sdg_mapping.utils.misc_utils import fetch

def sdg_index_file_path(year):

    fname = f'{year}_sdg_index.xlsx'
    return f'{project_dir}/data/raw/{fname}' #/sdg_index

def fetch_index(year): #, fout=None
    url = None
    if year == 2019:
        url = 'https://github.com/sdsna/2019GlobalIndex/raw/master/2019GlobalIndexResults.xlsx'

        fname = f'{year}_sdg_index.xlsx'
    return urllib.request.urlretrieve(url, f'{project_dir}/data/raw/{fname}')

def read_workbook(data_sheet_name, data_path):
    # SDR2019 Data
    df = pd.read_excel(open(data_path, 'rb'),
              sheet_name=data_sheet_name)
    df.columns = df.iloc[0].values

    return df

def parse_2019_sdg_index(dataset):
    #{project_dir}
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

    sdg_index_19_df.to_csv('test.csv')

    return

def load_sdg_index(year, sheet_name):

    # fetch_index(year) make separate
    fin = sdg_index_file_path(year)
    df = read_workbook(sheet_name, fin)
    df = parse_2019_sdg_index(df)

    return df

if __name__ ==' __main__':
    # 2019 'SDR2019 Data'
    load_sdg_index(sys.argv[1], sys.argv[2])

    # https://sdsna.github.io/2019GlobalIndex/2019GlobalIndexResults.xlsx
    # https://github.com/sdsna/2018GlobalIndex/raw/master/2018GlobalIndexResults.xlsx
    # https://github.com/sdsna/2017GlobalIndex/blob/master/2017GlobalIndexResults.xlsx
