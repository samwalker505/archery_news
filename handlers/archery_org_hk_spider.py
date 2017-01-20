#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import md5
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
            tag = row.xpath('descendant::div[@class="terms"]//text()')[0]
            contentRaw = row.xpath('descendant::div[contains(@class, "content")]//text()')
            content = u''.join(contentRaw) if contentRaw else u''
            content = re.sub(r' +', u' ', content)
            content = re.sub(r'\n+', u'\n', content)
            content = content.strip()
            content = content.encode('utf-8')
            result = {
                'title': title,
                'url': url,
                'tag': tag,
                'content': content,
                'content_hash': md5.new(content).hexdigest(),
                'url_hash':md5.new(url).hexdigest(),
            }
            results.append(result)

        return {'results': results}

app = webapp2.WSGIApplication([
    (r'/api/v1/archery_org_hk_spider', ArcheryOrgHkSpiderHandler),
])
