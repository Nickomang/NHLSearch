import engine
import time
import requests

start_time = time.time()

# Example 1:
# Corey Perry (ANA) All goals from 2014-2015, on Home Broadcast

# Information
playername = "Corey Perry"
team = "ANA"
year = 2015
month = 02
fullyear = str(year-1)+str(year)
location = 'h'
event_types_key = [0,1,0]

url = "http://e1.cdnak.neulion.com/nhl/vod/2015/02/03/755/2_755_car_ana_1415_h_discrete_ana212_goal_1_1600.mp4?eid=742358&pid=742897&gid=3000&pt=1"
print requests.get(url)
# active_event_types = engine.get_event_types(event_types_key)

# game_ids = engine.get_game_ids(team,year,month)
# active_event_types = engine.get_event_types(event_types_key)

# ext_ids = engine.filter_game_ids(game_ids, active_event_types,fullyear,location)
# print ext_ids

# final_urls = engine.parse_for_player(playername, ext_ids)

# print "Found", len(final_urls), active_event_types, ":"
# print final_urls

print "Took", time.time() - start_time, "to run."