"""Test data models."""

import pytest
from datetime import date

from src.models import Product, Chunk, Node, Edge


def test_product_validation():
    """Test product model validation."""
    # Valid product
    product = Product(
        razin="R1",
        asin="A1",
        qty=100,
        cm3=1.5,
        mc_volume=0.1,
        is_oversize=0,
        parcels_per_mc=10
    )
    assert product.razin == "R1"
    assert product.currency == "USD"  # Default value
    
    # Invalid quantity
    with pytest.raises(ValueError):
        Product(
            razin="R1",
            asin="A1",
            qty=0,  # Must be > 0
            cm3=1.5,
            mc_volume=0.1,
            is_oversize=0,
            parcels_per_mc=10
        )


def test_chunk_creation():
    """Test chunk creation from product."""
    product = Product(
        razin="R1",
        asin="A1",
        qty=100,
        cm3=1.5,
        mc_volume=0.1,
        is_oversize=0,
        parcels_per_mc=10
    )
    
    chunk = Chunk(
        chunk_id="chunk-001",
        product=product,
        ready_date=date.today()
    )
    
    assert chunk.razin == "R1"
    assert chunk.qty == 100
    assert chunk.cm3 == 1.5
    assert chunk.origin == "Supplier"  # Default


def test_node_validation():
    """Test node model validation."""
    # Valid node
    node = Node(
        name="Shanghai",
        node_group="Source Port",
        stage=2,
        cluster="CN",
        cost_method="0",
        feasibility_method="1",
        lt_method="0"
    )
    assert node.name == "Shanghai"
    
    # Supplier node with empty name
    supplier = Node(
        name="",
        node_group="Supplier",
        stage=1,
        cluster="Source"
    )
    assert supplier.name == "Supplier"  # Auto-filled


def test_edge_validation():
    """Test edge model validation."""
    edge = Edge(
        node1="Shanghai",
        node2="Los Angeles",
        cost_method="cluster_costs",
        feasibility_method="1",
        lt_method="21"
    )
    assert edge.node1 == "Shanghai"
    assert edge.node2 == "Los Angeles"