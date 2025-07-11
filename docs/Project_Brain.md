# Project Brain - Supply Chain Allocation Engine v2.0

## Overview
A flexible inventory allocation engine that optimizes product routing through supply chain networks using graph algorithms, Pydantic validation, and memoization.

## Architecture
```
Input CSVs → Pydantic Models → NetworkX Graph → Path Finding → 
Evaluation (Memoized) → CM3 Optimization → Allocation Results
```

## Core Components

### 1. Data Models (`src/models/`)
- **Product**: SKU data with validation
- **Chunk**: Processing unit with origin
- **Node/Edge**: Network components
- **EvaluationContext**: Caching-aware context

### 2. Graph Engine (`src/graph/`)
- **NetworkBuilder**: Constructs directed graph
- **PathFinder**: Finds all/shortest paths

### 3. Evaluators (`src/evaluators/`)
- **BaseEvaluator**: Abstract interface
- **SimpleEvaluator**: Basic calculations
- **Memoization**: Automatic result caching

### 4. Allocation (`src/allocation/`)
- **PathEvaluator**: Evaluates complete paths
- **Allocator**: Optimizes by CM3 score

## Usage
```bash
python -m src.main --products data.csv --nodes nodes.csv --edges edges.csv
```

## Key Features
- ✅ Type-safe with Pydantic
- ✅ Memoized evaluators
- ✅ Flexible graph structure
- ✅ CM3-optimized allocation
- ✅ Extensible evaluator system
