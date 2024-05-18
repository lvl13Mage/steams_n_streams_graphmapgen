import numpy as np
import scipy as sp
from json import load, dump
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
 
 
def generate_graph(n, w, h):
    x = np.random.randint(0, w, dtype=int, size=n)
    y = np.random.randint(0, h, dtype=int, size=n)
    points = np.array([x, y]).T
    triangulation = sp.spatial.Delaunay(points)
    offsets, neighbours = triangulation.vertex_neighbor_vertices
    offsets = [*offsets, len(neighbours)]
    edges = np.array([
        sorted((i, neighbour))
        for i, (start, end) in enumerate(zip(offsets[:-1], offsets[1:]))
        for neighbour in neighbours[start:end]
    ])
 
    return points, edges
 
 
def plot_graph(points, edges):
    plt.plot(*points.T, 'rx')
    plt.gca().add_collection(LineCollection(points[edges]))
    plt.show()
 
 
def to_json(points, edges, path):
    with open(path, 'w') as f:
        dump(dict(points=points.tolist(), edges=edges.tolist()), f)
 
 
def to_graph(path):
    with open(path, 'r') as f:
        json = load(f)
        return (
            np.array(json['points'], dtype=int),
            np.array(json['edges'], dtype=int),
        )
 
 
def main():
    graph = generate_graph(n=1000, w=800, h=600)
    plot_graph(*graph)
    to_json(*graph, 'test.json')
    graph = to_graph('test.json')
 
    print(graph)
 
 
if __name__ == '__main__': main()