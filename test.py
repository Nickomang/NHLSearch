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



print "testing for the ducks in 2016"

team = "ANA"
year = "2016"
month = "03"





def getGameIDs(team, year, month):
	team = "ANA"
	year = "2016"
	month = "03"

	url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + year + "/" + month + "/iphone/clubschedule.json"

	game_ids = []

	schedule = requests.get(url).json()

	game_count = 0
	for game in schedule['games']:
		game_ids.append(game['gameId'])

	print game_ids

getGameIDs(team, year, month)


