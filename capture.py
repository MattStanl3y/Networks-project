import subprocess
import time
import os
import platform

def list_interfaces():
    # Check if we're on Windows or macOS and use appropriate tshark path
    if platform.system() == "Windows":
        cmd = ["tshark", "-D"]
    else:  # macOS or other
        cmd = ["/Applications/Wireshark.app/Contents/MacOS/tshark", "-D"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("Available interfaces:")
    print(result.stdout)

def capture_traffic(duration=120, output_file="results/result.pcapng", interface=None):
    my_ip = "172.20.3.231"
    
    # Build the tshark command for Windows
    cmd = ["C:\\Program Files\\Wireshark\\tshark.exe", "-w", output_file]
    
    # Add interface if specified
    if interface:
        cmd.extend(["-i", interface])
    
    # Filter specifically for Call of Duty UDP traffic on port 3074
    cod_filter = f"host {my_ip} and udp port 3074"
    
    # Add filter to command
    cmd.extend(["-f", cod_filter])
    
    # Start capture
    print(f"Starting capture for {duration} seconds...")
    print(f"Using filter: {cod_filter}")
    
    process = subprocess.Popen(cmd)
    time.sleep(duration)
    process.terminate()
    print(f"Capture complete. File saved to {output_file}")
    
    return output_file

def get_user_input():
    # List available interfaces
    list_interfaces()
    
    # Get interface selection from user
    interface = input("Enter interface number or name to use [default=auto]: ").strip()
    if not interface:
        interface = None  # Let tshark auto-select
    
    # Get capture duration
    duration_str = input("Enter capture duration in seconds [120]: ")
    duration = int(duration_str) if duration_str.strip() else 120
    
    return interface, duration

if __name__ == "__main__":
    # Get user input
    interface, duration = get_user_input()
    
    # Capture traffic with standardized output filename
    capture_file = capture_traffic(
        duration=duration,
        output_file="results/result.pcapng",
        interface=interface
    )
    
    print(f"Created capture file: {os.path.abspath(capture_file)}")