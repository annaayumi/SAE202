from scipy.spatial import Voronoi
import folium
import numpy as np

# Préparation des points
coords_latlon = np.array([(station['lat'], station['lon']) for station in stations_data])
coords_lonlat = np.array([(station['lon'], station['lat']) for station in stations_data])  # Pour Voronoï
triangulation = Delaunay(coords_latlon)
vor = Voronoi(coords_lonlat)

# Création de la carte
carte_combinee = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Ajout des stations (bleu)
for station in stations_data:
    folium.CircleMarker(
        location=[station['lat'], station['lon']],
        radius=3,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(carte_combinee)

# Triangles de Delaunay (vert)
for simplex in triangulation.simplices:
    polygone = [tuple(coords_latlon[i]) for i in simplex]
    folium.Polygon(locations=polygone, color="green", weight=0.5).add_to(carte_combinee)

# Arêtes de Voronoï (rouge)
for ridge_vertices in vor.ridge_vertices:
    if -1 in ridge_vertices:
        continue  # Ignore les bords infinis
    pt1 = vor.vertices[ridge_vertices[0]]
    pt2 = vor.vertices[ridge_vertices[1]]
    folium.PolyLine(
        locations=[(pt1[1], pt1[0]), (pt2[1], pt2[0])],
        color="red",
        weight=1
    ).add_to(carte_combinee)

# Ajout d'une légende
legende_html = """
<div style="position: fixed;
bottom: 50px; left: 50px; width: 220px; height: 110px;
background: white; z-index:9999; font-size:14px; padding:10px; border:1px solid gray;">
<b>Légende :</b><br>
<span style="color:blue;">●</span> Stations Vélib'<br>
<span style="color:green;">▭</span> Triangles de Delaunay<br>
<span style="color:red;">―</span> Arêtes de Voronoï
</div>
"""
carte_combinee.get_root().html.add_child(folium.Element(legende_html))

# Sauvegarde et affichage
carte_combinee.save("velib_delaunay_voronoi.html")
display(carte_combinee)
