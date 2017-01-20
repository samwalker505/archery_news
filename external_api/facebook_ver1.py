from google.appengine.api import urlfetch
from google.appengine.api import memcache
import urlparse
import logging
import json
import functools


class Facebook(object):
  api_ver = 'v2.8'
  base_url = 'https://graph.facebook.com/{}'.format(api_ver)
  def __init__(self, access_token):
    self.access_token = access_token
    self.headers = {'Authorization': 'OAuth {}'.format(self.access_token)}

  @classmethod
  def app_init(cls, client_id, client_secret):
    url = '{}/oauth/access_token?client_id={}&client_secret={}&grant_type=client_credentials'.format(Facebook.base_url, client_id, client_secret)
    logging.debug(url)
    try:
      result = urlfetch.fetch(url)
      result_dict = json.loads(result.content)
      logging.debug(result_dict)
      return Facebook(result_dict['access_token'])
    except Exception as e:
      raise e

  def me(self):
    return self._get('me')

  def me_accounts(self):
    return self._get('me/accounts')

  def page(self, page_id):
    return self._get('{}?fields=name,id,about,picture,category'.format(page_id))

  def posts(self, page_id, limit=100):
    result = self._get('{}/posts?fields=id'.format(page_id))
    posts = []
    count = 0

    def handle_result(rpc):
      post = rpc.get_result()
      post = json.loads(post.content)
      posts.append(post)

    while count < limit:
      rpcs = []
      for post in result['data']:
        rpc = self._get_async('{}?fields=id,name,picture,caption,attachments'.format(post['id']), handle_result)
        if count < limit:
          rpcs.append(rpc)
          count += 1
        else:
          break
      for rpc in rpcs:
        rpc.wait()
      if result['paging']['next'] and count < limit:
        result = self._get('{}/posts?fields=id&next={}'.format(page_id, result['paging']['next']))
      else:
        break
    return posts, count

  # def crawl_post(self, owner_id, obj_id):
  #   complex_id = '{}_{}'.format(owner_id, obj_id)
  #   logging.debug('crawling %s', complex_id)
  #   post = self._get_post(complex_id)
  #   message = post.get('message', '')
  #   description = post.get('description', '')
  #
  #   result = {}
  #   result['content'] = u'{}\n{}'.format(message, description) # concat two status together
  #   result['link'] = post.get('link', None)
  #
  #   resources = self._get_images(complex_id)
  #
  #   if not resources: # try if it is a photo post, which dont have attachments
  #     picture_url = post.get('full_picture', None)
  #     if picture_url:
  #       image = Facebook._add_photo(picture_url)
  #       resources = [{'id':image.key.id(), 'url':image.url}]
  #
  #   result['images'] = resources
  #   return result
  #
  #
  # def crawl(self, fb_url):
  #   parse_result = urlparse.urlparse(fb_url)
  #   split_result = parse_result.path.split('/')
  #   owner = next(item for item in split_result if item) # get the first obj is not empty
  #   owner_id = self._get_id_by_name(owner)
  #   obj_id = next(item for item in reversed(split_result) if item)
  #   return self.crawl_post(owner_id, obj_id)



  # def _get_images(self, complex_id):
  #   data = self._get('{}/attachments'.format(complex_id))['data']
  #   if data:
  #     media_urls = Facebook._get_media_urls(data)
  #     resources = []
  #     for media_url in media_urls:
  #       image = Facebook._add_photo(media_url)
  #       if image:
  #         resources.append({'id':image.key.id(), 'url':image.url})
  #     return resources
  #   else:
  #     return None

  # @staticmethod
  # def _get_media_urls(data):
  #   sub = data[0].get('subattachments')
  #   if sub:
  #     sub_data = sub['data']
  #     data_length = min(len(sub_data), 6)
  #     media_urls = []
  #     for i in range(0, data_length):
  #       media = sub_data[i]['media']
  #       image = media.get('image', None)
  #       if image:
  #         logging.debug(image['width'])
  #         logging.debug(image['src'])
  #         media_urls.append(image['src'])
  #     logging.debug(media_urls)
  #     return media_urls
  #   else:
  #     return []
  #
  # @staticmethod
  # def _add_photo(url):
  #   result = urlfetch.fetch(url=url, method=urlfetch.GET, deadline=20)
  #   if result.status_code != 200:
  #     logging.debug(result.status_code)
  #   img = result.content
  #   image = Image.add(None, img)
  #   return image
  #
  # def _get_post(self, post_id):
  #   return self._get('{}?fields=message,link,description,full_picture'.format(post_id))
  #
  # def _get_id_by_name(self, name):
  #   result_dict = self._get(name)
  #   return result_dict['id']

  def _get_async(self, url, callback, option=None):
    url = '{}/{}'.format(Facebook.base_url, url)
    logging.debug(url)
    logging.debug(self.access_token)
    logging.debug(self.headers)
    rpc = urlfetch.create_rpc()
    rpc.callback = functools.partial(callback, rpc)
    if not option:
      option = {'headers':self.headers}
    urlfetch.make_fetch_call(rpc, url, **option)
    return rpc

  def _get(self, url, option=None):
    url = '{}/{}'.format(Facebook.base_url, url)
    logging.debug(url)
    logging.debug(self.access_token)
    logging.debug(self.headers)
    if not option:
      option = {'headers':self.headers}
      return json.loads(urlfetch.fetch(url, **option).content)
