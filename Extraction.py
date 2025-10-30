import requests
import json

url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"

requete = requests.get(url)
requete.raise_for_status()

data = requete.json()
stations = data.get("data", {}).get("stations", [])

StationsPret = [
    {
        "station_id": station.get("station_id"),
        "lat": station.get("lat"),
        "lon": station.get("lon"),
        "capacity": station.get("capacity", 0)
    }
    for station in stations
]

with open("stations_data.json", "w", encoding="utf-8") as f:
    json.dump(StationsPret, f, indent=4, ensure_ascii=False)

print(f"Reussi")
