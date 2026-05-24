import json
import requests
import os
from pathlib import Path
from file_manager import save_fixture_player_stats, load_json, save_matches_by_date

from datetime import date
from typing import Dict, Any, List

def match_playerdata_file_name(match_id: int) -> Path:
    return Path(f"match_data/match_{match_id}_player_stats.json")
def fixture_file_name(fixture_date: date) -> Path:
    return Path(f"match_list/{fixture_date}_matches.json")

def get_match_playerdata(match_id: int, force_download=False):
    '''Gets the playerdata from a game, if already saved, gets it from local file
    force_download forces it to update the file from api'''

    file_path =  match_playerdata_file_name(match_id)
    if file_path.exists() and not force_download:
        print("Got data from lokal file")
        return load_json(file_path)
    else:
        print("Got data from api")
        return save_fixture_player_stats(match_id, file_path=file_path)
    

def get_fixtures(fixture_date: date = None, team=None, league=None):
    '''Gets the playerdata from a game, if already saved, gets it from local file
    force_download forces it to update the file from api'''

    if fixture_date is None:
        fixture_date = date.today().strftime("%Y-%m-%d")

    file_path =  fixture_file_name(fixture_date)
    if file_path.exists():
        print("Got data from lokal file")
        data = load_json(file_path)
    else:
        print("Got data from api")
        data = save_matches_by_date(fixture_date, file_path=file_path)
    
    if team is None and league is None:
        return data
    
    ret_data = []
    for fixture in data:
        match_team = team and team in (fixture["teams"]["home"]["name"], fixture["teams"]["away"]["name"])
        match_league = league and fixture["league"]["name"] == league
        
        if match_team or match_league:
            ret_data.append(fixture)

    return ret_data
        

def calculate_player_points(raw_player_stats):
    rules = load_json(Path("rating_rules/example.json"))

    player_stats = process_player_data(raw_player_stats)

    total_points = 30.0
    breakdown = {}

    # Végigmegyünk a szabályzat kategóriáin (games, shots, goals, stb.)
    for category, metrics in rules.items():
        # Megkeressük ugyanezt a kategóriát a játékos adatainál
        player_category = player_stats.get(category, {})

        if player_category:
            category_score = 0.0

            # Végigmegyünk a kategórián belüli konkrét mutatókon (minutes, total, on, stb.)
            for metric_name, multiplier in metrics.items():
                value = player_category.get(metric_name)

                # Csak akkor számolunk, ha az adat létezik és nem null
                if value is not None:
                    # A Python a True/False értékeket automatikusan 1-nek és 0-nak számolja float() esetén
                    category_score += float(value) * multiplier

            if category_score != 0:
                total_points += category_score
                breakdown[category] = round(category_score, 2)

    return {"total_points": round(total_points, 2), "breakdown": breakdown}


def process_player_data(raw: Dict) -> Dict:
    '''prcesses the player data into a dict, that contains exatly the data, that worth point'''
    # Biztonságos értékkinyerő: ha None vagy hiányzik, 0-t ad vissza, és számmá alakít
    def get_val(category, key):
        try:
            val = raw.get(category, {}).get(key)
            if val is None:
                return 0
            return int(val)
        except (ValueError, TypeError, AttributeError):
            return 0
    
    # Tizenegyesek
    pen_won = get_val("penalty", "won")
    pen_scored = get_val("penalty", "scored")
    
    # Cselek
    dribble_attempts = get_val("dribbles", "attempts")
    dribble_success = get_val("dribbles", "success")
    
    # Passzok
    passes_total = get_val("passes", "total")
    passes_completed = get_val("passes", "accuracy") # A mintád alapján az accuracy a sikeres passzok száma
    
    # Párharcok
    duels_total = get_val("duels", "total")
    duels_won = get_val("duels", "won")

    # Kapott gól és játékpercek a Cleansheet (kapott gól nélküli meccs) számításához
    conceded = get_val("goals", "conceded")
    minutes = get_val("games", "minutes")
    cleansheet = 1 if (minutes > 0 and conceded == 0) else 0

    # --- A RENDSZEREZETT DICTIONARY ÖSSZEÁLLÍTÁSA ---
    processed = {
        "decisive": {
            "goals": get_val("goals", "total"),
            "assists": get_val("goals", "assists"),
            "red card": get_val("cards", "red"),
            # Kivonjuk a belőtt tizenegyest, és figyelünk, hogy ne menjen mínuszba:
            "penalty won": max(0, pen_won - pen_scored), 
            "penalty missed": get_val("penalty", "missed"),
            "penalty saved": get_val("penalty", "saved"),
            "penalty commited": get_val("penalty", "commited")
        },
        "defense": {
            "cleansheet": cleansheet,
            "tackles": get_val("tackles", "total"),
            "blocks": get_val("tackles", "blocks"),
            "interceptions": get_val("tackles", "interceptions"),
            "dribbled past": get_val("dribbles", "past"),
            "goals conceded": conceded,
            "saves": get_val("goals", "saves")
        },
        "attack": {
            "shots": get_val("shots", "total"),
            "shots on target": get_val("shots", "on"),
            "succesful drible": dribble_success,
            "failed drible": max(0, dribble_attempts - dribble_success)
        },
        "passes": {
            "pass completed": passes_completed,
            "pass missed": max(0, passes_total - passes_completed),
            "key passes": get_val("passes", "key")
        },
        "physicality": {
            "duel won": duels_won,
            "duel lost": max(0, duels_total - duels_won),
            "fouls drawn": get_val("fouls", "drawn"),
            "fouls committed": get_val("fouls", "committed"),
            "yellow card": get_val("cards", "yellow")
        }
    }

    return processed