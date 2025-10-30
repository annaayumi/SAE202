from scipy.spatial import Voronoi
import folium

# Étape 1 : Calcul du diagramme de Voronoï
# Inverser les coordonnées (lon, lat) pour Voronoï
points_voronoi = np.array([(station['lon'], station['lat']) for station in stations_data])
vor = Voronoi(points_voronoi)

# Étape 2 : Création d'une carte Folium centrée sur Paris
carte_voronoi = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Ajouter les stations sur la carte
for station in stations_data:
    folium.CircleMarker(
        location=[station['lat'], station['lon']],
        radius=3,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(carte_voronoi)

# Étape 3 : Tracer les arêtes de Voronoï
for ridge_vertices in vor.ridge_vertices:
    if -1 in ridge_vertices:
        continue  # Ignore les arêtes infinies
    point1 = vor.vertices[ridge_vertices[0]]
    point2 = vor.vertices[ridge_vertices[1]]
    folium.PolyLine(
        locations=[(point1[1], point1[0]), (point2[1], point2[0])],
        color="red",
        weight=1
    ).add_to(carte_voronoi)

# Sauvegarder la carte avec le diagramme de Voronoï
carte_voronoi.save("velib_voronoi.html")
display(carte_voronoi)
