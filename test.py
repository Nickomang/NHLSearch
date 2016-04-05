# Url for player images
# http://tsnimages.tsn.ca/ImageProvider/PlayerHeadshot?seoId=[first]-[last]

# NHL Game ID
# First 4 digits : year in which season begins
# Digits 5-6
# 	01 : Preseason
#	02 : Regular Season 
# 	03 : Playoffs
#	09 : Olympics
# Digits 7-10 :

# Highlight videos
# http://live.nhle.com/GameData/[year]/[game_id]/gc/gcgm.jsonp


#so lets test the ducks.

import json
import json
from bson import json_util, ObjectId
import sys
import requests
import re



print "testing for the Calgary in March (03) of 2015"

team = "CGY"
year = "2015"
fullyear = "20142015"
month = "03"

def get_game_ids(team, year, month):
	url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + year + "/" + month + "/iphone/clubschedule.json"

	game_ids = []

	response = requests.get(url).json()

	game_count = 0
	for game in response['games']:
		game_ids.append(str(game['gameId']))

	return game_ids

def get_ext_ids(game_id, year):
	url = "http://live.nhle.com/GameData/" + year + "/" + game_id + "/gc/gcgm.jsonp"
	response = requests.get(url).text
	trimmed_response = response[10:-1]

	json_response = json.loads(trimmed_response)

	ext_ids = []

	for event in json_response['video']['events']:
		for feed in event['feeds']:
			ext_ids.append(str(feed['extId']))



	return ext_ids

def get_highlight_url(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	response = requests.get(url).json()
	return response[0]['publishPoint']




game_ids  = get_game_ids(team, year, month)
print 
ext_ids = get_ext_ids(game_ids[2], fullyear)

highlight_urls = []

# Could change to only get english and home links
p = re.compile('.*(goal).*')

for ext_id in ext_ids:
	highlight_url = get_highlight_url(ext_id)
	if p.match(highlight_url):
		highlight_urls.append(highlight_url)


print highlight_urls




