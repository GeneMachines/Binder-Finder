from pyramid.config import Configurator
from waitress import serve

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    wsgiapp = config.make_wsgi_app()
    return serve(wsgiapp, listen='localhost:5000', url_scheme='https')
