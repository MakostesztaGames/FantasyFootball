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
        

def calculate_player_points(player_stats):
    rules = load_json(Path("rating_rules/example.json"))


    total_points = 0.0
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
