%matplotlib inline
import numpy as np
from scipy.spatial import Delaunay
import json
import folium
from IPython.display import display
import matplotlib.pyplot as plt

# 1) Chargement des données
json_file = "station_information.json"
with open(json_file, 'r', encoding='UTF-8') as file:
    velib = json.load(file)

stations_data = velib['data']['stations']

# 2) Triangulation de Delaunay
coordonnees = np.array([(station['lat'], station['lon']) for station in stations_data])
triangulation = Delaunay(coordonnees)

# 3) Carte Folium
carte = folium.Map(location=[48.8566, 2.3522], zoom_start=11)

for station in stations_data:
    folium.CircleMarker(
        location=[station['lat'], station['lon']],
        radius=station['capacity'] // 4,
        color='blue',
        weight=0.5,
        fill=True,
        fill_color='blue'
    ).add_to(carte)

for simplexe in triangulation.simplices:
    polygone = [tuple(coordonnees[sommet]) for sommet in simplexe]
    folium.Polygon(locations=polygone, color="green", weight=0.5).add_to(carte)

legende_html = """
<div style="position: fixed;
bottom: 50px; left: 50px; width: 200px; height: 100px;
background: white; z-index: 9999; font-size: 14px;">
&nbsp;&nbsp;&nbsp; <i class="fa fa-map-marker fa-2x" style="color: blue"></i> Stations<br>
&nbsp;&nbsp;&nbsp; <i class="fa fa-draw-polygon fa-2x" style="color: green"></i> Triangles de Delaunay
</div>
"""
carte.get_root().html.add_child(folium.Element(legende_html))
carte.save('velib_stations_delaunay.html')
display(carte)

# 4) Construction de la liste d'adjacence
def construire_liste_adjacence(triangulation, stations):
    liste_adjacence = {station['station_id']: [] for station in stations}
    for simplexe in triangulation.simplices:
        for i in range(3):
            index_1 = simplexe[i]
            index_2 = simplexe[(i + 1) % 3]
            station_id_1 = stations[index_1]['station_id']
            station_id_2 = stations[index_2]['station_id']
            if station_id_2 not in liste_adjacence[station_id_1]:
                liste_adjacence[station_id_1].append(station_id_2)
            if station_id_1 not in liste_adjacence[station_id_2]:
                liste_adjacence[station_id_2].append(station_id_1)
    return liste_adjacence

liste_adjacence = construire_liste_adjacence(triangulation, stations_data)

# 5) Visualisation du graphe avec Matplotlib
# Utilise les coordonnées (lon, lat) pour tracer les nœuds et arêtes.
station_coords = {
    station['station_id']: (station['lon'], station['lat'])
    for station in stations_data
}

plt.figure(figsize=(10, 10))

# Tracer les nœuds
for station_id, (x, y) in station_coords.items():
    plt.plot(x, y, 'bo', markersize=3)  # Un petit point bleu
    # Pour alléger, on peut désactiver ou réduire la taille des labels :
    # plt.text(x, y, str(station_id), fontsize=6, ha='right', va='bottom')

# Tracer les arêtes (pour éviter les doublons, on stocke les arêtes déjà tracées)
edges_drawn = set()
for station_id, voisins in liste_adjacence.items():
    for voisin in voisins:
        edge = tuple(sorted((station_id, voisin)))
        if edge not in edges_drawn:
            x1, y1 = station_coords[station_id]
            x2, y2 = station_coords[voisin]
            plt.plot([x1, x2], [y1, y2], 'k-', lw=0.3)
            edges_drawn.add(edge)

plt.title("Graphe du réseau de stations Vélib' (Matplotlib)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)
plt.show()
