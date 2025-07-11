"""Memoization utilities for evaluator caching."""

from functools import wraps
from typing import Dict, Any, Callable, Optional
import hashlib
import json
from datetime import datetime


class CacheStats:
    """Track cache performance metrics."""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.size = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def __str__(self) -> str:
        return f"Hits: {self.hits}, Misses: {self.misses}, Hit Rate: {self.hit_rate:.2%}, Size: {self.size}"


class EvaluatorCache:
    """Cache for evaluator results."""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self.stats = CacheStats()
    
    def _hash_key(self, key: str) -> str:
        """Create hash of cache key."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve cached value."""
        hashed = self._hash_key(key)
        if hashed in self._cache:
            self.stats.hits += 1
            return self._cache[hashed]["value"]
        self.stats.misses += 1
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Store value in cache."""
        hashed = self._hash_key(key)
        self._cache[hashed] = {
            "value": value,
            "timestamp": datetime.now(),
            "key": key
        }
        self.stats.size = len(self._cache)
    
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
        self.stats = CacheStats()
    
    def invalidate(self, pattern: str) -> None:
        """Invalidate entries matching pattern."""
        to_remove = []
        for hashed, entry in self._cache.items():
            if pattern in entry["key"]:
                to_remove.append(hashed)
        
        for hashed in to_remove:
            del self._cache[hashed]
        
        self.stats.size = len(self._cache)


# Global cache instance
_evaluator_cache = EvaluatorCache()


def memoize(func: Callable) -> Callable:
    """Decorator to memoize evaluator functions."""
    
    @wraps(func)
    def wrapper(context, *args, **kwargs):
        # Use context's cache_key property
        cache_key = context.cache_key if hasattr(context, "cache_key") else str(context)
        
        # Check cache
        cached_value = _evaluator_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Compute and cache
        result = func(context, *args, **kwargs)
        _evaluator_cache.set(cache_key, result)
        
        return result
    
    # Add cache management methods
    wrapper.cache_stats = lambda: _evaluator_cache.stats
    wrapper.clear_cache = lambda: _evaluator_cache.clear()
    wrapper.invalidate_cache = lambda pattern: _evaluator_cache.invalidate(pattern)
    
    return wrapper