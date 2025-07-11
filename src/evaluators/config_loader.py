"""Load evaluator configurations."""

import json
from pathlib import Path
from typing import Dict, Any

from .base import EvaluatorRegistry
from .simple import SimpleEvaluator


# Register default evaluators
EvaluatorRegistry.register("simple", SimpleEvaluator)


def load_evaluator_config(config_path: Path) -> Dict[str, Any]:
    """Load evaluator configuration from JSON."""
    if not config_path.exists():
        # Return default config if file doesn't exist
        return get_default_config()
    
    with open(config_path, 'r') as f:
        return json.load(f)


def get_default_config() -> Dict[str, Any]:
    """Get default evaluator configuration."""
    return {
        "evaluator_type": "simple",
        "evaluators": {
            "cluster_costs": {
                "type": "expression",
                "description": "Calculate cost based on cluster pair"
            },
            "cluster_LTs": {
                "type": "lookup",
                "description": "Look up lead time by cluster pair"
            },
            "cluster_feas": {
                "type": "rule",
                "description": "Check feasibility rules"
            },
            "wh_cost": {
                "type": "calculation",
                "description": "Calculate warehouse storage cost"
            }
        }
    }


def create_evaluator(config: Dict[str, Any]) -> BaseEvaluator:
    """Create evaluator instance from config."""
    evaluator_type = config.get("evaluator_type", "simple")
    evaluator_class = EvaluatorRegistry.get(evaluator_type)
    return evaluator_class(config)