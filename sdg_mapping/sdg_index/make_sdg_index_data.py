import numpy as np
import pandas as pd

import logging
import sys
import os
import urllib

from sdg_mapping import project_dir

from sdg_mapping.utils.misc_utils import fetch_sdg_index

logger = logging.getLogger(__name__)

def make_sdg_index_raw():
    '''make_sdg_index_raw
    Download and store SDG Index datasets.
    '''
    with open(f'{project_dir}/data/aux/sdg_index_url_suffixes.json', 'r') as f:
        sdg_index_url_suffixes = json.load(f)

    for year, url in cordis_url_suffixes.items():
        logger.info(f'Downloading {yaer} ')
        fname = f'{year}_sdg_index.xlsx'
        urllib.request.urlretrieve(url, f'{project_dir}/data/raw/{fname}')



if __name__ ==' __main__':
    make_sdg_index_raw()

    # https://sdsna.github.io/2019GlobalIndex/2019GlobalIndexResults.xlsx
    # https://github.com/sdsna/2018GlobalIndex/raw/master/2018GlobalIndexResults.xlsx
    # https://github.com/sdsna/2017GlobalIndex/blob/master/2017GlobalIndexResults.xlsx