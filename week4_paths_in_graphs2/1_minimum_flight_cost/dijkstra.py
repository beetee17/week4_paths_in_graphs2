#Uses python3

import sys
from collections import defaultdict
from queue import Queue
import math
import heapq


class Vertex():
    def __init__(self, index):
        self.index = index

        # for computing of shortest path
        self.dist = math.inf
        self.prev = None

    def __lt__(self, other):
        return self.dist < other.dist


class Graph():
    def __init__(self, edges, vertices):

        # create a dict with vertex as key and list of its neighbours as values
        self.adj = defaultdict(list)

        self.edges = edges

        # for a directed graph with edge weights, b is adjacent to a with cost of w but not vice versa
        for ((a, b), w) in edges:
            self.adj[vertices[a-1]].append((vertices[b-1], w))
                    
        self.vertices = vertices

        self.heap = None

    def get_shortest_path(self, s, t):
        """Given the index of a source vertex, compute the shortest path lengths of all vertices reachable from the source"""

        s = self.vertices[s]
        s.dist = 0

        self.heap = [s]

        # stop iterating once all vertices are of known distances
        while len(self.heap) > 0:
            
            u = heapq.heappop(self.heap)

            if u.index == t: break

            for (v, w) in self.adj[u]:

                if v.dist > u.dist + w:

                    v.dist = u.dist + w
                    v.prev = u
                    heapq.heappush(self.heap, v)
       

def distance(graph, u, v):
    """"Given a directed graph with positive edge weights, and the indices of 2 vertices u and v, return the length of the shortest path from u to v using dijkstra's algorithm. Return -1 if there is no path i.e. v is not reachable from u"""
    graph.get_shortest_path(u, v)
    result = graph.vertices[v].dist

    v = graph.vertices[v]
    print(v.index+1)
    while v.prev:
        print(v.prev.index+1)
        v = v.prev
   
    return result if not math.isinf(result) else -1


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]

    vertices = [Vertex(i) for i in range(n)]

    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]

    u, v = data[0] - 1, data[1] - 1
    print(distance(Graph(edges, vertices), u, v))
