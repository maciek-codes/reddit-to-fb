from lib.post import PostLoader
from azure.storage import TableService, Entity
import json, urllib2, urllib
from datetime import datetime
from time import sleep

# Read config
tiwt_keys = open('keys.json')
keys = json.load(tiwt_keys)
tiwt_keys.close()

graph_url = "https://graph.facebook.com/v2.2/"
table_service = TableService(account_name=keys['azure_storage_account'], account_key=keys['azure_storage_key'])

try_count = 0

def post_to_page(access_token, post):

	pageid = keys['page_id']

	data = urllib.urlencode({
		'message': post.title,
		'link': post.url
	})

	url = graph_url + pageid + "/feed?access_token=" + str(access_token)
	
	req = urllib2.Request(url, data)
	resp =  urllib2.urlopen(req)
	res = resp.read()

def main():
	global try_count

	if try_count >= 5:
		print "Max try count reached"
		return

	# Load posts
	postLoader = PostLoader()

	try:
		posts = postLoader.get_posts()
	except urllib2.HTTPError as err:

		print err

		# 429 -- Too many requests
		if(err.code == 429):	
			# Wait and try again
			try_count += 1
			sleep(30)
			return main()
		else:
			return 

	# Success
	try_count = 0

	if(len(posts) == 0):
		print "No posts fetched"
		return

	# Create table if not exist
	table_service.create_table('posts')

	for post in posts:

		# Check if the post was there
		existing_posts = table_service.query_entities('posts', "PartitionKey eq 'topposts' and RowKey eq '"+post.id+"'")

		if(len(existing_posts) > 0):
			continue

		#Create new post
		new_post = {
		 	'PartitionKey': 'topposts',
		 	'RowKey': post.id,
		 	'url' : post.url,
		 	'title': post.title,
		 	'created_at': datetime.now().isoformat()
		 }
		
		# Add to the table
		table_service.insert_entity('posts', new_post)
		
		# Get access token
		access_token = keys['access_token']
		post_to_page(access_token, post)

		print "Added: "+ str(post.title) + " at url: " + str(post.url)
		return

	return

if __name__ == '__main__':
	main()