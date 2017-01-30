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
from external_api.facebook import Facebook as FacebookApi

class ArcheryOrgHkSpiderHandler(BaseHandler):

    def create_post(self, post, client):
        post_content = []
        title = post.title or ''
        content = post.content.replace('\n', '%0A') or ''
        tag_arr = [u'%23{}'.format(tag) for tag in post.tags]
        tags = u'%20'.join(tag_arr)
        if title:
            post_content.append(title)
        if content:
            post_content.append(content)
        if tags:
            post_content.append(tags)
        post_fb_content = u'%0A'.join(post_content)
        logging.debug('entered')
        logging.debug(post_fb_content)
        link = '{}/archery_org_hk?post_id={}'.format(self.request.host_url, post.key.id())
        result = client.create_post(post_fb_content, link)

    @Output.json
    def get(self, *args, **kwargs):
        pageNum = 0
        url_format = 'https://www.archery.org.hk/frontpage?page={}'
        url = url_format.format(pageNum)
        results = []
        while url:
            get_result = urlfetch.fetch(url)
            page = etree.HTML(get_result.content)

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

            if page.xpath('//li[contains(@class, "pager-last")]'):
                pageNum += 1
                url = url_format.format(pageNum)
            else:
                url = None

        logging.debug('done fetching')
        result_ids = ['{}:{}'.format(r['url_hash'], r['content_hash']) for r in results]

        keys = [ndb.Key(ArcheryOrgHkPost, str(rid)) for rid in result_ids]
        created_posts = ndb.get_multi(keys)
        to_create = [r for r, p in zip(results, created_posts) if not p]
        if to_create:
            created_post_keys = ArcheryOrgHkPost.create_from_spider_batch(to_create)
            created_posts = ndb.get(created_post_keys)
            client = FacebookApi()
            for post in created_posts:
                self.create_post(post, client)
        else:
            logging.debug('no to create')
        return {}

app = webapp2.WSGIApplication([
    (r'/api/v1/cron_jobs/archery_org_hk_spider', ArcheryOrgHkSpiderHandler),
])
