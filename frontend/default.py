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
from ..forms import SearchCreateForm, SearchUpdateForm
from ..services.record import SearchRecordService

from ..scripts.patentview import search_patentview

class HomeViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def reqts(self):
        return self.search_form.get_widget_resources()

    @view_config(route_name='home', renderer='../templates/view.jinja2')
    def view_home(self):
        page = {'name':'Home', 'creator':'Jake', 'data':'this is the front page'}
        return dict(page=page)    


class SearchViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def reqts(self):
        return self.search_form.get_widget_resources()

    @property
    def searchid(self):
        return shortuuid.uuid()[:10] # generate new search 

    @view_config(route_name='search-page', renderer='string')
    def search(self):
       return HTTPFound(location=self.request.route_url('search-submit',
                                                         searchid=self.searchid))

    @view_config(route_name='search',
                 renderer='../templates/submit.jinja2')    
    def search_action(self):
        entry = SearchRecord()
        form = SearchCreateForm(self.request.POST)
        if self.request.method == 'POST' and form.validate():
            uuid = self.searchid
            keywords = form.data['keywords']
            entry.id = uuid
            entry.keywords = keywords
            entry.pfams = form.data['pfams']
            self.request.dbsession.add(entry)
            return HTTPFound(location=self.request.route_url('results',
                                                             slug=urlify(keywords), searchid=uuid))
        return dict()


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
        def retrieve_search(request):
        # get search terms using id
            searchid = self.request.matchdict.get('searchid')
            entry = SearchRecordService.by_id(searchid, request)
            pfams = entry.pfams.split(",")
            return entry.keywords, pfams

        def query_and_filter_database(request, pfams=['PF07686',]):
            try:
                query = request.dbsession.query(Search, Sequence.seq)
                results = query.filter(
                    (Domain.emblID == Sequence.emblID)
                    #& (Domain.pfamID.in_(pfams))
                    #& (Sequence.patID == Search.patID)
                    )
            except DBAPIError:
                return Response(db_err_msg, content_type='text/plain', status=500)
            return results

        def convert_results_to_display(results):
            data = []
            for res in list(results):
                data.append((res.Search.title, 
                             'US'+res.Search.patID, res.Search.abstract))
            return data
            
        keywords, pfams = retrieve_search(self.request)
        response = search_patentview(keywords, verbose=True)
        populate_search_table(request, response)
        results = query_and_filter_database(self.request, pfams=pfams)

#        print ("######")
#        print (results.all())

        data = convert_results_to_display(results)
        if data:
            page = {'name':'Results', 'creator':'Jake', 'data':data}
        else:
            data = [('Jake', 'Parker', 
                     'Is a computational biologist, not a web dev')]
            page = {'name':'Results', 'creator':'Jake', 'data':data}
        return dict(page=page)


db_err_msg = """\
Could not find any results matching your criterea. 
"""
