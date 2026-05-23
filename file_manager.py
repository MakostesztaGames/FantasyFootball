import json
import requests
import os
from pathlib import Path

from datetime import date
from typing import Dict, Any, List
from api_requests import load_match_data_from_api, load_matches_by_date_api


JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def save_dict(data: Dict, file_path: Path, overwrite=False):
    if file_path.exists and not overwrite:
        raise FileExistsError("File already exists, if you want to overwrite it use overwrite=True")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Sikeres mentés! Fájlnév: {file_path}")


def save_fixture_player_stats(fixture_id, api_key):
    """Lekéri egy adott meccs játékos statisztikáit az API-Football-ból,
    és elmenti egy JSON fájlba.
    """
    
    file_path= Path(f"match_data/match_{fixture_id}_player_stats.json")
    if file_path.exists():
        raise FileExistsError("Stat already loaded, use load instead of saving it.")

    try:
        response_data = load_match_data_from_api(fixture_id)
        if not response_data:
            print("No data got!")
            return None
        save_dict(response_data, file_path, overwrite=True)
        return response_data

    except requests.exceptions.RequestException as error:
        print(f"Hiba történt a lekérés során: {error}")
        return None
    

def print_fixtures(target_date: date, fixtures: Dict):
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


def save_matches_by_date(api_key, target_date=None, print_it=False, file_path=None):
    """Lementi egy adott nap meccseit (Hazai vs Vendég) és a hozzájuk tartozó Fixture ID-t."""

    # Ha nem adtál meg dátumot, akkor a mai napot használja (ÉÉÉÉ-HH-NN formátumban)
    if target_date is None:
        target_date = date.today().strftime("%Y-%m-%d")

    if file_path is None:
        file_path=Path(f"match_list/{target_date}_matches.json")
    if file_path.exists():
        raise FileExistsError("Stat already loaded, use load instead of saving it.")

    try:
        fixtures = load_matches_by_date_api(target_date, api_key=api_key)
        if not fixtures:
            print(f"Ezen a napon ({target_date}) nincsenek meccsek az API-ban")
            return None

        save_dict(fixtures, file_path, overwrite=True)

        if print_it:
            print_fixtures(target_date, fixtures)  

        return fixtures    
        
    except requests.exceptions.RequestException as e:
        print(f"Hiba a meccsek lekérése közben: {e}")
        return None

def load_json() -> Dict[str, Any]:
    if not os.path.exists(JSON_FILE_PATH):
        return None
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
