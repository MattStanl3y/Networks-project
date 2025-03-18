import subprocess
import time
import os

def list_interfaces():
    """List available network interfaces"""
    cmd = ["/Applications/Wireshark.app/Contents/MacOS/tshark", "-D"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("Available interfaces:")
    print(result.stdout)

def capture_traffic(duration=300, output_file="game_traffic.pcapng", interface="en0", ip_address=None):
    """
    Capture network traffic using tshark for a specified duration.
    
    Args:
        duration (int): Capture duration in seconds (default is 5 minutes)
        output_file (str): Path to save the capture file
        interface (str): Network interface to capture on
        ip_address (str, optional): IP address of the gaming PC to filter traffic
    
    Returns:
        str: Path to the saved capture file
    """
    # Build the tshark command
    cmd = ["/Applications/Wireshark.app/Contents/MacOS/tshark", "-w", output_file, "-i", interface]
    
    # Add IP filter if specified
    if ip_address:
        # Filter for traffic to or from the specified IP
        filter_expression = f"host {ip_address}"
        cmd.extend(["-f", filter_expression])
    
    # Start capture
    print(f"Starting capture for {duration} seconds on interface {interface}...")
    if ip_address:
        print(f"Filtering for traffic to/from {ip_address}")
    
    process = subprocess.Popen(cmd)
    
    # Wait for specified duration
    time.sleep(duration)
    
    # Stop capture
    process.terminate()
    print(f"Capture complete. File saved to {output_file}")
    
    return output_file

def get_user_input():
    """Get user input for capture parameters"""
    # Ask for the gaming PC's IP address
    gaming_pc_ip = input("Enter your gaming PC's IP address: ")
    
    # Ask for capture duration (with default)
    duration_str = input("Enter capture duration in seconds [300]: ")
    duration = int(duration_str) if duration_str.strip() else 300
    
    # Ask for output filename (with default)
    filename = input("Enter output filename [cod_gameplay.pcapng]: ")
    output_file = filename if filename.strip() else "cod_gameplay.pcapng"
    
    return gaming_pc_ip, duration, output_file

if __name__ == "__main__":
    # Get user input
    gaming_pc_ip, duration, output_file = get_user_input()
    
    # Capture traffic
    capture_file = capture_traffic(
        duration=duration,
        output_file=output_file,
        interface="en0",
        ip_address=gaming_pc_ip
    )
    
    print(f"Created capture file: {os.path.abspath(capture_file)}")