import numpy as np
import pandas as pd

import sys
import os
import json

from sdg_mapping import project_dir

with open(f'{project_dir}/data/aux/sdg_index_data_opts.json', 'r') as f:
    state_dict = json.load(f)
    for i in state_dict.keys():
        state_dict[i]["header"] = int(state_dict[i]["header"])

def sdg_index_file_path(year):
    """sdg_index_file_path
    Generates file path for SDG Index datasets.

    Args:
        year (str): Year of SDG Index datasets

    Returns:
        (str): File path

    """
    fname = f'{year}_sdg_index.xlsx'
    return f'{project_dir}/data/raw/{fname}'


def read_workbook(data_path, state):
    """read_workbook
    To read in the Excel workbook- which includes the raw and processed
    Excel spreadsheets that can be used for the SDG index analysis

    Args:
        data_path (str): File path of an SDG Index dataset
        state (str): State of dataset needed; raw or data
    Returns:
        (pd.DataFrame): Parsed SDG Index data
    """
    read_opts = state_dict[state]
    df = pd.read_excel(data_path, na_values='.', **read_opts)
    return df

def parse_2019_sdg_indicator(dataset):
    """parse_2019_sdg_index
    To clean SDG (2019) Index data

    Args:
        dataset (pd.DataFrame): SDG Index dataframe

    Returns:
        (pd.DataFrame): Cleaned SDG Index data
    """

    with open(f'{project_dir}/data/aux/sdg_index_mappings.json', 'r') as f:
        maps = json.load(f)

    trend_map = maps['trend_map']
    achievement_map = maps['achievement_map']

    sdg_index_19_df = dataset
    trend_columns = [i for i in sdg_index_19_df.columns if 'Trend' in i]
    dashboard_columns = [i for i in sdg_index_19_df.columns if (('Dashboard' in i) and ('Goal' in i))]

    for j in trend_columns:
        sdg_index_19_df[j] = sdg_index_19_df[j].map(trend_map)
    for j in dashboard_columns:
        sdg_index_19_df[j] = sdg_index_19_df[j].map(achievement_map)

    return sdg_index_19_df

def load_sdg_index(year, state):
    """load_sdg_index
    A function to complete the start to end process of cleaning the
    dataset

    Args:
        year (str): Year of SDG Index datasets
        state (str): State of dataset needed; raw or data

    Returns:
        (pd.DataFrame): Cleaned SDG Index data

    """

    fin = sdg_index_file_path(year)

    df = read_workbook(fin,state)
    if (year == 2019) and (state == 'data'):
        df = parse_2019_sdg_indicator(df)
    df.columns = [i.lower().replace(" ", "_") for i in df.columns]

    return df
