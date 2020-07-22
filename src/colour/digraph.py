"""
Abstract Data Type: DiGraph
---------------------------

DiGraph implementation created by me by adapting the
implementation found in Micahel Goodrich's book
'Data Structures & Algorithms'. This implementation uses
an adjaceny map to hold the structure of the graph.

TODO:
    Adjust class to support adding weights to edges.
    This will allow me to weight edges according to how long
    each colour_space conversion takes. In the case that I expand
    the colour spaces my Conversion Graph can handle, this would
    allow me to pick the fastest route between colour spaces.
"""


class DiGraph:
    # ------ Nested Classes
    class Vertex:
        __slots__ = "_element"
        def __init__(self, element):
            self._element = element

        def element(self):
            return self._element

        def __hash__(self):
            return hash(id(self))

    class Edge:
        __slots__ = "_origin", "_destination", "_element"
        def __init__(self, start, end, element):
            self._origin = start
            self._destination = end
            self._element = element

        def endpoints(self):
            return (self._origin, self._destination)

        def opposite(self, vert):
            if vert is self._origin:
                return self._destination

            else:
                return self._origin

        def element(self):
            return self._element

        def __hash__(self):
            return hash((self._origin, self._destination))

    # ------ Class Methods
    def __init__(self):
        self._outgoing = {}
        self._incoming = {}
        self._vertices = {}

    def __contains__(self, value):
        return value in self._outgoing or value in self._vertices

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return self._outgoing.keys()

    def edge_count(self):
        edge_count = 0
        for vertex in self._outgoing:
            edge_count += len(self._outgoing[vertex])
        return edge_count

    def edges(self):
        edge_list = []
        for secondary_map in self._outgoing.values():
            edge_list.extend(secondary_map.values())
        return edge_list

    def get_edge(self, start, end):
        return self._outgoing[start].get(end)

    def degree(self, vertex, direction):
        if direction == "in":
            return len(self._incoming[vertex])
        elif direction == "out":
            return len(self._outgoing[vertex])
        elif direction == "all":
            return self.degree(vertex, "in") + self.degree(vertex, "out")
        else:
            raise ValueError(f"{direction} is not 'in', 'out' or 'all")

    def incident_edges(self, vertex, outgoing=True):
        if outgoing:
            vert_map = self._outgoing
        else:
            vert_map = self._incoming

        for edge in vert_map[vertex].values():
            yield edge

    def insert_vertex(self, element=None):
        vertex = self.Vertex(element)
        self._vertices[element] = vertex
        self._outgoing[vertex] = {}
        self._incoming[vertex] = {}
        return vertex

    def insert_edge(self, start, end, element=None):
        edge = self.Edge(start,end, element)
        self._outgoing[start][end] = edge
        self._incoming[end][start] = edge
        return edge


    def dfs(self, current_vert, discovered):
        for edge in self.incident_edges(current_vert):
            next_vert = edge.opposite(current_vert)
            if next_vert not in discovered:
                discovered[next_vert] = edge
                self.dfs(next_vert, discovered)

    def bfs(self, start_vert, discovered):
        level = [start_vert]
        while len(level) > 0:
            next_level = []
            for vert in level:
                for edge in self.incident_edges(vert):
                    next_vert = edge.opposite(vert)
                    if next_vert not in discovered:
                        discovered[next_vert] = edge
                        next_level.append(next_vert)
            level = next_level
        return discovered

    def find_vert(self, element):
        return self._vertices[element]

    def search(self, start_vert, search_type):
        discovered = {}

        if search_type == "dfs":
            self.dfs(start_vert, discovered)
        elif search_type == "bfs":
            self.bfs(start_vert, discovered)
        else:
            raise ValueError("search_type must be 'bfs' or 'dfs'")
        return discovered

    def construct_path(self, start_vert, end_vert, discovered):
        path = []

        if end_vert in discovered:
            next_vert = end_vert

            while next_vert is not start_vert:
                path.append(discovered[next_vert])
                next_vert = discovered[next_vert].opposite(next_vert)

        return path[::-1]

    def find_path(self, start_element, end_element, search_type):
        start_vert = self.find_vert(start_element)
        end_vert = self.find_vert(end_element)
        discovered = self.search(start_vert, search_type)
        path = self.construct_path(start_vert, end_vert, discovered)
        return path

if __name__ == "__main__":
    graph = DiGraph()
    rgb = graph.insert_vertex("rgb")
    xyz = graph.insert_vertex("xyz")
    hsv = graph.insert_vertex("hsv")
    lab = graph.insert_vertex("lab")
    hcl = graph.insert_vertex("hcl")

    graph.insert_edge(rgb, xyz, "rgb_to_xyz")
    graph.insert_edge(xyz, rgb, "xyz_to_rgb")
    graph.insert_edge(xyz, lab, "xyz_to_lab")
    graph.insert_edge(lab, xyz, "lab_to_xyz")
    graph.insert_edge(lab, hcl, "lab_to_hcl")
    graph.insert_edge(hcl, lab, "hcl_to_lab")

    graph.insert_edge(rgb, hsv, "rgb_to_hsv")
    graph.insert_edge(hsv, rgb, "hsv_to_rgb")

    path = graph.find_path("hcl", "hsv", "dfs")
    for i in path:
        print("--> " + i.element())
