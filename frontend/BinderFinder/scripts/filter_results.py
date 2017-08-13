import transaction

import colander
import deform.widget

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError

from ..models import Search, Domain, Sequence
from ..models.search import TempSearch
from ..services.record import SearchRecordService

def retrieve_search(request):
    """
    get search terms using id
    """
    searchid = request.matchdict.get('searchid') # get the unique search id from the URL.
    entry = SearchRecordService.by_id(searchid, request) # retrieve the search using the searchid
    pfams = [int(pf[2:]) for pf in entry.pfams.split(",")] # extract the list of pfams
    return entry.keywords, pfams


def pop_temp_search_table(request, response, searchid):
    # This should work when creating a temporary table:
    #TempSearch.__table__.create(request.dbsession.bind)
    # but it does not and I don't know why : / 
    # Instead I've just executed the text statement. Hacky but it works. 

    request.dbsession.execute(
            'CREATE TEMPORARY TABLE temp_search ('
            'patent_number VARCHAR NOT NULL, '
            'patent_title VARCHAR NOT NULL, '
            'patent_abstract VARCHAR, '
            'CONSTRAINT pk_temp_search PRIMARY KEY (patent_number)'
            ')'
            )
    patents = [TempSearch(**entry) for entry in response.json()['patents']] # build list of objects to add
    request.dbsession.add_all(patents) # add search results to the temp table
    transaction.commit() # commit changes

    print('Number of search results added: '.format(request.dbsession.query(TempSearch).count()))


def query_and_filter_database(request, pfams=list('07686')):
    try:
        query = request.dbsession.query(TempSearch)
        results = query.filter(
            (Domain.emblID == Sequence.emblID)
            & (Domain.pfamID.in_(pfams))
            & (Sequence.patID == TempSearch.patent_number)
            )
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return results

def convert_results_to_display(results):
    data = []
    for res in list(results):
        data.append((res.Search.title,
                     res.Search.patID, res.Search.abstract))
    return data
