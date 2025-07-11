"""Find paths through supply chain network."""

import networkx as nx
from typing import List, Set, Optional
from itertools import islice


class PathFinder:
    """Finds paths through the network."""
    
    def __init__(self, graph: nx.DiGraph, max_hops: int = 5):
        self.graph = graph
        self.max_hops = max_hops
    
    def find_all_paths(self, origin: str, destinations: Set[str]) -> List[List[str]]:
        """Find all paths from origin to any destination."""
        all_paths = []
        
        for dest in destinations:
            if nx.has_path(self.graph, origin, dest):
                # Get all simple paths up to max_hops length
                paths = nx.all_simple_paths(
                    self.graph, 
                    origin, 
                    dest, 
                    cutoff=self.max_hops
                )
                all_paths.extend(paths)
        
        return all_paths
    
    def find_shortest_paths(self, origin: str, destinations: Set[str], k: int = 3) -> List[List[str]]:
        """Find k-shortest paths to each destination."""
        shortest_paths = []
        
        for dest in destinations:
            if nx.has_path(self.graph, origin, dest):
                try:
                    # Get k shortest paths
                    paths = list(islice(
                        nx.shortest_simple_paths(self.graph, origin, dest),
                        k
                    ))
                    shortest_paths.extend(paths)
                except nx.NetworkXNoPath:
                    continue
        
        return shortest_paths
    
    def get_path_edges(self, path: List[str]) -> List[tuple]:
        """Get edge pairs for a path."""
        edges = []
        for i in range(len(path) - 1):
            edges.append((path[i], path[i + 1]))
        return edges
    
    def validate_path(self, path: List[str]) -> bool:
        """Check if path is valid in the graph."""
        if len(path) < 2:
            return False
        
        for i in range(len(path) - 1):
            if not self.graph.has_edge(path[i], path[i + 1]):
                return False
        
        return True
