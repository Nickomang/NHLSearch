# Example 1
# Shows all of a player's desired events for a given month of a season

import engine
import time
import json

start_time = time.time()

# Information
# playername = "Corey Perry"
# team = "ANA"
# season = 2014
# month = 1
# fullyear = str(season-1)+str(season)
# location = 'h'
# event_types_key = [0,1,0]

# Function Calls
def final(playername, team, season, month, fullyear, location, event_types_key):
	active_event_types = engine.get_event_types(event_types_key)
	print "Looking for ", playername, active_event_types, "from", season, "/", month
	game_ids = engine.get_game_ids(team,season,month)
	active_event_types = engine.get_event_types(event_types_key)
	ext_ids = engine.filter_game_ids(game_ids, active_event_types,fullyear,location)
	# print ext_ids
	final_urls = engine.parse_for_player(playername, ext_ids)
	print "Found", len(final_urls), active_event_types, ":"

	final_dict = {}
	final_dict['links'] = final_urls
	final_json = json.dumps(final_dict)

	return final_json
	# print json.loads(final_dict)
print "Took", time.time() - start_time, "to run."
# Usually takes around 35 seconds