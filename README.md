# Supply Chain Allocation Engine

A flexible inventory allocation engine using graph-based supply chain network with Pydantic validation and memoization.

## Features
- 🔗 Graph-based supply chain network
- ✅ Pydantic data validation
- 🚀 Memoized evaluators for performance
- 📊 CM3-optimized allocation
- 🔧 Configurable evaluation methods

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run allocation
python -m src.main --products data/products.csv --nodes data/nodes.csv --edges data/node-node.csv
```

## Project Structure
```
├── src/
│   ├── models/       # Pydantic data models
│   ├── graph/        # Network graph engine
│   ├── evaluators/   # Cost/feasibility/LT evaluators
│   ├── allocation/   # Allocation algorithm
│   └── main.py       # Entry point
├── data/             # CSV input files
├── config/           # Evaluator configurations
└── tests/            # Unit tests
```