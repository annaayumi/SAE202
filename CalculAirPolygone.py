from scipy.spatial import Voronoi
import numpy as np

def aire_polygone(points):
    """Calcule l’aire d’un polygone à partir de la formule de Shoelace"""
    x = points[:, 0]
    y = points[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

# Récupérer les points (lat, lon)
points = np.array([(station['lat'], station['lon']) for station in stations_data])
vor = Voronoi(points)

aires = []
for point_idx, region_idx in enumerate(vor.point_region):
    region = vor.regions[region_idx]
    if -1 in region or len(region) == 0:
        continue  # Ignore les cellules infinies
    sommets = np.array([vor.vertices[i] for i in region])
    aire = aire_polygone(sommets)
    aires.append(aire)

aires = np.array(aires)
moyenne = np.mean(aires)
ecart_type = np.std(aires)
cv = ecart_type / moyenne

print(f"Nombre de cellules considérées : {len(aires)}")
print(f"Moyenne des aires : {moyenne:.6f}")
print(f"Écart-type des aires : {ecart_type:.6f}")
print(f"Coefficient de variation (CV) : {cv:.4f}")
