#!/usr/bin/python
# -*- coding: utf-8 -*-
import webapp2
import logging
import json

from common.json_encoder import JSONEncoder
import common.config as config
class Output(object):
    @staticmethod
    def json(func):
        def func_wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.response.headers['Content-Type'] = 'application/json'
            if isinstance(result, dict):
                content = json.dumps(result, cls=JSONEncoder)
                self.response.set_status(200)
                self.response.write(content)
            else:
                logging.error('result is not dict')
                self.response.set_status(400)
                self.response.write(json.dumps({'error': 'check log la'}, cls=JSONEncoder))
        return func_wrapper



class BaseHandler(webapp2.RequestHandler):

    def __init__(self, request, response):
        self.json_body = {}
        self.initialize(request, response)

    def query(self, kls, per_page=1000, filters=[]):
        from google.appengine.datastore.datastore_query import Cursor
        cursor = Cursor.from_websafe_string(str(self.request.get('cursor')))
        query = kls.query()
        if filters:
            logging.debug('filters: {}'.format(filters))
            for f in filters:
                query.filter(f)

        results, next_cursor, more = query.fetch_page(per_page, start_cursor=cursor)
        result = {
            'cursor': next_cursor,
            'results': [result.to_dict() for result in results],
            'count': query.count(),
            'more': more
        }

        return result

    def handle_exception(self, exception, debug):
        # Log the error.
        logging.exception(exception)
        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        self.response.headers['Content-Type'] = 'application/json'
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)
        # Set a custom message.
        self.response.write(json.dumps({'error': exception.message}, cls=JSONEncoder))

    def dispatch(self):
        content_type = self.request.headers.get('Content-Type')
        if content_type and content_type.split(';')[0] == 'application/json':
            logging.debug('Content-Type: json')
            self.json_body = json.loads(self.request.body)
        # don't indent it ....

        super(BaseHandler, self).dispatch()

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
