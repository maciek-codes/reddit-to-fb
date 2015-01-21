from flask import Flask, flash, request, redirect, render_template, url_for
import urllib2
import urllib
import json
import urlparse

# FB Client and secret should go here
FB_CLIENT_ID = ''
FB_CLIENT_SECRET = ''
pageid = '' # FB Page ID here

# Flask setup
app = Flask(__name__)
app.config.from_object(__name__)

# rauth OAuth 2.0 service wrapper
graph_url = 'https://graph.facebook.com/'

def get_page_access_token(user_access_token, pageid):

    url = graph_url + "me/accounts/?access_token=" + str(user_access_token)
    res = json.loads(urllib2.urlopen(url).read())

    for data in res['data']:
        if(data['id'] != pageid):
            pass
        return data['access_token']
    
    raise Error("Unable to find page access token")


# views
@app.route('/')
def login():

    redirect_uri = url_for('callback', _external=True)
    url = "https://www.facebook.com/dialog/oauth?client_id=" + str(FB_CLIENT_ID) + \
        '&redirect_uri=' + redirect_uri + \
        '&response_type=code&scope=manage_pages,publish_actions'

    print url
    return redirect(url)

@app.route('/hello')
def hello():
    return "Hello world"

def callback_code(code):

    print "Exchanging the token"

    redirect_uri = url_for('callback', _external=True)

    url = "https://graph.facebook.com/oauth/access_token?client_id=" + str(FB_CLIENT_ID) + \
        '&redirect_uri=' + redirect_uri + \
        '&client_secret=' + str(FB_CLIENT_SECRET) + "&code=" + str(code)

    try:

        res = urllib2.urlopen(url)
        parsed = urlparse.parse_qs(res.read())
        access_token = parsed['access_token'][0]
        print get_page_access_token(access_token, pageid)
    except Exception as ex:
        print ex

    return "Access token generated, see output."

@app.route('/callback')
def callback():

    print "callback!"
    try:
        
        # check to make sure the user authorized the request
        if 'code' in request.args:
            code = request.args['code']
            return callback_code(code)
        else:
            return "Not authenticated"
    except Error as er:
        print er
        return "Error"

if __name__ == '__main__':
    app.run(None, 3000)