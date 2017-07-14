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

from ..models import Search, SearchRecord, Domain, Sequence
from ..forms import SearchCreateForm, SearchUpdateForm




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
        return shortuuid.uuid() # generate new search id  

    @property
    def keywords(self):
        return 'slug' # replace with keywords from search

    @property
    def slug(self):
        return urlify(self.keywords)

    @view_config(route_name='submit-search', match_param='action=create',
             renderer='BinderFinder:templates/search.jinja2')
    def submit_search(request):
        entry = SearchRecord()
        form = SearchCreateForm(request.POST)
        if request.method == 'POST' and form.validate():
            form.populate_obj(entry)
            return HTTPFound(location=request.route_url('search', searchid=self.searchid))
        return {'form': form, 'action': request.matchdict.get('action')}

    @view_config(route_name='search',
                 renderer='../templates/search.jinja2')
    def search(self):
        keywords = self.keywords
        pfamIDs = 
        response = search_patentview(entry.keywords, verbose=False)
        if response.status_code == requests.codes.ok:
            #request.dbsession.add(response.json())
            #results_url = self.request.route_url('results', slug=self.slug, searchid=self.searchid)
            #return HTTPFound(results_url)
            pass # populate database with results
        else:
            # redirect to a "server not found" page
            print ('error contacting patentwise server')




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

    @view_config(route_name='results', renderer='../templates/results.jinja2')
    def view_results(self):
        def query_and_filter_database(request, pfams=[3,4,5,6]):
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

        results = query_and_filter_database(self.request, pfams=[3,4,5,6]).all()
        data = convert_results_to_display(results)

        page = {'name':'Results', 'creator':'Jake', 'data':data} # some standard results page
        return dict(page=page)


db_err_msg = """\
Could not find any results matching your criterea. 
"""
