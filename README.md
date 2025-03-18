# Project Cleanup Guidelines

## Files to Keep:

- capture.py
- process.py
- visualize.py
- main.py
- results/ (directory)

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
python3 main.py
```
