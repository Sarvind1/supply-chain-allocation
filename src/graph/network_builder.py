"""Network builder for constructing supply chain graph."""

from typing import List, Dict, Any, Set, Tuple
import networkx as nx

from ..models import Node, Edge, NetworkGraph


class NetworkBuilder:
    """Builds and manages the supply chain network graph."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes_data: Dict[str, Node] = {}
        self.edges_data: List[Edge] = []
        
    def build(self, nodes: List[Node], edges: List[Edge]) -> NetworkGraph:
        """Build network graph from nodes and edges."""
        # Store data
        self.nodes_data = {node.name: node for node in nodes}
        self.edges_data = edges
        
        # Add nodes to graph
        for node in nodes:
            self.graph.add_node(
                node.name,
                node_group=node.node_group,
                stage=node.stage,
                cluster=node.cluster,
                cost_method=node.cost_method,
                feasibility_method=node.feasibility_method,
                lt_method=node.lt_method
            )
        
        # Add edges to graph
        for edge in edges:
            self.graph.add_edge(
                edge.node1,
                edge.node2,
                cost_method=edge.cost_method,
                feasibility_method=edge.feasibility_method,
                lt_method=edge.lt_method
            )
        
        return NetworkGraph(
            nodes=self.nodes_data,
            edges={f"{e.node1}->{e.node2}": e for e in edges},
            graph=self.graph
        )
    
    def validate_connectivity(self) -> None:
        """Validate that the graph is properly connected."""
        # Find supplier nodes (stage 1)
        suppliers = [n for n, d in self.graph.nodes(data=True) if d['stage'] == 1]
        if not suppliers:
            raise ValueError("No supplier nodes found (stage 1)")
        
        # Find FC nodes (highest stage)
        max_stage = max(d['stage'] for n, d in self.graph.nodes(data=True))
        fcs = [n for n, d in self.graph.nodes(data=True) if d['stage'] == max_stage]
        if not fcs:
            raise ValueError(f"No FC nodes found (stage {max_stage})")
        
        # Check if at least one path exists from any supplier to any FC
        has_path = False
        for supplier in suppliers:
            for fc in fcs:
                if nx.has_path(self.graph, supplier, fc):
                    has_path = True
                    break
            if has_path:
                break
        
        if not has_path:
            raise ValueError("No path exists from suppliers to FCs")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get network statistics."""
        stages = {}
        for node, data in self.graph.nodes(data=True):
            stage = data['stage']
            if stage not in stages:
                stages[stage] = []
            stages[stage].append(node)
        
        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'stages': stages,
            'is_connected': nx.is_weakly_connected(self.graph)
        }
    
    def find_all_paths(self, source: str, max_length: int = 5) -> List[List[str]]:
        """Find all paths from source to any FC node."""
        # Find all FC nodes (highest stage)
        max_stage = max(d['stage'] for n, d in self.graph.nodes(data=True))
        fc_nodes = [n for n, d in self.graph.nodes(data=True) if d['stage'] == max_stage]
        
        all_paths = []
        for fc in fc_nodes:
            try:
                # Use cutoff to limit path length
                paths = list(nx.all_simple_paths(
                    self.graph, 
                    source, 
                    fc, 
                    cutoff=max_length
                ))
                all_paths.extend(paths)
            except nx.NetworkXNoPath:
                continue
        
        return all_paths
    
    def get_node(self, node_name: str) -> Node:
        """Get node data by name."""
        return self.nodes_data.get(node_name)
    
    def get_edge_data(self, node1: str, node2: str) -> Dict[str, Any]:
        """Get edge data between two nodes."""
        if self.graph.has_edge(node1, node2):
            return self.graph[node1][node2]
        return {}
