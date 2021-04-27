#Uses python3

import sys
from collections import defaultdict
import math

class Vertex():
    def __init__(self, index):
        self.index = index

        self.visited = 0

        # for computing of shortest path
        self.dist = math.inf


class Graph():
    def __init__(self, edges, vertices):

        # create a dict with vertex as key and list of its neighbours as values
        self.adj = defaultdict(list)

        self.edges = edges
                    
        self.vertices = vertices
        self.num_comp = 1
        self.components = defaultdict(lambda : None)
    
    def explore(self, v):

        # pre-vist block
        v.visited = -1
        
        if not self.components[self.num_comp]:
            self.components[self.num_comp] = v

        # explore each neighbour of the vertex 
        for neighbour in self.adj[v]:
            if neighbour.visited == 0:
                self.explore(neighbour)

        # post-visit block
        v.visited = 1
            

    def DFS(self):
        
        for v in self.vertices:
            # explore each vertex (and its neighbours)
            if v.visited == 0:
                self.explore(v)
                # once all neighbours of the vertex have been explored, they form a single connected component
                self.num_comp += 1

        self.num_comp -= 1

    def bellman_ford(self, s):
        
        s.dist = 0
    
        for i in range(len(self.vertices) - 1):

            no_neg_cycle = True

            for ((u, v), w) in self.edges:

                if v.dist > u.dist + w:

                    v.dist = u.dist + w
                    
                    no_neg_cycle = False
            
            if no_neg_cycle:

                break

        return no_neg_cycle

    def negative_cycle(self):
        for s in self.components.values():
            
            no_neg_cycle = self.bellman_ford(s)

            if not no_neg_cycle:

                for ((u, v), w) in self.edges:

                    if v.dist > u.dist + w:

                        v.dist = u.dist + w

                        # negative cycle found
                        return 1

        return 0




def negative_cycle(graph):
    """Given a directed graph with possibly negative edge weights, check whether it contains a cycle of negative weight"""

    # In the problem, the question asked is if there are any negative cycles.  NOTICE that you do not have a source vertex.  The graph that will be provided may have more than one connected components--e.g., there may be no way to convert  from US Dollars to some currency.

    # Does this mean that Bellman-Ford cannot be used in this situation?  Not at all. Here are a few options:

    # Apply Bellman-Ford over every vertex, making it the source. This is the brute force approach. This sounds like a waste of time and it may take a long, long time in a big graph.  While this may help you pass the assignment, that's not optimal.

    # Calculate the connected components and pick one vertex in each connected component and call Bellman-Ford using the vertex as the source.  This is doable.  You need to write an algorithm to implement the connected components. You can adapt one of the algorithms in the Week 1 for this

    # Remember that you may have more than one connected component.  A solution is to create a dummy vertex (say v), create directed edges from v --> any other vertex with a weight of zero and now you can apply Bellman-Ford to using the newly created vertex as the source, iterating a Vth time to see if any edge is relaxed.  The reason why this works is because it allows you to connect v to any other vertex, converting the graph into a connected graph--you can reach any other vertex from the newly created vertex--with zero cost.  Algorithms in C++, 3rd Edition, and Algorithms, 4th Edition, both by Sedgwick, have this as an exercise for the reader.

    # Similarly, instead of creating a new vertex, you can initialize all distances to zero instead of infinity. The purpose of using zero is--IMO--to make all vertices equidistant and when relaxing the edges the negative cycles will "pop up" in the Vth iteration of Bellman-Ford. Algorithms in C++, 3rd Edition, and Algorithms, 4th Edition, both by Sedgwick, ALSO have this as an exercise for the reader.
    graph.DFS()
    return graph.negative_cycle()
 



    
if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]

    vertices = [Vertex(i) for i in range(n)]

    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]

    edges = [((vertices[a-1], vertices[b-1]), w) for ((a, b), w) in edges]

    print(negative_cycle(Graph(edges, vertices)))
