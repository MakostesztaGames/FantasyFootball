import json
import requests
from datetime import date
from fileManager import * 
from dataCollector import *


# --- Így tudod használni a gyakorlatban: ---
if __name__ == "__main__":
    # Cseréld ki a saját API kulcsodra és egy valós meccs ID-ra (pl. egy Premier League meccsre)
    MY_API_KEY = "3990a2fd3eb7167b7f460efce9dd2deb"
    SAMPLE_MATCH_ID = "1544596"

    # 1. Teszt: Hány lekérésed van még?
    check_api_status(MY_API_KEY)

    # 2. Teszt: Mai meccsek listázása
    list_matches_by_date(MY_API_KEY, target_date="2026-05-22")

    # save_fixture_player_stats(fixture_id=SAMPLE_MATCH_ID, api_key=MY_API_KEY)