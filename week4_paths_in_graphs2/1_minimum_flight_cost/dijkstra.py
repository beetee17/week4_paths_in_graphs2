  
#Uses python3

import sys
from collections import defaultdict
from queue import Queue
import math

KEY = 1

class Heap():

    def __init__(self, data, size, key=None):
        self.data = data
        self.size = size
        self.swaps = []
        self.key = key

        if self.key:
           self.data = [(item, key(item)) for item in self.data]
    
    
    # for zero-based indexing
    # left_child of node[i] = 2i + 1
    # right child of node[i] = 2i + 2
    # parent of node[i] = round_up(i/2) - 1

    def get_parent(self, i):
        index = math.ceil(i/2) - 1
        return index if index > 0 and index < self.size else i

    def get_left_child(self, i):
        index = 2*i + 1
        return index if index < self.size else i

    def get_right_child(self, i):
        index = 2*i + 2
        return index if index < self.size else i

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.swaps.append((i, j))

    def sift_down(self, i):
        # to sift a node down in min heap, check that it is strictly greater than any of its children. 
        # If both are >, swap it with the greater of the 2 children
        # If one of them are >, swap with that child
        # If neither are >, do nothing


        left_child_i = self.get_left_child(i)
        right_child_i = self.get_right_child(i)

        if self.key:

            global KEY
    
            node = self.data[i][KEY]
            left_child = self.data[left_child_i][KEY]
            right_child = self.data[right_child_i][KEY]

        else:
            node = self.data[i]
            left_child = self.data[left_child_i]
            right_child = self.data[right_child_i]

        if node > left_child and node > right_child:

            if left_child <= right_child:
                j =  left_child_i

            else:
                j = right_child_i

            self.swap(i, j)
            self.sift_down(j)
        
        elif node > left_child:
            j = left_child_i
            self.swap(i, j)
            self.sift_down(j)
        
        elif node > right_child:
            j = right_child_i
            self.swap(i, j)
            self.sift_down(j)

    
    # to build a min heap from an array, sift down all nodes from the top to second-last layer (nodes i = n/2 to 1, n = len(array))
    def build_heap(self):
        for i in range(self.size//2, -1, -1):
            self.sift_down(i)
    
    def insert(self, element):
        if self.key:
            self.data = [(element, self.key(element))] + self.data
        else:
            self.data = [element] + self.data

        self.sift_down(0)
        self.size += 1

    def extractMin(self):
        if self.key:

            min_item = self.data[0][0]

        else:

            min_item = self.data[0]

        self.data = self.data[1:]
        self.size -= 1

        if self.size > 0:
            self.sift_down(0)

        return min_item

    def isEmpty(self):
        return self.size == 0

class Vertex():
    def __init__(self, index):
        self.index = index

        self.visited = 0

        self.pre = None
        self.post = None

        # for computing of shortest path
        self.dist = math.inf

        # for computing layer of vertex in tree and retracing shortest path  
        self.prev = None


class Graph():
    def __init__(self, edges, vertices):

        # create a dict with vertex as key and list of its neighbours as values
        self.adj = defaultdict(list)

        self.edges = edges

        # for a directed graph with edge weights, b is adjacent to a with cost of w but not vice versa
        for ((a, b), w) in edges:
            self.adj[vertices[a-1]].append((vertices[b-1], w))
                    
        self.vertices = vertices

    def get_shortest_path(self, s):
        """Given the index of a source vertex, compute the shortest path lengths of all vertices reachable from the source"""

        s = self.vertices[s]
        s.dist = 0

        # use a binary min heap as priority queue for constant time extraction of min dist vertex
        minHeap = Heap(self.vertices[:], len(self.vertices), key=lambda x: x.dist)

        minHeap.build_heap()

        known_region = []

        # stop iterating once all vertices are of known distances
        while len(known_region) < len(self.vertices):

            u = minHeap.extractMin()

            if not u in known_region:
                known_region.append(u)

            for (v, w) in self.adj[u]:

                if v.dist > u.dist + w and not v in known_region:

                    v.dist = u.dist + w

                    # for backtracing of shortest path
                    v.prev = u

                    minHeap.insert(v)
       





def distance(graph, u, v):
    """"Given a directed graph with positive edge weights, and the indices of 2 vertices u and v, return the length of the shortest path from u to v using dijkstra's algorithm. Return -1 if there is no path i.e. v is not reachable from u"""
    graph.get_shortest_path(u)
    result = graph.vertices[v].dist
   

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
