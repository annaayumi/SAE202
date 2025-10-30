%matplotlib inline
import numpy as np
from scipy.spatial import Delaunay
import json
import folium
from IPython.display import display
import matplotlib.pyplot as plt
import math
import networkx as nx

# --- Chargement des données ---
json_file = "station_information.json"
with open(json_file, 'r', encoding='UTF-8') as file:
    velib = json.load(file)
stations_data = velib['data']['stations']

# --- Étape 2 : Triangulation de Delaunay ---
coordonnees = np.array([(station['lat'], station['lon']) for station in stations_data])
triangulation = Delaunay(coordonnees)

# --- Étape 3 : Carte Folium ---
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

# --- Étape 4 : Construction de la liste d'adjacence ---
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

# Création d'un dictionnaire pour les positions (lon, lat)
station_coords = {station['station_id']: (station['lon'], station['lat']) for station in stations_data}

# --- Étape 5 : Construction du graphe pondéré et calcul du MST ---
def distance(coord1, coord2):
    return math.sqrt((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2)

G = nx.Graph()

# Ajout des nœuds
for station in stations_data:
    station_id = station['station_id']
    G.add_node(station_id, pos=(station['lon'], station['lat']))

# Ajout des arêtes pondérées (à partir de la liste d'adjacence)
for station_id, voisins in liste_adjacence.items():
    for voisin in voisins:
        if G.has_edge(station_id, voisin):
            continue
        coord1 = station_coords[station_id]
        coord2 = station_coords[voisin]
        w = distance(coord1, coord2)
        G.add_edge(station_id, voisin, weight=w)

# Calcul du MST
mst = nx.minimum_spanning_tree(G)

# --- Étape 6 : Visualisation combinée du réseau et du MST ---
plt.figure(figsize=(10, 10))

# 1. Afficher toutes les arêtes du réseau en gris clair
for edge in G.edges():
    n1, n2 = edge
    x1, y1 = G.nodes[n1]['pos']
    x2, y2 = G.nodes[n2]['pos']
    plt.plot([x1, x2], [y1, y2], lw=0.3, color='gray')

# 2. Superposer le MST en rouge
for edge in mst.edges():
    n1, n2 = edge
    x1, y1 = G.nodes[n1]['pos']
    x2, y2 = G.nodes[n2]['pos']
    plt.plot([x1, x2], [y1, y2], lw=1.5, color='black')

# 3. Afficher les nœuds (points bleus)
for station_id in G.nodes():
    x, y = G.nodes[station_id]['pos']
    plt.plot(x, y, 'bo', markersize=3)

plt.title("Réseau complet et arbre couvrant minimal (MST) du réseau Vélib'")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)
plt.show()
