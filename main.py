import json
import requests
from datetime import date
from api_requests import *
from data_collector import DataCollector
from file_manager import FileManager


# --- Így tudod használni a gyakorlatban: ---
if __name__ == "__main__":
    # Cseréld ki a saját API kulcsodra és egy valós meccs ID-ra (pl. egy Premier League meccsre)
    SAMPLE_MATCH_ID = "1489369"

    _data_collector = DataCollector(FileManager())

    # _data_collector.get_fixtures(date(2026,6,12))

    _data_collector.get_match_playerdata(1539000)
    _data_collector.get_match_playerdata(1538999)
    
    
    #data = get_match_playerdata(SAMPLE_MATCH_ID, force_download=False)
    #for team in data["response"]:
    #    players = []
    #    for p in team["players"]:
    #        stats = p["statistics"][0]
    #        if stats["games"]["minutes"] != 0:
    #            points = calculate_player_points(stats)
    #            player = {"name":p["player"]["name"], "rating_old": stats["games"]["rating"], 
    #                    "my_rating": points["total_points"], "detailes": points["breakdown"] }
    #            players.append(player)
#
    #    players.sort(key=lambda x: x["my_rating"], reverse=True)
    #    for i in players:
    #        print(f"{i['name']}\t{i['my_rating']}\t{i['rating_old']}")
#
    #        print(i["detailes"])
    #