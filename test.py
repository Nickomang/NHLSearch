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


# Earliest we can do is 20132014
# Got 2015 from 20152016 working



import json
import json
from bson import json_util, ObjectId
import sys
import requests
import re

team = "ANA"
year = "2016"
fullyear = "20152016"
month = "01"

playername = "Corey Perry"

print "Testing for the team " + team + " in the year " + fullyear + ", " + month

def get_game_ids(team, year, month):
	url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + year + "/" + month + "/iphone/clubschedule.json"

	game_ids = []

	response = requests.get(url).json()

	game_count = 0
	for game in response['games']:
		game_ids.append(str(game['gameId']))
	print game_ids
	return game_ids

def get_ext_ids(game_id, fullyear):
	url = "http://live.nhle.com/GameData/" + fullyear + "/" + game_id + "/gc/gcgm.jsonp"
	response = requests.get(url).text
	if (fullyear == "20142015" or fullyear == "20152016"):
		trimmed_response = response[10:-1]
	else:
		trimmed_response = response[10:-2]
	print 
	json_response = json.loads(trimmed_response)
	ext_ids = []

	for event in json_response['video']['events']:
		for feed in event['feeds']:
			ext_ids.append(str(feed['extId']))

	print ext_ids
	return ext_ids

# Returns the ext_ids of events involving the player named
def parse_for_player(playername, ext_ids):
	highlight_urls = []
	p = re.compile('.*(' + playername + ').*')
	for ext_id in ext_ids:
		highlight_desc = get_description_of_event(ext_id)
		if p.match(highlight_desc):
			highlight_url = get_highlight_url(ext_id)
			highlight_urls.append(highlight_url)
	return highlight_urls




# Returns the URLs to Goals from the passed array of events
def parse_for_goals(ext_ids):
	p = re.compile('.*(goal).*')
	highlight_urls = []
	for ext_id in ext_ids:
		highlight_url = get_highlight_url(ext_id)
		if p.match(highlight_url):
			highlight_urls.append(highlight_url)
	return highlight_urls

def parse_for_saves(ext_ids):
	p = re.compile('.*(save).*')
	highlight_urls = []
	for ext_id in ext_ids:
		highlight_url = get_highlight_url(ext_id)
		if p.match(highlight_url):
			highlight_urls.append(highlight_url)
	return highlight_urls

def parse_for_both(playername, event_type, ext_ids):
	p1 = re.compile('.*(' + event_type + ').*')
	p2 = re.compile('.*(' + playername + ').*')


def get_description_of_event(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	response = requests.get(url).json()
	return response[0]['name']

def get_highlight_url(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	response = requests.get(url).json()
	return response[0]['publishPoint']




game_ids  = get_game_ids(team, year, month)
print 
ext_ids = get_ext_ids(game_ids[2], fullyear)
set1 = parse_for_player("Corey Perry", ext_ids)
set2 = parse_for_goals(ext_ids)



# print get_description_of_event(ext_ids[2])
# print parse_for_goals(ext_ids)






