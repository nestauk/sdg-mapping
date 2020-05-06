import json
import logging
import os
import pandas as pd
import urllib

from sdg_mapping import project_dir
from sdg_mapping.utils.misc_utils import camel_to_snake, fetch

logger = logging.getLogger(__name__)


def cordis_file_path(fp_name, resource_name):
    '''cordis_file_path
    Create the file path for a CORDIS dataset given a Framework Programme and 
    an entity such as projects or organizations.

    Args:
        fp_name (str): Name of Framework Programme
        resource_name (str): Entity type e.g., projects, organizations

    Returns:
        (str): File path 
    '''
    fname = f'{fp_name}_{resource_name}.csv'
    return f'{project_dir}/data/raw/cordis/{fp_name}/{fname}'


def fetch_cordis(fp_name, resource_name, fout=None):
    '''fetch_cordis
    Download raw CORDIS dataset given a Framework Programme and an entity such 
    as projects or organizations.

    Args:
        fp_name (str): Name of Framework Programme
        resource_name (str): Entity type e.g., projects, organizations
    '''
    base_url = 'https://cordis.europa.eu/data/{}'

    with open(f'{project_dir}/data/aux/cordis_url_suffixes.json', 'r') as f:
        cordis_url_suffixes = json.load(f)
    url = base_url.format(cordis_url_suffixes[fp_name][resource_name])
    if fout is None:
        fout = cordis_file_path(fp_name, resource_name)

    if not os.path.isdir(os.path.dirname(fout)):
        os.makedirs(os.path.dirname(fout))
    fetch(url, fout)


def parse_cordis(df, list_cols, list_sep, drop_cols):
    '''parse_cordis
    Parse and clearn raw CORDIS data.
    ''' 
    for col in list_cols:
        df[col] = df[col].str.split(list_sep)

    df = df.drop(drop_cols, axis=1)
    df.columns = [camel_to_snake(col) for col in df.columns]
    return df


def load_cordis(fp_name=None, resource_name=None):
    '''load_cordis
    Load a CORDIS dataset for a particular Framework Programme and entity 
    such as projects or organizations.

    Args:
        fp_name (str): Name of Framework Programme
        resource_name (str): Entity type e.g., projects, organizations

    Returns:
        (pd.DataFrame): Parsed CORDIS data
    '''
    fin = cordis_file_path(fp_name, resource_name)
    parse_opts = [fp_name]
    with open(f'{project_dir}/data/aux/cordis_parse_opts.json', 'r') as f:
        parse_opts = json.load(f)[resource_name]

    with open(f'{project_dir}/data/aux/cordis_read_opts.json', 'r') as f:
        read_opts = json.load(f)[resource_name]
    
    df = pd.read_csv(fin, **read_opts)
    df = parse_cordis(df, **parse_opts)
    return df


def load_all_cordis_projects(resource_name):
    '''load_all_cordis_projects
    Loads projects for all CORDIS Framework Programmes as a single DataFrame.

    Args:
        resource_name (str): Entity type e.g., projects, organizations

    Returns:
        (pd.DataFrame): Parsed CORDIS projects for all Framework Programmes
    '''
    fps = ['h2020', 'fp7', 'fp6', 'fp5', 'fp4', 'fp3', 'fp2', 'fp1']
    dfs = []
    for fp in fps:
        dfs.append(load_cordis(fp, resource_name))
    return pd.concat(dfs, axis=1)

