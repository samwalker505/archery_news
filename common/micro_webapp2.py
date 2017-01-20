import inspect
import webapp2
import logging
import collections

import common.config as config
class WSGIApplication(webapp2.WSGIApplication):
    def __init__(self, *args, **kwargs):
        super(WSGIApplication, self).__init__(*args, **kwargs)
        self.router.set_dispatcher(self.__class__.custom_dispatcher)

    @staticmethod
    def custom_dispatcher(router, request, response):
        rv = router.default_dispatcher(request, response)
        if isinstance(rv, basestring):
            rv = webapp2.Response(rv)
        elif isinstance(rv, tuple):
            rv = webapp2.Response(*rv)

        return rv

    def route(self, url='/', *args, **kwargs):
        def wrapper(func):
            self.router.add(webapp2.Route(url, handler=func, *args, **kwargs))
            return func
        return wrapper

    def api(self, url='/', api_ver=config.API_VER, format_func=None, *args, **kwargs):
        logging.debug('enter api')
        def wrapper(func):
            base_url = '/api/{}{}'.format(api_ver, url)
            logging.debug(base_url)

            if inspect.isclass(func) and format_func != None:
                for attr in func.__dict__: # there's propably a better way to do this
                    if inspect.ismethod(getattr(func, attr)):
                        setattr(func, attr, format_func(getattr(func, attr))) # bind format to each method

            self.router.add(webapp2.Route(base_url, handler=func, *args, **kwargs))
            return func

        return wrapper




    def routes(self, urls, *args, **kwargs):
        if not isinstance(urls, collections.Iterable):
            raise Exception('urls is not a list')
        def wrapper(func):
            for url in urls:
                self.router.add(webapp2.Route(url, handler=func, *args, **kwargs))
            return func
        return wrapper
