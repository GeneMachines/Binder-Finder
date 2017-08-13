import colander
import deform.widget

import shortuuid # produces unique uuid
from webhelpers2.text import urlify # produces slugs

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from sqlalchemy.exc import DBAPIError

from ..models import Search, Domain, Sequence
from ..models.records import SearchRecord
from ..models.search import TempSearch
from ..forms import SearchCreateForm, SearchUpdateForm
from ..services.record import SearchRecordService

from ..scripts.patentview import search_patentview
from ..scripts.filter_results import *

class ResultsViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def reqts(self):
        return self.results_form.get_widget_resources()

    @property
    def searchid(self):
        searchid = self.request.matchdict['searchid']
        return searchid

    @view_config(route_name='results',
                 renderer='../templates/results.jinja2')
    def view_results(self):
        def convert_results_to_display(results):
            data = []
            for res in list(results):
                data.append((res.Search.title, 
                             'US'+str(res.Search.patID), res.Search.abstract))
            return data
        
        # gets search parameters from webform
        keywords, pfams = retrieve_search(self.request)
        # submits search to patentview
        response = search_patentview(keywords, verbose=True)
        # populates the search table with results
        print ("###########1")
        r = pop_temp_search_table(self.request, response, self.searchid)

        # filter results against domain information
        print ("###########2")
        #results = query_and_filter_database(self.request, pfams=pfams)
        print ("###########3")
        #results = results.all()
        print ("###########4")
        #data = convert_results_to_display(results)
        data = None
        print ("###########5")

        if data:
            page = {'name':'Results', 'creator':'Jake', 'data':data}
        else:
        # TODO change this so it redirects to a standard "no results" page 
            data = [('Jake', 'Parker', 
                     'Is a computational biologist, not a web dev')]
            page = {'name':'Results', 'creator':'Jake', 'data':data}
        
        #print (dir(self.request.dbsession))
        #Search.__table__.drop(self.request.dbsession.engine())

        return dict(page=page)


db_err_msg = """\
Could not find any results matching your criterea. 
"""
