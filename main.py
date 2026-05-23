import json
import requests
from datetime import date
from file_manager import * 
from api_requests import *


# --- Így tudod használni a gyakorlatban: ---
if __name__ == "__main__":
    # Cseréld ki a saját API kulcsodra és egy valós meccs ID-ra (pl. egy Premier League meccsre)
    SAMPLE_MATCH_ID = "1391197"

    # 1. Teszt: Hány lekérésed van még?
    check_api_status()

    # 2. Teszt: Mai meccsek listázása
    # save_matches_by_date(MY_API_KEY, print_it=True)

    save_fixture_player_stats(fixture_id=SAMPLE_MATCH_ID, api_key=MY_API_KEY)