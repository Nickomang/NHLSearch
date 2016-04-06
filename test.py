import json
import requests
import re
import time

event_dict = {'hit': 503, 'goal': 505, 'save': 506}

start_time = time.time()

team = "ANA"
year = "2016"
fullyear = "20152016"
month = "01"

playername = "Corey Perry"

event_type = 'hit'
location = 'h'

print "Testing for the team " + team + " in the year " + fullyear + ", " + month
print "Looking for " + playername + " " + event_type + "s."  


# Returns a list of the game ids for a given team during a given year and month
def get_game_ids(team, year, month):
	url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + year + "/" + month + "/iphone/clubschedule.json"

	game_ids = []

	response = requests.get(url).json()

	game_count = 0
	for game in response['games']:
		game_ids.append(str(game['gameId']))
	return game_ids

# 
def get_ext_ids(game_id, fullyear, event_num, location):
	url = "http://live.nhle.com/GameData/" + fullyear + "/" + game_id + "/gc/gcgm.jsonp"
	response = requests.get(url).text
	if (fullyear == "20142015" or fullyear == "20152016"):
		trimmed_response = response[10:-1]
	else:
		trimmed_response = response[10:-2]
	json_response = json.loads(trimmed_response)
	ext_ids = []

	# 503 hits?
	# If goals, 505
	# If saves, 506

	for event in json_response['video']['events']:
		# if (event['type'] == event_type):
		if (event['type'] == event_num):
			for feed in event['feeds']:
				if (str(feed['extId']).endswith(location)):
					ext_ids.append(str(feed['extId']))
	# print ext_ids
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

# Currently just doing event type
def parse_for_both(playername, event_type, ext_ids):
	p1 = re.compile('.*(' + event_type + ').*')
	p2 = re.compile('.*(' + playername + ').*')
	highlight_urls = []
	for ext_id in ext_ids:
		highlight_data = get_event_data(ext_id)
		highlight_url = get_highlight_url(ext_id)
		if (p1.match(highlight_data['publishPoint'])):
			if(p2.match(highlight_data['name'])):
				highlight_urls.append(highlight_url)
				print "Found a " + event_type
	return highlight_urls


def get_event_data(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	response = requests.get(url).json()
	return response[0]

def get_description_of_event(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	response = requests.get(url).json()
	return response[0]['name']

def get_highlight_url(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	response = requests.get(url).json()
	return response[0]['publishPoint']


# Gets Corey Perry goals from January 2016

game_ids  = get_game_ids(team, year, month)
print 
ext_ids = []
for game_id in game_ids:
	ext_ids_single = get_ext_ids(game_id, fullyear, event_dict[event_type], location)
	for ext_id_single in ext_ids_single:
		ext_ids.append(ext_id_single)
print len(ext_ids)
print parse_for_both(playername, event_type, ext_ids)
print "Took ", time.time() - start_time, " to run."

# Average times :
	# hits   -> 15s
	# goals  -> 35s
	# saves  -> 120s





