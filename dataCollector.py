import json
import requests
from datetime import date

def load_match_data_from_api(api_key, fixture_id):
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


def load_matches_by_date_api(api_key, target_date):
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
    
def check_api_status(api_key):
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


# --- Így tudod használni a gyakorlatban: ---
if __name__ == "__main__":
    # Cseréld ki a saját API kulcsodra és egy valós meccs ID-ra (pl. egy Premier League meccsre)
    MY_API_KEY = "3990a2fd3eb7167b7f460efce9dd2deb"
    SAMPLE_MATCH_ID = "1544596"  # Ez csak egy példa ID

    # 1. Teszt: Hány lekérésed van még?
    check_api_status(MY_API_KEY)

    # 2. Teszt: Mai meccsek listázása
    list_matches_by_date(MY_API_KEY, target_date="2026-05-22")

    # save_fixture_player_stats(fixture_id=SAMPLE_MATCH_ID, api_key=MY_API_KEY)