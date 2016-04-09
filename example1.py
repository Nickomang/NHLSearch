# Example 1
# Shows all of a player's desired events for a given month of a season

import engine
import time
import json

start_time = time.time()

# Information
playername = "Patrice Bergeron"
team = "BOS"
season = 2015
month = 12
fullyear = str(season-1)+str(season)
location = 'h'
event_types_key = [0,1,0]

# Function Calls
active_event_types = engine.get_event_types(event_types_key)
print "Looking for ", playername, active_event_types, "from", season, "/", month
game_ids = engine.get_game_ids(team,season,month)
active_event_types = engine.get_event_types(event_types_key)
ext_ids = engine.filter_game_ids(game_ids, active_event_types,fullyear,location)
# print ext_ids
final_urls = engine.parse_for_player(playername, ext_ids)
print "Found", len(final_urls), active_event_types, ":"
print json.loads(final_urls)
print "Took", time.time() - start_time, "to run."
# Usually takes around 35 seconds