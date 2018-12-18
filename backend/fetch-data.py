import requests
import json

for num in [10]:
	print("starting with file number... " + str(num))
	response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random?number=100", 
		headers={"X-RapidAPI-Key": "UveLnbWodemshBlgXyS83ro6CVBIp1K11zBjsnloE1sEipxwmP"})
	data = response.json()
	filename = ('100recipes' + str(num) + '.json')
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)
	print("done")