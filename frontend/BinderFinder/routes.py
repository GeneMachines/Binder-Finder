def includeme(config):
    config.add_route('home', '/')
    config.add_route('submit-search', 'submit-search')
    config.add_route('search', 'search')
    config.add_route('results', '{slug}/{searchid}')
    config.add_static_view('static', 'static', cache_max_age=3600)

