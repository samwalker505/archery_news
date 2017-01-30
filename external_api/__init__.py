#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.api import urlfetch
import logging
import urllib

class ExternalBase(object):

  def __init__(self, base_url):
    logging.debug('init: {}'.format(base_url))
    self.base_url = base_url

  def post(self, url, payload=None, headers=None):
    url = u'{}/{}'.format(self.base_url, url)
    logging.debug(u'post: {}'.format(url))
    return urlfetch.fetch(
        url=url,
        payload=payload,
        method=urlfetch.POST,
        headers=headers)

  def post_async(self, url, payload=None, headers=None, rpc=None):
    if rpc is None:
      logging.debug('No rpc')
      raise Exception('No rpc')
    url = '{}/{}'.format(self.base_url, url)
    urlfetch.make_fetch_call(rpc, url, payload=payload, headers=headers, method=urlfetch.POST)
    return rpc


  def get(self, url, query=None, headers=None):
    url_params = urllib.urlencode(query)
    url_w_params = u'{}/{}?{}'.format(self.base_url, url, url_params)
    logging.debug(u'get: {}'.format(url_w_params))
    return urlfetch.fetch(
        url=url_w_params,
        method=urlfetch.GET,
        headers=headers)
