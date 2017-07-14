def includeme(config):
    config.add_route('home', '/')
    config.add_route('search', 'search')
    config.add_route('submit', 'submit')
    config.add_route('results', '{slug}/{searchid}')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static/')
