import requests
from datetime import date

MY_API_KEY = "3990a2fd3eb7167b7f460efce9dd2deb"

def load_match_data_from_api(fixture_id: int, api_key=MY_API_KEY):
    # Az API-Football v3-as végpontja a meccs-játékos statisztikákhoz
    url = "https://v3.football.api-sports.io/fixtures/players"

    # API fejléc az azonosításhoz
    headers = {
        "x-apisports-key": api_key  # FIGYELEM: Ha RapidAPI-t használsz, ez 'x-rapidapi-key' legyen!
    }
    # A lekérdezés paraméterei (a keresett meccs ID-ja)
    query_params = {"fixture": fixture_id}

    print(f"-> Adatok lekérése a(z) {fixture_id} azonosítójú meccshez...")

    response = requests.get(url, headers=headers, params=query_params)

    # Hiba esetén kivételt dob (pl. 404 vagy 401 hibás API kulcsnál)
    response.raise_for_status()
    response_data = response.json()

    # Ellenőrizzük, hogy kaptunk-e valódi adatot vagy üres-e a válasz
    if not response_data.get("response"):
        print(
            "¡ Figyelem: Az API nem küldött adatot erre a meccs ID-ra (lehet, hogy rossz az ID, vagy még nem játszották le)."
        )
        return None
    return response_data

def load_matches_by_date_api( target_date: date, api_key=MY_API_KEY):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": api_key}

    params = {
        'date': target_date,
        'timezone': 'Europe/Budapest'
    }

    print(f"-> Meccsek lekérése a következő napra: {target_date}...")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    fixtures = data.get("response", [])
    
    return fixtures
    
def check_api_status(api_key=MY_API_KEY):
    """Lekéri a fiók státuszát és kiírja, hogy hány lekérdezés van még hátra aznap."""
    url = "https://v3.football.api-sports.io/status"
    headers = {"x-apisports-key": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Az API válaszából kiszedjük a kérésekre vonatkozó adatokat
        requests_info = data.get("response", {}).get("requests", {})

        if not requests_info:
            print("Nem sikerült lekérni a státusz információkat.")
            return

        current = requests_info.get("current", 0)
        limit_day = requests_info.get("limit_day", 0)
        remaining = limit_day - current

        print("=== API STÁTUSZ ===")
        print(f"Mai nap elhasznált lekérések: {current}")
        print(f"Napi limited: {limit_day}")
        print(f"👉 Még HÁTRAVAN a mai napon: {remaining} lekérdezés")
        print("===================\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ Hiba a státusz lekérése közben: {e}")
