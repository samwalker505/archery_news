#!/usr/bin/python
# -*- coding: utf-8 -*-
import webapp2
import logging
from handlers import BaseHandler, Output

class TestHandler(BaseHandler):

    @Output.json
    def get(self, *args, **kwargs):
        pass

app = webapp2.WSGIApplication([
    (r'/api/v1/test', TestHandler),
])
