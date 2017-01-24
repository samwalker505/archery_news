#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import md5
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2
import logging
from lxml import etree
from handlers import BaseHandler, Output
from models.post import ArcheryOrgHkPost

class ArcheryOrgHkSpiderHandler(BaseHandler):

    @Output.json(response_type='array')
    def get(self, *args, **kwargs):
        results = []
        def handle_result(rpc):
            result = rpc.get_result()
            # self.response.write(result.content)
            logging.info('Handling RPC in callback: result {}'.format(result))
            page = etree.HTML(result.content)

            for row in page.xpath('//div[contains(@class, "views-row")]'):
                title = row.xpath('descendant::h2/a/text()')[0]
                url = row.xpath('descendant::h2/a/@href')[0]
                tags = row.xpath('descendant::div[@class="terms"]//text()')
                tags = [tag for tag in tags if tag != '\n']
                contentRaw = row.xpath('descendant::div[contains(@class, "content")]//text()')
                content = u''.join(contentRaw) if contentRaw else u''
                content = re.sub(r' +', u' ', content)
                content = re.sub(r'(\n ?)+', u'\n', content)
                content = content.strip()
                content = content.encode('utf-8')
                result = {
                    'title': title,
                    'url': url,
                    'tags': tags,
                    'content': content,
                    'content_hash': md5.new(content).hexdigest(),
                    'url_hash':md5.new(url).hexdigest(),
                }
                results.append(result)


        urls = ['https://www.archery.org.hk',
                'https://www.archery.org.hk/frontpage?page=1',
                'https://www.archery.org.hk/frontpage?page=2',
                'https://www.archery.org.hk/frontpage?page=3',
                ]
        import functools
        rpcs = []
        for url in urls:
            rpc = urlfetch.create_rpc()
            rpc.callback = functools.partial(handle_result, rpc)
            urlfetch.make_fetch_call(rpc, url)
            rpcs.append(rpc)

        for rpc in rpcs:
            rpc.wait()
        logging.debug('done waiting')
        result_ids = ['{}:{}'.format(r['url_hash'], r['content_hash']) for r in results]

        keys = [ndb.Key(ArcheryOrgHkPost, str(rid)) for rid in result_ids]
        created_posts = ndb.get_multi(keys)
        to_create = [r for r, p in zip(results, created_posts) if not p]
        logging.debug('to_create: {}'.format(to_create))
        posts = ArcheryOrgHkPost.create_from_spider_batch(to_create)

        return {'results': [post.to_dict_for_owner() for post in posts]}

app = webapp2.WSGIApplication([
    (r'/api/v1/cron_jobs/archery_org_hk_spider', ArcheryOrgHkSpiderHandler),
])
