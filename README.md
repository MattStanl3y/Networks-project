# Project Cleanup Guidelines

## Files to Keep:

- capture.py
- process.py
- visualize.py
- main.py
- results/ (directory)

## Files to Remove:

- test_import.py (no longer needed for testing imports)
- config.py (not used in current implementation)
- utils.py (not used in current implementation)
- analyze.py (functionality integrated into other files)

## Updated Project Structure:

```
gaming_network_analysis/
├── capture.py          # Script for capturing network traffic
├── process.py          # Script for processing captured data
├── visualize.py        # Script for creating visualizations
├── main.py             # Main script to tie everything together
└── results/            # Directory for output files
    ├── result.pcapng   # Network capture file
    ├── result.csv      # Processed data file
    └── result_analysis.png  # Visualization image
```

## How to Run:

```bash
# Create the results directory (if it doesn't exist)
mkdir -p results

# Run the complete analysis pipeline
python3 main.py
```
