# Gaming Network Analysis Tool

A tool for capturing and analyzing network traffic during online gaming sessions.

## Project Structure

```
gaming_network_analysis/
├── capture.py             # Captures network traffic
├── process.py             # Processes the captured data
├── visualize.py           # Creates visualizations from data
├── main.py                # Main script to run the full analysis
└── results/               # Output files directory
    ├── result.pcapng      # Raw network capture file
    ├── result.csv         # Processed CSV data
    └── result_analysis.png# Traffic visualization
```

## Requirements

- Windows PC
- Python 3.6+
- Wireshark/tshark ([https://www.wireshark.org/](https://www.wireshark.org/))
- Python libraries:
  - `pyshark`
  - `pandas`
  - `matplotlib`
  - `seaborn`

Install dependencies:

```bash
pip install pyshark pandas matplotlib seaborn
```

## ▶️ How to Run

```bash
python main.py
```

### What to Expect

- Confirm your IP address
- Enter the game UDP port to monitor
- Start and stop capture manually
- View generated visualizations after capture ends

## 🎮 Common Game UDP Ports

| Game         | UDP Port Range |
| ------------ | -------------- |
| Call of Duty | 3074           |
| Fortnite     | 9000–9100      |
| Apex Legends | 37000–40000    |
| Valorant     | 7000–8000      |
| PUBG         | 7086–8100      |

> Search "[Game Name] UDP port" online to find specific ports.

## Warning

Some anti-cheat systems may flag or close the game if packet capturing is detected.  
To reduce risk, keep capture sessions short (30–60 seconds).
