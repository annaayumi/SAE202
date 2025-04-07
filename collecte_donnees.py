# ETAPE 1 : Extraction de données
import json

# Charger les données des stations depuis le fichier JSON fourni
with open("station_information.json", 'r', encoding='UTF-8') as fichier:
    velib = json.load(fichier)

# Extraire les informations des stations
stations = velib['data']['stations']

# Afficher le nombre de stations
print(f"Nombre de stations: {len(stations)}")
