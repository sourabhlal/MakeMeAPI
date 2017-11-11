import json
import pprint

from clarifai import rest
from clarifai.rest import Image as ClImage
from clarifai.rest import ClarifaiApp

YOUR_API_KEY = "d0b5b9f355e24b4abf3ede112d787d9f"

app = ClarifaiApp(api_key=YOUR_API_KEY)
image = ClImage(url='https://samples.clarifai.com/metro-north.jpg')

model = app.models.get("general-v1.3")
response = model.predict([image])

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(response)

# result = response['outputs'][0]['data']['concepts']

# for i in result[:5]:
# 	print (i['name'], i['value'])
