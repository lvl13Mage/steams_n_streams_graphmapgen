# Braucht numpy, scipy und matplotlib!
 
import numpy as np
import scipy as sp
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
 
 
def generate_edges(points):
    edges = set()
    triangulation = sp.spatial.Delaunay(points)
    offsets, neighbours = triangulation.vertex_neighbor_vertices
    offsets = [*offsets, len(neighbours)]
    for i, (start, end) in enumerate(zip(offsets[:-1], offsets[1:])):
        if start == end: continue
        cluster_edges = {
            (*sorted((i, neighbour)),)
            for neighbour in neighbours[start:end]
        }
        edges |= cluster_edges
 
    return np.array([*edges])
 
 
def connect_clusters(points, centroids, cluster_mapping):
    trees = tuple(
        sp.spatial.KDTree(points[(cluster_mapping == cluster)])
        for cluster in range(centroids.shape[0])
    )
    closest_points = defaultdict(dict)
    for left in range(centroids.shape[0]):
        for right in range(centroids.shape[0]):
            if left == right or right in closest_points[left]: continue
 
            cluster_mask = (cluster_mapping == left)
            point_indices = np.where(cluster_mask == 1)[0]
            left_points = points[cluster_mask]
            distances = np.array([trees[right].query(p) for p in left_points])
            closest = int(distances[:, 1][np.argmin(distances[:, 0])])
            closest_point = trees[right].data[closest]
            for i, p in enumerate(points):
                if all(np.isclose(p, closest_point)):
                    closest_points[left][right] = i
                    break
 
    edges = set()
    for left, right in {(*e,) for e in generate_edges(centroids)}:
        edge = (*sorted(
            (closest_points[left][right], closest_points[right][left])
        ),)
        edges.add(edge)
 
    return edges
 
 
def generate_graph(n, k):
    points = np.random.rand(n, 2)
 
    edges = set()
    centroids, _ = sp.cluster.vq.kmeans(points, k)
    cluster_mapping, _ = sp.cluster.vq.vq(points, centroids)
    for cluster in range(centroids.shape[0]):
        cluster_mask = (cluster_mapping == cluster)
        point_indices = np.where(cluster_mask == 1)[0]
        edges |= {
            (*point_indices[edge],)
            for edge in generate_edges(points[cluster_mask])
        }
    edges = np.array([
        *edges,
        *connect_clusters(points, centroids, cluster_mapping,
    )])
 
    return points, edges, centroids
 
 
def plot_graph():
    points, edges, centroids = generate_graph(n=20, k=4)
    plt.plot(*points.T, 'rx')
    plt.plot(*centroids.T, 'bo')
    plt.gca().add_collection(LineCollection(points[edges]))
    plt.show()
 
 
if __name__ == '__main__': plot_graph()