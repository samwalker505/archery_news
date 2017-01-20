#!/usr/bin/python
# -*- coding: utf-8 -*-
from google.appengine.api import urlfetch
import webapp2
import logging
from lxml import etree
from handlers import BaseHandler, Output

class ArcheryOrgHkSpiderHandler(BaseHandler):

    @Output.json
    def get(self, *args, **kwargs):
        result = urlfetch.fetch('http://www.archery.org.hk')
        page = etree.HTML(result.content)
        results = []
        for row in page.xpath('//div[contains(@class, "views-row")]'):
            title = row.xpath('descendant::h2/a/text()')[0]
            url = row.xpath('descendant::h2/a/@href')[0]
            logging.debug(url)
            result = {
                'title': title,
                'url': url
            }
            results.append(result)

        return {'results': results}

app = webapp2.WSGIApplication([
    (r'/api/v1/archery_org_hk_spider', ArcheryOrgHkSpiderHandler),
])
