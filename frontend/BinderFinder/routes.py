def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('search-page', 'search-page')
    config.add_route('search', '/search')
    config.add_route('results', '{searchid}/{slug}')
    config.add_route('no-results', '{searchid}/{slug}/no-results')

