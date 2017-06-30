import requests

def build_query_string(query_string, num_results='10000'):
    """
    This function takes a search string and other search parameters as input and returns
    the query url for the patent view REST API.
    """

    domain = 'http://www.patentsview.org/api/patents/'
    query = 'query?q={"_text_any":{"patent_abstract":"%s"}}' % (query_string)
    options = '&o={"page":1,"per_page":%s}' % (num_results)
    form = '&f=["patent_number","patent_abstract","patent_title"]'

    return (domain + query + options + form)


def query_patentview(query_string, url, verbose=False):
    """
    Takes a query url and returns a list of patent results.
    """
    
    response = requests.get(url) # query patent view

    # number of hits
    if verbose:
        print ("Number of hits for '{}': ".format(query_string), response.json()['count'])

    return response


def search_patentview(query_string, verbose=False):
    """
    The main function of the search script. Takes a query string and returns a search response.
    """

    url = build_query_string(query_string)
    response = query_patentview(query_string, url, verbose)
    
    return response


if __name__ == "__main__":
    query_string = "tnf"
    response = search_patentview(query_string, True)
