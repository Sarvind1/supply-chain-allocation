#!/usr/bin/env python3
"""Visualize the supply chain network."""

import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.utils import load_nodes, load_edges
from src.graph import NetworkBuilder


def visualize_network(nodes_file, edges_file, output_file="network_graph.png"):
    """Create network visualization."""
    # Load data
    nodes = load_nodes(Path(nodes_file))
    edges = load_edges(Path(edges_file))
    
    # Build network
    builder = NetworkBuilder()
    graph = builder.build(nodes, edges)
    
    # Create layout
    pos = nx.spring_layout(graph, k=2, iterations=50)
    
    # Color nodes by stage
    node_colors = []
    for node in graph.nodes():
        stage = graph.nodes[node]['stage']
        if stage == 1:
            node_colors.append('lightblue')  # Supplier
        elif stage == 2:
            node_colors.append('lightgreen')  # Source Port
        elif stage == 3:
            node_colors.append('yellow')  # Destination Port
        elif stage == 4:
            node_colors.append('orange')  # Warehouse
        else:
            node_colors.append('red')  # FC
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Draw network
    nx.draw(graph, pos, 
            node_color=node_colors,
            node_size=1500,
            with_labels=True,
            font_size=8,
            font_weight='bold',
            arrows=True,
            arrowsize=20,
            edge_color='gray',
            alpha=0.7)
    
    # Add title and legend
    plt.title("Supply Chain Network", size=16)
    
    # Create legend
    import matplotlib.patches as mpatches
    supplier_patch = mpatches.Patch(color='lightblue', label='Supplier')
    source_patch = mpatches.Patch(color='lightgreen', label='Source Port')
    dest_patch = mpatches.Patch(color='yellow', label='Destination Port')
    wh_patch = mpatches.Patch(color='orange', label='Warehouse')
    fc_patch = mpatches.Patch(color='red', label='FC')
    
    plt.legend(handles=[supplier_patch, source_patch, dest_patch, wh_patch, fc_patch],
               loc='upper right')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Network visualization saved to {output_file}")
    
    # Print network statistics
    print(f"\nNetwork Statistics:")
    print(f"  Nodes: {graph.number_of_nodes()}")
    print(f"  Edges: {graph.number_of_edges()}")
    print(f"  Average degree: {sum(dict(graph.degree()).values()) / graph.number_of_nodes():.2f}")
    

if __name__ == "__main__":
    # Visualize simple network
    visualize_network(
        "data/dummy/nodes_simple.csv",
        "data/dummy/node-node_simple.csv",
        "results/network_simple.png"
    )
    
    # Visualize complex network
    visualize_network(
        "data/dummy/nodes_complex.csv",
        "data/dummy/node-node_complex.csv",
        "results/network_complex.png"
    )
