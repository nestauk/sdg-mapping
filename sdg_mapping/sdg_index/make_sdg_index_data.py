import numpy as np
import pandas as pd
import json

import logging
import sys
import os
# import urllib

from sdg_mapping import project_dir

from sdg_mapping.utils.misc_utils import fetch

logger = logging.getLogger(__name__)

def make_sdg_index_raw():
    '''make_sdg_index_raw
    Download and store SDG Index datasets.
    '''
    with open(f'{project_dir}/data/aux/sdg_index_url_suffixes.json', 'r') as f:
        sdg_index_url_suffixes = json.load(f)
        print(sdg_index_url_suffixes)

    for year, url in sdg_index_url_suffixes.items():
        sys.stdout.write(year)
        sys.stdout.write(url)
        logger.info(f'Downloading {year} ')
        fname = f'{year}_sdg_index.xlsx'

        fetch(url, f'{project_dir}/data/raw/{fname}')



if __name__ =='__main__':
    make_sdg_index_raw()

    # https://sdsna.github.io/2019GlobalIndex/2019GlobalIndexResults.xlsx
    # https://github.com/sdsna/2018GlobalIndex/raw/master/2018GlobalIndexResults.xlsx
    # https://github.com/sdsna/2017GlobalIndex/blob/master/2017GlobalIndexResults.xlsx
