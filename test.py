import numpy as np

from main import generate_points
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Vytvorenie fiktívnych dát
# X, y = make_blobs(n_samples=20000, centers=4, random_state=42, cluster_std=0.60)

# DATASET ==> list bodov (x, y)
DATASET = generate_points()

# Konvertovanie DATASETu na numpy array
DATASET = np.array(DATASET)

# Zobrazenie pôvodných dát
plt.scatter(DATASET[:, 0], DATASET[:, 1], cmap='viridis')
plt.title("Pôvodné dáta")
plt.show()

# Aglomeratívne zhlukovanie
model = AgglomerativeClustering(n_clusters=4, linkage='single', metric='euclidean')
y_pred = model.fit_predict(DATASET)

# Získanie centroidov pre každý zhluk
centroids = []
for i in range(4):
    cluster_points = DATASET[y_pred == i]
    centroid = np.mean(cluster_points, axis=0)
    centroids.append(centroid)

centroids = np.array(centroids)

# Zobrazenie výsledkov
plt.scatter(DATASET[:, 0], DATASET[:, 1], c=y_pred, cmap='viridis')
plt.scatter(centroids[:, 0], centroids[:, 1], marker='o', c='red', s=100, label='Centroidy')
plt.title("Aglomeratívne zhlukovanie s centroidom")
plt.show()

# # Vytvorenie dendrogramu
# linked = linkage(DATASET, 'ward')
# dendrogram(linked, orientation='top', distance_sort='descending', show_leaf_counts=True)
# plt.title("Dendrogram")
# plt.show()
