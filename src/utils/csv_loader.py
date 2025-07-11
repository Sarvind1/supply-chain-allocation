"""CSV data loading utilities."""

import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

from ..models import Product, Node, Edge


def load_products(filepath: Path) -> List[Product]:
    """Load products from CSV."""
    df = pd.read_csv(filepath)
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Map to expected names
    column_map = {
        'razin_(sku)': 'razin',
        'master_carton_volume': 'mc_volume',
        'is_oversize': 'is_oversize',
        'parcels_per_mc': 'parcels_per_mc'
    }
    df.rename(columns=column_map, inplace=True)
    
    products = []
    for _, row in df.iterrows():
        products.append(Product(**row.to_dict()))
    
    return products


def load_nodes(filepath: Path) -> List[Node]:
    """Load nodes from CSV."""
    df = pd.read_csv(filepath)
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Handle empty node names for Supplier
    df['node'] = df.apply(
        lambda x: 'Supplier' if pd.isna(x['node']) and x['node_group'] == 'Supplier' else x['node'],
        axis=1
    )
    
    # Convert string methods to str type
    df['cost_method'] = df['cost_method'].astype(str)
    df['feasibility_method'] = df['feasibility_method'].astype(str)
    df['lt_method'] = df['lt_method'].astype(str)
    
    nodes = []
    for _, row in df.iterrows():
        nodes.append(Node(name=row['node'], **row.to_dict()))
    
    return nodes


def load_edges(filepath: Path) -> List[Edge]:
    """Load edges from CSV."""
    df = pd.read_csv(filepath)
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Map to expected names
    column_map = {
        'node_1': 'node1',
        'node_2': 'node2'
    }
    df.rename(columns=column_map, inplace=True)
    
    # Convert methods to strings
    df['cost_method'] = df['cost_method'].astype(str)
    df['feasibility_method'] = df['feasibility_method'].astype(str)
    df['lt_method'] = df['lt_method'].astype(str)
    
    edges = []
    for _, row in df.iterrows():
        edges.append(Edge(**row.to_dict()))
    
    return edges


def validate_network_integrity(nodes: List[Node], edges: List[Edge]) -> None:
    """Validate that all edge nodes exist in node list."""
    node_names = {node.name for node in nodes}
    
    for edge in edges:
        if edge.node1 not in node_names:
            raise ValueError(f"Edge references unknown node: {edge.node1}")
        if edge.node2 not in node_names:
            raise ValueError(f"Edge references unknown node: {edge.node2}")
