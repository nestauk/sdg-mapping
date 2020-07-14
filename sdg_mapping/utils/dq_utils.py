import numpy as np
import pandas as pd

def missing_values(data,col = True):
    """missing_values
    Calculates the number of missing values (across rows or columns)
    Args:
        data (:obj:`iter` of :obj:`obj`): A sequence of objects.
        col (str): Boolean.
    Returns:
        missing_count_df (:obj:`pandas.DataFrame`): A series with column names and missing value frequency (columns)
    """
    df = pd.DataFrame(data)
    if col == True:
        missing_count_df = df.isnull().sum().sort_values(ascending=False)
    if col == False:
        missing_count_df = df.isnull().sum(axis=1).sort_values(ascending=False)


    missing_count_df = pd.DataFrame(missing_count_df)
    missing_count_df.columns = ['frequency']
    missing_count_df.index.name = 'field'
    missing_count_df = missing_count_df.reset_index()
    return missing_count_df
