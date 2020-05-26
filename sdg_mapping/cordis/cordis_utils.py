import json
import logging
import os
import pandas as pd
import urllib

from sdg_mapping import project_dir
from sdg_mapping.utils.misc_utils import camel_to_snake, fetch

logger = logging.getLogger(__name__)

FRAMEWORK_PROGRAMMES = ['fp1', 'fp2', 'fp3', 'fp4', 'fp5', 'fp6', 'fp7', 'h2020']


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


def parse_cordis_projects(df, list_cols, list_sep, drop_cols):
    '''parse_cordis_projects
    Parse and clearn raw CORDIS data.
    ''' 
    for col in list_cols:
        df[col] = df[col].str.split(list_sep)

    df = df.drop(drop_cols, axis=1)
    df.columns = [camel_to_snake(col) for col in df.columns]
    return df


def load_cordis_projects(fp_name):
    '''load_cordis
    Load a datasets of CORDIS projects.

    Args:
        fp_name (str): Name of Framework Programme
        resource_name (str): Entity type e.g., projects, organizations

    Returns:
        (pd.DataFrame): Parsed CORDIS data
    '''
    resource_name = 'projects'
    fin = cordis_file_path(fp_name, resource_name)
    with open(f'{project_dir}/data/aux/cordis_parse_opts.json', 'r') as f:
        parse_opts = json.load(f)[resource_name]

    with open(f'{project_dir}/data/aux/cordis_read_opts.json', 'r') as f:
        read_opts = json.load(f)[resource_name]
    
    df = pd.read_csv(fin, **read_opts)
    df = parse_cordis_projects(df, **parse_opts)

    if fp_name == 'fp6':
        df = _parse_fp6_projects(df)
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
        dfs.append(load_cordis_projects(fp, resource_name))
    return pd.concat(dfs, axis=1)


def parse_cordis_sdgs(df, prediction_type):
    '''parse_cordis_projects
    Parse and clearn raw CORDIS data.

    Args:
        df (pd.DataFrame): Raw SDG prediction data.
        prediction_type (str): One of label, probability or strict_label

    Returns:
        df (pd.DataFrame): SDG predictions or probabilities with columns as
            integer goal names. Includes the project RCN.
    '''
    if prediction_type == 'label':
        k = [c for c in df.columns if (c[2:] == 'pred') or (c[3:] == 'pred')]
    elif prediction_type == 'probability':
        k = [c for c in df.columns if 'prob' in c]
    elif prediction_type == 'strict_label':
        k = [c for c in df.columns if (c[9:] == 'pred') or (c[10:] == 'pred')]
    df = df.set_index('rcn')[k]
    df.columns = [int(c.split('_')[0]) for c in df.columns]
    df = df.reset_index()
    return df


def load_cordis_project_sdgs(fp_name, prediction_type='label'):
    '''load_cordis_sdgs
    Load a dataset of SDG labels for CORDIS projects.

    Args:
        fp_name (str): Name of Framework Programme
        prediction_type (str): Must be one of:
            - label - SDG labels based on 0.5 probability threshold. 
            - probability - SDG classification probabilities.
            - strict_label - SDG labels based on manually determined 
                probability thresholds. These can be seen in 
                https://github.com/nestauk/sdg-classification

    Returns:
        (pd.DataFrame): Parsed SDG label for CORDIS project dataset
    '''
    allowed = ['label', 'probability', 'strict_label']
    if prediction_type not in allowed:
        raise Exception(f'prediction_type must be one of {(", ").join(allowed)}')

    fin = cordis_file_path(fp_name, 'sdgs') 
    df = pd.read_csv(fin)
    df = parse_cordis_sdgs(df, prediction_type)
    return df

def _parse_fp6_projects(df):
    '''parse_fp6_projects
    Correct an issue where some space characters exist in FP6 funding data.
    '''
    correct_cols = ['ec_max_contribution', 'total_cost']
    for c in correct_cols:
        df[c] = (df[c]
                .str.replace(',', '.')
                .str.replace(' ', '')
                .astype(float))
    return df
