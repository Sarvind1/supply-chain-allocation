"""Base evaluator interface and registry."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from ..models import EvaluationContext
from ..utils import memoize


class BaseEvaluator(ABC):
    """Base class for all evaluators."""
    
    @abstractmethod
    def evaluate(self, context: EvaluationContext) -> Any:
        """Evaluate based on context."""
        pass


class EvaluatorRegistry:
    """Registry for evaluator types."""
    
    _evaluators: Dict[str, Type[BaseEvaluator]] = {}
    
    @classmethod
    def register(cls, name: str, evaluator_class: Type[BaseEvaluator]):
        """Register an evaluator type."""
        cls._evaluators[name] = evaluator_class
    
    @classmethod
    def get(cls, name: str) -> Type[BaseEvaluator]:
        """Get evaluator class by name."""
        if name not in cls._evaluators:
            raise ValueError(f"Unknown evaluator type: {name}")
        return cls._evaluators[name]
    
    @classmethod
    def list_types(cls) -> list:
        """List all registered evaluator types."""
        return list(cls._evaluators.keys())