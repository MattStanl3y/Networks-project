import os
from capture import capture_traffic, get_user_input
from process import analyze_capture
from visualize import visualize_traffic

def main():
    # Get user input
    gaming_pc_ip, duration = get_user_input()
    
    # Capture traffic
    capture_file = capture_traffic(
        duration=duration,
        output_file="result.pcapng",
        interface="en0",
        ip_address=gaming_pc_ip
    )
    
    print(f"Created capture file: {os.path.abspath(capture_file)}")
    
    # Process the capture
    analyze_capture(capture_file, "result.csv")
    
    # Visualize the data
    visualize_traffic("result.csv")

if __name__ == "__main__":
    main()