import json
import requests
import os

from datetime import date
from typing import Dict, Any, List
from dataCollector import load_match_data_from_api, load_matches_by_date_api


JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")


def save_fixture_player_stats(fixture_id, api_key, filename=None):
    """Lekéri egy adott meccs játékos statisztikáit az API-Football-ból,

    és elmenti egy JSON fájlba.
    """

    # Ha nem adsz meg egyedi fájlnevet, automatikusan a meccs ID alapján nevezi el
    if filename is None:
        filename = f"match_{fixture_id}_player_stats.json"

    try:
        response_data = load_match_data_from_api(api_key, fixture_id)

        # Mentés JSON fájlba strukturált, szép formátumban (indent=4)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(response_data, file, ensure_ascii=False, indent=4)

        print(f"Sikeres mentés! Fájlnév: {filename}")
        return response_data

    except requests.exceptions.RequestException as error:
        print(f"Hiba történt a lekérés során: {error}")
        return None

def list_matches_by_date(api_key, target_date=None):
    """Kilistázza egy adott nap meccseit (Hazai vs Vendég) és a hozzájuk tartozó Fixture ID-t."""

    # Ha nem adtál meg dátumot, akkor a mai napot használja (ÉÉÉÉ-HH-NN formátumban)
    if target_date is None:
        target_date = date.today().strftime("%Y-%m-%d")

    try:
        fixtures = load_matches_by_date_api(api_key, target_date)
        if not fixtures:
            print(f"Ezen a napon ({target_date}) nincsenek meccsek az API-ban.")

        print(
            f"\n=== MECCSEK ÉS ID-K ({target_date}) - Összesen: {len(fixtures)} db ==="
        )
        print(f"{'FIXTURE ID':<12} | {'BAJNOKSÁG':<25} | {'MÉRKŐZÉS':<45} | STAT")
        print("-" * 95)

        for item in fixtures:
            fixture_id = item["fixture"]["id"]
            league_name = item["league"]["name"]
            home_team = item["teams"]["home"]["name"]
            away_team = item["teams"]["away"]["name"]
            status = item["fixture"]["status"]["short"]  # Pl. FT (vége), NS (még nem kezdődött el)

            # Szépen formázott kiírás
            match_str = f"{home_team} vs {away_team}"
            print(
                f"{fixture_id:<12} | {league_name[:23]:<25} | {match_str[:43]:<45} | {status}"
            )

        print("-" * 95)

    except requests.exceptions.RequestException as e:
        print(f"Hiba a meccsek lekérése közben: {e}")

def load_json() -> Dict[str, Any]:
    if not os.path.exists(JSON_FILE_PATH):
        return {"users": [], "baskets": []}
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
