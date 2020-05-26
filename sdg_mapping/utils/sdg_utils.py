import json
import re

from sdg_mapping import project_dir


def sdg_names():
    '''sdg_names
    Returns a dictionary with integer keys 1 - 17 and values of full SDG names.
    '''
    path = "data/aux/sdg_names.json"
    return _sdg_property(path)


def sdg_hex_color_codes():
    '''sdg_hex_color_codes
    Returns a dictionary with integer keys 1 - 17 and the official hex color 
    codes for each SDG.
    '''
    path = "data/aux/sdg_hex_color_codes.json"
    return _sdg_property(path)


def _sdg_property(path):
    '''_sdg_property
    Reads and returns a json with property values for SDGs 1 - 17.
    '''
    with open(project_dir / path, "rt") as f:
       property  = json.load(f)
    return {int(k): v for k, v in property.items()}

# def num_to_sdg(num):
# 
#     def get_num(s):
#         return int(re.findall(r'\d+', s)[0])
# 
#     names = sdg_names()
#     if isinstance(num, str):
#         return names[get_num(num)]
#     else:
#         return [names[get_num(n)] for n in num]

