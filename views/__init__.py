import os
import urllib
import jinja2

import webapp2
import re
import logging
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
def camelcase_to_underscore(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()

class BaseView(webapp2.RequestHandler):

    def __init__(self, request, response):
        logging.debug('entered handlers')
        self.template = ''
        self.values = {}
        self.initialize(request, response)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def render(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        self.render(*args, **kwargs)
        template = JINJA_ENVIRONMENT.get_template(self.template if self.template else '{}.html'.format(camelcase_to_underscore(self.__class__.__name__)))
        self.response.write(template.render(self.values if self.values else {}))
