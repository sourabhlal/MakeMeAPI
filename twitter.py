import tweepy

#from our keys module (keys.py), import the keys dictionary
from keys import twitter_keys

from keys import clarifai_key

import json
import pprint
from clarifai import rest
from clarifai.rest import Image as ClImage
from clarifai.rest import ClarifaiApp

YOUR_API_KEY = clarifai_key

app = ClarifaiApp(api_key=YOUR_API_KEY)

def clarifai_predict(image):
	# get the general model
	model = app.models.get("general-v1.3")
	response = model.predict([image])

	# pp = pprint.PrettyPrinter(indent=2)
	# pp.pprint(response)

	result = response['outputs'][0]['data']['concepts']

	reply = "The 5 best descriptions for this picture are: "
	for i in result[:4]:
		reply += i['name']
		reply += ", "
	reply += result[4]['name']
	return reply


def processTweet(s,api):
	#get image
	#not all tweets will have media url, so lets skip them
	reply=""
	try:
		print ("image url = ", s.entities['media'][0]['media_url'])
	except (NameError, KeyError):
		#we dont want to have any entries without the media_url so lets do nothing
		print ('no media')
		reply = "You didn't send me an image"
		pass
	else:
		image = ClImage(url=s.entities['media'][0]['media_url'])
		reply = clarifai_predict(image)

	print (s.text)
	sn = s.user.screen_name
	m = "@%s %s!" % (sn,reply)
	print(m)
	s = api.update_status(m, s.id)


CONSUMER_KEY = twitter_keys['consumer_key']
CONSUMER_SECRET = twitter_keys['consumer_secret']
ACCESS_KEY = twitter_keys['access_token']
ACCESS_SECRET = twitter_keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)
# api.update_status('Test')

replied_to = []

twt = api.search(q="@LauzHackApiDemo")

# while twt != []:
for s in twt:
	if s.id not in replied_to:
		if s.text.split(' ',1)[0] != "RT":
			processTweet(s,api)
		replied_to.append(s.id)
	# twt = api.search(q="@LauzHackApiDemo")