# Project Brain - Supply Chain Allocation Engine

## Overview
A flexible inventory allocation engine that optimizes product routing through supply chain networks using graph algorithms, Pydantic validation, and memoization.

## Core Principles
1. **Graph-Based Network**: Supply chain as directed graph (nodes & edges)
2. **Pydantic Models**: Type-safe data validation
3. **Memoization**: Cache evaluator results for performance
4. **Modular Evaluators**: Pluggable cost/feasibility/lead-time calculations

## Key Components
- **Data Models**: Pydantic schemas for Products, Nodes, Edges
- **Graph Engine**: NetworkX for path finding
- **Evaluator System**: JSON-configured calculators with caching
- **Allocation Algorithm**: Path evaluation with CM3 optimization

## Data Flow
1. Load CSVs → 2. Build Graph → 3. Find Paths → 4. Evaluate → 5. Allocate
