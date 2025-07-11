"""Evaluation context and result models."""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

from .product import Chunk
from .network import Node, Edge


class EvaluationContext(BaseModel):
    """Context for evaluator execution."""
    
    chunk: Chunk = Field(..., description="Chunk being evaluated")
    from_node: Optional[str] = Field(None, description="Origin node")
    to_node: Optional[str] = Field(None, description="Destination node")
    current_node: Optional[str] = Field(None, description="Current node")
    method: str = Field(..., description="Evaluator method name")
    supplemental_data: Dict[str, Any] = Field(default_factory=dict)
    
    @property
    def cache_key(self) -> str:
        """Generate cache key for memoization."""
        parts = [self.method]
        
        if self.from_node and self.to_node:
            parts.extend([self.from_node, self.to_node])
        elif self.current_node:
            parts.append(self.current_node)
        
        # Add relevant chunk attributes
        parts.extend([
            str(self.chunk.qty),
            str(self.chunk.product.is_oversize),
            self.chunk.product.razin
        ])
        
        return ":".join(parts)


class PathEvaluation(BaseModel):
    """Evaluation results for a path."""
    
    path: List[str] = Field(..., description="Node sequence")
    total_cost: float = Field(..., ge=0, description="Total path cost")
    total_lead_time: int = Field(..., ge=0, description="Total days")
    feasible: bool = Field(..., description="Path feasibility")
    cm3_score: float = Field(..., description="CM3 / cost ratio")
    evaluations: List[Dict[str, Any]] = Field(default_factory=list)


class AllocationResult(BaseModel):
    """Final allocation result."""
    
    chunk_id: str = Field(..., description="Allocated chunk")
    razin: str = Field(..., description="Product SKU")
    selected_path: List[str] = Field(..., description="Chosen path")
    total_cost: float = Field(..., ge=0)
    total_lead_time: int = Field(..., ge=0)
    cm3_score: float = Field(...)
    eta: datetime = Field(..., description="Estimated arrival")
    feasible: bool = Field(...)
    stockout_risk: bool = Field(default=False)