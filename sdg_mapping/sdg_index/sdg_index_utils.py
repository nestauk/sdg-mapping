import numpy as np
import pandas as pd

import sys
import os
import json

from sdg_mapping import project_dir

with open(f'{project_dir}/data/aux/sdg_index_data_opts.json', 'r') as f:
    state_dict = json.load(f)


def sdg_index_file_path(year):
    """sdg_index_file_path
    To fetch filepath of SDG Index datasets.

    Args:
        year (str): Year of SDG Index datasets

    Returns:
        (str): File path

    """
    fname = f'{year}_sdg_index.xlsx'
    return f'{project_dir}/data/raw/{fname}'


def read_workbook(data_path, state):
    """read_workbook
    To read an Excel read_workbook

    Args:
        data_path (str): File path of an SDG Index dataset
        state (str): State of dataset needed; raw or data

    Returns:
        (pd.DataFrame): Parsed SDG Index data

    """
    if state == 'data':
        df = pd.read_excel(open(data_path, 'rb'),
                  sheet_name=state_dict[state],header = 1)

    elif state == 'raw':
        df = pd.read_excel(open(data_path, 'rb'),
                  sheet_name=state_dict[state])
    return df

def parse_2019_sdg_index(dataset, state):
    """parse_2019_sdg_index
    To clean SDG (2019) Index data

    Args:
        dataset (pd.DataFrame): SDG Index dataframe
        state (str): State of dataset needed; raw or data

    Returns:
        (pd.DataFrame): Cleaned SDG Index data

    """
    with open(f'{project_dir}/data/aux/sdg_index_mappings.json', 'r') as f:
        maps = json.load(f)

    trend_map = maps['trend_map']
    achievement_map = maps['achievement_map']

    sdg_index_19_df = dataset.copy()
    trend_columns = [i for i in sdg_index_19_df.columns if 'Trend' in i]
    dashboard_columns = [i for i in sdg_index_19_df.columns if (('Dashboard' in i) and ('Goal' in i))]

    # ignores '.' and replaces with NaN
    for j in trend_columns:
        sdg_index_19_df[j] = sdg_index_19_df[j].map(trend_map)
    for j in dashboard_columns:
        sdg_index_19_df[j] = sdg_index_19_df[j].map(achievement_map)

    return sdg_index_19_df

def load_sdg_index(year, state):
    """load_sdg_index
    To run wrap and run previous function

    Args:
        year (str): Year of SDG Index datasets
        state (str): State of dataset needed; raw or data

    Returns:
        (pd.DataFrame): Cleaned SDG Index data

    """

    fin = sdg_index_file_path(year)
    if (year == 2019 and state == 'data'):

        df = read_workbook(fin, state)
        df = parse_2019_sdg_index(df, state)
        df.columns = [i.lower().replace(" ", "_") for i in df.columns]
        return df

    else:
        df = read_workbook(fin, state)
        df.columns = [i.lower().replace(" ", "_") for i in df.columns]
        return df


if __name__ ==' __main__':

    load_sdg_index(sys.argv[1], sys.argv[2])

    # https://sdsna.github.io/2019GlobalIndex/2019GlobalIndexResults.xlsx
    # https://github.com/sdsna/2018GlobalIndex/raw/master/2018GlobalIndexResults.xlsx
    # https://github.com/sdsna/2017GlobalIndex/blob/master/2017GlobalIndexResults.xlsx
