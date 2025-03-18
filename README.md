# Project Setup

````gaming_network_analysis/
├── capture.py          # Script for capturing network traffic
├── process.py          # Script for processing captured data
├── visualize.py        # Script for creating visualizations
├── analyze.py          # Script for analyzing the processed data
├── main.py             # Main script to tie everything together
├── utils.py            # Utility functions used across scripts
└── config.py           # Configuration parameters```
````

### commands

'python3 main.py'

current issues(things i want to fix):

- too much i/o, also just call every file result....., i still want to enter ip tho
- tcp/http are not working rn 0.
  - **problems may include**
  1. Port filtering issue: The capture might not be including traffic on ports 80/443 (HTTP/HTTPS)
  2. IP filtering too restrictive: If your gaming PC uses multiple IPs or the traffic routes differently than expected
  3. TLS encryption: HTTPS traffic may be captured but identified as "TLS" rather than "HTTP"
- too many comments, need it simple for rn this is just small version of overall project
