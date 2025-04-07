%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# Préparer les points pour le diagramme de Voronoï.
# Attention : nos points sont au format (lat, lon). Pour un tracé classique,
# nous plaçons la longitude en abscisse et la latitude en ordonnée.
points_vor = np.array([(station['lat'], station['lon']) for station in stations_data])

# Calculer le diagramme de Voronoï
vor = Voronoi(points_vor)

# Visualiser le diagramme de Voronoï
plt.figure(figsize=(10,10))
# La fonction voronoi_plot_2d trace le diagramme. On désactive l'affichage des sommets pour alléger le graph.
voronoi_plot_2d(vor, show_vertices=False, line_colors='orange', line_width=1.5, line_alpha=0.6, point_size=2)
# Tracer les stations en bleu. Ici, on inverse l'ordre pour que x corresponde à la longitude et y à la latitude.
plt.plot(points_vor[:,1], points_vor[:,0], 'bo', markersize=3)
plt.title("Diagramme de Voronoï des stations Vélib'")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
