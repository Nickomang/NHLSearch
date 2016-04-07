import json
import requests
import re
import time

event_dict = {'hit': 503, 'goal': 505, 'save': 506}
event_types = ['hit','goal','save']
event_types_key = [1,0,0]

def get_player_team(playername):
	return "ANA"

bruh = 33

# Returns a list of the game ids for a given team during a given year and month
def get_game_ids(team, year, month):
	if (month > 7):
		url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(year - 1) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
	else:
		url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(year) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
	game_ids = []
	response = requests.get(url).json()
	for game in response['games']:
		game_ids.append(str(game['gameId']))
	return game_ids

# Returns a list of game_id's for a given team during the entirety of a given year
def get_game_ids_full(team, year):
	game_ids = []
	if year == 2016:
		# Need to get october goals
		for month in (10,11,12,1,2):
			if (month > 7):
				url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(year-1) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
			else:
				url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(year) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
			response = requests.get(url).json()
			for game in response['games']:
				game_ids.append(str(game['gameId']))
	else:
		for month in (10,11,12,1,2,3,4,5,6,7):
			if (month > 7):
				url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(year-1) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
			else:
				url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(year) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
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
		# print "checking ext_id", ext_id
		highlight_desc = get_description_of_event(ext_id)
		if p.match(highlight_desc):
			highlight_url = get_highlight_url(ext_id)
			highlight_urls.append(highlight_url)
			print "Found one!"
	return highlight_urls

def get_event_data(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	response = requests.get(url).json()
	return response[0]

def get_description_of_event(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	# Because of fuckin ryan o'reilly
	response = requests.get(url).text
	response = response.replace("'","")
	response = response.replace("\\","")

	json_response = json.loads(response)
	return json_response[0]['name']

def get_highlight_url(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	response = requests.get(url).json()
	return response[0]['publishPoint']

def get_event_types(event_types_key):
	results = []
	count = 0
	for key in event_types_key:
		if key == 1:
			results.append(event_types[count])
		count += 1
	return results


def filter_game_ids(game_ids, event_types, fullyear, location):
	ext_ids = []
	for game_id in game_ids:
		for event_type in event_types:
			# print event_dict[event_type]
			ext_ids_single = get_ext_ids(game_id, fullyear, event_dict[event_type], location)
			for ext_id_single in ext_ids_single:
				# print ext_id_single
				ext_ids.append(ext_id_single)
	return ext_ids




# INFORMATION THAT WILL BE POTENTIALLY PASSED IN BY USER


# team = "ANA"
# year = 2015 # NOTE: This is the later part of the season's year (e.g 2014/2015 = 2015)
# fullyear = str(year-1)+str(year)
# print fullyear
# month = 1

# playername = "Corey Perry"

# event_type = 'goal'
# location = 'h'

# event_types = ['hit', 'goal', 'save']
# event_types_key = [1,0,0]

# active_event_types = get_event_types(event_types_key)

# game_ids  = get_game_ids(team, year, month)
# # game_ids = get_game_ids_full(team,year)
# print game_ids
# print 
# active_event_types = get_event_types(event_types_key)
# print active_event_types

# ext_ids = filter_game_ids(game_ids, active_event_types)

# print ext_ids
# print len(ext_ids)

# print parse_for_player(playername, ext_ids)




# print len(get_game_ids_full(team,year))

# active_event_types = get_event_types(event_types_key)
# print active_event_types
# print parse_for_saves(ext_ids)
# print parse_for_event(ext_ids, active_event_types)



# print "Took ", time.time() - start_time, " to run."
# Average times :
	# hits   -> 15s
	# goals  -> 35s
	# saves  -> 120s


# Use prechecking with 503, etc codes instead of regex match

# Possible queries
# For each: all time, month, and game specific
# For each: single events, multiple events, 
# Team event
# Player event
# Team + team event
# Player + Player
# Player + Team event





