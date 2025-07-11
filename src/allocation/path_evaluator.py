"""Evaluate paths for cost, lead time, and feasibility."""

from typing import List, Dict, Any
from datetime import datetime, timedelta

from ..models import Chunk, EvaluationContext, PathEvaluation
from ..evaluators import BaseEvaluator
from ..graph import NetworkBuilder


class PathEvaluator:
    """Evaluates paths through the network."""
    
    def __init__(self, network_builder: NetworkBuilder, evaluator: BaseEvaluator):
        self.network = network_builder
        self.evaluator = evaluator
        self.graph = network_builder.graph
    
    def evaluate_path(self, chunk: Chunk, path: List[str]) -> PathEvaluation:
        """Evaluate a complete path for a chunk."""
        total_cost = 0.0
        total_lead_time = 0
        feasible = True
        evaluations = []
        
        # Evaluate each node in the path
        for node_name in path:
            node = self.network.get_node(node_name)
            
            # Create context for node evaluation
            context = EvaluationContext(
                chunk=chunk,
                current_node=node_name,
                method=node.cost_method,
                supplemental_data={
                    "node_group": node.node_group,
                    "cluster": node.cluster
                }
            )
            
            # Evaluate node cost
            if node.cost_method != "0":
                cost = self.evaluator.evaluate(context)
                total_cost += cost
                evaluations.append({
                    "type": "node",
                    "name": node_name,
                    "cost": cost
                })
            
            # Evaluate node feasibility
            context.method = node.feasibility_method
            if node.feasibility_method != "1":
                feas = self.evaluator.evaluate(context)
                feasible = feasible and feas
                evaluations.append({
                    "type": "node_feasibility",
                    "name": node_name,
                    "feasible": feas
                })
            
            # Evaluate node lead time
            context.method = node.lt_method
            if node.lt_method != "0":
                lt = self.evaluator.evaluate(context)
                total_lead_time += int(lt)
                evaluations.append({
                    "type": "node_lt",
                    "name": node_name,
                    "lead_time": lt
                })
        
        # Evaluate edges between nodes
        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            
            # Get edge data
            edge_data = self.graph[from_node][to_node]
            
            # Get cluster info for context
            from_cluster = self.graph.nodes[from_node].get("cluster", "")
            to_cluster = self.graph.nodes[to_node].get("cluster", "")
            
            # Create context for edge evaluation
            context = EvaluationContext(
                chunk=chunk,
                from_node=from_node,
                to_node=to_node,
                method=edge_data["cost_method"],
                supplemental_data={
                    "from_cluster": from_cluster,
                    "to_cluster": to_cluster
                }
            )
            
            # Evaluate edge cost
            if edge_data["cost_method"] != "0":
                cost = self.evaluator.evaluate(context)
                total_cost += cost
                evaluations.append({
                    "type": "edge",
                    "from": from_node,
                    "to": to_node,
                    "cost": cost
                })
            
            # Evaluate edge feasibility
            context.method = edge_data["feasibility_method"]
            if edge_data["feasibility_method"] != "1":
                feas = self.evaluator.evaluate(context)
                feasible = feasible and feas
                evaluations.append({
                    "type": "edge_feasibility",
                    "from": from_node,
                    "to": to_node,
                    "feasible": feas
                })
            
            # Evaluate edge lead time
            context.method = edge_data["lt_method"]
            if edge_data["lt_method"] != "0":
                lt = self.evaluator.evaluate(context)
                total_lead_time += int(lt)
                evaluations.append({
                    "type": "edge_lt",
                    "from": from_node,
                    "to": to_node,
                    "lead_time": lt
                })
        
        # Calculate CM3 score
        cm3_score = chunk.cm3 / total_cost if total_cost > 0 else float('inf')
        
        return PathEvaluation(
            path=path,
            total_cost=total_cost,
            total_lead_time=total_lead_time,
            feasible=feasible,
            cm3_score=cm3_score,
            evaluations=evaluations
        )