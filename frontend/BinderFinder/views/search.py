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

from ..models.records import SearchRecord
from ..forms import SearchCreateForm

class HomeViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def reqts(self):
        return self.search_form.get_widget_resources()

    @view_config(route_name='home', renderer='../templates/view.jinja2')
    def view_home(self):
        page = {'name':'Home', 'creator':'Jake', 'data':'this is the front page'\
}
        return dict(page=page)


class SearchViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def reqts(self):
        return self.search_form.get_widget_resources()

    @property
    def searchid(self):
        return shortuuid.uuid()[:10] # generate new search id

    @view_config(route_name='search-page', renderer='string')
    def search(self):
       return HTTPFound(location=self.request.route_url('search-submit',
                                                         searchid=self.searchid)
                        )

    @view_config(route_name='search',
                 renderer='../templates/submit.jinja2')
    def search_action(self):
        """
        This function creates a search id, record, and redirects to the results page.
        """
        # create search record
        entry = SearchRecord()
        form = SearchCreateForm(self.request.POST)
        if self.request.method == 'POST' and form.validate():
            # create unique search id
            uuid = self.searchid
            # extract keyword arguments from the web form
            keywords = form.data['keywords']
            entry.id = uuid
            entry.keywords = keywords
            # extract the pfams from the web form
            if form.data['pfams']:
                entry.pfams = form.data['pfams']
            else:
                entry.pfams = 'PF07686' # default pfam is the v-set
            self.request.dbsession.add(entry) # populate the database entry
            return HTTPFound(location=self.request.route_url('results',
                                                             slug=urlify(keywords), 
                                                             searchid=uuid))
        return dict()
