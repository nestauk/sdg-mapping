import re
from urllib.request import urlretrieve

def camel_to_snake(name):
    '''Convert lowerCamelCase or upperCamelCase to snake_case
    Args:
        name (str): lowerCamelCase or upperCamelCase word.
    Returns:
        _name (str): snake_case word.
    '''
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def fetch(url, fout):
    '''fetch
    Fetches a file from the web and saves to a location on disk.
    '''
    urlretrieve(url, fout)

def _decode_json_int(o):
    """_decode_json_int
    Loads integers in a json as int. Pass in as parameter `object_hook` for
    `json.load`.
    """
    if isinstance(o, str):
        try:
            return int(o)
        except ValueError:
            return o
    elif isinstance(o, dict):
        return {_decode_json_int(k): _decode_json_int(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [_decode_json_int(v) for v in o]
    else:
        return o
