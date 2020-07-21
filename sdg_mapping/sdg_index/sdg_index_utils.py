import numpy as np
import pandas as pd

import sys
import os
import json

from sdg_mapping import project_dir
from sdg_mapping.utils.misc_utils import _decode_json_int

def _load_read_opts():
    """_load_read_opts
    Loads dict of kwargs for `pd.read_excel` when reading SDG Index files.
    """
    with open(f'{project_dir}/data/aux/sdg_index_data_opts.json', 'r') as f:
        index_read_opts = json.load(f, object_hook=_decode_json_int)
    return index_read_opts


def sdg_index_file_path(year):
    """sdg_index_file_path
    Generates file path for SDG Index datasets.

    Args:
        year (str): Year of SDG Index dataset

    Returns:
        (str): File path

    """
    fname = f'{year}_sdg_index.xlsx'
    return f'{project_dir}/data/raw/sdg_index/{fname}'


def read_workbook(data_path, year, index_type):
    """read_workbook
    To read in the Excel workbook- which includes the raw and processed
    Excel spreadsheets that can be used for the SDG index analysis

    Args:
        data_path (str): File path of an SDG Index dataset
        year (int): Year of SDG Index.
        index_type (str): Index of dataset needed; raw or report
    Returns:
        (pd.DataFrame): Parsed SDG Index data
    """
    read_opts = _load_read_opts()[year][index_type]
    df = pd.read_excel(data_path, **read_opts)
    return df


def _map_dashboard_symbols(df):
    """_map_dashboard_symbols
    Map progress symbols and colours from SDG Index dashboard to human readable strings.

    Args:
        dataset (pd.DataFrame): SDG Index dataframe

    Returns:
        (pd.DataFrame): Cleaned SDG Index data
    """

    with open(f'{project_dir}/data/aux/sdg_index_mappings.json', 'r') as f:
        maps = json.load(f)

    trend_map = maps['trend_map']
    achievement_map = maps['achievement_map']

    trend_columns = [i for i in df.columns if 'Trend' in i]
    dashboard_columns = [i for i in df.columns if (('Dash' in i) and ('Goal' in i))]

    for col in trend_columns:
        df[col] = df[col].map(trend_map)
    for col in dashboard_columns:
        df[col] = df[col].map(achievement_map)

    return df


def _parse_raw(df, year):
    """_parse_raw
    Currently returns raw data as is.
    """
    return df


def _parse_report(df, year):
    """_parse_report
    Parse data and map values for the SDG Index report worksbook sheet.

    Args:
        df (pd.DataFrame): Raw SDG Index report table.
        year (int): Year of the index. 

    Returns:
        df (pd.DataFrame): Clean data.
    """
    df = _map_dashboard_symbols(df)
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    if year == 2017:
        old = "average_score_on_sdg"
        new = "goal_"
        df.columns = [c.replace(old, new) + "_score" for c in df.columns]
    if year == 2020:
        df.columns = [c.replace(":", "") for c in df.columns]
    df = df[[c for c in df.columns if 'unnamed' not in c]]
    return df


def _parse_codebook(df, year):
    """_parse_codebook
    Parse codebook data for SDG Index workbook sheet.

    Args:
        df (pd.DataFrame): Raw data from codebook sheet.
        year (int): Year of the index.

    Returns:
        df (pd.DataFrame): Clean codebook.
    """
    df.columns = [c.replace('(= ', '(=') for c in df.columns]
    if year == 2019:
        df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    elif year == 2020:
        df.columns = [c.lower() for c in df.columns]
    return df



def load_sdg_index(year, index_type):
    """load_sdg_index
    A function to complete the start to end process of cleaning the
    dataset

    Args:
        year (str): Year of SDG Index datasets
        index_type (str): Index of dataset needed; options are raw, report or 
            codebook.

    Returns:
        (pd.DataFrame): Cleaned SDG Index data

    """

    if year < 2016:
        raise Exception('SDG Index Reports are only available from 2016 onwards' )

    if (index_type in ['raw', 'codebook']) and (year < 2019):
        raise Exception(f'{index_type.title()} data only available from 2019 onwards.')

    fin = sdg_index_file_path(year)
    df = read_workbook(fin, year, index_type)

    if index_type == 'report':
        df = _parse_report(df, year)
    elif index_type == 'raw':
        df = _parse_raw(df)
    if index_type == 'codebook':
        df = _parse_codebook(df, year)
    df = df.rename(columns={'id': 'iso_3_code'})
    return df

