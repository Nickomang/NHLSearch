# Engine for NHL Video Database Search
# Possible queries
# For each: all time, month, and game specific
# For each: single events, multiple events, 
# Team event
# Player event
# Team + team event
# Player + Player
# Player + Team event

# Dependencies
import json
import requests
import re

# Global Variables
event_dict = {'hit': 503, 'goal': 505, 'save': 506}
event_types = ['hit','goal','save']
event_types_key = [1,0,0]

# Returns a list of the game ids for a given team during a given year and month
def get_game_ids(team, season, month):
	if (month > 7):
		url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season - 1) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
	else:
		url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
	game_ids = []
	response = requests.get(url).json()
	for game in response['games']:
		game_ids.append(str(game['gameId']))
	return game_ids

# Returns a list of game_id's for a given team during the entirety of a given season
def get_game_ids_full(team, season):
	game_ids = []
	if season == 2016:
		# Need to get october goals
		for month in (10,11,12,1,2):
			if (month > 7):
				url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season-1) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
			else:
				url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
			response = requests.get(url).json()
			for game in response['games']:
				game_ids.append(str(game['gameId']))
	else:
		for month in (10,11,12,1,2,3,4,5,6,7):
			if (month > 7):
				url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season-1) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
			else:
				url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
			response = requests.get(url).json()
			for game in response['games']:
				game_ids.append(str(game['gameId']))
	return game_ids

# Gets the ext_id's from a given game id. Options for event type and home/away broadcast
def get_ext_ids(game_id, fullyear, event_num, location):
	url = "http://live.nhle.com/GameData/" + fullyear + "/" + game_id + "/gc/gcgm.jsonp"
	if (not requests.get(url)):
		print "NHL fucked up"
		return []
	response = requests.get(url).text

	# Necesarry because sometimes the NHL has game ids that don't actually correspond to anything
	print "using game", game_id
	trimmed_response = response[10:-1]
	try:
		json_response = json.loads(trimmed_response)
	except ValueError:
		print "NHL fucked up again"
		trimmed_response = response[10:-2]
		try:
			json_response = json.loads(trimmed_response)
		except ValueError:
			print "THEY FUCKED UP A THIRD TIME"
			trimmed_response = response[10:-3]
			try:
				json_response = json.loads(trimmed_response)
			except ValueError:
				print "Fuck bettman"
				return []
	
	# This block is because sometimes the NHL fucks up and the older ones need the newer treatment
	try:
		json_response = json.loads(trimmed_response)
		
	except ValueError:
		trimmed_response = response[10:-1]
		
	json_response = json.loads(trimmed_response)
	ext_ids = []

	# Needs this because the NHL inexplicably sometimes uses events and sometimes uses ingame
	key = ''
	if(json_response['video']['events']):
		key = 'events'
	elif(json_response['video']['ingame']):
		key = 'ingame'
	else:
		return ext_ids

	for event in json_response['video'][key]:
		if 'type' in event:
			if (event['type'] == event_num):
				for feed in event['feeds']:
					if (str(feed['extId']).endswith(location)):
						ext_ids.append(str(feed['extId']))
	return ext_ids

# Returns the ext_ids of events involving the player named
def parse_for_player(playername, ext_ids):
	highlight_urls = []
	p = re.compile('.*(' + playername + ').*')
	for ext_id in ext_ids:
		print "checking ext_id", ext_id
		highlight_desc = get_description_of_event(ext_id)
		if p.match(highlight_desc):
			highlight_url = get_highlight_url(ext_id)
			highlight_urls.append(highlight_url)
			print "Found one!"
	print highlight_urls
	return highlight_urls

# Returns a JSON description of the event associated with the given ext_id
def get_description_of_event(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	# Because of fuckin ryan o'reilly
	response = requests.get(url).text
	response = response.replace("'","")
	response = response.replace("\\","")

	json_response = json.loads(response)
	return json_response[0]['name']

# Gets the link to the .mp4 file of the highlight
def get_highlight_url(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	response = requests.get(url).json()
	return response[0]['publishPoint']

# Takes the event_types_key and returns a list of the event types specified
# e.g [0,1,0] -> ['goal']
def get_event_types(event_types_key):
	results = []
	count = 0
	for key in event_types_key:
		if key == 1:
			results.append(event_types[count])
		count += 1
	return results

# Takes what would be a list of lists of ext_ids and turns it into a single list of ext_ids
def filter_game_ids(game_ids, event_types, fullyear, location):
	ext_ids = []
	for game_id in game_ids:
		for event_type in event_types:
			ext_ids_single = get_ext_ids(game_id, fullyear, event_dict[event_type], location)
			for ext_id_single in ext_ids_single:
				ext_ids.append(ext_id_single)
	return ext_ids
