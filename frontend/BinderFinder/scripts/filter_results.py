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
    searchid = request.matchdict.get('searchid')
    entry = SearchRecordService.by_id(searchid, request)
    pfams = entry.pfams.split(",")
    return entry.keywords, pfams

def populate_search_table(request, response, searchid):
    for patent in response.json()['patents']:
        entry = Search()
        entry.patID = patent['patent_number']
        entry.title = patent['patent_title']
        entry.abstract = patent['patent_abstract']
        entry.creator = searchid
        request.dbsession.add(entry)

def pop_temp_search_table(request, response, searchid):
    engine = sa.create_engine('sqlite:///test.sqlite')
    TempSearch.__table__.create(engine)
    for patent in response.json()['patents']:
        entry = TempSearch()
        entry.patID = patent['patent_number']
        entry.title = patent['patent_title']
        entry.abstract = patent['patent_abstract']
        entry.creator = searchid
        request.dbsession.add(entry)

def query_and_filter_database(request, pfams=['PF07686',]):
    try:
        query = request.dbsession.query(Search, Sequence.seq)
        results = query.filter(
            (Domain.emblID == Sequence.emblID)
            & (Domain.pfamID.in_(pfams))
            & (Sequence.patID == Search.patID)
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
