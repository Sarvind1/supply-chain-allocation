"""Network graph data models."""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import networkx as nx


class Node(BaseModel):
    """Network node from Nodes.csv."""
    
    name: str = Field(..., description="Node identifier")
    node_group: str = Field(..., description="Node type")
    stage: int = Field(..., ge=1, le=5, description="Supply chain stage")
    cluster: str = Field(..., description="Geographic/operational cluster")
    cost_method: str = Field(default="0", description="Cost evaluator")
    feasibility_method: str = Field(default="1", description="Feasibility evaluator")
    lt_method: str = Field(default="0", description="Lead time evaluator")
    
    @validator("name")
    def default_supplier(cls, v, values):
        if not v and values.get("node_group") == "Supplier":
            return "Supplier"
        return v


class Edge(BaseModel):
    """Network edge from Node-Node.csv."""
    
    node1: str = Field(..., description="Origin node")
    node2: str = Field(..., description="Destination node")
    cost_method: str = Field(default="0", description="Cost evaluator")
    feasibility_method: str = Field(default="1", description="Feasibility evaluator")
    lt_method: str = Field(default="0", description="Lead time evaluator")
    
    @validator("node1", "node2")
    def validate_nodes(cls, v):
        if not v or not v.strip():
            raise ValueError("Node cannot be empty")
        return v.strip()


class NetworkGraph(BaseModel):
    """Supply chain network graph."""
    
    nodes: List[Node] = Field(default_factory=list)
    edges: List[Edge] = Field(default_factory=list)
    
    class Config:
        arbitrary_types_allowed = True
    
    def to_networkx(self) -> nx.DiGraph:
        """Convert to NetworkX directed graph."""
        G = nx.DiGraph()
        
        # Add nodes with attributes
        for node in self.nodes:
            G.add_node(node.name, **node.dict(exclude={"name"}))
        
        # Add edges with attributes
        for edge in self.edges:
            G.add_edge(edge.node1, edge.node2, **edge.dict(exclude={"node1", "node2"}))
        
        return G