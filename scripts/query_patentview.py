#!/usr/bin/python

import requests
#import urllib
#import time
#import json
from pprint import pprint

def build_query_string(query_string, num_results='10000'):
    """
    This function takes a search string and other search parameters as input and returns
    the query url for the patent view REST API.
    """

    domain = 'http://www.patentsview.org/api/patents/'
    query = 'query?q={"_text_any":{"patent_abstract":"%s"}}' % (query_string)
    options = '&o={"page":1,"per_page":%s}' % (num_results)
    form = '&f=["patent_number","patent_date","patent_title"]'

    return (domain + query + options + form)


def query_patentview(query_string, url, verbose=False):
    """
    Takes a query url and returns a list of patent results.
    """

    # query patent view
    response = requests.get(url)

    # number of hits
    if verbose:
        print ("Number of hits for '{}': ".format(query_string), response.json()['count'])

    patent_ids = {}
    for i, entry in enumerate(response.json()["patents"]):
        if verbose and i < 5:
            pprint(entry)
        patent_ids[entry["patent_number"]] = entry

    return patent_ids


def format_results(search_results):
    """
    Takes the results of the patentview query and formats them for comparison with the domain
    information.
    """
    pass


def main():
    query_string = "tnf"
    url = build_query_string(query_string)
    search_patents = query_patentview(query_string, url, verbose=False)
    
    return search_patents


if __name__ == "__main__":
    main()
