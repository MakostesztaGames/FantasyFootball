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

    # save_fixture_player_stats(fixture_id=SAMPLE_MATCH_ID)
    data = get_match_playerdata(SAMPLE_MATCH_ID, force_download=True)
    for team in data["response"]:
        print(team["players"][0])

    