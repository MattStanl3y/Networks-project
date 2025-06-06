import subprocess
import time
import os
import platform
import socket

def list_interfaces():
    if platform.system() == "Windows":
        cmd = ["tshark", "-D"]
    else:  # macOS or other
        cmd = ["/Applications/Wireshark.app/Contents/MacOS/tshark", "-D"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("Available interfaces:")
    print(result.stdout)

def get_my_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Could not automatically detect IP: {e}")
        return None

def get_user_input():
    detected_ip = get_my_ip()
    if detected_ip:
        print(f"Detected your IP address as: {detected_ip}")
        ip_confirm = input(f"Is this your correct IP address? [Y/n]: ").strip().lower()
        if ip_confirm == "" or ip_confirm.startswith("y"):
            my_ip = detected_ip
        else:
            my_ip = input("Enter your correct IP address: ").strip()
    else:
        my_ip = input("Could not detect IP automatically. Enter your IP address: ").strip()
    
    print("\nSelect game:")
    print("1. Call of Duty (UDP port 3074)")
    print("2. Other (custom port)")
    
    port_choice = input("\nSelect option (1-2): ").strip()
    if port_choice == "1":
        game_port = 3074
        game_name = "Call of Duty"
    else:
        game_port = int(input("Enter custom UDP port number: "))
        game_name = "Custom"
    
    duration_str = input("\nEnter capture duration in seconds [60]: ")
    duration = int(duration_str) if duration_str.strip() else 60
    
    print("\nAvailable network interfaces:")
    list_interfaces()
    interface = ""
    while not interface:
        interface = input("\nSelect interface (required): ").strip()
        if not interface:
            print("Interface selection is required. Please choose an interface.")
    
    print(f"\nReady to capture {game_name} traffic on port {game_port}")
    print(f"IP Address: {my_ip}")
    print(f"Duration: {duration} seconds")
    print(f"Interface: {interface}")
    
    start = input("\nType 'start' to begin capture: ").strip().lower()
    if start != "start":
        print("Capture cancelled.")
        exit()
    
    return interface, duration, my_ip, game_port, game_name

def capture_traffic(duration=60, output_file="results/result.pcapng", interface=None, my_ip="127.0.0.1", game_port=3074, game_name="Unknown"):

    game_filter = f"host {my_ip} and udp port {game_port}"
    
    cmd = ["C:\\Program Files\\Wireshark\\tshark.exe", "-w", output_file]
    
    if interface:
        cmd.extend(["-i", interface])
    
    # Add filter to command
    cmd.extend(["-f", game_filter])
    
    print(f"Starting capture for {game_name} on port {game_port}...")
    print(f"Capturing for {duration} seconds...")
    print(f"Using filter: {game_filter}")
    
    process = subprocess.Popen(cmd)
    time.sleep(duration)
    process.terminate()
    print(f"Capture complete. File saved to {output_file}")
    
    return output_file

if __name__ == "__main__":
    interface, duration, my_ip, game_port, game_name = get_user_input()
    
    capture_file = capture_traffic(
        duration=duration,
        output_file="results/result.pcapng",
        interface=interface,
        my_ip=my_ip,
        game_port=game_port,
        game_name=game_name
    )
    
    print(f"Created capture file: {os.path.abspath(capture_file)}")