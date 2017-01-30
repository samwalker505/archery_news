#!/usr/bin/python
# -*- coding: utf-8 -*-
import webapp2
import logging
from handlers import BaseHandler, Output
from external_api.facebook import Facebook as FacebookApi
class TestHandler(BaseHandler):
    @Output.json
    def get(self, *args, **kwargs):
        logging.debug('entered')
        client = FacebookApi()
        result = client.create_post('hihihi')
        logging.debug(result)
        logging.debug(result.content)
        logging.debug(result.status_code)
        return {'result': result.content}

app = webapp2.WSGIApplication([
    (r'/api/v1/test', TestHandler),
])
