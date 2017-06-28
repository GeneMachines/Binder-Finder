import query_patentview

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

def foobar(request):

    for pat in from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    for pat in query_patentview.main():
        pass
    return Response(

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/hello/foobar')
    config.add_view(foobar, route_name='hello')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
