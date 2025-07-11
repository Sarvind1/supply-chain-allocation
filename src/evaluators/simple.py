"""Simple evaluator implementations."""

from typing import Any, Union

from .base import BaseEvaluator
from ..models import EvaluationContext
from ..utils import memoize


class SimpleEvaluator(BaseEvaluator):
    """Simple evaluator for fixed values or basic lookups."""
    
    def __init__(self, config: dict):
        self.config = config
    
    @memoize
    def evaluate(self, context: EvaluationContext) -> Union[float, int, bool]:
        """Evaluate based on method type."""
        method = context.method
        
        # Handle numeric methods (fixed values)
        if method.isdigit():
            return float(method)
        
        # Handle always feasible
        if method == "1" and "feasibility" in context.method:
            return True
        
        # Handle no cost/lead time
        if method == "0":
            return 0.0
        
        # Handle named methods
        if method == "cluster_costs":
            return self._evaluate_cluster_cost(context)
        elif method == "cluster_LTs":
            return self._evaluate_cluster_lt(context)
        elif method == "cluster_feas":
            return self._evaluate_cluster_feasibility(context)
        elif method == "wh_cost":
            return self._evaluate_warehouse_cost(context)
        
        # Default fallback
        return self._default_value()
    
    def _evaluate_cluster_cost(self, context: EvaluationContext) -> float:
        """Simple cluster-based cost calculation."""
        # Base rate by cluster pair
        base_rates = {
            ("CN", "US_West"): 1200.0,
            ("CN", "US_East"): 1500.0,
            ("US_West", "US_East"): 300.0,
            ("3PL_East", "US_East"): 50.0,
        }
        
        # Get clusters from context
        from_cluster = context.supplemental_data.get("from_cluster", "")
        to_cluster = context.supplemental_data.get("to_cluster", "")
        
        # Look up base rate
        rate = base_rates.get((from_cluster, to_cluster), 100.0)
        
        # Adjust by quantity
        qty = context.chunk.qty
        return rate * (qty / 1000)  # Per thousand units
    
    def _evaluate_cluster_lt(self, context: EvaluationContext) -> int:
        """Simple cluster-based lead time."""
        # Transit times by cluster pair
        transit_times = {
            ("CN", "US_West"): 21,
            ("CN", "US_East"): 28,
            ("US_West", "US_East"): 5,
            ("3PL_East", "US_East"): 2,
        }
        
        from_cluster = context.supplemental_data.get("from_cluster", "")
        to_cluster = context.supplemental_data.get("to_cluster", "")
        
        return transit_times.get((from_cluster, to_cluster), 7)
    
    def _evaluate_cluster_feasibility(self, context: EvaluationContext) -> bool:
        """Check if route is feasible for product."""
        # Check oversize handling
        if context.chunk.product.is_oversize:
            # Only certain routes can handle oversize
            allowed_clusters = {"US_West", "US_East"}
            to_cluster = context.supplemental_data.get("to_cluster", "")
            return to_cluster in allowed_clusters
        
        return True
    
    def _evaluate_warehouse_cost(self, context: EvaluationContext) -> float:
        """Simple warehouse storage cost."""
        # Storage rate per unit per day
        storage_rate = 0.10
        
        # Assume average 7 days storage
        days = 7
        
        return context.chunk.qty * storage_rate * days
    
    def _default_value(self) -> Any:
        """Return default value based on context."""
        return 0.0