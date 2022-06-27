import json
import requests

# Add your Microsoft Account Key to a file called bing.key
def read_bing_key():
    """
    reads the BING API key from a file called 'bing.key'
    remember to put bing.key in your .gitignore file to avoid committing it
    :return: a string which is either NONE, i.e. no key found, or with a key

     See Python Anti-Patterns - it is an awesome resource to improve your python code
     Here ware using "with" when opening documents
     http://bit.ly/twd-antipattern-open-files
    """

    bing_api_key = None
    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline().strip()

    except:
        try:
            with open('../bing.key', 'r') as f:
                bing_api_key = f.readline().strip()

        except:
            raise IOError('bing.key file not found')

    if not bing_api_key:
        raise KeyError('Bing key not found')

    return bing_api_key

def run_query(search_terms):
    """
    See Microsoft's documentation on other parameters that you can set.
    http://bit.ly/twd-bing-api

    :param search_terms:
    :return:
    """

    bing_key = read_bing_key()
    search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
    headers = {'Ocp-Apim-Subscription-Key': bing_key}
    params = {'q': search_terms, 'textDecorations': True, 'textFormat': 'HTML'}

    # Issue the request, given the details above
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # With the response now in play, build up a Python list
    results = []
    for result in search_results['webPages']['value']:
        results.append({
            'title': result['name'],
            'link': result['url'],
            'summary': result['snippet']})
    return results