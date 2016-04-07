import engine
import time

start_time = time.time()

# Information
playername = "Max Pacioretty"
team = "MTL"
year = 2015
fullyear = str(year-1)+str(year)
# h or a or fr (seems they dont store all french broadcasts)
location = 'h'
# [hits, goals, saves]
event_types_key = [0,1,0]



engine.get_ext_ids("2014030111", "20132014", 505,"fr")

# # Function Calls
active_event_types = engine.get_event_types(event_types_key)
print active_event_types
game_ids = engine.get_game_ids_full(team,year)
print game_ids
print len(game_ids)
ext_ids = engine.filter_game_ids(game_ids, active_event_types,fullyear,location)
print ext_ids
final_urls = engine.parse_for_player(playername, ext_ids)

print "Found", len(final_urls), active_event_types, ":"
print final_urls

print "Took", time.time() - start_time, "to run."

# Takes about a minute and a half for all of max's goals