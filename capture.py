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
    # Create results directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Check if we're on Windows or macOS and use appropriate tshark path
    if platform.system() == "Windows":
        tshark_cmd = "tshark"
    else:  # macOS or other
        tshark_cmd = "/Applications/Wireshark.app/Contents/MacOS/tshark"
    
    # Build the tshark command
    cmd = [tshark_cmd, "-w", output_file]
    
    # Only specify interface if one was provided
    if interface:
        cmd.extend(["-i", interface])
    
    # Start capture
    print(f"Starting capture for {duration} seconds...")
    if interface:
        print(f"Using interface: {interface}")
    
    process = subprocess.Popen(cmd)
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print("\nCapture stopped early by user.")
    finally:
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