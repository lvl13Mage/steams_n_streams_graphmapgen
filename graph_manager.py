import json
import os
import networkx as nx
from networkx.readwrite import json_graph
import math
import numpy as np
from scipy.spatial import Delaunay
from pprint import pprint

class GraphManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.num_nodes = 20
        self.path = 'map.json'
        if not self.from_json():
            self.points, self.edges = self.generate_graph()
            self.to_json()
            print('Generated new graph')

    def from_json(self):
        print('Loading graph from file')
        # check if file exists
        if not os.path.exists(self.path):
            return False
        with open(self.path, 'r') as f:
            data = json.load(f)
            self.points = np.array(data['points'], dtype=int)
            self.edges = np.array(data['edges'], dtype=int)
            self.num_nodes = len(self.points)
        return True

    def generate_graph(self):
        x = np.random.randint(0, self.width, dtype=int, size=self.num_nodes)
        y = np.random.randint(0, self.height, dtype=int, size=self.num_nodes)
        points = np.array([x, y]).T
        triangulation = Delaunay(points)
        offsets, neighbours = triangulation.vertex_neighbor_vertices
        offsets = [*offsets, len(neighbours)]
        edges = np.array([
            sorted((i, neighbour))
            for i, (start, end) in enumerate(zip(offsets[:-1], offsets[1:]))
            for neighbour in neighbours[start:end]
        ])
    
        return points, edges
    
    def to_json(self):
        with open(self.path, 'w') as f:
            json.dump(dict(points=self.points.tolist(), edges=self.edges.tolist()), f)
