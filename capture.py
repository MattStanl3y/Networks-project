import subprocess
import time
import os
import socket

def list_interfaces():
    # List available network interfaces
    cmd = ["/Applications/Wireshark.app/Contents/MacOS/tshark", "-D"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("Available interfaces:")
    print(result.stdout)

def capture_traffic(duration=120, output_file="results/result.pcapng", interface="en0", ip_address=None, capture_web=True):
    # Build the tshark command
    cmd = ["/Applications/Wireshark.app/Contents/MacOS/tshark", "-w", output_file, "-i", interface]
    
    # Build filter expression
    filter_parts = []
    
    # Add IP filter if specified
    if ip_address:
        filter_parts.append(f"host {ip_address}")
    
    # Add HTTP/HTTPS ports if requested
    if capture_web:
        web_filter = "tcp port 80 or tcp port 443 or tcp port 8080"
        if filter_parts:
            # Add web ports as an OR condition with the IP filter
            filter_expression = f"({filter_parts[0]}) or ({web_filter})"
        else:
            filter_expression = web_filter
    else:
        filter_expression = filter_parts[0] if filter_parts else None
    
    # Add filter to command if we have one
    if filter_expression:
        cmd.extend(["-f", filter_expression])
    
    # Start capture
    print(f"Starting capture for {duration} seconds on interface {interface}...")
    if filter_expression:
        print(f"Using filter: {filter_expression}")
    
    process = subprocess.Popen(cmd)
    time.sleep(duration)
    process.terminate()
    print(f"Capture complete. File saved to {output_file}")
    
    return output_file

def get_user_input():
    # Get user input for capture parameters
    print("Since you're capturing from your MacBook but analyzing a gaming PC:")
    gaming_pc_ip = input("Enter your gaming PC's IP address: ")
    
    # Make sure an IP was provided
    while not gaming_pc_ip.strip():
        print("An IP address is required to filter only your gaming traffic.")
        gaming_pc_ip = input("Enter your gaming PC's IP address: ")
    
    duration_str = input("Enter capture duration in seconds [120]: ")
    duration = int(duration_str) if duration_str.strip() else 120
    
    # Optionally add port filters for HTTP/HTTPS
    add_web_ports = input("Include HTTP/HTTPS traffic? (y/n) [y]: ").lower().strip()
    capture_web = add_web_ports != 'n'
    
    return gaming_pc_ip, duration, capture_web

if __name__ == "__main__":
    # Get user input
    ip_filter, duration, capture_web = get_user_input()
    
    # Capture traffic with standardized output filename
    capture_file = capture_traffic(
        duration=duration,
        output_file="result.pcapng",
        interface="en0",
        ip_address=ip_filter,
        capture_web=capture_web
    )
    
    print(f"Created capture file: {os.path.abspath(capture_file)}")