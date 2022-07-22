from cmath import inf
from typing import List, Tuple

class RiskMap():
    """
    A class to store the chiton risk map
    The risk map is a 2 dimensional array of integers
    """
    def __init__(self,risk_map:List[List[int]]) -> None:
        """Initialise and name the attributes"""
        self.risk_map = risk_map
        # self.y_map_size = len(risk_map)
        self.x_map_size = len(risk_map[0])

    @property
    def y_map_size(self):
        return len(self.risk_map)

    def print_map(self) -> None:
        """Print the risk map"""
        print(self.risk_map)

    def initialise_distances(self):
        """
        Function to create a dictionary of all nodes and initialise the distances to infinity
        Each key is a Tuple of the y and x coordinates
        Each value is infinity
        """
        node_distances = {}
        for y_value in range(self.y_map_size):
            for x_value in range(self.x_map_size):
                node_distances[(y_value,x_value)] = float(inf)
        return node_distances

    def initialise_unvisited_nodes(self):
        """
        Fucntion to create a Set containing all the nodes in the graph
        Each node is a Tuple with a y and x coordinate
        """
        unvisited_nodes = set()
        for y_value in range(self.y_map_size):
            for x_value in range(self.x_map_size):
                unvisited_nodes.add((y_value,x_value))
        return unvisited_nodes

    def get_nodes_neighbours(self,node:Tuple[int]) -> List[Tuple[int]]:
        """Return the node's neighbours' coordinates"""
        neighbour_list = []
        y_coord = node[0]
        x_coord = node[1]
        if node[0] != 0:
            neighbour_list.append((y_coord-1,x_coord))
        if node[0] != self.y_map_size - 1:
            neighbour_list.append((y_coord+1,x_coord))
        if node[1] != 0:
            neighbour_list.append((y_coord,x_coord-1))
        if node[1] != self.x_map_size - 1:
            neighbour_list.append((y_coord,x_coord+1))
        return neighbour_list

    def shortest_path(self, start:Tuple[int], end:Tuple[int]) -> int:
        """
        Calculate the lowest cost path between the start and end coordinates
        Return the cost of the lowest cost path

        visted_nodes is a set that stores the nodes/points as they are visited
        """
        # Mark all points (nodes) in the risk_map as unvisited
        # Assign to every point a Tentative Distance initialised to infinity
        # Set the starting node as current and its tenative distance to 0
        unvisited_nodes = self.initialise_unvisited_nodes()
        node_distances = self.initialise_distances()
        current_node = start
        node_distances[current_node] = 0

        # For the current node consider its unvisited neighbours
        # Calculate for each unvisited neighbour its tentative distance through the current node
        # Compare new tentative distance with the current one and assign the smaller distance
        # Once all unvisited neighbours are processed, mark the current node as visited
        # If destination node has been marked visited then stop
        # Else select the unvisited node with the smallest tentative distance and set as current and LOOP
        while end in unvisited_nodes:
            current_node_distance = node_distances[current_node]
            current_neighbours = self.get_nodes_neighbours(current_node)
            for neighbour in current_neighbours:
                if neighbour not in unvisited_nodes:
                    pass
                else:
                    neighbour_tenative_distance = current_node_distance + self.risk_map[neighbour[0]][neighbour[1]]
                    if neighbour_tenative_distance < node_distances[neighbour]:
                        node_distances[neighbour] = neighbour_tenative_distance
            unvisited_nodes.remove(current_node)
            if current_node == end:
                break
            else:
                smallest_distance = float(inf)
                for node in unvisited_nodes:
                    if node_distances[node] < smallest_distance:
                        smallest_distance = node_distances[node]
                        current_node = node
        return node_distances[end]
