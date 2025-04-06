import numpy as np
from scipy.spatial import Delaunay

# ETAPE 2 : Triangulation de Delaunay avec SciPy
# Extraire les coordonnées géographiques
coordonnees = np.array([(station['lat'], station['lon']) for station in stations])

# Générer la triangulation de Delaunay
triangulation = Delaunay(coordonnees)


# ETAPE 3 : Visualisation sur une carte
import folium
# Créer une carte centrée sur Paris
carte = folium.Map(location=[48.8566, 2.3522], zoom_start=11)

# Ajouter des marqueurs pour chaque station
for station in stations:
    folium.CircleMarker(
        location=[station['lat'], station['lon']],
        radius=station['capacity'] // 4,
        color='blue',
        weight=0.5,
        fill=True,
        fill_color='blue'
    ).add_to(carte)

# Ajouter les triangles de Delaunay
for simplexe in triangulation.simplices:
    polygone = [tuple(coordonnees[sommet]) for sommet in simplexe]
    folium.Polygon(locations=polygone, color="green", weight=0.5).add_to(carte)

# Ajouter une légende
legende_html = """
<div style="position: fixed;
bottom: 50px; left: 50px; width: 200px; height: 100px;
background: white; z-index: 9999; font-size: 14px;
">
&nbsp;&nbsp;&nbsp; <i class="fa fa-map-marker fa-2x" style="color: blue"></i> Stations<br>
&nbsp;&nbsp;&nbsp; <i class="fa fa-draw-polygon fa-2x" style="color: green"></i> Triangles de Delaunay
</div>
"""
carte.get_root().html.add_child(folium.Element(legende_html))

# Sauvegarder et afficher la carte
carte.save('velib_stations_delaunay.html')
carte

# ETAPE 4 : Transcription en Liste d'Adjacence
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

liste_adjacence = construire_liste_adjacence(triangulation, stations)

# Afficher la liste d'adjacence pour vérification
print(liste_adjacence)
