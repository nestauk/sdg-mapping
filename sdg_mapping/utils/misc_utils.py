import re
import urllib

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
    urllib.request.urlretrieve(url, fout)
