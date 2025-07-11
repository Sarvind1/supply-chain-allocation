"""Main allocation algorithm."""

from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from ..models import Chunk, Product, AllocationResult
from ..graph import NetworkBuilder, PathFinder
from ..evaluators import BaseEvaluator
from .path_evaluator import PathEvaluator


class Allocator:
    """Allocates chunks to optimal paths."""
    
    def __init__(self, network_builder: NetworkBuilder, evaluator: BaseEvaluator):
        self.network = network_builder
        self.evaluator = evaluator
        self.path_finder = PathFinder(network_builder.graph)
        self.path_evaluator = PathEvaluator(network_builder, evaluator)
    
    def allocate_products(self, products: List[Product]) -> List[AllocationResult]:
        """Allocate all products to optimal paths."""
        results = []
        
        # Convert products to chunks
        chunks = self._create_chunks(products)
        
        # Get destination nodes
        destinations = self.network.get_destinations()
        
        # Allocate each chunk
        for chunk in chunks:
            result = self.allocate_chunk(chunk, destinations)
            if result:
                results.append(result)
        
        return results
    
    def allocate_chunk(self, chunk: Chunk, destinations: set) -> Optional[AllocationResult]:
        """Allocate a single chunk to optimal path."""
        # Find all possible paths
        paths = self.path_finder.find_all_paths(chunk.origin, destinations)
        
        if not paths:
            print(f"No paths found for chunk {chunk.chunk_id}")
            return None
        
        # Evaluate all paths
        best_path = None
        best_evaluation = None
        best_score = -float('inf')
        
        for path in paths:
            evaluation = self.path_evaluator.evaluate_path(chunk, path)
            
            # Skip infeasible paths
            if not evaluation.feasible:
                continue
            
            # Check if this is the best path so far
            if evaluation.cm3_score > best_score:
                best_score = evaluation.cm3_score
                best_path = path
                best_evaluation = evaluation
        
        if not best_path:
            print(f"No feasible path found for chunk {chunk.chunk_id}")
            return None
        
        # Create allocation result
        eta = datetime.now() + timedelta(days=best_evaluation.total_lead_time)
        
        return AllocationResult(
            chunk_id=chunk.chunk_id,
            razin=chunk.razin,
            selected_path=best_path,
            total_cost=best_evaluation.total_cost,
            total_lead_time=best_evaluation.total_lead_time,
            cm3_score=best_evaluation.cm3_score,
            eta=eta,
            feasible=True,
            stockout_risk=False  # TODO: Implement stockout check
        )
    
    def _create_chunks(self, products: List[Product]) -> List[Chunk]:
        """Convert products to chunks for processing."""
        chunks = []
        
        for product in products:
            chunk = Chunk(
                chunk_id=str(uuid.uuid4())[:8],
                product=product,
                origin="Supplier",
                ready_date=datetime.now().date()
            )
            chunks.append(chunk)
        
        return chunks