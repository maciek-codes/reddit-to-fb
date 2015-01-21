import urllib
import urllib2
import json
import re

class Post(object):

    def __init__(self, title, url, id):
        self.title = self.removeTILandThat(title)
        self.url = url
        self.id = id

    def cap(self, str):
        return str[0].upper() + str[1:]

    def removeTILandThat(self, title):

        new_title = re.sub("^TIL:?(\s?that)?(\s?-\s?)?", "", title, flags=re.I).strip()
        new_title = self.cap(new_title)
        return new_title

class PostSource(object):
    """Source of posts"""
    def __init__(self):
        return
        

class RedditPostSource(PostSource):
    """Reddit as post source"""
    def __init__(self, url, limit=24, time='day'):
        super(RedditPostSource, self).__init__()
        self.url = url
        self.limit = limit
        self.time = time

    def load_json(self):
        
        jsonUrl = self.url + "/top.json?t={0}&limit={1}".format(self.time, str(self.limit))

        params = urllib.urlencode({
          'limit': self.limit,
          't': 'day'
        })

        response = urllib2.urlopen(jsonUrl)
        ret = json.loads(response.read())

        return ret

class PostLoader(object):

    def __init__(self, sub = "todayilearned"):
        self.baseUrl = "http://reddit.com/"
        self.url = self.baseUrl + "r/" + sub
        self.sub = sub

    def get_posts(self, postSource = None):

        if(postSource is None):
            postSource = RedditPostSource(self.url)

        jsonResponse = postSource.load_json()

        posts = []

        for child in jsonResponse['data']['children']:
            data = child['data']
            posts.append(Post(data['title'], data['url'], data['id']))

        return posts