import json
import requests
import os
from pathlib import Path
from file_manager import save_fixture_player_stats, load_json

from datetime import date
from typing import Dict, Any, List

def match_playerdata_file_name(match_id: int):
    return Path(f"match_data/match_{match_id}_player_stats.json")

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
    
