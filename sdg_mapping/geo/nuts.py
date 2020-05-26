import geopandas as gpd
import logging
import numpy as np
import os
import pandas as pd
from zipfile import ZipFile

from sdg_mapping import project_dir

logger = logging.getLogger(__name__)


def load_nuts_regions(year, shapefile_dir, level=2, projection=4326, resolution=1, countries=['UK']):
    '''load_nuts_regions
    Loads NUTS shapefiles.

    Args:
        year (int): NUTS version year.
        shapefile_dir (str): Directory where shapefiles are stored. 
        projection (int): Coordinate projection of shapefile. 
            Choice of EPSG 3035, 3857 or 4326. Default is 4326
        resolution (int): Shapefile resolution in metres.
        countries (list): List of 2 letter country codes to filter by. If None, 
            all regions will be returned. Default is `["UK"]`.
    '''
    
    resolution = str(resolution).zfill(2)

    nuts_dir = (f'{shapefile_dir}/'
                f'ref-nuts-{year}-{resolution}m.shp/'
                f'NUTS_RG_{resolution}M_{year}_{projection}_LEVL_{level}.shp')
    
    if not os.path.isdir(nuts_dir):
        with ZipFile(f'{nuts_dir}.zip','r') as archive:
            archive.extractall(nuts_dir)
        
    nuts_fin = (f'{nuts_dir}/'
                f'NUTS_RG_{resolution}M_{year}_{projection}_LEVL_{level}.shp')
    nuts_gdf = gpd.read_file(nuts_fin)
    
    if countries is not None:
        nuts_gdf = nuts_gdf.set_index('CNTR_CODE').loc[countries].reset_index()
        
    return nuts_gdf


