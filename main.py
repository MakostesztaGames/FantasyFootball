import json
import requests
from datetime import date
from file_manager import * 
from api_requests import *
from data_collector import *


# --- Így tudod használni a gyakorlatban: ---
if __name__ == "__main__":
    # Cseréld ki a saját API kulcsodra és egy valós meccs ID-ra (pl. egy Premier League meccsre)
    SAMPLE_MATCH_ID = "1391197"

    # 1. Teszt: Hány lekérésed van még?
    check_api_status()

    # 2. Teszt: Mai meccsek listázása
    # save_matches_by_date(print_it=True)

    b = 1
    # save_fixture_player_stats(fixture_id=SAMPLE_MATCH_ID)
    data = get_match_playerdata(SAMPLE_MATCH_ID, force_download=False)
    for team in data["response"]:
        players = []
        for p in team["players"]:
            stats = p["statistics"][0]
            if stats["games"]["minutes"] != 0:
                points = calculate_player_points(stats)
                player = {"name":p["player"]["name"], "rating_old": stats["games"]["rating"], 
                        "my_rating": points["total_points"], "detailes": points["breakdown"] }
                players.append(player)

        players.sort(key=lambda x: x["my_rating"], reverse=True)
        for i in players:
            print(f"{i['name']}\t{i['my_rating']}\t{i['rating_old']}")

            print(i["detailes"])
    