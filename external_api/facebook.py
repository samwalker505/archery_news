#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.api import urlfetch
import logging
import urllib

from keys import FacebookAccessToken
from . import ExternalBase

class Facebook(ExternalBase):

    def __init__(self):
        version = '2.8'
        base_url = 'https://graph.facebook.com/v{}'.format(version)
        super(Facebook, self).__init__(base_url)
        self.access_token = FacebookAccessToken.PRO
        self.post_id = '378001692556714'


    def post(self, url, payload=None):
        url = u'{}/{}'.format(self.base_url, url)
        logging.debug(u'post: {}'.format(url))
        headers = {'Authorization': 'OAuth {}'.format(self.access_token)}
        logging.debug(headers)
        return urlfetch.fetch(
            url=url,
            payload=payload,
            method=urlfetch.POST,
            headers=headers)

    def create_post(self, content, link=None):
        if link:
            endpoint = u'{}/feed?message={}&link={}'.format(self.post_id, content, link)
        else:
            endpoint = u'{}/feed?message={}'.format(self.post_id, content)
        endpoint.encode('utf-8')

        return self.post(endpoint)
