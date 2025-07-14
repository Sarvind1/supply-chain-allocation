# Supply Chain Allocation Engine

A flexible inventory allocation engine that optimizes product routing through supply chain networks using graph algorithms, validation, and memoization.

## Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/Sarvind1/supply-chain-allocation.git
cd supply-chain-allocation

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Example
```bash
# Using the provided script
chmod +x run_example.sh
./run_example.sh

# Or directly
python -m src.main \
    --products data/examples/products.csv \
    --nodes data/examples/nodes.csv \
    --edges data/examples/node-node.csv \
    --output allocation_results.json
```

## Project Structure
```
supply-chain-allocation/
├── src/
│   ├── models/         # Pydantic data models
│   ├── graph/          # Network graph construction
│   ├── evaluators/     # Cost/feasibility evaluators
│   ├── allocation/     # Allocation algorithm
│   └── utils/          # Utilities (CSV loading, memoization)
├── data/examples/      # Example CSV files
├── tests/              # Unit tests
└── docs/               # Documentation
```

## Features
- **Type-safe**: Pydantic models with validation
- **Memoized**: Automatic caching of evaluator results
- **Flexible**: JSON-configurable evaluators
- **Optimized**: CM3-based allocation scoring
- **Graph-based**: NetworkX for path finding

## Documentation
- [Project Brain](docs/Project_Brain.md) - Technical overview
- [Commits Guide](docs/Commits_Guide.md) - Development history

## Input Files
The system requires three CSV files:
1. **products.csv**: SKU data to allocate
2. **nodes.csv**: Network nodes (suppliers, ports, warehouses, FCs)
3. **node-node.csv**: Edges connecting nodes

See `data/examples/` for format examples.

## Output
JSON file with allocation results including:
- Selected paths for each product
- Total cost and lead time
- CM3 optimization score
- Feasibility status
