# Test Data Directory

## Directory Structure

```
data/
├── examples/          # Basic example files
├── dummy/            # Test datasets of various sizes
└── README.md         # This file
```

## Dummy Data Files

### Products Data
- `products_small.csv` - 10 SKUs for quick testing
- `products_medium.csv` - 25 SKUs for moderate testing
- `products_large.csv` - 50 SKUs across 10 categories
- `products_test_*.csv` - Generated test files

### Network Data
- `nodes_simple.csv` - Basic 5-node network (1 port, 1 warehouse, 1 FC)
- `nodes_complex.csv` - Complex 23-node network (3 ports, 9 warehouses, 4 FCs)

### Edge Data
- `node-node_simple.csv` - Simple linear path
- `node-node_complex.csv` - Complex network with multiple paths

### Supporting Data
- `shipping_times.csv` - Transit times between clusters
- `warehouse_rates.csv` - Storage costs by warehouse
- `ocean_rates.csv` - Shipping rates by port pairs
- `hazmat_rules.csv` - Hazardous material restrictions

## Data Characteristics

### Product Categories
- ELEC: Electronics (high volume, low CM3)
- HOME: Home goods (medium volume, medium CM3)
- TOYS: Toys (varied attributes)
- SPRT: Sports equipment (often oversized)
- BOOK: Books (very high volume, low CM3)
- FASH: Fashion (seasonal patterns)
- FOOD: Food items (time-sensitive)
- PETS: Pet supplies (mixed sizes)
- AUTO: Auto parts (often oversized)
- GARD: Garden supplies (seasonal, oversized)

### Network Clusters
- CN: China origin
- US_West: West Coast US
- US_East: East Coast US
- US_Central: Central US
- US_South: Southern US
- 3PL_*: Third-party logistics centers

## Usage Examples

```bash
# Test with simple network
python -m src.main \
    --products dummy/products_small.csv \
    --nodes dummy/nodes_simple.csv \
    --edges dummy/node-node_simple.csv

# Test with complex network
python -m src.main \
    --products dummy/products_large.csv \
    --nodes dummy/nodes_complex.csv \
    --edges dummy/node-node_complex.csv
```