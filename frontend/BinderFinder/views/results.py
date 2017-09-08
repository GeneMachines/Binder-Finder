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


    @view_config(route_name='no-results',
                 renderer='../templates/no_results.jinja2')
    def view_no_results(self):
        return dict()


    @view_config(route_name='results',
                 renderer='../templates/results.jinja2')
    def view_results(self):
        def convert_results_to_display(results):
            data = []
            if len(results) == 0:
                return None
            for res in results:
                print('#####')
                print(res.patent_title)
                data.append((res.patent_title, 
                             'US'+str(res.patent_number), 
                             res.patent_abstract))
            return data
        
        # gets search parameters from webform
        keywords, pfams = retrieve_search(self.request)
        # submits search to patentview
        response = search_patentview(keywords, verbose=True)
        # populates the search table with results
        r = pop_temp_search_table(self.request, response, self.searchid)

        # filter results against domain information
        results = query_and_filter_database(self.request, pfams=pfams)
        results = results.all()
        data = convert_results_to_display(results)

        if data:
            page = {'name':'Results', 'creator':'Jake', 'data':data}
        else:

        # TODO change this so it redirects to a standard "no results" page 
            data = [('', '', 
                     'There are no results for these search terms. Please try again.')]
            page = {'name':'Results', 'creator':'Jake', 'data':data}
            return HTTPFound(location=self.request.route_url('no-results',
                                                             searchid=self.searchid,
                                                             slug=urlify(keywords))
                        )

        return dict(page=page)


db_err_msg = """\
Could not find any results matching your criterea. 
"""
