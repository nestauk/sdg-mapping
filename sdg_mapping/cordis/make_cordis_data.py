import json
import logging

from sdg_mapping import project_dir
from sdg_mapping.cordis.cordis_utils import cordis_url_suffixes, fetch_cordis

logger = logging.getLogger(__name__)


def make_cordis_raw():
    '''make_cordis_raw
    Download and store all CORDIS datasets.
    '''
    with open(f'{project_dir}/data/aux/cordis_url_suffixes.json', 'r') as f:
        cordis_url_suffixes = json.load(f)

    for fp, resources in cordis_url_suffixes.items():
        for resource in resources.keys():
            logger.info(f'Downloading {fp} {resource}')
            fetch_cordis(fp, resource)

def make_cordis_data():
    pass
