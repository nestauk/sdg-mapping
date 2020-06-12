import json

import logging

from sdg_mapping import project_dir

from sdg_mapping.utils.misc_utils import fetch

logger = logging.getLogger(__name__)

def make_sdg_index_raw():
    '''make_sdg_index_raw
    Download and store SDG Index datasets.
    '''
    with open(f'{project_dir}/data/aux/sdg_index_urls.json', 'r') as f:
        sdg_index_urls = json.load(f)

    for year, url in sdg_index_urls.items():
        logger.info(f'Downloading {year} ')
        fname = f'{year}_sdg_index.xlsx'

        fetch(url, f'{project_dir}/data/raw/{fname}')



if __name__ =='__main__':
    make_sdg_index_raw()
