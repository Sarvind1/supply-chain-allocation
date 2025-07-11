"""Test allocation algorithm."""

import pytest
from datetime import datetime

from src.models import Product, Chunk, Node, Edge
from src.graph import NetworkBuilder
from src.evaluators import SimpleEvaluator
from src.allocation import Allocator


def create_test_network():
    """Create a simple test network."""
    nodes = [
        Node(name="Supplier", node_group="Supplier", stage=1, cluster="Source"),
        Node(name="Port1", node_group="Source Port", stage=2, cluster="CN"),
        Node(name="Port2", node_group="Destination Port", stage=3, cluster="US"),
        Node(name="FC", node_group="FC", stage=4, cluster="US")
    ]
    
    edges = [
        Edge(node1="Supplier", node2="Port1", lt_method="7"),
        Edge(node1="Port1", node2="Port2", cost_method="100", lt_method="21"),
        Edge(node1="Port2", node2="FC", cost_method="50", lt_method="2")
    ]
    
    builder = NetworkBuilder()
    builder.build(nodes, edges)
    return builder


def test_simple_allocation():
    """Test basic allocation flow."""
    # Create network
    network = create_test_network()
    
    # Create evaluator
    config = {"evaluator_type": "simple"}
    evaluator = SimpleEvaluator(config)
    
    # Create allocator
    allocator = Allocator(network, evaluator)
    
    # Create test product
    product = Product(
        razin="TEST1",
        asin="A1",
        qty=100,
        cm3=2.0,
        mc_volume=0.1,
        is_oversize=0,
        parcels_per_mc=10
    )
    
    # Allocate
    results = allocator.allocate_products([product])
    
    assert len(results) == 1
    result = results[0]
    
    assert result.razin == "TEST1"
    assert result.selected_path == ["Supplier", "Port1", "Port2", "FC"]
    assert result.total_lead_time == 30  # 7 + 21 + 2
    assert result.total_cost == 150  # 100 + 50
    assert result.feasible is True