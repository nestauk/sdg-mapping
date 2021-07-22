import os
from collections import defaultdict
from datetime import datetime
import pandas as pd

from sdg_mapping import project_dir


ANNOTATED_DIR = f'{project_dir}/data/raw/annotated/'


def extract_date(filename):
    date = ' '.join(file.replace('.csv', '').split('_')[-3:])
    dt = pd.to_datetime(date)
    return dt


def collate_annotated():
    to_keep = defaultdict(list)
    for sdg_dir in os.listdir(ANNOTATED_DIR):
        if sdg_dir == '.DS_Store':
            continue

        sdg = sdg_dir.split('/')[-1]
        sdg = int(sdg.split('_')[-1])
        file_cache = defaultdict(list)
        sdg_dir = os.path.join(ANNOTATED_DIR, sdg_dir)

        for file in os.listdir(sdg_dir):
            file_date = extract_date(file)
            file_project = file.split('_')[1]
            file_cache[file_project].append(file_date)

        for proj, date in file_cache.items():
            dt = sorted(date)[-1]
            dt = datetime.strftime(dt, format="%a_%b_%d_%Y")
            fname = f'project_{proj}_labels_{dt}.csv'
            to_keep[sdg].append(fname)
            
    sdg_dfs = {}

    for sdg, fnames in to_keep.items():
        sdg = f'sdg_{str(sdg).zfill(2)}'
        labelled_datasets = []
        for fname in fnames:
            
            fname = os.path.join(ANNOTATED_DIR, sdg, fname)
            labelled_datasets.append(pd.read_csv(fname))
        labelled_dataset = pd.concat(labelled_datasets)
        labelled_dataset.drop_duplicates(subset='ID')
        labelled_dataset.to_csv(
            os.path.join(ANNOTATED_DIR, 'collated', sdg, index=False))
        sdg_dfs[sdg] = labelled_dataset
    
    return sdg_dfs


def import_collated(sdg):
    sdg = str(sdg).zfill(2)
    sdg_df = pd.read_csv(
        os.path.join(ANNOTATED_DIR, 'collated', f'sdg_{sdg}.csv')
                        )
    sdg_df['title'], sdg_df['abstract'] = zip(*sdg_df['Text'].apply(clean_annotated_text))
    sdg_df = sdg_df.drop('Text', axis=1)
    return sdg_df

            
def clean_annotated_text(text):
    text = text.split('=====')
    title = text[1].strip()
    abstract = text[-1].strip()
    return title, abstract