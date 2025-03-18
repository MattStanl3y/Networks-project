import subprocess
import time
import os

def list_interfaces():
    # List available network interfaces
    cmd = ["/Applications/Wireshark.app/Contents/MacOS/tshark", "-D"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("Available interfaces:")
    print(result.stdout)

def capture_traffic(duration=300, output_file="result.pcapng", interface="en0", ip_address=None):
    # Build the tshark command
    cmd = ["/Applications/Wireshark.app/Contents/MacOS/tshark", "-w", output_file, "-i", interface]
    
    # Add IP filter if specified
    if ip_address:
        cmd.extend(["-f", f"host {ip_address}"])
    
    # Start capture
    print(f"Starting capture for {duration} seconds on interface {interface}...")
    if ip_address:
        print(f"Filtering for traffic to/from {ip_address}")
    
    process = subprocess.Popen(cmd)
    time.sleep(duration)
    process.terminate()
    print(f"Capture complete. File saved to {output_file}")
    
    return output_file

def get_user_input():
    # Get user input for capture parameters
    gaming_pc_ip = input("Enter your gaming PC's IP address: ")
    
    duration_str = input("Enter capture duration in seconds [300]: ")
    duration = int(duration_str) if duration_str.strip() else 300
    
    return gaming_pc_ip, duration

if __name__ == "__main__":
    # Get user input
    gaming_pc_ip, duration = get_user_input()
    
    # Capture traffic with standardized output filename
    capture_file = capture_traffic(
        duration=duration,
        output_file="result.pcapng",
        interface="en0",
        ip_address=gaming_pc_ip
    )
    
    print(f"Created capture file: {os.path.abspath(capture_file)}")